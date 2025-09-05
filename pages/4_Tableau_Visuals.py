import streamlit as st

st.title("📊 Tableau Visuals")

st.markdown("""
Here you can view interactive Tableau dashboards directly inside our app.  
We use Tableau for **rich visualizations**, while keeping calculations & forecasting in Python.
""")

# Example Tableau Public embed (replace link with your own)
tableau_url = "https://public.tableau.com/views/RegionalSampleWorkbook/Storms"

st.markdown(
    f"""
    <iframe src="{tableau_url}" width="100%" height="600" frameborder="0"></iframe>
    """,
    unsafe_allow_html=True
)
