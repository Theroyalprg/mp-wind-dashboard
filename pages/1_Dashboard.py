import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 Wind Forecast & ROI Dashboard")

# User input
years = st.slider("Select Project Lifetime (Years)", 1, 25, 10)
capacity_mw = st.number_input("Turbine Capacity (MW)", 0.5, 10.0, 2.0)
avg_wind_speed = st.slider("Average Wind Speed (m/s)", 3.0, 12.0, 6.0)

# Simplified estimation formula
estimated_generation = capacity_mw * 8760 * (avg_wind_speed/12) * 0.35
roi = estimated_generation * 0.05 * years

st.metric("Estimated Annual Generation (MWh)", f"{estimated_generation:,.0f}")
st.metric("ROI over project lifetime", f"₹ {roi:,.0f}")

# Plot simple trend
years_range = np.arange(1, years+1)
gen_trend = [estimated_generation * y for y in years_range]

fig, ax = plt.subplots()
ax.plot(years_range, gen_trend, marker="o")
ax.set_xlabel("Years")
ax.set_ylabel("Cumulative Energy (MWh)")
ax.set_title("Projected Energy Output")
st.pyplot(fig)
