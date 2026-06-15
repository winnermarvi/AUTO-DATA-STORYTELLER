from eda.eda import analyze_data                                           # raw  df  -> report
from insights.insight_pipeline import insight_pipeline                     # report -> insights
from preprocessing.pipeline import preprocess_data_pipeline                # raw df -> preprocessed data
from ml.ml_pipeline import ml_pipeline                                     # preprocessed data -> 
import pandas as pd



def main_pipeline(df,target_col):

    print("Starting EDA...")
    report = analyze_data(df)
    print("EDA Complete")

    print("Generating EDA insights...")
    df_report = insight_pipeline(report)
    print("EDA Insights Complete")

    target = df[target_col]

    features = df.drop(columns=[target_col])

    print("Starting preprocessing...")
    processed_df = preprocess_data_pipeline(features)
    print("Preprocessing Complete")

    processed_df[target_col] = target

    #===================temporary===================================================================
    print("Shape:", processed_df.shape)

    print("Missing Values:", processed_df.isnull().sum().sum())

    print("Non-Numeric Columns:",len(processed_df.select_dtypes(exclude=['number']).columns))

    #=================================================================================================

    print("Starting ML pipeline...")
    ml_report = ml_pipeline(processed_df, target_col)
    print("ML Pipeline Complete")

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


df = pd.read_csv('data/titanic.csv')
target_col = "Survived"

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