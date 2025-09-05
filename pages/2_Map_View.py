import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🗺️ Wind Map of Madhya Pradesh")

# MP center coordinates
m = folium.Map(location=[23.5, 78.5], zoom_start=6)

# Example districts (we’ll plug real govt data later)
districts = {
    "Bhopal": {"coords": [23.2599, 77.4126], "wind": "5.6 m/s"},
    "Indore": {"coords": [22.7196, 75.8577], "wind": "6.0 m/s"},
    "Jabalpur": {"coords": [23.1815, 79.9864], "wind": "5.4 m/s"},
    "Ratlam": {"coords": [23.3342, 75.0370], "wind": "6.2 m/s"},
}

for name, data in districts.items():
    folium.Marker(
        location=data["coords"],
        popup=f"{name}: {data['wind']} wind",
        tooltip=name,
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

st_folium(m, width=700, height=500)
