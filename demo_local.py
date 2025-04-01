from audio_analyser import convert_and_retranscript
from pdf_handler import generate_pdf_informations
from synchronizer import synchronize_audio_to_pdf

from tkinter import Tk, Label
from PIL import Image, ImageTk

import fitz

input_audio_path = "data/audios/carroll_de_l'autre_cote_du_miroir/6 8990 Vexée et irritée Alice s’en va mais est interrompue par un fracas dans le bois.m4a"
input_pdf_path = "data/pdf/caroll_de_autre_cote_miroir.pdf"

# Transcription
with open(input_audio_path, "rb") as audio_file:
    audio_transcription = convert_and_retranscript(audio_file)

# Analyse PDF
with open(input_pdf_path, "rb") as pdf_file:
    pdf_text = generate_pdf_informations(pdf_file)

# Synchronisation
aligned_data = synchronize_audio_to_pdf(audio_transcription, pdf_text, 89, 90)
print(aligned_data)

# Visualisation avec Tkinter
def highlight_line_in_pdf(pdf_path, aligned_data):
    doc = fitz.open(pdf_path)

    root = Tk()
    root.title("PDF Highlighter")
    label = Label(root)
    label.pack()

    def highlight_next(index=0):
        if index >= len(aligned_data):
            doc.close()
            return

        data = aligned_data[index]
        page_number = data["page_num"] - 1
        rect = fitz.Rect(data["pdf_coords"])

        page = doc[page_number]
        highlight = page.add_highlight_annot(rect)
        highlight.update()

        temp_pdf_path = "temp_output.pdf"
        doc.save(temp_pdf_path)

        pixmap = page.get_pixmap()
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk

        delay = int((data["audio_end"] - data["audio_start"]) * 1000)
        page.delete_annot(highlight)
        root.after(delay, highlight_next, index + 1)

    highlight_next()
    root.mainloop()

highlight_line_in_pdf(input_pdf_path, aligned_data)
