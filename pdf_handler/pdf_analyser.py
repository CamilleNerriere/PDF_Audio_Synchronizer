import fitz
import re

def generate_pdf_informations(book):
    doc = fitz.open(book)
    text_divided_by_pages = []
    text_divided_by_blocks = []

    def format_text(text):
            text = text.replace('-', ' ')
            text = re.sub(r"[^\w\s'’]", '', text)
            text = text.lower()
            return text.strip()

    for page_number, page in enumerate(doc):

        blocks  = page.get_text("blocks")

        for block in blocks:
            x0, y0, x1, y1, text = block[:5]

            bloc_data = {
                "text": format_text(text),
                "x0" : x0,
                "y0" : y0,
                "x1" : x1,
                "y1" : y1,
            }

            text_divided_by_blocks.append(bloc_data)

        text = page.get_text("text")
        lines = text.split('\n')

        pages_divided_by_lines = {
            f"page_{page_number}": {
                f"line_{i}" : format_text(line) for i, line in enumerate(lines)
            }
        }

        text_divided_by_pages.append(pages_divided_by_lines)

    return text_divided_by_blocks


book = "../data/pdf/caroll_de_autre_cote_miroir.pdf"

print(generate_pdf_informations(book))




