from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import markdown
import os
from datetime import datetime

def extract_csv_table_from_markdown(markdown_text):
    """Extract and parse any CSV table present in the Markdown text."""
    lines = markdown_text.splitlines()
    table_lines = []
    in_table = False
    for line in lines:
        if line.strip().startswith("|"):
            in_table = True
            table_lines.append(line.strip())
        elif in_table:
            if line.strip() == "":
                break
            table_lines.append(line.strip())

    if not table_lines:
        return None

    table_data = []
    for line in table_lines:
        row = [cell.strip() for cell in line.split("|") if cell]
        table_data.append(row)

    return table_data

def generate_pdf(header, content, method, metrica, output_folder="reports/"):
    """
    Generate a PDF report with evaluation and review content.
    """
    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_folder, f"Evaluacion_Report_IA_Gemini_{timestamp}.pdf")

    try:
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Header: Evaluation details
        header_data = [
            ["Curso:", header['curso']['nombre']],
            ["Docente DNI:", header['docente']['dni']],
            ["Evaluación:", header['nombre']],
            ["Descripción:", header['descripcion']],
            ["Método:", method],
            ["Métrica:", metrica]
        ]

        table = Table(header_data, colWidths=[120, 380])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # IA Gemini Response Section
        elements.append(Paragraph("Revisión de IA Gemini", styles['Heading2']))
        elements.append(Spacer(1, 10))

        if content:
            html_content = markdown.markdown(content)
            elements.append(Paragraph(html_content, styles['BodyText']))
        else:
            elements.append(Paragraph("No se pudo obtener contenido de la revisión de IA Gemini.", styles['BodyText']))

        elements.append(Spacer(1, 20))

        # Extracted CSV Table
        csv_table = extract_csv_table_from_markdown(content)
        if csv_table:
            table = Table(csv_table, colWidths=[80] * len(csv_table[0]))
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No se detectaron tablas CSV en el contenido.", styles['BodyText']))

        elements.append(Spacer(1, 50))

        # Footer
        def footer(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 9)
            canvas.drawString(30, 30, "© CodeGuard - Todos los derechos reservados.")
            canvas.drawRightString(A4[0] - 30, 30, f"Página {doc.page}")
            canvas.restoreState()

        doc.build(elements, onFirstPage=footer, onLaterPages=footer)
        return output_file
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
