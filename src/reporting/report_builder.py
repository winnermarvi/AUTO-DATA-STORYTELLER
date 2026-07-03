def build_report(
    eda_story,
    ml_story,
    feature_importance_story,
    recommendation_story,
    llm_report,
    problem_info,
    best_model_info
):
    report = {
        "executive_summary": llm_report["narrative"],
        "dataset_overview": {
            "problem_type": problem_info["problem_type"],
            "best_model": best_model_info["best_model"]
        },
        "data_quality": eda_story,
        "model_findings": ml_story,
        "key_drivers": feature_importance_story,
        "recommendations": recommendation_story
    }

    return report
