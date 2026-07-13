import streamlit as st
import pandas as pd
import requests
import plotly.io as pio
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="AI Business Analyst", layout="wide")

suggested_questions = [
    "Can you summarize this dataset?",
    "What data quality issues did you find?",
    "Which features are the most important?",
    "Why was this model selected as the best model?",
    "Explain the model performance in simple terms.",
    "What business recommendations do you have?",
    "What are the key insights from the analysis?",
    "What patterns or trends stand out in this dataset?",
    "What should I improve in this dataset before building another model?",
    "Explain this analysis as if I were presenting it to a business stakeholder."
]

st.title("💬 Chat with Data")

if not st.session_state.get("analysis_complete", False):
    st.warning("Please analyze a dataset first.")
    st.stop()

if "processing_question" not in st.session_state:
    st.session_state["processing_question"] = None

result = st.session_state.result

st.markdown("---")

# 💡 Suggested Questions Section
st.markdown("### 💡 Suggested Questions")

grid_col1, grid_col2 = st.columns(2)

# 2. Buttons ONLY set the next question to process
with grid_col1:
    for i in range(5):
        if st.button(f"[Q{i+1}] {suggested_questions[i]}", key=f"q_{i+1}", width='stretch'):
            st.session_state["processing_question"] = suggested_questions[i]
            st.rerun()

with grid_col2:
    for i in range(5, 10):
        if st.button(f"[Q{i+1}] {suggested_questions[i]}", key=f"q_{i+1}", width='stretch'):
            st.session_state["processing_question"] = suggested_questions[i]
            st.rerun()

# 3. Handle Custom Chat Inputs the same way
if user_query := st.chat_input("Ask a question..."):
    st.session_state["processing_question"] = user_query
    st.rerun()

# 4. UNIFIED API EXECUTION ENGINE (Runs safely outside button scopes)
if st.session_state["processing_question"]:
    current_q = st.session_state["processing_question"]
    st.session_state["processing_question"] = None # Reset immediately to avoid infinite loops
    
    # Append the User prompt to the visible history
    st.session_state["conversation_history"].append({"role": "user", "content": current_q})
    
    with st.spinner("AI is thinking..."):
        try:

            df = st.session_state.get("df")
            if df is not None:
                # .fillna(None) converts NaN/NaT values to Python None (JSON null)
                # .astype(object) ensures pandas allows None values without converting them back to NaN
                df_clean = df.astype(object).where(pd.notnull(df), None)
                df_json = df_clean.to_dict(orient="records")
            else:
                df_json = []

            analysis = st.session_state.get("result", {}).get("analysis", {})

            payload = {
                "df": df_json,
                "analysis": analysis,
                "question": current_q,
                "conversation_history": st.session_state["conversation_history"]
            }
            chat_response = requests.post(f"{BACKEND_URL}/chat", json=payload)
            
            if chat_response.status_code == 200:
                res_json = chat_response.json()
                chart_json = res_json.get("chart")
                ai_answer = res_json.get("response") or "⚠️ Empty response content received from API."
                st.session_state["conversation_history"].append({"role": "assistant", "content": ai_answer, "chart": chart_json})
            else:
                st.error(f"Backend Error: {chat_response.status_code}")
        except Exception as e:
            st.error(f"Connection failed: {e}")


st.markdown("---")
st.markdown("### 💬 Conversation")

# 5. Render everything together flawlessly
for msg in st.session_state["conversation_history"]:
    with st.chat_message(msg["role"]):
        
        st.write(msg["content"])

        if msg.get("chart"):

            fig = pio.from_json(msg["chart"])

            st.plotly_chart(
                fig,
                width='stretch'
            )