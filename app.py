import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests

# -----------------------------
# Load dataset
# -----------------------------
@st.cache_data
def load_district_data():
    return pd.read_csv("mp_wind_dataset.csv")

district_data = load_district_data()

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Wind Forecast & ROI Dashboard",
    page_icon="🌬️",
    layout="wide"
)

# -----------------------------
# Helper functions
# -----------------------------
def safe_div(a, b):
    try:
        return a / b if b != 0 else float('nan')
    except Exception:
        return float('nan')

def pct(x):
    return f"{x*100:.1f}%" if not np.isnan(x) else "N/A"

def rupee(x):
    try:
        return f"₹ {x:,.0f}"
    except:
        return "N/A"

# -----------------------------
# Styling (DeepSeek + colorful KPIs)
# -----------------------------
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1f77b4; margin-bottom: 1rem;}
    .metric-card {background-color: #f0f2f6; padding: 1rem; border-radius: 0.75rem; margin-bottom: 1rem; text-align:center;}
    .metric-value {font-size: 1.5rem; font-weight: bold; color: #1f77b4;}
    .metric-label {font-size: 0.9rem; color: #7f7f7f;}
    .footer {text-align: center; margin-top: 2rem; color: #7f7f7f; font-size: 0.8rem;}
    .metric-card-energy {background: linear-gradient(90deg,#a1c4fd,#c2e9fb);}
    .metric-card-finance {background: linear-gradient(90deg,#d4fc79,#96e6a1);}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🌬️ Wind Forecast & ROI Dashboard</h1>', unsafe_allow_html=True)

# -----------------------------
# Sidebar inputs
# -----------------------------
with st.sidebar:
    st.header("Project Inputs")

    # District selector
    districts = district_data['District'].tolist()
    selected_district = st.selectbox("Select a District", districts)
    district_row = district_data[district_data['District'] == selected_district].iloc[0]

    st.markdown(f"**Baseline Wind Speed:** {district_row['Baseline_Wind_Speed(m/s)']} m/s")
    st.markdown(f"[Baseline Source]({district_row['Baseline_Source']})")

    # Fetch realtime wind with spinner
    realtime_wind_speed = district_row['Baseline_Wind_Speed(m/s)']  # default
    with st.spinner(f"Fetching realtime wind for {selected_district}..."):
        try:
            response = requests.get(district_row['Realtime_API'], timeout=5)
            response.raise_for_status()
            data_json = response.json()
            if "hourly" in data_json and "windspeed_10m" in data_json["hourly"]:
                realtime_wind_speed = data_json["hourly"]["windspeed_10m"][0]
                st.success(f"Realtime Wind (10m height): {realtime_wind_speed:.1f} m/s")
                st.markdown(f"[Realtime API]({district_row['Realtime_API']})")
            else:
                st.warning("Realtime wind data unavailable, using baseline.")
        except Exception as e:
            st.error(f"Error fetching realtime wind, using baseline. ({e})")

    # Other financial parameters
    years = st.slider("Project Lifetime (Years)", 1, 25, 10)
    capacity_mw = st.number_input("Turbine Capacity (MW)", 0.5, 10.0, 2.0, step=0.5)
    turbine_cost_lakh_per_mw = st.number_input("Turbine Cost (₹ lakhs / MW)", 100, 2000, 650)
    om_cost_lakh_per_mw_per_year = st.number_input("O&M Cost (₹ lakhs / MW / year)", 1, 500, 25)
    tariff_rate_per_kwh = st.number_input("Electricity Tariff (₹ / kWh)", 0.5, 20.0, 4.5, step=0.1)
    st.markdown("---")
    st.info("Adjust parameters to see financial projections for the selected district.")

# -----------------------------
# Financial Calculations
# -----------------------------
V_ref = 12.0
CF_ref = 0.35
capacity_factor = CF_ref * (realtime_wind_speed / V_ref)
capacity_factor = max(0.0, min(capacity_factor, 0.6))

hours_per_year = 8760
estimated_annual_generation_mwh = capacity_mw * hours_per_year * capacity_factor

turbine_cost_rupees = capacity_mw * turbine_cost_lakh_per_mw * 100000
annual_om_cost_rupees = capacity_mw * om_cost_lakh_per_mw_per_year * 100000
annual_revenue_rupees = estimated_annual_generation_mwh * 1000 * tariff_rate_per_kwh

annual_cash_flow_rupees = annual_revenue_rupees - annual_om_cost_rupees
total_revenue_rupees = annual_revenue_rupees * years
total_om_costs_rupees = annual_om_cost_rupees * years
net_profit_rupees = total_revenue_rupees - turbine_cost_rupees - total_om_costs_rupees

roi_pct = safe_div(net_profit_rupees, turbine_cost_rupees) * 100
payback_years = safe_div(turbine_cost_rupees, annual_cash_flow_rupees)

# -----------------------------
# Charts and KPIs
# -----------------------------
col1, col2 = st.columns([2, 1])

with col1:
    years_range = np.arange(1, years + 1)
    cumulative_generation = [estimated_annual_generation_mwh * y for y in years_range]
    cumulative_revenue = [annual_revenue_rupees * y for y in years_range]
    cumulative_cash_flow = [annual_cash_flow_rupees * y - turbine_cost_rupees for y in years_range]

    chart_option = st.radio("Select Chart View", 
                           ["Energy Output", "Financial Performance", "Cash Flow Analysis"], 
                           horizontal=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_option == "Energy Output":
        ax.plot(years_range, cumulative_generation, marker="o", linewidth=2, color="#1f77b4")
        ax.set_ylabel("Cumulative Energy (MWh)")
        ax.set_title(f"{selected_district} - Energy Output Over Time")
    elif chart_option == "Financial Performance":
        ax.plot(years_range, cumulative_revenue, marker="s", linewidth=2, color="#2ca02c", label="Revenue")
        ax.axhline(y=turbine_cost_rupees, color="#d62728", linestyle="--", label="Initial Investment")
        ax.set_ylabel("Amount (₹)")
        ax.set_title(f"{selected_district} - Financial Performance")
        ax.legend()
    else:
        ax.plot(years_range, cumulative_cash_flow, marker="^", linewidth=2, color="#ff7f0e")
        ax.axhline(y=0, color="#d62728", linestyle="--")
        ax.set_ylabel("Net Cash Flow (₹)")
        ax.set_title(f"{selected_district} - Cash Flow Over Time")

    ax.set_xlabel("Years")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with col2:
    st.subheader("Key Performance Indicators")
    metrics = [
        ("Capacity Factor", pct(capacity_factor)),
        ("Annual Energy Generation", f"{estimated_annual_generation_mwh:,.0f} MWh"),
        ("Total Investment", rupee(turbine_cost_rupees)),
        ("Net Profit", rupee(net_profit_rupees)),
        ("ROI", f"{roi_pct:.1f}%"),
        ("Payback Period", f"{payback_years:.1f} years" if np.isfinite(payback_years) else "N/A")
    ]
    for label, value in metrics:
        # Use different colors for financial vs energy metrics
        cls = "metric-card-energy" if label in ["Capacity Factor","Annual Energy Generation"] else "metric-card-finance"
        st.markdown(f'<div class="metric-card {cls}">', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-label">{label}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{value}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Methodology / References
# -----------------------------
st.markdown("---")
expander = st.expander("Methodology & Sources")
with expander:
    st.markdown(f"""
**How it works:**
- Baseline wind speed from WeatherSpark (MP districts): [{district_row['Baseline_Source']}]({district_row['Baseline_Source']})
- Realtime wind via Open-Meteo API: [{district_row['Realtime_API']}]({district_row['Realtime_API']})
- Capacity factor CF ≈ 0.35 × (V_avg / 12 m/s)
- Annual Energy (MWh) = MW × 8760 × CF
- Revenue = Energy (kWh) × Tariff (₹/kWh)
- Costs: turbine (CapEx) & O&M (OpEx) in ₹
- ROI and Payback calculated from net profit vs initial investment
""")

st.markdown('<p class="footer">© 2025 Wind Energy Analytics Dashboard | Source-backed & live</p>', unsafe_allow_html=True)
