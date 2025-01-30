import subprocess
import wave
import json
from vosk import Model, KaldiRecognizer


def convert_mp4_to_wave(input_file, output_file):
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
        print(f"Erreur lors de la conversion : {result.stderr}")
    else:
        print("Conversion réussie!")


def retranscript_audio(input_file):

    model_path= "vosk-model-fr-0.22"
    model = Model(model_path)

    wf = wave.open(input_file, "rb")

    rec = KaldiRecognizer(model, wf.getframerate())

    audio_texts = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            text_extract = json.loads(rec.Result())["text"]
            audio_texts.append(text_extract)
    return " ".join(audio_texts)

input_file = "../data/audios/carroll_de_l'autre_cote_du_miroir/6 8889 Alice dit au revoir, Gros Coco dit qu’il ne la reconnaîtra pas son visage étant si commun.m4a"
output_file = "../data/audios/carroll_de_l'autre_cote_du_miroir/6 8889 Alice dit au revoir, Gros Coco dit qu’il ne la reconnaîtra pas son visage étant si commun.wav"

def convert_and_retranscript(input_file, output_file):
    convert_mp4_to_wave(input_file, output_file)
    return retranscript_audio(output_file)

text = convert_and_retranscript(input_file, output_file)

print(text)