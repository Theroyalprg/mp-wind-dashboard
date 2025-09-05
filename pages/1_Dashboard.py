import streamlit as st
import pandas as pd
import requests

# Load district data
@st.cache
def load_district_data():
    return pd.read_csv("mp_wind_dataset.csv")

district_data = load_district_data()

# Sidebar for user input
with st.sidebar:
    st.header("Select District")
    selected_district = st.selectbox("Choose a district", district_data['District'])
    district_row = district_data[district_data['District'] == selected_district].iloc[0]

    st.write(f"**Latitude**: {district_row['Latitude']}")
    st.write(f"**Longitude**: {district_row['Longitude']}")
    st.write(f"**Baseline Wind Speed**: {district_row['Baseline_Wind_Speed(m/s)']} m/s")
    st.write(f"**Baseline Source**: {district_row['Baseline_Source']}")
    st.write(f"**Realtime API**: {district_row['Realtime_API']}")

# Fetch real-time wind speed
realtime_wind_speed = district_row['Baseline_Wind_Speed(m/s)']  # Default to baseline
try:
    response = requests.get(district_row['Realtime_API'], timeout=5)
    response.raise_for_status()
    data_json = response.json()
    if "hourly" in data_json and "windspeed_10m" in data_json["hourly"]:
        realtime_wind_speed = data_json["hourly"]["windspeed_10m"][0]
        st.success(f"Realtime Wind Speed: {realtime_wind_speed} m/s")
    else:
        st.warning("Realtime wind data unavailable, using baseline.")
except Exception as e:
    st.error(f"Error fetching realtime wind data: {e}, using baseline.")

# Display district information
st.write(f"### {selected_district}")
st.write(f"Latitude: {district_row['Latitude']}")
st.write(f"Longitude: {district_row['Longitude']}")
st.write(f"Baseline Wind Speed: {district_row['Baseline_Wind_Speed(m/s)']} m/s")
st.write(f"Baseline Source: {district_row['Baseline_Source']}")
st.write(f"Realtime API: {district_row['Realtime_API']}")

# Additional analysis and visualizations can be added here

