import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
import streamlit.components.v1 as components
import plotly.express as px

def render_map_view(df):
    st.subheader("🗺️ Geospatial Hazard Density & K-Means Risk Clustering Map")
    st.markdown("Interactive map showing location risk clusters and incident severity density.")

    if df.empty:
        st.warning("No location data available to display on the map.")
        return

    m_col1, m_col2 = st.columns([3, 1])
    
    with m_col2:
        st.markdown("#### ⚙️ Map Filters & View")
        risk_filter = st.multiselect("Filter Risk Levels", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
        map_engine = st.radio("Map Rendering Engine", ["Folium (Interactive)", "Plotly Map (Density/Scatter)"], index=0)
        show_heatmap = st.checkbox("Show Density Heatmap", value=True)

    filtered_df = df[df["Risk_Level"].isin(risk_filter)].copy()
    
    if filtered_df.empty:
        st.info("No locations match the selected risk filter.")
        return

    avg_lat = float(filtered_df["Latitude"].mean())
    avg_lon = float(filtered_df["Longitude"].mean())

    if "Folium" in map_engine:
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11, tiles="OpenStreetMap")
        
        if show_heatmap:
            heat_data = [[float(row["Latitude"]), float(row["Longitude"]), float(row["Severity_Score"])] for _, row in filtered_df.iterrows()]
            HeatMap(heat_data, radius=18, blur=12, max_zoom=1).add_to(m)
            
        color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
        
        for _, row in filtered_df.iterrows():
            loc_name = str(row.get("Location_Name", "Unknown Location"))
            risk_lvl = str(row.get("Risk_Level", "Unknown"))
            sev_score = float(row.get("Severity_Score", 0.0))
            fatalities = int(row.get("Fatalities", 0))
            injuries = int(row.get("Injuries", 0))
            cost = float(row.get("Material_Loss_Cost", 0.0))
            
            popup_html = f"""
            <div style="font-family: Arial, sans-serif; min-width: 180px;">
                <h4 style="margin:0 0 6px 0; color:#1e293b;">{loc_name}</h4>
                <p style="margin:2px 0;"><b>Risk Level:</b> <span style="color:{color_map.get(risk_lvl, '#333')}; font-weight:bold;">{risk_lvl}</span></p>
                <p style="margin:2px 0;"><b>Severity Score:</b> {sev_score:.2f}</p>
                <p style="margin:2px 0;"><b>Fatalities:</b> {fatalities}</p>
                <p style="margin:2px 0;"><b>Injuries:</b> {injuries}</p>
                <p style="margin:2px 0;"><b>Loss Cost:</b> ${cost:,.2f}</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[float(row["Latitude"]), float(row["Longitude"])],
                radius=7 + (sev_score / 6.0),
                color=color_map.get(risk_lvl, "#3b82f6"),
                fill=True,
                fill_color=color_map.get(risk_lvl, "#3b82f6"),
                fill_opacity=0.8,
                popup=folium.Popup(popup_html, max_width=280)
            ).add_to(m)
            
        with m_col1:
            map_html = m._repr_html_()
            components.html(map_html, height=520, scrolling=False)
            
    else:
        with m_col1:
            color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
            if hasattr(px, "scatter_map"):
                fig_map = px.scatter_map(
                    filtered_df,
                    lat="Latitude",
                    lon="Longitude",
                    color="Risk_Level",
                    size="Severity_Score",
                    hover_name="Location_Name",
                    hover_data={"Fatalities": True, "Injuries": True, "Material_Loss_Cost": ":$.2f", "Severity_Score": ":.2f"},
                    color_discrete_map=color_map,
                    zoom=10,
                    center={"lat": avg_lat, "lon": avg_lon},
                    title="Geospatial Risk Distribution",
                    map_style="open-street-map",
                    template="plotly_dark"
                )
            else:
                fig_map = px.scatter_mapbox(
                    filtered_df,
                    lat="Latitude",
                    lon="Longitude",
                    color="Risk_Level",
                    size="Severity_Score",
                    hover_name="Location_Name",
                    hover_data={"Fatalities": True, "Injuries": True, "Material_Loss_Cost": ":$.2f", "Severity_Score": ":.2f"},
                    color_discrete_map=color_map,
                    zoom=10,
                    center={"lat": avg_lat, "lon": avg_lon},
                    title="Geospatial Risk Distribution",
                    mapbox_style="open-street-map",
                    template="plotly_dark"
                )
            fig_map.update_layout(
                height=520,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_map, width="stretch")
