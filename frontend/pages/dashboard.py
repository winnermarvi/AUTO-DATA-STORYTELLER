import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="AI Business Analyst", layout="wide")

st.title("📊 Dashboard")

if not st.session_state.get("analysis_complete", False):
    st.warning("Please analyze a dataset first.")
    st.stop()
else:
    result = st.session_state.result
    df = st.session_state.df

    metric_name = result.get("best_metric")
    metric_value = result.get("best_score")

    if result.get("problem_type") == "classification":
        display_value = f"{metric_value * 100:.1f}%"
    else:
        display_value = f"{metric_value:.3f}"

    # ================= KEY METRICS (3x2 Grid) =================
    st.markdown("### Key Metrics")
    
    # Row 1
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        with st.container(border=True):
            st.markdown("🎯 **Problem Type**")
            st.subheader(str(result.get("problem_type")).capitalize()) 
    with m_col2:
        with st.container(border=True):
            st.markdown("🏆 **Best Model**")
            st.subheader(str(result.get("best_model")).upper())
    with m_col3:
        with st.container(border=True):
            st.markdown("📊 **Dataset Size**")
            st.markdown(f"**{df.shape[0]:,}** Rows | **{df.shape[1]}** Columns")

    # Row 2
    m_col4, m_col5, m_col6 = st.columns(3)
    with m_col4:
        with st.container(border=True):
            st.markdown("🧹 **Missing Data**")
            st.subheader(f"{result['missing_pct']}%")
    with m_col5:
        with st.container(border=True):
            st.markdown("💚 **Health Score**")
            st.subheader(f"{result['health_score']}/100")
    with m_col6:
        with st.container(border=True):
            st.markdown(f"🚀 **{str(metric_name).upper()} Score**")
            st.subheader(display_value)

    st.markdown("---")

    # ================= NARRATIVE INSIGHTS (Stacked to avoid gaps) =================
    with st.container(border=True):
        st.markdown("### 📑 Executive Summary")
        st.write(result.get("narrative"))
        
    with st.container(border=True):
        st.markdown("### 💡 Recommendations")
        st.code(result.get("recommendation_story"))

    st.markdown("---")

    # ================= VISUALIZATIONS GRID =================
    st.markdown("### Visualizations")
    
    chart_row1_col1, chart_row1_col2 = st.columns(2)
    
    # 1. Gauge Chart
    with chart_row1_col1:
        with st.container(border=True):
            st.markdown(f"**Model Performance ({result['best_metric']})**")
            score = result.get("best_score") * 100
            gauge_fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    gauge={
                        "axis": {"range": [0, 100]},
                        "steps": [
                            {"range": [0, 60], "color": "#f8fafc"},
                            {"range": [60, 80], "color": "#e2e8f0"},
                            {"range": [80, 100], "color": "#cbd5e1"}
                        ],
                        "bar": {"color": "#2563eb"}
                    }
                )
            )
            gauge_fig.update_layout(height=330, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(gauge_fig, width='stretch')

    # 2. Target Distribution
    with chart_row1_col2:
        with st.container(border=True):
            st.markdown(f"**Distribution of {result.get('target_column')}**")
            target_df = pd.DataFrame(list(result.get("target_distribution").items()), columns=["Class", "Count"])
            target_fig = px.pie(target_df, names="Class", values="Count", hole=0.4)
            target_fig.update_layout(height=330, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(target_fig, width='stretch')

    chart_row2_col1, chart_row2_col2 = st.columns(2)

    # 3. Feature Importance
    with chart_row2_col1:
        with st.container(border=True):
            st.markdown("**Key Drivers (Feature Importance)**")
            importance_df = pd.DataFrame(result["feature_importance"], columns=["Feature", "Importance"])
            importance_df = importance_df.sort_values(by="Importance", ascending=True).tail(10)
            fig = px.bar(importance_df, x="Importance", y="Feature", orientation="h")
            fig.update_layout(xaxis_title="Score", yaxis_title="", showlegend=False, height=330, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, width='stretch')

    # 4. Missing Data
    with chart_row2_col2:
        with st.container(border=True):
            st.markdown("**Data Quality (Missing Values)**")
            missing_df = pd.DataFrame(list(result["missing_values"].items()), columns=["Column", "Missing"])
            missing_df = missing_df[missing_df["Missing"] > 0].sort_values(by="Missing", ascending=True)
            
            if not missing_df.empty:
                missing_fig = px.bar(missing_df, x="Missing", y="Column", orientation="h")
                missing_fig.update_layout(xaxis_title="Count", yaxis_title="", showlegend=False, height=330, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(missing_fig, width='stretch')
            else:
                st.info("✅ No missing values found in this dataset.")

    st.markdown("---")

    # ================= TECHNICAL LOGS =================
    st.markdown("### Technical Details")
    with st.expander("View Dataset Insights & EDA Logs"):
        st.code(result.get("eda_story"))

    with st.expander("View Model Training Findings"): 
        st.code(result.get("ml_story"))