import streamlit as st
import pandas as pd
import requests


# ================= TITLE =================

st.set_page_config(page_title="AI Business Analyst", layout="wide")

st.title("🤖 AI Business Analyst")

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

# ================= FILE UPLOAD =================

uploaded_file = st.file_uploader(
"Upload CSV File",
type=["csv"]
)

if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)

    st.session_state.file_bytes = uploaded_file.getvalue()

    st.session_state.file_name = uploaded_file.name

    st.success("File uploaded successfully!")

df = st.session_state.df

# ================= TARGET COLUMN =================

if df is not None:

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

if st.button("Generate Analysis"):

    with st.spinner("Generating Analysis....."):

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
            "http://127.0.0.1:8000/analyze",
            files=files,
            data=data
        )

        st.session_state.result = response.json()
        st.session_state.target_col = target_col
        st.session_state.analysis_complete = True
        st.session_state.conversation_history = []


# ================= DISPLAY RESULTS =================

if st.session_state.result is not None:


    result = st.session_state.result

    with st.expander("Executive Summary"):
        st.write(result.get("narrative"))

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Problem Type",
            value=result.get("problem_type", "N/A")
        )

    with col2:
        st.metric(
            label="Best Model",
            value=result.get("best_model", "N/A")
        )

    st.subheader("Dataset Insights")
    st.code(result.get("eda_story"))

    st.subheader("Model Findings")
    st.code(result.get("ml_story"))

    st.subheader("Key Drivers")
    st.code(result.get("feature_importance_story"))

    st.subheader("Recommendations")
    st.code(result.get("recommendation_story"))

    
    st.success("Analysis complete.")

    # ================= PDF DOWNLOAD =================

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

        pdf_response = requests.post(
            "http://127.0.0.1:8000/generate-report",
            files=files,
            data=data
        )

        st.download_button(
            label="📥 Download PDF",
            data=pdf_response.content,
            file_name="data_report.pdf",
            mime="application/pdf"
        )

# ================= RESET BUTTON =================

if st.session_state.result is not None:
    if st.button("🔄 Reset Analysis"):

        st.session_state.result = None
        st.session_state.df = None
        st.session_state.target_col = None
        st.session_state.analysis_complete = False
        st.session_state.file_bytes = None
        st.session_state.file_name = None
        st.session_state.conversation_history = []

        st.rerun()