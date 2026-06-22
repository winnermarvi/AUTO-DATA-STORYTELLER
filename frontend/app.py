import streamlit as st
import pandas as pd
import requests

if "result" not in st.session_state:
    st.session_state.result = None

if "df" not in st.session_state:
    st.session_state.df = None

if "target_col" not in st.session_state:
    st.session_state.target_col = None

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

st.title("AUTO DATA STORYTELLER")

uploaded_file = st.file_uploader(
"Upload CSV File",
type=["csv"]
)

if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

df = st.session_state.df

if df is not None:
    target_col = st.selectbox(
        "Select Target Column",
        df.columns,
        index=list(df.columns).index(st.session_state.target_col)
        if st.session_state.target_col in df.columns
        else 0
    )

files = None
data = None

if st.button("Generate Analysis"):
    if uploaded_file is None:
        st.error("NO Dataset found")
    else:
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

        pdf_response = requests.post(
                "http://127.0.0.1:8000/genrate-report",
                files=files,
                data=data
            )

        file_bytes = pdf_response.content


        st.download_button(
                    label="📥 Download PDF",
                    data=file_bytes,
                    file_name="data_report.pdf",
                    mime="application/pdf"
                )
        
        if st.button("🔄 Reset Analysis"):
            for key in [
                "result",
                "df",
                "target_col",
                "analysis_complete"
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()