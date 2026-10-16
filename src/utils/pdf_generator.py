"""
PDF Assessment Report Generator for FINScore
Creates printable executive fintech PDF reports.
"""

import io
import datetime
from typing import Dict, Any

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_report(applicant_name: str, raw_input: Dict[str, Any], result: Dict[str, Any], explanation: Dict[str, Any]) -> bytes:
    """
    Generates a PDF report bytes object.
    """
    buffer = io.BytesIO()

    if not REPORTLAB_AVAILABLE:
        # Fallback text representation if reportlab is not available
        content = f"FINScore Assessment Report for {applicant_name}\n"
        content += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"Financial Health Score: {result.get('financial_health_score')}/100 ({result.get('financial_health_category')})\n"
        content += f"Default Risk: {result.get('default_probability_pct')}%\n"
        content += f"Approval Probability: {result.get('approval_probability_pct')}%\n"
        content += f"Decision Support: {result.get('decision')}\n"
        return content.encode("utf-8")

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor("#0EA5E9"),
        spaceAfter=15
    )
    heading2_style = ParagraphStyle(
        'DocHeading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    )
    disclaimer_style = ParagraphStyle(
        'DocDisclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748B")
    )

    elements = []

    # Header
    elements.append(Paragraph("FINScore Assessment Report", title_style))
    elements.append(Paragraph("INTELLIGENT FINANCIAL HEALTH & CREDIT RISK ASSESSMENT", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=15))

    # Applicant Meta Table
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_data = [
        [Paragraph(f"<b>Applicant Name:</b> {applicant_name}", body_style), Paragraph(f"<b>Date:</b> {now_str}", body_style)],
        [Paragraph(f"<b>Annual Income:</b> ${float(raw_input.get('annual_inc', 0)):,.2f}", body_style), Paragraph(f"<b>Requested Loan:</b> ${float(raw_input.get('loan_amnt', 0)):,.2f}", body_style)],
        [Paragraph(f"<b>FICO Score:</b> {int(raw_input.get('fico_score', 0))}", body_style), Paragraph(f"<b>DTI Ratio:</b> {float(raw_input.get('dti', 0)):.1f}%", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 15))

    # Key Hero Outputs Table
    hero_data = [
        ["FINANCIAL HEALTH SCORE", "DEFAULT RISK", "APPROVAL PROBABILITY", "DECISION SUPPORT"],
        [
            f"{result.get('financial_health_score')}/100\n({result.get('financial_health_category')})",
            f"{result.get('default_probability_pct')}%\n({result.get('risk_band')})",
            f"{result.get('approval_probability_pct')}%",
            f"{result.get('decision')}"
        ]
    ]
    t_hero = Table(hero_data, colWidths=[135, 135, 135, 135])
    t_hero.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F1F5F9")),
        ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor("#0F172A")),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(t_hero)
    elements.append(Spacer(1, 15))

    # Financial Health Breakdown
    elements.append(Paragraph("Financial Health Dimension Breakdown", heading2_style))
    breakdown = result.get("health_breakdown", {})
    b_data = [["Dimension", "Score (0-100)"]]
    for k, v in breakdown.items():
        b_data.append([k, f"{v}/100"])
    
    t_break = Table(b_data, colWidths=[350, 190])
    t_break.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_break)
    elements.append(Spacer(1, 15))

    # Explainable Risk Factors
    elements.append(Paragraph("Explainable Risk Assessment Factors", heading2_style))
    pos = explanation.get("positive_factors", [])
    pos_str = "<br/>".join([f"• {p}" for p in pos])
    neg = explanation.get("risk_factors", [])
    neg_str = "<br/>".join([f"• {n}" for n in neg])

    exp_data = [
        [Paragraph("<b>Positive Financial Mitigants</b>", body_style), Paragraph("<b>Key Risk Drivers</b>", body_style)],
        [Paragraph(pos_str, body_style), Paragraph(neg_str, body_style)]
    ]
    t_exp = Table(exp_data, colWidths=[270, 270])
    t_exp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#ECFDF5")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FEF2F2")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_exp)
    elements.append(Spacer(1, 20))

    # Disclaimer
    disclaimer_text = (
        "<b>Important Regulatory Disclaimer:</b> This assessment is a predictive decision-support output and is not a "
        "guaranteed lending decision. Production lending use requires appropriate validation, calibration, fairness "
        "assessment, regulatory compliance review, and human oversight."
    )
    elements.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
