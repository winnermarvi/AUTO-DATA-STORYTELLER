from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
Image,
PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(report, output_path="src/reports/report/final_report.pdf"):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph("AUTO DATA STORYTELLER REPORT", styles["Title"])
    content.append(title)
    content.append(Spacer(1, 12))


    # Executive Summary
    content.append(Paragraph("Executive Summary", styles["Heading1"]))
    content.append(
        Paragraph(report["executive_summary"], styles["BodyText"])
    )
    content.append(Spacer(1, 12))


    # Dataset Overview
    content.append(Paragraph("Dataset Overview", styles["Heading1"]))

    overview = report["dataset_overview"]

    content.append(
        Paragraph(
            f"Problem Type: {overview['problem_type']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Best Model: {overview['best_model']}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))


    # Data Quality
    content.append(Paragraph("Data Quality", styles["Heading1"]))
    content.append( Paragraph( report["data_quality"][1], styles["BodyText"] ))
    content.append( Paragraph( report["data_quality"][3], styles["BodyText"] ))
    content.append( Paragraph( report["data_quality"][4], styles["BodyText"] ))
    content.append( Paragraph( report["data_quality"][-1], styles["BodyText"] ))
    content.append(Spacer(1, 12))


    # Model Findings
    content.append(Paragraph("Model Findings", styles["Heading1"]))
    for item in report["model_findings"]:
            content.append(
                Paragraph(item, styles["BodyText"])
            )
    content.append(Spacer(1, 12))


    # Key Drivers
    content.append(Paragraph("Key Drivers", styles["Heading1"]))
    for item in report["key_drivers"]:
            content.append(
                Paragraph(item, styles["BodyText"])
            )
    content.append(Spacer(1, 12))


    # Recommendations
    content.append(Paragraph("Recommendations", styles["Heading1"]))
    for item in report["recommendations"]:
            content.append(
                Paragraph(item, styles["BodyText"])
            )
    content.append(Spacer(1, 20))


    # Charts
    content.append(PageBreak())

    content.append(Paragraph("Feature Importance", styles["Heading1"]))
    content.append(
        Image(
            "src/reports/charts/feature_importance.png",
            width=400,
            height=250
        )
    )

    content.append(Spacer(1, 20))

    content.append(Paragraph("Missing Values", styles["Heading1"]))
    content.append(
        Image(
            "src/reports/charts/missing_values.png",
            width=400,
            height=250
        )
    )

    doc.build(content)