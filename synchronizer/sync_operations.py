from difflib import SequenceMatcher

def synchronize_audio_to_pdf(audio_transcription, pdf_text, start_page=None, end_page=None):
    aligned_data = []

    total_pages = len(pdf_text)
    start_index = start_page  if start_page is not None else 0
    end_index = end_page  if end_page is not None else total_pages

    selected_pages = pdf_text[start_index:end_index]

    last_page_num = start_page if start_page else 1
    last_line_num = 1

    for segment in audio_transcription:

        text = segment["text"]
        start = segment["start"]
        end = segment["end"]

        best_match = None
        highest_similarity = 0

        for page in selected_pages:
            for page_num, lines in page.items():
                actual_page_num = int(page_num.split("_")[1])

                if actual_page_num < last_page_num:
                    continue

                for line_num, line_text in lines.items():
                    actual_line_num = int(line_num.split('_')[1])

                    if actual_page_num == last_page_num and actual_line_num < last_line_num:
                        continue

                    similarity = SequenceMatcher(None, text, line_text).ratio()

                    proximity_bonus = 0
                    if actual_page_num == last_page_num:
                        if actual_line_num == last_line_num + 1:
                            proximity_bonus = 0.1
                        elif actual_line_num == last_line_num + 2:
                            proximity_bonus = 0.05

                    adjusted_similarity = similarity + proximity_bonus

                    if adjusted_similarity > highest_similarity:
                        highest_similarity = adjusted_similarity
                        best_match = (page_num, line_num, actual_page_num, actual_line_num)

        if best_match and highest_similarity > 0.1:
            last_page_num = best_match[2]
            last_line_num = best_match[3]
            aligned_data.append(
                {"text": text, "start": start, "end": end, "page": best_match[0], "line": best_match[1]})

    print(aligned_data)

    return aligned_data