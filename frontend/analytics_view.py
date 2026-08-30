import streamlit as st
import pandas as pd
import plotly.express as px

def render_analytics_view(df):
    st.subheader("📊 Visual Analytics & Trend Analysis")
    st.markdown("Graphical insights into historical accident distributions, temporal trends, and location risk counts.")
    
    df_copy = df.copy()
    df_copy["Hour"] = pd.to_datetime(df_copy["Time"], format="%H:%M").dt.hour
    df_copy["Date_Parsed"] = pd.to_datetime(df_copy["Date"])
    
    a_col1, a_col2 = st.columns(2)
    
    with a_col1:
        hourly_counts = df_copy.groupby("Hour").size().reset_index(name="Incident_Count")
        fig_hourly = px.bar(
            hourly_counts, x="Hour", y="Incident_Count",
            title="Hourly Incident Frequency (24-Hour Cycle)",
            labels={"Hour": "Hour of Day", "Incident_Count": "Total Incidents"},
            color="Incident_Count", color_continuous_scale="Reds",
            template="plotly_dark"
        )
        fig_hourly.update_layout(height=350)
        st.plotly_chart(fig_hourly, width="stretch")
        
    with a_col2:
        trend_df = df_copy.groupby("Date_Parsed")["Severity_Score"].sum().reset_index()
        fig_trend = px.line(
            trend_df, x="Date_Parsed", y="Severity_Score",
            title="Cumulative Risk Severity Trend Over Time",
            labels={"Date_Parsed": "Date", "Severity_Score": "Total Severity Score"},
            template="plotly_dark"
        )
        fig_trend.update_traces(line_color="#38bdf8", line_width=2.5)
        fig_trend.update_layout(height=350)
        st.plotly_chart(fig_trend, width="stretch")
        
    a_col3, a_col4 = st.columns(2)
    
    with a_col3:
        loc_df = df_copy.groupby("Location_Name")[["Injuries", "Fatalities"]].sum().reset_index()
        fig_loc = px.bar(
            loc_df, x="Location_Name", y=["Injuries", "Fatalities"],
            barmode="group", title="Injuries vs Fatalities by Location",
            color_discrete_sequence=["#f59e0b", "#ef4444"],
            template="plotly_dark"
        )
        fig_loc.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig_loc, width="stretch")
        
    with a_col4:
        weather_df = df_copy.groupby("Weather_Condition").size().reset_index(name="Count")
        fig_weather = px.pie(
            weather_df, names="Weather_Condition", values="Count",
            title="Incident Breakdown by Weather Condition",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4, template="plotly_dark"
        )
        fig_weather.update_layout(height=350)
        st.plotly_chart(fig_weather, width="stretch")
