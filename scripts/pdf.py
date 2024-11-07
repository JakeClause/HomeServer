import fitz  # PyMuPDF
import os
import logging

# Configure logging for the pdf.py module
logger = logging.getLogger(__name__)

def pdf_to_jpg(pdf_file, output_folder):
    logger.info(f"Converting PDF '{pdf_file}' to JPG in folder '{output_folder}'")

    # Use os.path.join to construct the path
    pdf_document = fitz.open(pdf_file)
    pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    os.makedirs(pdf_output_folder, exist_ok=True)  # Create subfolder for each PDF

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap()
        image.save(os.path.join(pdf_output_folder, f'page_{page_number + 1}.jpg'), 'JPEG')

    logger.info(f"Conversion of PDF '{pdf_file}' to JPG complete")
