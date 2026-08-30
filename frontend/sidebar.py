import streamlit as st
import pandas as pd
import datetime
from database.db_manager import add_record, save_records, reset_database
from backend.dummy_generator import generate_dummy_data

def render_sidebar():
    st.sidebar.title("🚨 Controls & Data Input")
    st.sidebar.markdown("---")

    uploaded_file = st.sidebar.file_uploader("Upload CSV Logs", type=["csv"])
    if uploaded_file is not None:
        try:
            user_df = pd.read_csv(uploaded_file)
            required_cols = ["Date", "Time", "Location_Name", "Latitude", "Longitude", "Injuries", "Fatalities", "Material_Loss_Cost", "Road_Type", "Weather_Condition"]
            if all(col in user_df.columns for col in required_cols):
                save_records(user_df)
                st.session_state.df = user_df
                st.sidebar.success("CSV Uploaded & Saved to Local DB!")
            else:
                st.sidebar.error(f"CSV missing required columns: {required_cols}")
        except Exception as e:
            st.sidebar.error(f"Error parsing CSV: {e}")

    st.sidebar.subheader("➕ Manual Incident Logging")
    with st.sidebar.form("manual_entry_form"):
        m_date = st.date_input("Date", datetime.date.today())
        m_time = st.time_input("Time", datetime.datetime.now().time())
        m_loc = st.text_input("Location Name", "Highway Junction 42")
        m_lat = st.number_input("Latitude", value=12.9716, format="%.4f")
        m_lon = st.number_input("Longitude", value=77.5946, format="%.4f")
        m_injuries = st.number_input("Injuries", min_value=0, max_value=50, value=1)
        m_fatalities = st.number_input("Fatalities", min_value=0, max_value=20, value=0)
        m_cost = st.number_input("Material Loss Cost ($)", min_value=0.0, value=15000.0, step=1000.0)
        m_road = st.selectbox("Road Type", ["Highway", "Urban Road", "Rural Road", "Intersection", "Expressway"])
        m_weather = st.selectbox("Weather Condition", ["Clear", "Rainy", "Foggy", "Snow", "Stormy"])
        submit_btn = st.form_submit_button("Submit Incident Record")
        
        if submit_btn:
            rec = {
                "Date": m_date.strftime("%Y-%m-%d"),
                "Time": m_time.strftime("%H:%M"),
                "Location_Name": m_loc,
                "Latitude": m_lat,
                "Longitude": m_lon,
                "Injuries": m_injuries,
                "Fatalities": m_fatalities,
                "Material_Loss_Cost": m_cost,
                "Road_Type": m_road,
                "Weather_Condition": m_weather
            }
            add_record(rec)
            new_row = pd.DataFrame([rec])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.sidebar.success("New record logged & persistent in SQLite!")

    if st.sidebar.button("Reset to Default Synthetic Data"):
        dummy_df = generate_dummy_data()
        reset_database(dummy_df)
        st.session_state.df = dummy_df
        st.sidebar.info("Dataset & Local DB reset to synthetic baseline.")
