import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.title("AUTO DATA STORYTELLER")

st.header("DASHBOARD")

if st.session_state.get("result") is None:

    st.error(f"Generate Analysis for Dashboard")

else:

    result = st.session_state.result
    df = st.session_state.df

    metric_name = result.get("best_metric")
    metric_value = result.get("best_score")

    if result.get("problem_type") == "classification":
        display_value = f"{metric_value * 100:.1f}%"
    else:
        display_value = f"{metric_value:.3f}"

    model_score = round(result.get("best_score") * 100, 1)

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("🎯 **Problem Type**")
            st.subheader(str(result.get("problem_type")).upper()) 

    with col2:
        with st.container(border=True):
            st.markdown("🏆 **Best Model**")
            st.subheader(str(result.get("best_model")).upper())

    with col3:
        with st.container(border=True):
            st.markdown("📊 **Dataset Size**")
            st.markdown(f"**Rows:** {df.shape[0]:,} | **Cols:** {df.shape[1]}")

    with col4:
        with st.container(border=True):
            st.markdown("🧹 **Missing Data**")
            st.subheader(f"{result['missing_pct']}%")

    with col5:
        with st.container(border=True):
            st.markdown("💚 **Health Score**")
            st.subheader(f"{result['health_score']}/100")

    with col6:
        with st.container(border=True):
            st.markdown(f"🚀 **{str(metric_name).upper()} Score**")
            st.subheader(display_value)

    st.header("MODEL PERFORMANCE")

    st.subheader("GUAGE SCORE")

    score = result.get("best_score") * 100

    gauge_fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={
                        "text":
                        f"{result['best_metric']} Score"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100]
                        },
                        "steps": [
                            {"range": [0, 60]},
                            {"range": [60, 80]},
                            {"range": [80, 100]}
                        ]
                    }
                )
            )

    st.plotly_chart(
                gauge_fig,
                use_container_width=True
            )


    st.subheader(f"🎯 Distribution of {result.get('target_column')}")
        
    target_df = pd.DataFrame( list(result.get("target_distribution").items()), columns=["Class", "Count"])
            
    target_fig = px.pie( target_df, names="Class", values="Count", title="Target Distribution")

    st.plotly_chart( target_fig, use_container_width=True)

    st.subheader("EXECUTIVE SUMMARY")
    st.write(result.get("narrative"))

    
    importance_df = pd.DataFrame( result["feature_importance"], columns=["Feature", "Importance"] )

    importance_df = importance_df.sort_values( by="Importance", ascending=True )

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Feature Importance"
    )

    fig.update_layout( xaxis_title="Importance Score", yaxis_title="", showlegend=False, height=450 )

    st.subheader("KEY DRIVERS")
    st.plotly_chart( fig, use_container_width=True )

    
    missing_df = pd.DataFrame( list(result["missing_values"].items()), columns=["Column", "Missing"] )

    missing_df = missing_df[missing_df["Missing"] > 0]
        
    missing_df = missing_df.sort_values(by="Missing", ascending=True)

    missing_fig = px.bar( missing_df, x="Missing", y="Column", orientation="h", title="Missing Values by Column")

    missing_fig.update_layout(
        xaxis_title="Missing Count",
        yaxis_title="",
        height=450,
        showlegend=False
    )

    st.subheader("DATA QUALITY")
    st.plotly_chart( missing_fig, use_container_width=True)

    st.subheader("RECOMMENDATIONS")
    st.code(result.get("recommendation_story"))

    st.subheader("TECHNICAL DETAILS")
            
    with st.expander("Dataset Insights"):

        st.code(result.get("eda_story"))

    with st.expander("Model Findings"): 
            
        st.code(result.get("ml_story"))
