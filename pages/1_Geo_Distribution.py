import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Geographic Distribution", layout="wide")
st.title("📍 Geographic Distribution & Overview")

@st.cache_data
def load_data():
    print("Loading data...")
    return pd.read_csv(r"C:\Users\julia\Downloads\RatingRegister.csv", index_col=False)

df = load_data()

metric = st.selectbox("Select Metric", [
    "EnergyStarRatingValue", 
    "WaterStarRatingValue", 
    "GHGEmissionsScope123WithRenewableElectricity"
])

df_map = df.dropna(subset=["Latitude", "Longitude", metric])
color_scale = px.colors.sequential.Viridis[::-1]

# Scatter map
fig = px.scatter_map(
    df_map,
    lat="Latitude",
    lon="Longitude",
    color=metric,
    hover_name="PremisesName",
    color_continuous_scale=color_scale,
    zoom=3,
    height=600,
)
st.plotly_chart(fig, use_container_width=True)


# Average ESG Ratings by State
st.subheader(f"Average {metric} by State")
group_metric_state = df.groupby('State')[metric].mean().reset_index()
group_metric_state[metric] = group_metric_state[metric].round(3)

fig_state = px.bar(
    group_metric_state,
    x='State',
    y=metric,
    color=metric,
    text=metric, 
    color_continuous_scale=color_scale,
    title=f"Average {metric} by State"
)
fig_state.update_traces(textposition='outside')
fig_state.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig_state, use_container_width=True)


# GHG Emissions Hotspot (top 10%)
st.subheader("GHG Emissions Hotspots (Top 10%)")
df_ghg = df.dropna(subset=["Latitude", "Longitude", "GHGEmissionsScope123WithRenewableElectricity"])
threshold = df_ghg["GHGEmissionsScope123WithRenewableElectricity"].quantile(0.90)
df_hotspots = df_ghg[df_ghg["GHGEmissionsScope123WithRenewableElectricity"] >= threshold]
fig_hotspots = px.scatter_map(
    df_hotspots,
    lat="Latitude",
    lon="Longitude",
    size="GHGEmissionsScope123WithRenewableElectricity",
    color="GHGEmissionsScope123WithRenewableElectricity",
    hover_name="PremisesName",
    color_continuous_scale="reds",
    size_max=15,
    zoom=3,
    height=600,
)
st.plotly_chart(fig_hotspots, use_container_width=True)
