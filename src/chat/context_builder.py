def build_context(analysis):

    eda = analysis['eda']
    ml = analysis['ml']
    llm = analysis['llm']

    context = f"""
        You are analyzing the following dataset.

        -------------------------
        EXECUTIVE SUMMARY
        -------------------------

        {llm["narrative"]}

        -------------------------
        DATA QUALITY / EDA FINDINGS
        -------------------------

        {eda["eda_story"]}

        -------------------------
        MODEL FINDINGS
        -------------------------

        {ml["ml_story"]}

        -------------------------
        FEATURE IMPORTANCE
        -------------------------

        {ml["feature_importance_story"]}

        -------------------------
        BUSINESS RECOMMENDATIONS
        -------------------------

        {ml["recommendation_story"]}
        """

    return context.strip()