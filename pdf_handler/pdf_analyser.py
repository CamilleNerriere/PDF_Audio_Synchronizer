import fitz
import re

def generate_pdf_informations(book):
    doc = fitz.open(book)
    text_divided_by_pages = []

    def format_text(text):
            text = text.replace('-', ' ')
            text = re.sub(r"[^\w\s'’]", '', text)
            text = text.lower()
            return text.strip()

    for page_number, page in enumerate(doc):

        lines = []

        text_dict = page.get_text("dict")

        for block in text_dict["blocks"]:
            if "lines" in block:

                for line in block["lines"] :
                    line_text = "". join([span["text"] for span in line["spans"]])

                    x0, y0, x1, y1 = line["bbox"]

                    line_data = {
                        "text": format_text(line_text),
                        "coord" : [x0, y0, x1, y1],
                    }

                    lines.append(line_data)

        text_divided_by_pages.append({f"page_{page_number + 1}" : lines})

    return text_divided_by_pages






