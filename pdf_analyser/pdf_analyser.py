from PyPDF2 import PdfReader
import re

# def generate_pdf_informations(book):
#     reader = PdfReader(book)
#     total_pages = len(reader.pages)
#     text_divided_by_pages = []
#     page_number = 1
#     for page in range(total_pages):
#         page = reader.pages[page]
#         cleaned_text = page.extract_text().replace('\n', '').replace('\\', '')
#         re.sub(r'(?<=\w)\s+(?=\w)', '', cleaned_text) #remove extra-space in words
#         page_information = {
#             "text": page.extract_text().replace('\n', '').replace('\\', ''),
#             "page": page_number,
#         }
#         page_number += 1
#         text_divided_by_pages.append(page_information)
#     return text_divided_by_pages

def generate_pdf_informations(book):
    reader = PdfReader(book)
    total_pages = len(reader.pages)
    text_divided_by_pages = []
    pages_divided_by_lines = {}
    page_number = 1

    for page in range(total_pages):
        page = reader.pages[page]
        text = page.extract_text()
        lines = text.split('\n')

        pages_divided_by_lines = {}


        pages_divided_by_lines[f"page_{page_number}"] = {f"line_{i + 1}": line for i, line in enumerate(lines)}
        text_divided_by_pages.append(pages_divided_by_lines)

        page_number += 1

    return text_divided_by_pages


book_infos = generate_pdf_informations("../data/pdf/caroll_de_autre_cote_miroir.pdf")

print(book_infos)

