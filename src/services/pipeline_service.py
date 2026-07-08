from src.services.eda_service import run_eda
from src.services.ml_service import run_ml
from src.services.llm_service import generate_summary
from src.services.chart_service import generate_chart
from src.services.report_service import generate_report
import pandas as pd

def run_pipeline(df,target_col):

    eda = run_eda(df)
    
    ml = run_ml(df,target_col)

    llm = generate_summary(
        ml_story= ml["ml_story"],
        feature_importance_story= ml["feature_importance_story"],
        recommendation_story= ml["recommendation_story"]
    )

    pdf_path = generate_report(eda,ml,llm)

    generate_chart(
        feature_importance= ml["feature_importance"],
        missing_values= eda["report"]["missing_values"]
    )

    analysis = {
        "eda": eda,
        "ml": ml,
        "llm": llm
    }

    return {
        "analysis" : analysis,
        "pdf_path" : pdf_path
    }

df = pd.read_csv('data/titanic.csv')
target_col = "Survived"


result = run_pipeline(df,target_col)

print("======================================================")
print(result['analysis']['eda'])
print("======================================================")
print(result['analysis']['ml'])
print("======================================================")
print(result['analysis']['llm'])