from eda.eda import analyze_data                                           # raw  df  -> report
from insights.insight_pipeline import insight_pipeline                     # report -> insights
from preprocessing.pipeline import preprocess_data_pipeline                # raw df -> preprocessed data
from ml.ml_pipeline import ml_pipeline                                     # preprocessed data -> 
import pandas as pd



def main_pipeline(df,target_col):

    report = analyze_data(df)

    df_report = insight_pipeline(report)

    target = df[target_col]

    features = df.drop(columns=[target_col])

    processed_features = preprocess_data_pipeline(features)

    processed_df = processed_features
    processed_df[target_col] = target

    ml_report = ml_pipeline(processed_df,target_col)

    return {
        "report": df_report['report'],
        "eda_insights": df_report['insights'],
        "eda_story": df_report['story'],

        "problem_info": ml_report["problem_info"],
        "evaluation_results": ml_report["evaluation_results"],
        "best_model_info": ml_report["best_model_info"],
        "ml_insights": ml_report["insights"],
        "ml_story": ml_report["story"]
    }


df = pd.read_csv('data/train.csv')
target_col = "SalePrice"

result = main_pipeline(df, target_col)

print("\n=== Problem Type ===")
print(result["problem_info"])

print("\n=== Best Model ===")
print(result["best_model_info"])

print("\n=== Evaluation Results ===")
for model, metrics in result["evaluation_results"].items():
    print(model, metrics)

print("\n=== ML Story ===")

for line in result["ml_story"]:
    print(line)

print("\n=== EDA Story ===")

for line in result["eda_story"]:
    print(line)