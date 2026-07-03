from src.eda.eda import analyze_data
from src.insights.insight_pipeline import insight_pipeline

def run_eda(df):

    report = analyze_data(df)

    df_report = insight_pipeline(report)

    return {
        "report": df_report['report'],
        "eda_insights": df_report['insights'],
        "eda_story": df_report['story']
    }