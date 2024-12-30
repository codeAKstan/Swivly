from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML
import os

def generate_pdf(order):
    # Render the template with context
    html_string = render_to_string('orders/pdf.html', {'order': order})

    # Generate the PDF file
    pdf_file = ContentFile(
        HTML(string=html_string).write_pdf()
    )
    return pdf_file
