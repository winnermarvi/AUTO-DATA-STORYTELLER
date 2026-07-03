from src.preprocessing.pipeline import preprocess_data_pipeline   
from src.ml.ml_pipeline import ml_pipeline

def run_ml(df,target_col):

    target = df[target_col]

    features = df.drop(columns=[target_col])

    processed_df = preprocess_data_pipeline(features)

    processed_df[target_col] = target

    ml_report = ml_pipeline(processed_df, target_col)

    target_distribution = ( target.value_counts().to_dict())

    return {
        "problem_info": ml_report["problem_info"],
        "evaluation_results": ml_report["evaluation_results"],
        "best_model_info": ml_report["best_model_info"],
        "ml_insights": ml_report["insights"],
        "ml_story": ml_report["story"],

        "feature_importance" : ml_report["feature_importance"],
        "feature_importance_insights" : ml_report["feature_importance_insights"],
        "feature_importance_story" : ml_report["feature_importance_story"],

        "recommendations" : ml_report["recommendations"],
        "recommendation_story" : ml_report["recommendation_story"],

        "target_distribution": target_distribution
    }