from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from app.services.dubbing_service import process_dubbing
from app.services import job_manager
from app.services.job_manager import clean_old_jobs
from io import BytesIO
import uuid
import asyncio
import base64
from app.services.credits import calculate_credits

router = APIRouter()

@router.post("/")
async def dub_video(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    enable_lip_sync: bool = Form(False),
    enable_subtitles: bool = Form(False),
    enable_audio_enhancement: bool = Form(True)
):
    dubbed_video = await process_dubbing(
        file=file,
        target_lang=target_lang,
        enable_lip_sync=enable_lip_sync,
        enable_subtitles=enable_subtitles,
        enable_audio_enhancement=enable_audio_enhancement
    )

    return StreamingResponse(
        BytesIO(dubbed_video),
        media_type="video/mp4",
        headers={"Content-Disposition": "inline; filename=dubbed_video.mp4"}
    )

@router.post("/start-dubbing/")
async def start_dubbing(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    enable_lip_sync: bool = Form(False),
    enable_subtitles: bool = Form(False),
    enable_audio_enhancement: bool = Form(True)
):
    job_id = str(uuid.uuid4())
    file_bytes = await file.read()

    # Guardar datos iniciales del job
    job_manager.create_job(job_id)

    # Lanzar proceso en segundo plano
    asyncio.create_task(
        job_manager.run_dubbing_job(
            job_id=job_id,
            file_bytes=file_bytes,
            target_lang=target_lang,
            enable_lip_sync=enable_lip_sync,
            enable_subtitles=enable_subtitles,
            enable_audio_enhancement=enable_audio_enhancement
        )
    )

    return JSONResponse(content={"job_id": job_id})

@router.get("/dubbing/result/{job_id}")
async def get_dubbing_result(job_id: str):
    clean_old_jobs()
    job = job_manager.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID no encontrado.")

    if job["status"] == "processing":
        return {"status": "processing", "progress": job["progress"]}

    if job["status"] == "error":
        return {"status": "error", "error": job["error"]}

    # Preparar métricas como headers
    metrics_headers = {f"X-Metric-{k}": str(v) for k, v in job["metrics"].items()}

    return StreamingResponse(
        BytesIO(job["video"]),
        media_type="video/mp4",
        headers={
            "Content-Disposition": "inline; filename=dubbed_video.mp4",
            **metrics_headers
        }
    )

@router.post("/dubbing/estimate/")
async def estimate_credits(
    enable_lip_sync: bool = Form(False),
    enable_subtitles: bool = Form(False),
    enable_audio_enhancement: bool = Form(True)
):
    credits = calculate_credits(
        enable_lip_sync=enable_lip_sync,
        enable_subtitles=enable_subtitles,
        enable_audio_enhancement=enable_audio_enhancement
    )
    return {"estimated_credits": credits}

@router.get("/dubbing/download/{job_id}")
async def download_dubbed_video(job_id: str):
    job = job_manager.get_job_status(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Vídeo no disponible para descarga.")

    return StreamingResponse(
        BytesIO(job["video"]),
        media_type="video/mp4",
        headers={"Content-Disposition": "attachment; filename=dubbed_video.mp4"}
    )

@router.get("/dubbing/metrics/{job_id}")
async def get_dubbing_metrics(job_id: str):
    job = job_manager.get_job_status(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Métricas no disponibles.")
    return job["metrics"]
@router.post("/dubbing/reprocess/{job_id}")
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

    # Lanzar reprocesado en segundo plano
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

@router.get("/dubbing/subtitles/{job_id}")
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