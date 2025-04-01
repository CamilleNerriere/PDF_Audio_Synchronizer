import subprocess
import wave
import json
from vosk import Model, KaldiRecognizer
import os
import tempfile
from utils.safe_remove import safe_remove
from utils.logger import logger
from utils.exceptions import AudioProcessingError

def convert_mp4_to_wave(input_file):
    output_file = input_file.replace(".m4a", ".wav")
    # -y : replace file if exists
    # only show errors in logs
    result = subprocess.run([
        'ffmpeg',
        '-y',
        '-loglevel', 'error',
        '-i', input_file,
        '-ar', '16000',  #16kHz
        '-ac', '1', #mono -> better for vosk
        output_file
    ], capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(f"Error converting mp4 to wave : {result.stderr}")
        raise AudioProcessingError("Invalid audio format or Invalid audio file.")
    else:
        logger.info(f"Wave converted : {output_file}")

    return output_file


def retranscript_audio(input_file):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "vosk-model-fr-0.22")
    if not os.path.exists(model_path):
        raise AudioProcessingError(
            "Vosk model not found. Please install Vosk first Download it and put it in 'audio_analyser/")
    model = Model(model_path)

    with wave.open(input_file, "rb") as wf:

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True) #timestamp for every words

        audio_texts = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                text_extract = json.loads(rec.Result())
                if "result" in text_extract:
                    words = text_extract["result"]
                    for i in range(0, len(words), 5):
                        group = words[i:i+5]
                        group_text = " ".join([word["word"] for word in group])
                        start_time = group[0]["start"]
                        end_time = group[-1]["end"]
                        audio_texts.append({"text": group_text, "start": start_time, "end": end_time})
    return audio_texts

def convert_and_retranscript(input_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_file:
        temp_file.write(input_file.read())
        temp_file_path = temp_file.name

        converted_file = None

        try:

            converted_file = convert_mp4_to_wave(temp_file_path)

            if not os.path.exists(converted_file):
                raise ValueError("Failed to convert audio file")

            transcription = retranscript_audio(converted_file)

            if not transcription:
                raise ValueError("Failed to generate transcription")

            return transcription

        finally:
            safe_remove(temp_file_path)
            safe_remove(converted_file)



