import streamlit as st
import pandas as pd
import requests

# -----------------------------
# Load dataset
# -----------------------------
@st.cache_data
def load_district_data():
    return pd.read_csv("mp_wind_dataset.csv")

data = load_district_data()

# -----------------------------
# Page title
# -----------------------------
st.title("🌬️ MP Wind Energy Dashboard (Districts)")

# -----------------------------
# District selector
# -----------------------------
districts = data['District'].tolist()
selected_district = st.selectbox("Select a District:", districts)

district_row = data[data['District'] == selected_district].iloc[0]

st.subheader(f"Wind Data for {selected_district}")

# Baseline wind speed
st.markdown(f"**Baseline Average Wind Speed:** {district_row['Baseline_Wind_Speed(m/s)']} m/s")
st.markdown(f"[Source: {district_row['Baseline_Source']}]({district_row['Baseline_Source']})")

# -----------------------------
# Fetch realtime wind from Open-Meteo API
# -----------------------------
realtime_api_url = district_row['Realtime_API']
try:
    response = requests.get(realtime_api_url)
    response.raise_for_status()
    data_json = response.json()
    
    # Extract 10m wind speed for current hour
    if "hourly" in data_json and "windspeed_10m" in data_json["hourly"]:
        current_wind_speed = data_json["hourly"]["windspeed_10m"][0]
        st.markdown(f"**Realtime Wind Speed (10m height):** {current_wind_speed:.1f} m/s")
        st.markdown(f"[API Reference]({realtime_api_url})")
    else:
        st.warning("Realtime wind data unavailable.")
except Exception as e:
    st.error(f"Error fetching realtime wind: {e}")

# -----------------------------
# Notes / methodology
# -----------------------------
st.markdown("---")
st.subheader("ℹ️ Methodology (Simple Explanation)")
st.markdown("""
- **Baseline Wind Speed**: Long-term average from WeatherSpark/IMD.  
- **Realtime Wind Speed**: Pulled from Open-Meteo API (10m height, current hour).  
- Both numbers help estimate energy output and project ROI.  

**How to verify:**  
1. Check the baseline link → WeatherSpark / IMD data for the district.  
2. Click the API reference → Open-Meteo API returns live wind readings.  
3. Capacity factor, generation, and financial calculations can be done using these wind speeds in a separate financial model.
""")
