"""PDF report generator for ADA Compliance Audit reports.

Produces a professional CASp-style PDF with cover page, executive summary,
violation details, and cost matrix using reportlab.
"""

import io
import logging
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)

SEVERITY_COLORS = {
    "high": "#DC2626",
    "medium": "#F59E0B",
    "low": "#3B82F6",
}

HEADER_BG = colors.HexColor("#1F2937")
HEADER_FG = colors.white


def _build_styles():
    """Build custom paragraph styles for the report."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontSize=26,
        leading=32,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#111827"),
        fontName="Helvetica-Bold",
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=16,
        leading=20,
        spaceBefore=16,
        spaceAfter=10,
        textColor=colors.HexColor("#1F2937"),
        fontName="Helvetica-Bold",
    ))

    styles.add(ParagraphStyle(
        name="ViolationTitle",
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    ))

    styles.add(ParagraphStyle(
        name="BodyGray",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4B5563"),
        fontName="Helvetica",
    ))

    styles.add(ParagraphStyle(
        name="Disclaimer",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#9CA3AF"),
        fontName="Helvetica-Oblique",
        alignment=TA_CENTER,
    ))

    return styles


def _header_table_style():
    """Return a TableStyle with dark header row and alternating body rows."""
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), HEADER_FG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])


def _severity_tag(severity, styles):
    """Return a Paragraph with colored severity label."""
    color = SEVERITY_COLORS.get(severity, "#6B7280")
    text = '<font color="{color}"><b>{sev}</b></font>'.format(
        color=color, sev=severity.upper()
    )
    return Paragraph(text, styles["BodyGray"])


def _build_cover_page(elements, report, location_label, space_type, image_bytes, styles):
    """Build Page 1: Cover page."""
    elements.append(Spacer(1, 1.5 * inch))
    elements.append(Paragraph("ADA Compliance Audit Report", styles["ReportTitle"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Subtitle info
    info_lines = [
        '<b>Location:</b> {}'.format(location_label),
        '<b>Space Type:</b> {}'.format(space_type.replace("_", " ").title()),
        '<b>Date:</b> {}'.format(date.today().strftime("%B %d, %Y")),
        '<b>Overall Risk:</b> <font color="{color}">{risk}</font>'.format(
            color=SEVERITY_COLORS.get(report.get("overall_risk", ""), "#6B7280"),
            risk=report.get("overall_risk", "N/A").upper(),
        ),
    ]
    for line in info_lines:
        elements.append(Paragraph(line, styles["BodyGray"]))
        elements.append(Spacer(1, 4))

    # Optional photo thumbnail
    if image_bytes is not None:
        try:
            img_buf = io.BytesIO(image_bytes)
            img = Image(img_buf, width=3 * inch, height=2.25 * inch)
            img.hAlign = "CENTER"
            elements.append(Spacer(1, 0.4 * inch))
            elements.append(img)
        except Exception:
            logger.warning("Could not embed image in PDF cover page")

    elements.append(PageBreak())


def _build_executive_summary(elements, report, styles):
    """Build Page 2: Executive summary."""
    elements.append(Paragraph("Executive Summary", styles["SectionHeader"]))
    elements.append(Paragraph(report.get("summary", ""), styles["BodyGray"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Metrics table
    cost = report.get("total_estimated_cost", {})
    cost_low = cost.get("low", 0)
    cost_high = cost.get("high", 0)

    metrics_data = [
        ["Metric", "Value"],
        ["Total Violations", str(report.get("violation_count", 0))],
        ["Confirmed", str(report.get("confirmed_count", 0))],
        ["Potential", str(report.get("potential_count", 0))],
        ["Estimated Cost", "${:,} - ${:,}".format(cost_low, cost_high)],
        ["Standard", report.get("standard_applied", "Federal ADA")],
    ]
    t = Table(metrics_data, colWidths=[2.5 * inch, 4 * inch])
    t.setStyle(_header_table_style())
    elements.append(t)
    elements.append(Spacer(1, 0.3 * inch))

    # Positive features
    positives = report.get("positive_features", [])
    if positives:
        elements.append(Paragraph("Positive Features", styles["SectionHeader"]))
        for feat in positives:
            elements.append(Paragraph("&#8226; {}".format(feat), styles["BodyGray"]))
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(PageBreak())


def _build_violation_pages(elements, violations, styles):
    """Build Pages 3+: Violation detail pages."""
    elements.append(Paragraph("Violation Details", styles["SectionHeader"]))
    elements.append(Spacer(1, 0.1 * inch))

    for i, v in enumerate(violations, 1):
        severity = v.get("severity", "medium")
        confidence = v.get("confidence", 0)
        color = SEVERITY_COLORS.get(severity, "#6B7280")

        # Title with severity color and confidence
        title_text = (
            '{num}. <font color="{color}">[{sev}]</font> '
            '{vtype} (Confidence: {conf:.0%})'
        ).format(
            num=i,
            color=color,
            sev=severity.upper(),
            vtype=v.get("violation_type", "Unknown").replace("_", " ").title(),
            conf=confidence,
        )
        elements.append(Paragraph(title_text, styles["ViolationTitle"]))

        # Description
        elements.append(Paragraph(
            "<b>Description:</b> {}".format(v.get("description", "")),
            styles["BodyGray"],
        ))

        # Reasoning
        elements.append(Paragraph(
            "<b>Reasoning:</b> {}".format(v.get("reasoning", "")),
            styles["BodyGray"],
        ))

        # Location in image
        elements.append(Paragraph(
            "<b>Location in Image:</b> {}".format(v.get("location_in_image", "")),
            styles["BodyGray"],
        ))

        elements.append(Spacer(1, 0.1 * inch))

        # Code reference table
        code_data = [
            ["Standard", "Section", "Title", "Requirement"],
            [
                "Federal ADA",
                v.get("ada_section", ""),
                v.get("ada_title", ""),
                Paragraph(v.get("ada_requirement", ""), styles["BodyGray"]),
            ],
        ]
        if v.get("cbc_section"):
            code_data.append([
                "CA CBC Title 24",
                v.get("cbc_section", ""),
                v.get("cbc_title", ""),
                Paragraph(v.get("cbc_requirement", ""), styles["BodyGray"]),
            ])
        ct = Table(code_data, colWidths=[1.2 * inch, 1 * inch, 1.3 * inch, 3 * inch])
        ct.setStyle(_header_table_style())
        elements.append(ct)

        # Stricter note
        if v.get("stricter_than_federal"):
            note_text = '<font color="#DC2626"><b>CA Stricter:</b></font> {}'.format(
                v.get("stricter_note", "")
            )
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(note_text, styles["BodyGray"]))

        # Remediation and cost
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            "<b>Remediation:</b> {}".format(v.get("remediation", "")),
            styles["BodyGray"],
        ))

        cost_low = v.get("cost_low", 0)
        cost_high = v.get("cost_high", 0)
        cost_unit = v.get("cost_unit", "")
        elements.append(Paragraph(
            "<b>Estimated Cost:</b> ${:,} - ${:,} ({})".format(
                cost_low, cost_high, cost_unit
            ),
            styles["BodyGray"],
        ))

        # Cost factors
        factors = v.get("cost_factors", [])
        if factors:
            elements.append(Paragraph(
                "<b>Cost Factors:</b> {}".format(", ".join(factors)),
                styles["BodyGray"],
            ))

        elements.append(Spacer(1, 0.25 * inch))

    elements.append(PageBreak())


def _build_cost_matrix(elements, report, styles):
    """Build final page: Cost matrix and disclaimer."""
    elements.append(Paragraph("Cost Summary Matrix", styles["SectionHeader"]))
    elements.append(Spacer(1, 0.1 * inch))

    violations = report.get("violations", [])

    matrix_data = [["#", "Violation", "Severity", "Cost Range"]]
    for i, v in enumerate(violations, 1):
        severity = v.get("severity", "medium")
        cost_low = v.get("cost_low", 0)
        cost_high = v.get("cost_high", 0)
        matrix_data.append([
            str(i),
            v.get("violation_type", "").replace("_", " ").title(),
            _severity_tag(severity, styles),
            "${:,} - ${:,}".format(cost_low, cost_high),
        ])

    # Total row
    total = report.get("total_estimated_cost", {})
    matrix_data.append([
        "",
        Paragraph("<b>TOTAL</b>", styles["BodyGray"]),
        "",
        Paragraph(
            "<b>${:,} - ${:,}</b>".format(
                total.get("low", 0), total.get("high", 0)
            ),
            styles["BodyGray"],
        ),
    ])

    mt = Table(matrix_data, colWidths=[0.5 * inch, 2.5 * inch, 1.5 * inch, 2 * inch])
    style = _header_table_style()
    # Bold the total row
    style.add("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F3F4F6"))
    style.add("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#1F2937"))
    mt.setStyle(style)
    elements.append(mt)

    # Disclaimer
    elements.append(Spacer(1, 0.5 * inch))
    disclaimer = report.get("disclaimer", "")
    if disclaimer:
        elements.append(Paragraph(disclaimer, styles["Disclaimer"]))


def generate_pdf_report(
    report: dict,
    location_label: str,
    space_type: str,
    image_bytes: bytes | None = None,
) -> bytes:
    """Generate a professional ADA compliance audit PDF report.

    Args:
        report: The enriched analysis report dict with violations, costs, etc.
        location_label: Human-readable location string.
        space_type: Type of space analyzed (e.g. 'entrance', 'restroom').
        image_bytes: Optional JPEG/PNG bytes for cover page thumbnail.

    Returns:
        PDF file contents as bytes.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = _build_styles()
    elements = []

    _build_cover_page(elements, report, location_label, space_type, image_bytes, styles)
    _build_executive_summary(elements, report, styles)

    violations = report.get("violations", [])
    if violations:
        _build_violation_pages(elements, violations, styles)

    _build_cost_matrix(elements, report, styles)

    doc.build(elements)
    return buf.getvalue()
