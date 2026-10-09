import streamlit as st
from database.db_manager import init_db, load_all_records, save_records
from backend.dummy_generator import generate_dummy_data
from backend.data_processing import calculate_severity
from backend.clustering import perform_clustering
from backend.predictor import train_predictive_model
from frontend.styles import apply_custom_styles
from frontend.sidebar import render_sidebar
from frontend.kpi_metrics import render_kpi_metrics
from frontend.place_registry import render_place_registry
from frontend.add_place_view import render_add_place_view
from frontend.map_view import render_map_view
from frontend.prediction_view import render_prediction_view
from frontend.analytics_view import render_analytics_view

st.set_page_config(
    page_title="Road Accident Analysis & Predictive Risk System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()
init_db()

if "df" not in st.session_state:
    existing_df = load_all_records()
    if existing_df.empty:
        dummy_df = generate_dummy_data()
        save_records(dummy_df)
        st.session_state.df = dummy_df
    else:
        st.session_state.df = existing_df

render_sidebar()

df = st.session_state.df.copy()
df = calculate_severity(df)
df = perform_clustering(df)
rf_model = train_predictive_model(df)

st.title("🛡️ Road Accident Analysis & Predictive Risk System")
st.markdown("Monitor registered locations, add new records, predict hazard levels, and plan safety interventions in real time.")
st.markdown("---")

render_kpi_metrics(df)

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Registered Places & Risk Status",
    "➕ Add New Location Record",
    "🤖 Risk Level Predictor",
    "🗺️ Geospatial Map View",
    "📊 Analytics & Trends"
])

with tab1:
    render_place_registry(df)

with tab2:
    render_add_place_view()

with tab3:
    render_prediction_view(rf_model, df)

with tab4:
    render_map_view(df)

with tab5:
    render_analytics_view(df)
