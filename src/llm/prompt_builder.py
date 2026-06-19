
def build_prompt(ml_story,feature_importance_story,recommendation_story):

    prompt = f"""You are a senior business analyst.

                Analyze the following machine learning findings and create a professional business summary.

                MODEL PERFORMANCE:
                {"\n".join(ml_story)}

                KEY DRIVERS:
                {"\n".join(feature_importance_story)}

                RECOMMENDATIONS:  
                {"\n".join(recommendation_story)}

                Write:
                1. Executive Summary
                2. Key Drivers
                3. Business Recommendations

                Use clear business language.
                Avoid technical jargon."""
    
    return prompt