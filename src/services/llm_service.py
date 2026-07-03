from src.llm.llm_pipeline import llm_pipeline

def generate_summary( ml_story, feature_importance_story, recommendation_story):

    llm_report = llm_pipeline( ml_story, feature_importance_story, recommendation_story)

    return llm_report