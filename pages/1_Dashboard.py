import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Wind Forecast & ROI Dashboard",
    page_icon="🌬️",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1f77b4; margin-bottom: 1rem;}
    .metric-card {background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;}
    .metric-value {font-size: 1.5rem; font-weight: bold; color: #1f77b4;}
    .metric-label {font-size: 0.9rem; color: #7f7f7f;}
    .footer {text-align: center; margin-top: 2rem; color: #7f7f7f; font-size: 0.8rem;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌬️ Wind Forecast & ROI Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.header("Project Parameters")
    
    years = st.slider("Project Lifetime (Years)", 1, 25, 10)
    capacity_mw = st.number_input("Turbine Capacity (MW)", 0.5, 10.0, 2.0, step=0.5)
    avg_wind_speed = st.slider("Average Wind Speed (m/s)", 3.0, 12.0, 6.0, step=0.5)
    turbine_cost = st.number_input("Turbine Cost (₹ lakhs/MW)", 500, 1000, 650)
    om_cost = st.number_input("O&M Cost (₹ lakhs/MW/year)", 10, 50, 25)
    tariff_rate = st.number_input("Electricity Tariff (₹/kWh)", 3.0, 8.0, 4.5, step=0.1)
    
    st.markdown("---")
    st.info("Adjust the parameters to see how they affect your wind project's financial viability.")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Calculations
    capacity_factor = 0.35 * (avg_wind_speed/12)
    estimated_annual_generation = capacity_mw * 8760 * capacity_factor
    annual_revenue = estimated_annual_generation * tariff_rate * 1000  # Convert to ₹
    total_investment = capacity_mw * turbine_cost * 100000  # Convert to ₹
    annual_om_cost = capacity_mw * om_cost * 100000  # Convert to ₹
    
    # Financial metrics
    annual_cash_flow = annual_revenue - annual_om_cost
    total_revenue = annual_revenue * years
    total_om_cost = annual_om_cost * years
    net_profit = total_revenue - total_investment - total_om_cost
    roi = (net_profit / total_investment) * 100
    payback_period = total_investment / annual_cash_flow
    
    # Create data for charts
    years_range = np.arange(1, years + 1)
    cumulative_generation = [estimated_annual_generation * y for y in years_range]
    cumulative_revenue = [annual_revenue * y for y in years_range]
    cumulative_cash_flow = [annual_cash_flow * y - total_investment for y in years_range]
    
    # Chart selection
    chart_option = st.radio("Select Chart View", 
                           ["Energy Output", "Financial Performance", "Cash Flow Analysis"], 
                           horizontal=True)
    
    # Create charts
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if chart_option == "Energy Output":
        ax.plot(years_range, cumulative_generation, marker="o", linewidth=2, color="#1f77b4")
        ax.set_ylabel("Cumulative Energy (MWh)")
        ax.set_title("Projected Energy Output Over Time")
    elif chart_option == "Financial Performance":
        ax.plot(years_range, cumulative_revenue, marker="s", linewidth=2, color="#2ca02c", label="Revenue")
        ax.axhline(y=total_investment, color="#d62728", linestyle="--", label="Initial Investment")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Financial Performance Over Time")
        ax.legend()
    else:
        ax.plot(years_range, cumulative_cash_flow, marker="^", linewidth=2, color="#ff7f0e")
        ax.axhline(y=0, color="#d62728", linestyle="--")
        ax.set_ylabel("Net Cash Flow (₹)")
        ax.set_title("Project Cash Flow Over Time")
    
    ax.set_xlabel("Years")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with col2:
    # Key metrics display
    st.subheader("Key Performance Indicators")
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Capacity Factor</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-value">{capacity_factor:.1%}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Annual Energy Generation</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-value">{estimated_annual_generation:,.0f} MWh</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Total Investment</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-value">₹ {total_investment:,.0f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Net Profit</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-value">₹ {net_profit:,.0f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">ROI</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-value">{roi:.1f}%</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Payback Period</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-value">{payback_period:.1f} years</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Additional information
st.markdown("---")
expander = st.expander("Assumptions & Methodology")
with expander:
    st.write("""
    This dashboard provides estimates based on the following assumptions:
    - Capacity factor is calculated as 35% of the ratio between actual wind speed and rated wind speed (12 m/s)
    - Operation and Maintenance costs are applied annually
    - Electricity tariff remains constant throughout the project lifetime
    - No financing costs or taxes are considered in this simplified model
    - Capacity factor calculation: CF = 0.35 × (V_avg / 12) where V_avg is the average wind speed
    """)

# Footer
st.markdown('<p class="footer">© 2023 Wind Energy Analytics Dashboard | For demonstration purposes only</p>', unsafe_allow_html=True)
