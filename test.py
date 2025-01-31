from audio_analyser import convert_and_retranscript
from pdf_handler import generate_pdf_informations
from rapidfuzz import fuzz
import re
import numpy as np

# audio transcription
input_file = "data/audios/carroll_de_l'autre_cote_du_miroir/6 8990 Vexée et irritée Alice s’en va mais est interrompue par un fracas dans le bois.m4a"
audio_transcription = convert_and_retranscript(input_file)

# pdf divided by pages divided by lines
pdf_path = "data/pdf/caroll_de_autre_cote_miroir.pdf"
pdf_text = generate_pdf_informations(pdf_path)

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = text.replace('-', ' ')
    return ' '.join(text.split())  # Normalize whitespace


def calculate_text_similarity(text1, text2):
    p_text1 = preprocess_text(text1)
    p_text2 = preprocess_text(text2)

    return fuzz.partial_ratio(p_text1, p_text2)


def synchronize_audio_to_pdf(audio_transcription, pdf_text, start_page=None, end_page=None, similarity_threshold=0.5):

    aligned_data = []

    total_pages = len(pdf_text)
    start_index = start_page - 1 if start_page is not None else 0
    end_index = end_page if end_page is not None else total_pages

    selected_pages = pdf_text[start_index:end_index]

    last_matched_page = start_page or 1
    last_matched_line_index = 0

    for audio_segment in audio_transcription:
        best_match = None
        highest_similarity = 0

        for page_dict in selected_pages:
            for page_num, lines in page_dict.items():
                page_num = int(page_num.split('_')[1])

                if page_num < last_matched_page:
                    continue

                for line_index, line_data in enumerate(lines):
                    line_text = line_data['text']

                    similarity = calculate_text_similarity(
                        audio_segment['text'],
                        line_text
                    )

                    context_bonus = 0
                    if page_num == last_matched_page:
                        line_distance = abs(line_index - last_matched_line_index)
                        context_bonus = max(0, 1 - (line_distance * 0.1))

                    adjusted_similarity = similarity + context_bonus

                    if adjusted_similarity > highest_similarity and adjusted_similarity >= similarity_threshold:
                        highest_similarity = adjusted_similarity
                        best_match = {
                            'audio_text': audio_segment['text'],
                            'audio_start': audio_segment['start'],
                            'audio_end': audio_segment['end'],
                            'pdf_text': line_text,
                            'pdf_coords': line_data['coord'],
                            'page_num': page_num,
                            'line_index': line_index,
                        }

        if best_match:
            aligned_data.append(best_match)
            last_matched_page = best_match['page_num']
            last_matched_line_index = best_match['line_index']

    return aligned_data

