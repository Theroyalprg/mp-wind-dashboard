import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="MP Wind Energy Dashboard", layout="wide")

st.title("🌪️ MP Wind Energy Dashboard - LIVE!")
st.caption("1M1B Salesforce Internship Project")

# ---- Sidebar controls ----
st.sidebar.header("Site Input")
location = st.sidebar.selectbox("Choose Location", ["Ratlam", "Mandsaur", "Dewas"])
years = st.sidebar.slider("Historical Years", 1, 5, 1)
hub_height = st.sidebar.slider("Hub Height (m)", 10, 120, 50)
loss_factor = st.sidebar.slider("Loss Factor (%)", 0, 30, 15) / 100.0

# ---- Fake historical data (for demo) ----
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=24*30, freq="H")
wind_speeds = np.random.normal(6, 1.5, len(dates))  # mean 6 m/s
wind_speeds = np.clip(wind_speeds, 0, None)
df = pd.DataFrame({"time": dates, "wind_speed": wind_speeds})

# ---- Forecast (simple persistence model) ----
forecast_hours = 72
future_dates = pd.date_range(start=dates[-1] + timedelta(hours=1), periods=forecast_hours, freq="H")
forecast_speed = np.repeat(df["wind_speed"].iloc[-1], forecast_hours)
forecast_df = pd.DataFrame({"time": future_dates, "wind_speed": forecast_speed})

# ---- Plot ----
fig = px.line(df, x="time", y="wind_speed", title=f"Historical Wind Speeds at {location}")
fig.add_scatter(x=forecast_df["time"], y=forecast_df["wind_speed"], mode="lines", name="Forecast")
st.plotly_chart(fig, use_container_width=True)

# ---- Energy estimation (simple model) ----
# Sample power curve
power_curve = {
    0: 0, 3: 0.2, 4: 0.5, 5: 1.2, 6: 2.5, 7: 4.0,
    8: 6.5, 9: 9.0, 10: 11.5, 11: 13, 12: 14, 13: 14.5,
    14: 14.8, 15: 15, 20: 15
}
pc_df = pd.DataFrame(list(power_curve.items()), columns=["wind_speed", "power_kw"])

def lookup_power(v):
    return np.interp(v, pc_df["wind_speed"], pc_df["power_kw"])

df["power_kw"] = df["wind_speed"].apply(lookup_power) * (1 - loss_factor)
annual_energy_kwh = df["power_kw"].sum()

# ---- KPI cards ----
col1, col2, col3 = st.columns(3)
col1.metric("Average Wind Speed", f"{df['wind_speed'].mean():.2f} m/s")
col2.metric("Capacity Factor", f"{(annual_energy_kwh / (15 * len(df))):.2%}")
col3.metric("Est. Annual Energy", f"{annual_energy_kwh:.0f} kWh")

# ---- Data preview ----
with st.expander("Show raw data"):
    st.write(df.head())
