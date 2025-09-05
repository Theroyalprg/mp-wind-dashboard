import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import time

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="MP Wind Energy Dashboard", layout="wide")

# ----------------------------
# Custom Loader Function
# ----------------------------
def custom_loader(style="wave", duration=3, message="Loading"):
    """Show a custom loader animation in Streamlit"""
    loaders = {
        "circle": """
        <div style="display:flex;justify-content:center;align-items:center;height:100px;">
          <div class="loader"></div>
        </div>
        <style>
        .loader {
          border: 8px solid #f3f3f3;
          border-top: 8px solid #00c4ff;
          border-radius: 50%;
          width: 60px;
          height: 60px;
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        </style>
        """,

        "dots": """
        <div style="display:flex;justify-content:center;align-items:center;height:100px;">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
        <style>
        .dot {
          height: 18px;
          width: 18px;
          margin: 0 5px;
          background-color: #00c4ff;
          border-radius: 50%;
          display: inline-block;
          animation: bounce 1.2s infinite ease-in-out;
        }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
        </style>
        """,

        "wave": """
        <div style="display:flex;justify-content:center;align-items:flex-end;height:100px;gap:6px;">
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
        </div>
        <style>
        .bar {
          width: 8px;
          height: 20px;
          background: #00c4ff;
          animation: wave 1s infinite ease-in-out;
        }
        .bar:nth-child(2) { animation-delay: 0.1s; }
        .bar:nth-child(3) { animation-delay: 0.2s; }
        .bar:nth-child(4) { animation-delay: 0.3s; }
        .bar:nth-child(5) { animation-delay: 0.4s; }

        @keyframes wave {
          0%, 40%, 100% { transform: scaleY(0.3); }
          20% { transform: scaleY(1); }
        }
        </style>
        """
    }

    placeholder = st.empty()
    placeholder.markdown(loaders[style], unsafe_allow_html=True)
    time.sleep(duration)
    placeholder.empty()
    st.success(f"✅ {message} Complete!")

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("🌪️ MP Wind Energy Dashboard - LIVE!")
st.caption("1M1B Salesforce Internship Project")

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.header("Site Input")
location = st.sidebar.selectbox("Choose Location", ["Ratlam", "Mandsaur", "Dewas"])
years = st.sidebar.slider("Historical Years", 1, 5, 1)
hub_height = st.sidebar.slider("Hub Height (m)", 10, 120, 50)
loss_factor = st.sidebar.slider("Loss Factor (%)", 0, 30, 15) / 100.0

# ----------------------------
# Button with Loader
# ----------------------------
if st.button("⚡ Generate Forecast"):
    custom_loader(style="wave", duration=3, message="Forecasting")

    # ---- Fake historical data (demo only) ----
    np.random.seed(42)
    dates = pd.date_range(end=datetime.today(), periods=24*30, freq="H")
    wind_speeds = np.random.normal(6, 1.5, len(dates))  # mean 6 m/s
    wind_speeds = np.clip(wind_speeds, 0, None)
    df = pd.DataFrame({"time": dates, "wind_speed": wind_speeds})

    # ---- Forecast (simple persistence model) ----
    forecast_hours = 72
    future_dates = pd.date_range(start=dates[-1] + timedelta(hours=1),
                                 periods=forecast_hours, freq="H")
    forecast_speed = np.repeat(df["wind_speed"].iloc[-1], forecast_hours)
    forecast_df = pd.DataFrame({"time": future_dates, "wind_speed": forecast_speed})

    # ---- Plot ----
    fig = px.line(df, x="time", y="wind_speed", title=f"Historical Wind Speeds at {location}")
    fig.add_scatter(x=forecast_df["time"], y=forecast_df["wind_speed"],
                    mode="lines", name="Forecast")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Energy estimation (simple model) ----
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
