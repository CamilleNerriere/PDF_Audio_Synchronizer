from audio_analyser import convert_and_retranscript
from pdf_handler import generate_pdf_informations
from synchronizer import synchronize_audio_to_pdf

from tkinter import Tk, Label
from PIL import Image, ImageTk

import fitz


# audio transcription
input_file = "data/audios/carroll_de_l'autre_cote_du_miroir/6 8990 Vexée et irritée Alice s’en va mais est interrompue par un fracas dans le bois.m4a"
audio_transcription = convert_and_retranscript(input_file)

# pdf divided by pages divided by lines
pdf_path = "data/pdf/caroll_de_autre_cote_miroir.pdf"
pdf_text = generate_pdf_informations(pdf_path)

aligned_data = synchronize_audio_to_pdf(audio_transcription, pdf_text, 89, 90)




# def highlight_line_in_pdf(pdf_path, aligned_data):

    # print("on entre dans hightlighter", aligned_data)
    # doc = fitz.open(pdf_path)
    #
    # root = Tk()
    # root.title("PDF Highlighter")
    # label = Label(root)
    # label.pack()
    #
    # for data in aligned_data:
    #     page_number = int(data["page"].split("_")[1]) -1
    #     line_number = int(data["line"].split("_")[1]) -1
    #
    #     page = doc[page_number]
    #     blocks = page.get_text("blocks")
    #
    #     if line_number < len(blocks):
    #
    #         block = blocks[line_number]
    #         rect = fitz.Rect(block[:4])
    #
    #         highlight = page.add_highlight_annot(rect)
    #         highlight.update()
    #
    #         # Sauvegarder temporairement pour afficher les modifications
    #         temp_pdf_path = "temp_output.pdf"
    #         doc.save(temp_pdf_path)
    #
    #         # Convertir la page en image
    #         pixmap = page.get_pixmap()
    #
    #         img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    #
    #         # Afficher l'image dans l'interface graphique
    #         img_tk = ImageTk.PhotoImage(img)
    #         label.config(image=img_tk)
    #         label.image = img_tk
    #
    #     delay = int((data["end"] - data["start"]) * 1000)  # Convertir en millisecondes
    #     root.after(delay, highlight_next, index + 1)  # Appeler
    #
    # doc.close()
    # root.mainloop()


def highlight_line_in_pdf(pdf_path, aligned_data):
    print("on entre dans hightlighter")

    # Ouvrir le document PDF
    doc = fitz.open(pdf_path)

    # Créer la fenêtre Tkinter
    root = Tk()
    root.title("PDF Highlighter")
    label = Label(root)
    label.pack()

    def highlight_next(index=0):
        if index >= len(aligned_data):  # Si toutes les données ont été traitées
            doc.close()  # Fermer le document PDF
            print("Surlignement terminé.")
            return

        # Récupérer les données alignées actuelles
        data = aligned_data[index]
        page_number = int(data["page"].split("_")[1]) -1
        line_number = int(data["line"].split("_")[1]) -1

        print(f"Traitement : Page {page_number}, Ligne {line_number}")

        # Charger la page correspondante
        page = doc[page_number]
        blocks = page.get_text("blocks")

        if line_number < len(blocks):
            block = blocks[line_number]
            rect = fitz.Rect(block[:4])

            # Ajouter un surlignement
            highlight = page.add_highlight_annot(rect)
            highlight.update()

            # Sauvegarder temporairement pour afficher les modifications
            temp_pdf_path = "temp_output.pdf"
            doc.save(temp_pdf_path)

            # Convertir la page en image
            pixmap = page.get_pixmap()
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

            # Afficher l'image dans le label
            img_tk = ImageTk.PhotoImage(img)
            label.config(image=img_tk)
            label.image = img_tk

        # Planifier le prochain surlignement après un délai (en millisecondes)
        delay = int((data["end"] - data["start"]) * 1000)  # Convertir en ms
        root.after(delay, highlight_next, index + 1)  # Appeler highlight_next avec index + 1

    # Démarrer avec le premier élément
    highlight_next()
    root.mainloop()


highlight_line_in_pdf(pdf_path, aligned_data)

