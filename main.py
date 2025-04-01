from http.client import HTTPException

from fastapi import FastAPI, UploadFile, File, Query, Request, HTTPException
from fastapi.responses import JSONResponse
from audio_analyser import convert_and_retranscript
from pdf_handler import generate_pdf_informations
from synchronizer import synchronize_audio_to_pdf
from utils.logger import logger
from utils.exceptions import AudioProcessingError, PDFProcessingError

app = FastAPI()

@app.post("/sync")
async def sync_endpoint(pdf: UploadFile = File(...), audio: UploadFile = File(...), start_page: int = Query(..., description="Page de début"),
    end_page: int = Query(..., description="Page de fin")):

    try:
        audio_transcription = convert_and_retranscript(audio.file)
        pdf_text = generate_pdf_informations(pdf.file)
        aligned_data = synchronize_audio_to_pdf(audio_transcription, pdf_text, start_page=start_page, end_page=end_page)

        return {"aligned_data": aligned_data}

    except AudioProcessingError as ae:
        logger.warning(f"[AUDIO] {ae}")
        raise HTTPException(status_code=422, detail=str(ae))

    except PDFProcessingError as pe:
        logger.warning(f"[PDF] {pe}")
        raise HTTPException(status_code=422, detail=str(pe))

    except Exception as e:
        logger.error(f"Exception during sync : {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Non Handled Exception during request {request.method} {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."},
    )
