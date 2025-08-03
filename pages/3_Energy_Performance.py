import os
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Energy Performance", layout="wide")
st.title("⚡ Energy Performance")

@st.cache_data
def load_data():
    print("Loading data...")
    return pd.read_csv(r"../data/RatingRegister.csv", index_col=False)

print("Current working directory:", os.getcwd())

df = load_data()

st.subheader("Energy Star Rating Distribution")
fig = px.histogram(df, x="EnergyStarRatingValue", nbins=20, color="BuildingType")
st.plotly_chart(fig, use_container_width=True)



st.subheader("Average Energy Intensity by Building Type")
energy_by_type = df.groupby("BuildingType")["EnergyIntensity"].mean().reset_index()
fig = px.bar(energy_by_type, x="BuildingType",   y="EnergyIntensity", color="EnergyIntensity", color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True)




# Energy Mix by Building Type
st.subheader("Renewable vs Non-Renewable by Building Type")

energy_mix = df.groupby("BuildingType")[[
    "TotalRenewableElectricity_kWh", 
    "NonRenewableElectricity_kWh"
]].sum().reset_index()

energy_mix_melted = energy_mix.melt(id_vars="BuildingType", 
                                     var_name="Energy Type", 
                                     value_name="kWh")

fig = px.bar(energy_mix_melted, 
             x="BuildingType", 
             y="kWh", 
             color="Energy Type", 
             barmode="stack",
             title="Stacked Energy Mix by Building Type",
             color_discrete_map={
                 "TotalRenewableElectricity_kWh": "green",
                 "NonRenewableElectricity_kWh": "red"
             })

st.plotly_chart(fig, use_container_width=True)