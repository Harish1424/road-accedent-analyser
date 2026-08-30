import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', system-ui, sans-serif;
    }
    .stMetric {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stMetric label {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700;
        font-size: 1.6rem;
    }
    div[data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #1e40af 100%);
    }
    .badge-high {
        background-color: #ef4444;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-medium {
        background-color: #f59e0b;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-low {
        background-color: #10b981;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .risk-card-high {
        background-color: #451a1a;
        border: 1px solid #ef4444;
        color: #fca5a5;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    .risk-card-medium {
        background-color: #45301a;
        border: 1px solid #f59e0b;
        color: #fde68a;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    .risk-card-low {
        background-color: #1a452a;
        border: 1px solid #10b981;
        color: #86efac;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
</style>
""",
        unsafe_allow_html=True,
    )
