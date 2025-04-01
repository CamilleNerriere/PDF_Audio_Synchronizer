import fitz
import re
import tempfile
from utils.safe_remove import safe_remove
from utils.logger import logger
from utils.exceptions import PDFProcessingError

def generate_pdf_informations(book):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(book.read())
        temp_pdf_path = temp_pdf.name

        try:
            text_divided_by_pages = []

            def format_text(text):
                    text = text.replace('-', ' ')
                    text = re.sub(r"[^\w\s'’]", '', text)
                    text = text.lower()
                    return text.strip()

            try:
                with fitz.open(temp_pdf_path) as doc:
                    if len(doc) == 0:
                        raise PDFProcessingError("PDF has no pages")

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

                        if len(text_divided_by_pages)==0:
                            raise PDFProcessingError("Unable to analyse PDF")
            except Exception as e:
                raise PDFProcessingError("Invalid PDF")

            return text_divided_by_pages

        finally:
            try:
                safe_remove(temp_pdf_path)
            except Exception as e:
                logger.warning(f"[WARN] Unable to delete {temp_pdf_path} : {e}")






