
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generate_receipt(sale):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=35,
        bottomMargin=35,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Custom text styles
    shop_style = ParagraphStyle(
        "ShopName",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    receipt_style = ParagraphStyle(
        "ReceiptTitle",
        parent=styles["Heading2"],
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=18,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=10,
    )

    normal_style = ParagraphStyle(
        "ReceiptNormal",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
    )

    amount_style = ParagraphStyle(
        "TotalAmount",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        alignment=TA_LEFT,
    )

    # Shop heading
    elements.append(Paragraph("BIKE SHOP", shop_style))
    elements.append(Paragraph("SALE RECEIPT", receipt_style))

    # Receipt information
    elements.append(
        Paragraph(f"Receipt No: {sale.id}", normal_style)
    )

    elements.append(
        Paragraph(
            f"Sale Date: {sale.sale_date.strftime('%d %B %Y')}",
            normal_style,
        )
    )

    elements.append(Spacer(1, 15))

    # Reusable table styling
    def create_details_table(data):
        formatted_data = [
            [
                Paragraph(escape(str(label)), normal_style),
                Paragraph(escape(str(value)), normal_style),
            ]
            for label, value in data
        ]

        table = Table(
            formatted_data,
            colWidths=[150, 330],
            hAlign="LEFT",
        )

        table.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.lightgrey),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ])
        )

        return table

    # Motorcycle details
    elements.append(Paragraph("Motorcycle Details", section_style))

    bike = sale.bike_info

    bike_data = [
        ["Company", bike.company],
        ["Model", bike.model],
        ["Model Year", bike.model_year],
        ["Registration No.", bike.registration_no or "N/A"],
        ["Engine No.", bike.engine_no],
        ["Chassis No.", bike.chassis_no],
    ]

    elements.append(create_details_table(bike_data))

    elements.append(Spacer(1, 12))

    # Buyer details
    elements.append(Paragraph("Buyer Details", section_style))

    buyer_data = [
        ["Buyer Name", sale.buyer_name],
        ["Phone Number", sale.buyer_phone or "N/A"],
        ["CNIC", sale.buyer_cnic or "N/A"],
    ]

    elements.append(create_details_table(buyer_data))

    elements.append(Spacer(1, 25))

    # Total sale amount
    elements.append(
        Paragraph(
            f"Total Sale Amount: Rs. {sale.sale_price:,}",
            amount_style,
        )
    )

    elements.append(Spacer(1, 55))

    # Signature section
    signature_data = [
        ["________________________", "________________________"],
        ["Seller Signature", "Buyer Signature"],
    ]

    signature_table = Table(
        signature_data,
        colWidths=[240, 240],
        hAlign="CENTER",
    )

    signature_table.setStyle(
        TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("TOPPADDING", (0, 1), (-1, 1), 8),
        ])
    )

    elements.append(signature_table)

    # Generate PDF
    doc.build(elements)

    return buffer.getvalue()
