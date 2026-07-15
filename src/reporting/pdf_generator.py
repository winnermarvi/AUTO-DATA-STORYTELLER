import re
from datetime import date

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle,
    ListFlowable,
    ListItem,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tableofcontents import TableOfContents


# ---------------------------------------------------------------------------
# Custom document class: adds header/footer page numbers and feeds section
# headings into the Table of Contents automatically.
# ---------------------------------------------------------------------------
class ReportDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        """Registers Heading1/Heading2 paragraphs into the TOC."""
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            text = flowable.getPlainText()

            if style_name == "SectionHeading":
                self.notify("TOCEntry", (0, text, self.page))
            elif style_name == "SubHeading":
                self.notify("TOCEntry", (1, text, self.page))

    def handle_pageBegin(self):
        super().handle_pageBegin()

    def afterPage(self):
        pass


def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(0.75 * inch, 0.5 * inch, "Auto Data Storyteller Report")
    canvas.drawRightString(
        letter[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}"
    )
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=24,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.grey,
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ZoneLabel",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#2E5090"),
            spaceBefore=18,
            spaceAfter=2,
            leading=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading1"],
            fontSize=15,
            textColor=colors.HexColor("#1A1A1A"),
            spaceBefore=6,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubHeading",
            parent=styles["Heading2"],
            fontSize=12,
            textColor=colors.HexColor("#333333"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=15,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
        )
    )
    return styles


def zone_header(text, styles):
    """A small eyebrow label that visually groups related sections together."""
    return [
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2E5090")),
        Paragraph(text.upper(), styles["ZoneLabel"]),
    ]


def bullet_list(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BulletBody"])) for item in items],
        bulletType="bullet",
        start="•",
        leftIndent=14,
        spaceBefore=2,
        spaceAfter=10,
    )


# The executive_summary string always arrives as one blob containing these
# four numbered sub-points back to back (e.g. "1. Executive Summary ... 2.
# Key Business Drivers ..."). We split on those known labels so each point
# renders as its own paragraph, and bold the label — no wording is changed.
EXEC_SUMMARY_LABELS = [
    "Executive Summary",
    "Key Business Drivers",
    "Business Implications",
    "Strategic Recommendations",
]


def format_executive_summary(text, styles):
    label_pattern = "|".join(re.escape(label) for label in EXEC_SUMMARY_LABELS)
    split_pattern = rf"(?=\d+\.\s+(?:{label_pattern}))"

    parts = [p.strip() for p in re.split(split_pattern, text) if p.strip()]

    # Fallback: labels not found (e.g. text doesn't match the expected
    # template) -> just render the original text as a single paragraph.
    if len(parts) <= 1:
        return [Paragraph(text, styles["ReportBody"])]

    flowables = []
    for part in parts:
        for label in EXEC_SUMMARY_LABELS:
            marker = f"{label} "
            if marker in part[:60]:
                part = part.replace(marker, f"<b>{label}.</b> ", 1)
                break
        flowables.append(Paragraph(part, styles["ReportBody"]))
        flowables.append(Spacer(1, 6))
    return flowables


def stat_table(overview):
    """Pulls the key overview numbers into a scannable table instead of
    burying them inside paragraph text."""
    data = [
        ["Problem Type", overview.get("problem_type", "-")],
        ["Best Model", overview.get("best_model", "-")],
    ]
    table = Table(data, colWidths=[1.8 * inch, 3.5 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF3FA")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E1EF")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return table


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------
def generate_pdf(report, output_path):
    styles = build_styles()

    doc = ReportDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
    )

    content = []

    # --- Title / metadata block -------------------------------------------------
    content.append(Paragraph("AUTO DATA STORYTELLER REPORT", styles["ReportTitle"]))
    content.append(
        Paragraph(
            f"Generated {date.today().strftime('%B %d, %Y')}",
            styles["ReportSubtitle"],
        )
    )

    # --- Table of contents --------------------------------------------------
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            name="TOCHeading1",
            fontSize=11,
            leading=16,
            leftIndent=0,
        ),
        ParagraphStyle(
            name="TOCHeading2",
            fontSize=10,
            leading=14,
            leftIndent=14,
            textColor=colors.grey,
        ),
    ]
    content.append(Paragraph("Contents", styles["SubHeading"]))
    content.append(toc)
    content.append(PageBreak())

    # =========================================================================
    # ZONE 1 — SUMMARY (narrative: what happened and what to do about it)
    # =========================================================================
    content.extend(zone_header("Summary", styles))

    content.append(Paragraph("Executive Summary", styles["SectionHeading"]))
    content.extend(format_executive_summary(report["executive_summary"], styles))

    content.append(Paragraph("Recommendations", styles["SubHeading"]))
    content.append(bullet_list(report["recommendations"], styles))

    content.append(PageBreak())

    # =========================================================================
    # ZONE 2 — DATA (the input side: what the dataset looks like)
    # =========================================================================
    content.extend(zone_header("Data", styles))

    content.append(Paragraph("Dataset Overview", styles["SectionHeading"]))
    content.append(stat_table(report["dataset_overview"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Data Quality", styles["SubHeading"]))
    data_quality_items = [
        report["data_quality"][1],
        report["data_quality"][3],
        report["data_quality"][4],
        report["data_quality"][-1],
    ]
    content.append(bullet_list(data_quality_items, styles))

    content.append(Paragraph("Missing Values", styles["SubHeading"]))
    content.append(
        Image(
            "src/reports/charts/missing_values.png",
            width=400,
            height=250,
        )
    )

    content.append(PageBreak())

    # =========================================================================
    # ZONE 3 — MODEL (the output side: how the model performed and why)
    # =========================================================================
    content.extend(zone_header("Model", styles))

    content.append(Paragraph("Model Findings", styles["SectionHeading"]))
    content.append(bullet_list(report["model_findings"], styles))

    content.append(Paragraph("Key Drivers", styles["SubHeading"]))
    content.append(bullet_list(report["key_drivers"], styles))

    content.append(Paragraph("Feature Importance", styles["SubHeading"]))
    content.append(
        Image(
            "src/reports/charts/feature_importance.png",
            width=400,
            height=250,
        )
    )

    # --- Build (two passes: first pass resolves TOC page numbers) -----------
    doc.multiBuild(content, onFirstPage=_draw_footer, onLaterPages=_draw_footer)

    return output_path