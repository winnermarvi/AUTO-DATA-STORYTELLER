from src.eda.eda import analyze_data                                           # raw  df  -> report
from src.insights.insight_pipeline import insight_pipeline                     # report -> insights
from src.preprocessing.pipeline import preprocess_data_pipeline                # raw df -> preprocessed data
from src.ml.ml_pipeline import ml_pipeline                                     # preprocessed data -> 
from src.llm.llm_pipeline import llm_pipeline
import pandas as pd
from datetime import datetime

from src.reporting.report_builder import build_report
from src.reporting.pdf_generator import generate_pdf

#=================== charts import ==========================
from src.visualization.feature_importance_chart import plot_feature_importance
from src.visualization.missing_value_chart import plot_missing_values



def main_pipeline(df,target_col):


    report = analyze_data(df)

    df_report = insight_pipeline(report)

    target = df[target_col]

    features = df.drop(columns=[target_col])

    processed_df = preprocess_data_pipeline(features)

    processed_df[target_col] = target

    ml_report = ml_pipeline(processed_df, target_col)

    llm_report = llm_pipeline(
        ml_story= ml_report["story"],
        feature_importance_story= ml_report["feature_importance_story"],
        recommendation_story= ml_report["recommendation_story"]
    )

    #================== charts =================================
    plot_feature_importance(ml_report["feature_importance"])
    plot_missing_values(report["missing_values"])


    output_path = f"src/reports/report/report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"

    target_distribution = ( target.value_counts().to_dict())


    result = {
        "report": df_report['report'],
        "eda_insights": df_report['insights'],
        "eda_story": df_report['story'],

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

        "llm_report" : llm_report,
        "target_distribution": target_distribution
    }

    pdf_report = build_report(result)

    pdf_path = generate_pdf(pdf_report,output_path)

    return {
        "analysis" : result,
        "pdf_path" : pdf_path
    }




""""

df = pd.read_csv('data/titanic.csv')
target_col = "Survived"

result = main_pipeline(df, target_col)


print(result['pdf_path'])

import os

print(os.path.exists(result["pdf_path"]))

print("PDF generated successfully!")

print(result['llm_report']['narrative'])

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

print("\n=== Feature Importance Story ===")

for line in result["feature_importance_story"]:
    print(line)

print("\n=== Recommendation Story ===")

for line in result["recommendation_story"]:
    print(line)  

"""