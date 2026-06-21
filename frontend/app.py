import streamlit as st
import pandas as pd
import requests

st.title("AUTO DATA STORYTELLER")

uploaded_file = st.file_uploader(
"Upload CSV File",
type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    target_col = st.selectbox(
        "Select Target Column",
        df.columns
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