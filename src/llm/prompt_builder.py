
def build_prompt(ml_story,feature_importance_story,recommendation_story):

    prompt = f"""
        You are a Senior Business Analyst preparing a report for executives and business stakeholders.

        Your task is to convert machine learning findings into clear business insights.

        IMPORTANT RULES:
        - Do NOT mention algorithms, model names, F1 scores, accuracy scores, or technical metrics unless absolutely necessary.
        - Do NOT use technical data science terminology.
        - Focus on business impact, opportunities, risks, and strategic actions.
        - Write in a professional consulting-style tone.
        - Make the insights actionable.
        - Avoid bullet points.
        - Write as a narrative report.

        MODEL FINDINGS:
        {" ".join(ml_story[1:])}

        KEY DRIVERS:
        {" ".join(feature_importance_story[1:])}

        RECOMMENDATIONS:
        {" ".join(recommendation_story[1:])}

        Generate an Executive Summary with the following structure:

        1. Executive Summary
        - Brief overview of findings
        - Overall confidence in the analysis

        2. Key Business Drivers
        - Explain the most important factors influencing outcomes
        - Explain why they matter from a business perspective

        3. Business Implications
        - Describe potential impact on operations, customers, revenue, risk, or decision-making

        4. Strategic Recommendations
        - Provide practical next steps for business stakeholders

        Length:
        - 3 to 5 concise paragraphs
        - Maximum 300 words

        Use professional business language suitable for executives.
        """
    return prompt