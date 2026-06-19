from src.llm.prompt_builder import build_prompt
from src.llm.narrative_generator import generate_narrative

def llm_pipeline(ml_story,feature_importance_story,recommendation_story):

    prompt = build_prompt(ml_story, feature_importance_story, recommendation_story)

    narrative = generate_narrative(prompt)

    return {
        "prompt" : prompt,
        "narrative" : narrative
    }