from datetime import datetime
from src.reporting.report_builder import build_report
from src.reporting.pdf_generator import generate_pdf

def generate_report(eda,ml,llm):

    output_path = f"src/reports/report/report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"

    pdf_report = build_report(
        eda_story=eda["eda_story"],
        ml_story=ml["ml_story"],
        feature_importance_story=ml["feature_importance_story"],
        recommendation_story=ml["recommendation_story"],
        llm_report=llm,
        problem_info=ml["problem_info"],
        best_model_info=ml["best_model_info"]
    )

    pdf_path = generate_pdf(pdf_report,output_path)

    return pdf_path