import streamlit as st

st.title("📚 Data Sources & Methodology")

st.markdown("""
### 🔹 Data Sources
- **IMD (India Meteorological Department)**: [imd.gov.in](https://mausam.imd.gov.in)
- **NIWE (National Institute of Wind Energy)**: [niwe.res.in](https://niwe.res.in)
- **NREL (US Dept. of Energy)**: [nrel.gov](https://www.nrel.gov)

### 🔹 Methodology (Easy Version)
1. **Collect wind speed data** 📊 from trusted govt. sources.
2. **Average wind speed → Energy** using turbine efficiency & power curves.
3. **Energy → ROI** by estimating returns on electricity sales.
4. **Interactive Tools** help users adjust project years, turbine size, and location.

👉 Think of it like filling water into buckets 💧 — faster wind = more water flow = more energy!
""")
