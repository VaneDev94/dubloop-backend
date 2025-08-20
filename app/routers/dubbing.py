from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from io import BytesIO
import os
import uuid
import asyncio
from typing import Optional

from app.services.dubbing_service import process_dubbing
from app.services import job_manager
from app.services.job_manager import clean_old_jobs
from app.models.user import User
from app.auth.auth_handler import get_current_user
from app.auth.dependencies import require_verified_email

router = APIRouter()

allowed_extensions = {".mp4", ".mov", ".avi", ".mkv"}


def validate_upload_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de archivo no permitido: {ext}. Formatos válidos: {', '.join(allowed_extensions)}"
        )


@router.get("/")
async def redirect_docs():
    return RedirectResponse(url="/docs")


@router.post("/")
async def dub_video(
    file: UploadFile = File(...),
    custom_voice: Optional[UploadFile] = File(None),
    target_lang: Optional[str] = Form(None),
    voice_source: str = Form("auto"),
    enable_lip_sync: bool = Form(False),
    enable_subtitles: bool = Form(False),
    enable_audio_enhancement: bool = Form(True),
    current_user: User = Depends(require_verified_email)
):
    validate_upload_file(file)
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")
    file.file.seek(0)

    if voice_source == "custom" and not custom_voice:
        raise HTTPException(status_code=400, detail="Se requiere un archivo de voz personalizado si seleccionas 'custom'.")

    if not target_lang:
        from app.services.language_detection import detect_language
        detected_lang = await detect_language(file)
        if not detected_lang:
            raise HTTPException(status_code=400, detail="No se pudo detectar el idioma del vídeo.")
        target_lang = detected_lang
        file.file.seek(0)

    dubbed_video = await process_dubbing(
        file=file,
        custom_voice=custom_voice,
        voice_source=voice_source,
        target_lang=target_lang,
        enable_lip_sync=enable_lip_sync,
        enable_subtitles=enable_subtitles,
        enable_audio_enhancement=enable_audio_enhancement,
        current_user=current_user
    )

    return StreamingResponse(
        BytesIO(dubbed_video),
        media_type="video/mp4",
        headers={"Content-Disposition": "inline; filename=dubbed_video.mp4"}
    )


@router.post("/start-dubbing/")
async def start_dubbing(
    file: UploadFile = File(...),
    target_language: str = Form(..., alias="target_lang"),
    voice_cloning: str = Form("false"),
    enable_lip_sync: str = Form("false"),
    enable_subtitles: str = Form("false"),
    enable_audio_enhancement: str = Form("true")
):
    validate_upload_file(file)
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")
    file.file.seek(0)

    def to_bool(value: str) -> bool:
        return value.lower() in ["true", "1", "yes", "sí"]

    job_id = str(uuid.uuid4())
    file_bytes = contents

    job_manager.create_job(job_id)

    asyncio.create_task(
        job_manager.run_dubbing_job(
            job_id=job_id,
            file_bytes=file_bytes,
            target_lang=target_language,
            enable_lip_sync=to_bool(enable_lip_sync),
            enable_subtitles=to_bool(enable_subtitles),
            enable_audio_enhancement=to_bool(enable_audio_enhancement)
        )
    )

    return JSONResponse(content={
        "job_id": job_id,
        "message": "Vídeo recibido correctamente",
        "filename": file.filename,
        "size_bytes": len(contents),
        "target_language": target_language,
        "voice_cloning": to_bool(voice_cloning)
    })


@router.get("/result/{job_id}")
async def get_dubbing_result(job_id: str):
    clean_old_jobs()
    job = job_manager.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID no encontrado.")

    if job["status"] == "processing":
        return {
            "status": "processing",
            "progress": job["progress"],
            "message": "Tu vídeo sigue procesándose. Puedes consultar este mismo enlace más tarde."
        }

    if job["status"] == "error":
        return {"status": "error", "error": job["error"]}

    metrics_headers = {f"X-Metric-{k}": str(v) for k, v in job["metrics"].items()}

    return StreamingResponse(
        BytesIO(job["video"]),
        media_type="video/mp4",
        headers={
            "Content-Disposition": "inline; filename=dubbed_video.mp4",
            **metrics_headers
        }
    )


@router.get("/download/{job_id}")
async def download_dubbed_video(job_id: str):
    job = job_manager.get_job_status(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Vídeo no disponible para descarga.")

    return StreamingResponse(
        BytesIO(job["video"]),
        media_type="video/mp4",
        headers={"Content-Disposition": "attachment; filename=dubbed_video.mp4"}
    )


@router.get("/metrics/{job_id}")
async def get_dubbing_metrics(job_id: str):
    job = job_manager.get_job_status(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Métricas no disponibles.")
    return job["metrics"]


@router.post("/reprocess/{job_id}")
async def reprocess_dubbing_job(
    job_id: str,
    target_lang: str = Form(...),
    enable_lip_sync: bool = Form(False),
    enable_subtitles: bool = Form(False),
    enable_audio_enhancement: bool = Form(True)
):
    job = job_manager.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID no encontrado.")

    asyncio.create_task(
        job_manager.rerun_dubbing_job(
            job_id=job_id,
            target_lang=target_lang,
            enable_lip_sync=enable_lip_sync,
            enable_subtitles=enable_subtitles,
            enable_audio_enhancement=enable_audio_enhancement
        )
    )

    return JSONResponse(content={"job_id": job_id, "message": "Reprocesando con nuevas opciones"})


@router.get("/subtitles/{job_id}")
async def get_subtitles(job_id: str, format: str = "srt"):
    job = job_manager.get_job_status(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Subtítulos no disponibles.")

    subtitles = job.get("subtitles")
    if not subtitles:
        raise HTTPException(status_code=404, detail="Este job no tiene subtítulos.")

    if format == "srt":
        content = subtitles.get("srt")
        filename = "subtitles.srt"
        media_type = "application/x-subrip"
    elif format == "vtt":
        content = subtitles.get("vtt")
        filename = "subtitles.vtt"
        media_type = "text/vtt"
    else:
        raise HTTPException(status_code=400, detail="Formato de subtítulo no válido. Usa 'srt' o 'vtt'.")

    if not content:
        raise HTTPException(status_code=404, detail=f"Subtítulos en formato {format} no disponibles.")

    return StreamingResponse(BytesIO(content.encode("utf-8")), media_type=media_type, headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })