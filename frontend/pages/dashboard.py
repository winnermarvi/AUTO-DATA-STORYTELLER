import streamlit as st

st.title("AUTO DATA STORYTELLER")

if st.session_state.get("result") is None:

    st.error(f"Generate Analysis for Dashboard")

else:

    result = st.session_state.result
    df = st.session_state.df

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("🎯 **Problem Type**")
            st.subheader(str(result.get("problem_type")).capitalize()) 

    with col2:
        with st.container(border=True):
            st.markdown("🏆 **Best Model**")
            st.subheader(result.get("best_model"))

    with col3:
        with st.container(border=True):
            st.markdown("📊 **Dataset Size**")
            st.markdown(f"**Rows:** {df.shape[0]:,} | **Cols:** {df.shape[1]}")

    st.header("EXECUTIVE SUMMARY")
    st.write(result.get("narrative"))

    col1,col2 = st.columns(2)

    with col1:
        st.header("KEY DRIVERS")
        st.image(
            "src/reports/charts/feature_importance.png",
            use_container_width=True
        )

    with col2:
        st.header("DATA QUALITY")
        st.image(
            "src/reports/charts/missing_values.png",
            use_container_width=True
        )


    st.header("RECOMMENDATIONS")
    st.code(result.get("recommendation_story"))

    st.header("TECHNICAL DETAILS")
            
    with st.expander("Dataset Insights"):

        st.code(result.get("eda_story"))

    with st.expander("Model Findings"): 
            
        st.code(result.get("ml_story"))
