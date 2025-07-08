# parsers/pdf_parser.py

# parsers/pdf_parser.py

import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts full text from a PDF file using pdfplumber, page by page.
    Returns nicely concatenated text for preview and further parsing.
    """
    extracted_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(f"--- Page {page_number} ---\n{page_text.strip()}\n")
                else:
                    extracted_text.append(f"--- Page {page_number} ---\n(No text found on this page)\n")
    except Exception as e:
        print(f"⚠️ Error reading PDF: {e}")
        return ""

    final_text = "\n".join(extracted_text)
    return final_text




# import fitz  # PyMuPDF
# import re

# def mask_pii(text, name_list=None):
#     text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****', text)
#     text = re.sub(r'\b\d{10}\b', '**********', text)
#     if name_list:
#         for name in name_list:
#             text = text.replace(name, '[REDACTED]')
#     return text

# def parse_pdf(file_path):
#     try:
#         doc = fitz.open(file_path)
#         text = "".join([page.get_text() for page in doc])
#         return mask_pii(text, name_list=["Hemachandra HD", "ABC Corporation"])
#     except Exception as e:
#         return f"Error parsing PDF: {e}"


# import pdfplumber

# def parse_pdf(file_path):
#     text = ""
#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text.strip()
