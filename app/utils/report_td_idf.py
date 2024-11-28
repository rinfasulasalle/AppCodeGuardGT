from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime

def format_plagiarism_cases(plagiarism_cases):
    """Format plagiarism cases into a table."""
    data = [["ID Código A", "DNI Estudiante A", "ID Código B", "DNI Estudiante B", "Score %"]]
    for case in plagiarism_cases:
        data.append([
            case["codigo_a"]["id_codigo"],
            case["codigo_a"]["estudiante"]["dni"],
            case["codigo_b"]["id_codigo"],
            case["codigo_b"]["estudiante"]["dni"],
            case["similarity_score"]*100
        ])
    return data

def format_comparisons(comparisons):
    """Format comparisons into a table."""
    data = [["ID Código A", "DNI Estudiante A", "ID Código B", "DNI Estudiante B", "Score %"]]
    for comparison in comparisons:
        data.append([
            comparison["codigo_a"]["id_codigo"],
            comparison["codigo_a"]["estudiante"]["dni"],
            comparison["codigo_b"]["id_codigo"],
            comparison["codigo_b"]["estudiante"]["dni"],
            comparison["similarity_score"]*100
        ])
    return data

def generate_pdf(header, result, method, output_folder="reports/"):
    """
    Generate a PDF report with evaluation and review content.
    
    Args:
        header (dict): Evaluation header information.
        result (dict): Review result content.
        method (str): Method used for the review (e.g., "TF-IDF").
        output_folder (str): Directory where the PDF will be stored.
    
    Returns:
        str: Path to the generated PDF file or None if an error occurred.
    """
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y.%m.%d_%H:%M:%S")
    output_file = os.path.join(output_folder, f"Evaluacion_Report_{timestamp}.pdf")

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
            ["Threshold:", result["threshold"]]
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

        # Section 1: Plagiarism cases
        elements.append(Paragraph("Casos de Plagio Detectados", styles['Heading2']))
        elements.append(Spacer(1, 10))

        if result["plagiarism_detected"]:
            cases_table = format_plagiarism_cases(result["plagiarism_cases"])
            table = Table(cases_table, colWidths=[80, 100, 80, 100, 60])
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
            elements.append(Paragraph("No se detectaron casos de plagio.", styles['BodyText']))

        elements.append(Spacer(1, 20))

        # Section 2: Detailed comparisons
        elements.append(Paragraph("Comparaciones Detalladas", styles['Heading2']))
        elements.append(Spacer(1, 10))

        comparisons_table = format_comparisons(result["comparisons"])
        table = Table(comparisons_table, colWidths=[80, 100, 80, 100, 60])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ]))
        elements.append(table)

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
