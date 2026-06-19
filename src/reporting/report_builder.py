def build_report(result):
    report = {
        "executive_summary": result['llm_report']['narrative'],
        "dataset_overview": {
            "problem_type": result["problem_info"]["problem_type"],
            "best_model": result["best_model_info"]["best_model"]
        },
        "data_quality": result["eda_story"],
        "model_findings": result["ml_story"],
        "key_drivers": result["feature_importance_story"],
        "recommendations": result["recommendation_story"]
    }
    return report

