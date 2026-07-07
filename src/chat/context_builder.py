def build_context(analysis):

    context = f"""
        You are analyzing the following dataset.

        -------------------------
        EXECUTIVE SUMMARY
        -------------------------

        {analysis["narrative"]}

        -------------------------
        DATA QUALITY / EDA FINDINGS
        -------------------------

        {analysis["eda_story"]}

        -------------------------
        MODEL FINDINGS
        -------------------------

        {analysis["ml_story"]}

        -------------------------
        FEATURE IMPORTANCE
        -------------------------

        {analysis["feature_importance_story"]}

        -------------------------
        BUSINESS RECOMMENDATIONS
        -------------------------

        {analysis["recommendation_story"]}
        """

    return context.strip()