import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Water Usage & Recycling", layout="wide")
st.title("💧 Water Usage and Recycling")

@st.cache_data
def load_data():
    print("Loading data...")
    return pd.read_csv(r"data\RatingRegister.csv", index_col=False)

print("Current working directory:", os.getcwd())
df = load_data()

st.subheader("Water Consumption vs Recycled Water")
fig_water = px.scatter(
    df.dropna(subset=["WaterConsumption", "WaterRecycled", "WaterRecycledPercent"]),
    x="WaterConsumption", 
    y="WaterRecycled", 
    color="BuildingType",
    size="WaterRecycledPercent",
    hover_name="PremisesName",
    log_x=True
)
st.plotly_chart(fig_water, use_container_width=True)


st.subheader("Water Intensity by Building Type")
water_by_type = df.groupby("BuildingType")["WaterIntensity"].mean().reset_index()
fig_water_intensity = px.bar(water_by_type, x="BuildingType", y="WaterIntensity", color="WaterIntensity", color_continuous_scale="Teal")
st.plotly_chart(fig_water_intensity, use_container_width=True)


st.subheader("Recycled Water Usage by State")
recycle_by_state = df.groupby("State")["WaterRecycledPercent"].mean().reset_index()
fig_recycle = px.bar(recycle_by_state, x="State", y="WaterRecycledPercent", color="WaterRecycledPercent", color_continuous_scale="Greens")
st.plotly_chart(fig_recycle, use_container_width=True)
