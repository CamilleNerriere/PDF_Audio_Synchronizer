
## PDF & Audio Synchronizer

A Python tool to **synchronize an audio file with the textual content of a PDF**, line by line, page by page.

---

### Overview

This project analyzes an audio file (e.g., `.m4a`, `.mp3`), automatically transcribes it, and aligns it with the corresponding text from a PDF document.

It’s ideal for audiobooks, learning tools, or accessibility use cases.

---

### Features

- Automatic audio ↔ PDF text alignment
- Audio transcription using [Vosk](https://alphacephei.com/vosk/)
- Structural PDF analysis (pages, lines, coordinates)
- Visual line highlighting with Tkinter
- Temporary file cleanup
- FastAPI-powered backend

---

### Installation

```bash
git clone https://github.com/your-username/Pdf-Audio-Synchronizer.git
cd Pdf-Audio-Synchronizer
pip install -r requirements.txt
```

---

### Install the French Vosk Model

This project uses the French Vosk model `vosk-model-fr-0.22`.  
➡️ Download here: [vosk-model-fr-0.22](https://alphacephei.com/vosk/models)

Unzip and place it inside `audio_analyser/`:

```
audio_analyser/
└── vosk-model-fr-0.22/
```

---

### Launch the API

```bash
uvicorn main:app --reload
```

Test interface: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Example request

```bash
curl -X 'POST' \
  'http://localhost:8000/sync?start_page=89&end_page=90' \
  -F 'pdf=@data/pdf/example.pdf' \
  -F 'audio=@data/audios/example.m4a'
```

Response:

```json
{
  "aligned_data": [
    {
      "text": "text excerpt",
      "page_num": 89,
      "pdf_coords": [x0, y0, x1, y1],
      "audio_start": 1.23,
      "audio_end": 3.45
    }
  ]
}
```

---

### Visual Demo

📺 [Watch demo on YouTube](https://www.youtube.com/watch?v=N4dsNjVjd44)  

---

###  Local Demo

Run the Tkinter-based demo:

```bash
python demo_local.py
```

Sample files are included in `data/`.

---

### Tech stack

- Python 3.13
- FastAPI
- PyMuPDF (fitz)
- ffmpeg
- vosk
- Tkinter
- Pillow

---

###  Possible improvements

- `.srt` subtitle export
- Web-based visual interface
- Collaborative annotation
- MongoDB or PostgreSQL storage

---

Licence MIT
