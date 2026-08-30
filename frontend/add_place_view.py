import streamlit as st
import pandas as pd
import datetime
from database.db_manager import add_record, reset_database
from backend.dummy_generator import generate_dummy_data

def render_add_place_view():
    st.subheader("➕ Add New Incident Record / Location")
    st.markdown("Enter details of a road incident or location record. The system will save it to the database and automatically re-calculate risk scores for all locations.")

    with st.form("add_place_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            m_loc = st.text_input("📍 Location Name", placeholder="e.g. Silk Board Junction")
            m_date = st.date_input("📅 Incident Date", datetime.date.today())
            m_time = st.time_input("⏰ Incident Time", datetime.datetime.now().time())
            m_road = st.selectbox("🛣️ Road Type", ["Highway", "Urban Road", "Rural Road", "Intersection", "Expressway"])
            m_weather = st.selectbox("🌤️ Weather Condition", ["Clear", "Rainy", "Foggy", "Snow", "Stormy"])
        with c2:
            m_lat = st.number_input("🌐 Latitude", value=12.9716, format="%.4f")
            m_lon = st.number_input("🌐 Longitude", value=77.5946, format="%.4f")
            m_injuries = st.number_input("🤕 Injuries", min_value=0, max_value=100, value=1)
            m_fatalities = st.number_input("💀 Fatalities", min_value=0, max_value=50, value=0)
            m_cost = st.number_input("💵 Material Loss Cost ($)", min_value=0.0, value=15000.0, step=1000.0)

        submitted = st.form_submit_button("📥 Save & Classify Risk Level")
        
        if submitted:
            if not m_loc.strip():
                st.error("Please enter a valid location name.")
            else:
                rec = {
                    "Date": m_date.strftime("%Y-%m-%d"),
                    "Time": m_time.strftime("%H:%M"),
                    "Location_Name": m_loc.strip(),
                    "Latitude": m_lat,
                    "Longitude": m_lon,
                    "Injuries": m_injuries,
                    "Fatalities": m_fatalities,
                    "Material_Loss_Cost": m_cost,
                    "Road_Type": m_road,
                    "Weather_Condition": m_weather
                }
                add_record(rec)
                new_df = pd.DataFrame([rec])
                st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                st.success(f"✅ Record for '{m_loc}' saved successfully! All place risk levels updated.")

    st.markdown("---")
    st.subheader("⚙️ Dataset Management")
    col_reset, col_csv = st.columns([1, 2])
    with col_reset:
        if st.button("🔄 Reset to Baseline Synthetic Data"):
            dummy_df = generate_dummy_data()
            reset_database(dummy_df)
            st.session_state.df = dummy_df
            st.info("Dataset reset to default synthetic baseline.")
