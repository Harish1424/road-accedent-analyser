import streamlit as st
import pandas as pd

def render_place_registry(df):
    st.subheader("📍 Monitored Locations & Risk Classification")
    st.markdown("Overview of all registered places with calculated risk categories based on historical incidents.")

    high_risk_df = df[df["Risk_Level"] == "High"]
    if not high_risk_df.empty:
        high_locations = high_risk_df["Location_Name"].unique()
        st.error(f"🚨 **HIGH RISK PLACES ({len(high_locations)}):** {', '.join(high_locations)}")
    else:
        st.success("✅ No High-Risk places detected.")

    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search Place / Location Name", "")
    with col2:
        filter_risk = st.selectbox("Filter by Risk Level", ["All", "High", "Medium", "Low"])

    display_df = df.copy()
    if search_query:
        display_df = display_df[display_df["Location_Name"].str.contains(search_query, case=False, na=False)]
    if filter_risk != "All":
        display_df = display_df[display_df["Risk_Level"] == filter_risk]

    cols_to_show = ["Location_Name", "Risk_Level", "Severity_Score", "Fatalities", "Injuries", "Material_Loss_Cost", "Road_Type", "Weather_Condition", "Date", "Time"]
    available_cols = [c for c in cols_to_show if c in display_df.columns]
    
    formatted_df = display_df[available_cols].copy()
    if "Severity_Score" in formatted_df.columns:
        formatted_df["Severity_Score"] = formatted_df["Severity_Score"].round(2)
    if "Material_Loss_Cost" in formatted_df.columns:
        formatted_df["Material_Loss_Cost"] = formatted_df["Material_Loss_Cost"].map(lambda x: f"${x:,.2f}")

    st.dataframe(
        formatted_df,
        column_config={
            "Location_Name": st.column_config.TextColumn("Location / Place"),
            "Risk_Level": st.column_config.TextColumn("Risk Level"),
            "Severity_Score": st.column_config.NumberColumn("Severity Score"),
            "Material_Loss_Cost": st.column_config.TextColumn("Loss Cost"),
        },
        use_container_width=True,
        hide_index=True
    )
