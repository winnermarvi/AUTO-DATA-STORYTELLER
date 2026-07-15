import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

# Restored layout to wide to use the full width of your screen
st.set_page_config(page_title="AI Business Analyst", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Style the primary button (Generate Analysis) to a professional green */
    .stButton > button[kind="primary"] {
        background-color: #059669; 
        color: white;
        border: none;
    }
    
    /* Slightly darker green on hover for a polished feel */
    .stButton > button[kind="primary"]:hover {
        background-color: #047857;
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ================= TITLE & HERO SECTION =================
st.title("🤖 AI Business Analyst")
st.markdown("Automated EDA, predictive modeling, and AI-powered business recommendations.")
st.markdown("---")

# ================= SESSION STATE =================
if "result" not in st.session_state:
    st.session_state.result = None

if "df" not in st.session_state:
    st.session_state.df = None

if "target_col" not in st.session_state:
    st.session_state.target_col = None

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if "file_bytes" not in st.session_state:
    st.session_state.file_bytes = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "pdf_response" not in st.session_state:                      ##########
    st.session_state.pdf_response = None

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv"]
)

if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.session_state.file_bytes = uploaded_file.getvalue()
    st.session_state.file_name = uploaded_file.name
    
    with st.container(border=True):
        st.markdown(f"📄 **Loaded File:** `{st.session_state.file_name}`")
        st.markdown(f"📊 **Dimensions:** {st.session_state.df.shape[0]:,} Rows | {st.session_state.df.shape[1]} Columns")

df = st.session_state.df

# ================= TARGET COLUMN =================
if df is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    target_col = st.selectbox(
        "Select Target Column",
        df.columns,
        index=(
            list(df.columns).index(st.session_state.target_col)
            if st.session_state.target_col in df.columns
            else 0
        )
    )

    # ================= ANALYSIS BUTTON =================
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate Analysis", type="primary", width='stretch'):
        with st.spinner("Generating Analysis..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            data = {
                "target_col": target_col
            }

            response = requests.post(
                f"{BACKEND_URL}/analyze",
                files=files,
                data=data
            )

            st.session_state.result = response.json()
            st.session_state.target_col = target_col
            st.session_state.analysis_complete = True
            st.session_state.conversation_history = []

# ================= DISPLAY RESULTS =================
if st.session_state.result is not None:
    st.markdown("---")
    result = st.session_state.result

    # 2x2 Metric Layout to prevent text truncation and ensure clean spelling display
    m_row1_col1, m_row1_col2 = st.columns(2)
    with m_row1_col1:
        with st.container(border=True):
            st.metric(label="🔢 Total Rows", value=f"{df.shape[0]:,}")
    with m_row1_col2:
        with st.container(border=True):
            st.metric(label="📋 Total Columns", value=f"{df.shape[1]}")

    m_row2_col1, m_row2_col2 = st.columns(2)
    with m_row2_col1:
        with st.container(border=True):
            st.metric(label="🎯 Problem Type", value=str(result.get("problem_type", "N/A")).capitalize())
    with m_row2_col2:
        with st.container(border=True):
            st.metric(label="🏆 Best Model Selected", value=str(result.get("best_model", "N/A")).upper())

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for modern distribution of information
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "EDA", "Machine Learning", "Recommendations"])

    with tab1:
        with st.container(border=True):
            st.markdown("### 📑 Executive Summary")
            st.write(result.get("narrative"))

    with tab2:
        with st.container(border=True):
            st.markdown("### 🔍 Dataset Insights")
            st.code(result.get("eda_story"))

    with tab3:
        with st.container(border=True):
            st.markdown("### 🤖 Model Findings")
            st.code(result.get("ml_story"))
        with st.container(border=True):
            st.markdown("### 🔑 Key Drivers")
            st.code(result.get("feature_importance_story"))

    with tab4:
        with st.container(border=True):
            st.markdown("### 💡 Strategic Recommendations")
            st.code(result.get("recommendation_story"))

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= ACTIONS ROW =================
    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if st.session_state.file_bytes is not None:
            if (
                st.session_state.file_bytes is not None
                and st.session_state.file_name is not None
            ):
                files = {
                    "file": (
                        st.session_state.file_name,
                        st.session_state.file_bytes,
                        "text/csv"
                    )
                }

            data = {
                "target_col": st.session_state.target_col
            }

            if st.session_state.pdf_response is None:
                st.session_state.pdf_response = requests.post(
                    f"{BACKEND_URL}/generate-report",
                    files=files,
                    data=data
                )

            st.download_button(
                label="📥 Download PDF Report",
                data=st.session_state.pdf_response.content,
                file_name="data_report.pdf",
                mime="application/pdf",
                width='stretch'
            )

    with action_col2:
        if st.button("🔄 Reset Analysis", width='stretch'):
            st.session_state.result = None
            st.session_state.df = None
            st.session_state.target_col = None
            st.session_state.analysis_complete = False
            st.session_state.file_bytes = None
            st.session_state.file_name = None
            st.session_state.conversation_history = []
            st.session_state.pdf_response = None
            st.rerun()