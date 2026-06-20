
def build_prompt(ml_story,feature_importance_story,recommendation_story):

    prompt = f"""Act as a senior business analyst.

                Translate the machine learning findings into business insights.

                Do not discuss algorithms, model names, or technical metrics unless necessary.
                Focus on business impact, drivers, risks, and recommendations.

                MODEL PERFORMANCE:
                {"\n".join(ml_story[1:])}

                KEY DRIVERS:
                {"\n".join(feature_importance_story[1:])}

                RECOMMENDATIONS:  
                {"\n".join(recommendation_story[1:])}

                Write a concise Executive Summary.

                Summarize:
                - overall model performance
                - major business drivers
                - business implications

                Maximum 2-3 paragraphs.
                Use clear business language.
                Avoid technical jargon."""
    
    return prompt