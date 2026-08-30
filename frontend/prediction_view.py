import streamlit as st
import pandas as pd
import plotly.express as px
from backend.predictor import predict_scenario_risk
from backend.recommendation import get_resource_recommendations

def render_prediction_view(rf_model):
    st.subheader("🤖 Predict Risk Level for Any Place & Conditions")
    st.markdown("Select condition parameters (time, day, road type, weather) to predict whether a scenario will result in **High**, **Medium**, or **Low** risk.")

    p_col1, p_col2 = st.columns([1, 1])
    
    with p_col1:
        st.markdown("#### ⚙️ Scenario Input Conditions")
        pred_hour = st.slider("⏰ Hour of Day (24h format)", 0, 23, 18)
        pred_day = st.selectbox("📅 Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        pred_road = st.selectbox("🛣️ Road Type", ["Highway", "Urban Road", "Rural Road", "Intersection", "Expressway"])
        pred_weather = st.selectbox("🌤️ Weather Condition", ["Clear", "Rainy", "Foggy", "Snow", "Stormy"])
        
        prediction, prob_dict = predict_scenario_risk(rf_model, pred_hour, pred_day, pred_road, pred_weather)
        
    with p_col2:
        st.markdown("#### 🎯 Prediction Outcome")
        if prediction == "High":
            st.markdown(f"<div class='risk-card-high'><h2>🔴 Predicted Risk: HIGH</h2>Confidence: {prob_dict.get('High', 0)*100:.1f}%</div>", unsafe_allow_html=True)
        elif prediction == "Medium":
            st.markdown(f"<div class='risk-card-medium'><h2>🟡 Predicted Risk: MEDIUM</h2>Confidence: {prob_dict.get('Medium', 0)*100:.1f}%</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='risk-card-low'><h2>🟢 Predicted Risk: LOW</h2>Confidence: {prob_dict.get('Low', 0)*100:.1f}%</div>", unsafe_allow_html=True)
            
        prob_df = pd.DataFrame({"Risk Category": list(prob_dict.keys()), "Probability": list(prob_dict.values())})
        fig_prob = px.bar(
            prob_df, x="Risk Category", y="Probability", color="Risk Category",
            color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"},
            title="Model Probability Breakdown", template="plotly_dark"
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
