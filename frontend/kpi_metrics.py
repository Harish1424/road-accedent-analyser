import streamlit as st

def render_kpi_metrics(df):
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_records = len(df)
    high_count = len(df[df["Risk_Level"] == "High"]) if "Risk_Level" in df.columns else 0
    med_count = len(df[df["Risk_Level"] == "Medium"]) if "Risk_Level" in df.columns else 0
    low_count = len(df[df["Risk_Level"] == "Low"]) if "Risk_Level" in df.columns else 0
    total_cost = df["Material_Loss_Cost"].sum() if "Material_Loss_Cost" in df.columns else 0.0

    col1.metric("📍 Total Places/Records", f"{total_records:,}")
    col2.metric("🔴 High Risk Places", f"{high_count:,}")
    col3.metric("🟡 Medium Risk Places", f"{med_count:,}")
    col4.metric("🟢 Low Risk Places", f"{low_count:,}")
    col5.metric("💰 Financial Loss", f"${total_cost:,.0f}")
