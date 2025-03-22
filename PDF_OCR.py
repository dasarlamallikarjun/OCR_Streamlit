from pdf2image import convert_from_path
import pytesseract
from docx import Document
import os
import re  # For text cleaning

# Specify Tesseract path explicitly
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

class PDF_OCR:
    def __init__(self, pdf_path, lang='eng'):
        self.pdf_path = pdf_path
        self.lang = lang
        self.poppler_path = "/usr/bin"  # Poppler path for PDF to Image conversion

    def clean_text(self, text):
        """Clean text by removing non-UTF8 characters and unnecessary control codes."""
        clean_text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-UTF8
        clean_text = clean_text.replace('\x0c', '')  # Remove form feed control code
        return clean_text.strip()

    def process_pdf(self):
        # Convert PDF to images
        pages = convert_from_path(self.pdf_path, poppler_path=self.poppler_path)

        # Create a new Word document
        doc = Document()

        # Perform OCR on each page and add text to the DOCX document
        for page in pages:
            text = pytesseract.image_to_string(page, lang=self.lang)
            sanitized_text = self.clean_text(text)  # Clean OCR text
            doc.add_paragraph(sanitized_text)
            doc.add_page_break()

        # Save the DOCX file
        output_path = self.pdf_path.replace('.pdf', '_output.docx')
        doc.save(output_path)
        return output_path
