import streamlit as st
import pandas as pd
import plotly.express as px
from backend.predictor import predict_scenario_risk
from backend.recommendation import get_resource_recommendations

def render_prediction_view(rf_model, df=None):
    st.subheader("🤖 Predict Risk Level & Location Risk Analysis")
    st.markdown("Search for a registered place or input custom conditions to evaluate historical hazard levels and predict real-time scenario risk.")

    road_options = ["Highway", "Urban Road", "Rural Road", "Intersection", "Expressway"]
    weather_options = ["Clear", "Rainy", "Foggy", "Snow", "Stormy"]
    day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    selected_location = None
    default_road = "Highway"
    default_weather = "Clear"
    hist_risk = None
    avg_severity = None
    total_accidents = 0
    lat_val = None
    lon_val = None

    if df is not None and not df.empty and "Location_Name" in df.columns:
        locations_list = sorted(list(df["Location_Name"].dropna().unique()))

        st.markdown("#### 📍 Search / Select Location")
        loc_col1, loc_col2 = st.columns([2, 1])

        with loc_col1:
            location_choice = st.selectbox(
                "🔍 Registered Monitored Location",
                ["-- Custom Scenario (No Location Selected) --"] + locations_list,
                index=0,
                help="Select a location to pre-fill known road conditions and review historical risk metrics."
            )

        if location_choice != "-- Custom Scenario (No Location Selected) --":
            selected_location = location_choice
            loc_df = df[df["Location_Name"] == selected_location]

            total_accidents = len(loc_df)

            if "Latitude" in loc_df.columns and not loc_df["Latitude"].isna().all():
                lat_val = float(loc_df["Latitude"].dropna().mean())
            if "Longitude" in loc_df.columns and not loc_df["Longitude"].isna().all():
                lon_val = float(loc_df["Longitude"].dropna().mean())

            if "Severity_Score" in loc_df.columns and not loc_df["Severity_Score"].isna().all():
                avg_severity = float(loc_df["Severity_Score"].dropna().mean())

            if "Risk_Level" in loc_df.columns and not loc_df["Risk_Level"].isna().all():
                mode_risk = loc_df["Risk_Level"].mode()
                hist_risk = mode_risk.iloc[0] if not mode_risk.empty else str(loc_df["Risk_Level"].iloc[0])

            if "Road_Type" in loc_df.columns and not loc_df["Road_Type"].isna().all():
                mode_road = loc_df["Road_Type"].mode()
                if not mode_road.empty and mode_road.iloc[0] in road_options:
                    default_road = mode_road.iloc[0]

            if "Weather_Condition" in loc_df.columns and not loc_df["Weather_Condition"].isna().all():
                mode_weather = loc_df["Weather_Condition"].mode()
                if not mode_weather.empty and mode_weather.iloc[0] in weather_options:
                    default_weather = mode_weather.iloc[0]

            with loc_col2:
                st.markdown("**Historical Location Profile**")
                risk_badge_color = "#ef4444" if hist_risk == "High" else ("#f59e0b" if hist_risk == "Medium" else "#10b981")
                st.markdown(
                    f"""
                    <div style="background-color: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 12px;">
                        <h4 style="margin: 0 0 4px 0; color: #38bdf8;">📍 {selected_location}</h4>
                        <p style="margin: 2px 0; font-size: 0.9rem;"><b>Historical Risk (K-Means):</b> <span style="color:{risk_badge_color}; font-weight:bold;">{hist_risk if hist_risk else 'N/A'}</span></p>
                        <p style="margin: 2px 0; font-size: 0.85rem; color: #94a3b8;"><b>Coordinates:</b> {f'{lat_val:.4f}, {lon_val:.4f}' if lat_val is not None and lon_val is not None else 'N/A'}</p>
                        <p style="margin: 2px 0; font-size: 0.85rem; color: #94a3b8;"><b>Total Logged Accidents:</b> {total_accidents}</p>
                        <p style="margin: 2px 0; font-size: 0.85rem; color: #94a3b8;"><b>Avg Severity Score:</b> {f'{avg_severity:.2f}' if avg_severity is not None else 'N/A'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown("---")

    p_col1, p_col2 = st.columns([1, 1])

    with p_col1:
        st.markdown("#### ⚙️ Scenario Input Conditions")

        road_idx = road_options.index(default_road) if default_road in road_options else 0
        weather_idx = weather_options.index(default_weather) if default_weather in weather_options else 0

        widget_key_suffix = f"_{selected_location}" if selected_location else "_custom"

        pred_hour = st.slider("⏰ Hour of Day (24h format)", 0, 23, 18, key=f"pred_hour{widget_key_suffix}")
        pred_day = st.selectbox("📅 Day of Week", day_options, index=0, key=f"pred_day{widget_key_suffix}")
        pred_road = st.selectbox("🛣️ Road Type", road_options, index=road_idx, key=f"pred_road{widget_key_suffix}")
        pred_weather = st.selectbox("🌤️ Weather Condition", weather_options, index=weather_idx, key=f"pred_weather{widget_key_suffix}")

        prediction, prob_dict = predict_scenario_risk(rf_model, pred_hour, pred_day, pred_road, pred_weather)

    with p_col2:
        st.markdown("#### 🎯 Model Prediction Outcome")
        loc_title = f" for {selected_location}" if selected_location else ""
        if prediction == "High":
            st.markdown(f"<div class='risk-card-high'><h2>🔴 ML Predicted Risk: HIGH{loc_title}</h2>Confidence / Class Prob: {prob_dict.get('High', 0)*100:.1f}%</div>", unsafe_allow_html=True)
        elif prediction == "Medium":
            st.markdown(f"<div class='risk-card-medium'><h2>🟡 ML Predicted Risk: MEDIUM{loc_title}</h2>Confidence / Class Prob: {prob_dict.get('Medium', 0)*100:.1f}%</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='risk-card-low'><h2>🟢 ML Predicted Risk: LOW{loc_title}</h2>Confidence / Class Prob: {prob_dict.get('Low', 0)*100:.1f}%</div>", unsafe_allow_html=True)

        prob_df = pd.DataFrame({"Risk Category": list(prob_dict.keys()), "Model Probability": list(prob_dict.values())})
        fig_prob = px.bar(
            prob_df, x="Risk Category", y="Model Probability", color="Risk Category",
            color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"},
            title="Random Forest Class Probability Breakdown", template="plotly_dark"
        )
        fig_prob.update_layout(height=240, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_prob, width="stretch")

    st.markdown("---")
    st.subheader("💡 Recommended Actions & Safety Interventions")

    risk_actions, env_actions = get_resource_recommendations(prediction, pred_weather, pred_road)
    rec_col1, rec_col2 = st.columns(2)

    with rec_col1:
        st.markdown("#### 🛡️ Direct Safety Interventions")
        for action in risk_actions:
            st.markdown(f"- {action}")

    with rec_col2:
        st.markdown("#### 🌧️ Weather & Road Specific Advisories")
        for rec in env_actions:
            st.markdown(f"- {rec}")
