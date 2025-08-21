import time
from datetime import datetime, timedelta
from app.services.dubbing_service import process_dubbing

# Diccionario para almacenar los jobs en memoria
jobs = {}

def create_job(job_id):
    jobs[job_id] = {
        "status": "processing",
        "progress": 0,
        "metrics": {},
        "video": None,
        "error": None,
        "error_step": None,
        "subtitles": None,
        "created_at": datetime.utcnow(),
        "steps": []
    }

async def run_dubbing_job(
    job_id,
    user_id,
    file_bytes,
    target_lang,
    enable_lip_sync,
    enable_subtitles,
    enable_audio_enhancement,
    voice_cloning
):
    try:
        start_time = time.time()
        jobs[job_id]["progress"] = 10
        jobs[job_id]["steps"].append("Transcripción iniciada")

        result = await process_dubbing(
            file=DummyUploadFile(file_bytes),
            target_lang=target_lang,
            enable_lip_sync=enable_lip_sync,
            enable_subtitles=enable_subtitles,
            enable_audio_enhancement=enable_audio_enhancement,
            voice_cloning=voice_cloning
        )

        jobs[job_id]["steps"].append("Transcripción completada")
        jobs[job_id]["progress"] = 20
        jobs[job_id]["metrics"]["transcription_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Traducción completada")
        jobs[job_id]["progress"] = 40
        jobs[job_id]["metrics"]["translation_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Clonación de voz completada")
        jobs[job_id]["progress"] = 60
        jobs[job_id]["metrics"]["voice_cloning_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Síntesis de audio completada")
        jobs[job_id]["progress"] = 75
        jobs[job_id]["metrics"]["audio_synthesis_time"] = time.time() - start_time

        if enable_lip_sync:
            jobs[job_id]["steps"].append("Lip sync completado")
            jobs[job_id]["progress"] = 85
            jobs[job_id]["metrics"]["lip_sync_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Merge finalizado")
        jobs[job_id]["progress"] = 90
        jobs[job_id]["metrics"]["merge_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Job completado")
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["metrics"].update(result["metrics"])
        jobs[job_id]["video"] = result["video"]
        jobs[job_id]["subtitles"] = result.get("subtitles") if result.get("subtitles") is not None else {}
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["error_step"] = "dubbing"

def get_job_status(job_id):
    return jobs.get(job_id, None)

def get_job_video(job_id):
    job = jobs.get(job_id)
    if job and job["video"]:
        return job["video"]
    return None

async def rerun_dubbing_job(
    job_id,
    target_lang,
    enable_lip_sync,
    enable_subtitles,
    enable_audio_enhancement,
    voice_cloning
):
    try:
        start_time = time.time()
        jobs[job_id]["progress"] = 10
        jobs[job_id]["steps"].append("Transcripción iniciada")

        file_bytes = get_job_video(job_id)
        if not file_bytes:
            raise ValueError("No se encontró el vídeo original para este job.")

        result = await process_dubbing(
            file=DummyUploadFile(file_bytes),
            target_lang=target_lang,
            enable_lip_sync=enable_lip_sync,
            enable_subtitles=enable_subtitles,
            enable_audio_enhancement=enable_audio_enhancement,
            voice_cloning=voice_cloning
        )

        jobs[job_id]["steps"].append("Transcripción completada")
        jobs[job_id]["progress"] = 20
        jobs[job_id]["metrics"]["transcription_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Traducción completada")
        jobs[job_id]["progress"] = 40
        jobs[job_id]["metrics"]["translation_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Clonación de voz completada")
        jobs[job_id]["progress"] = 60
        jobs[job_id]["metrics"]["voice_cloning_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Síntesis de audio completada")
        jobs[job_id]["progress"] = 75
        jobs[job_id]["metrics"]["audio_synthesis_time"] = time.time() - start_time

        if enable_lip_sync:
            jobs[job_id]["steps"].append("Lip sync completado")
            jobs[job_id]["progress"] = 85
            jobs[job_id]["metrics"]["lip_sync_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Merge finalizado")
        jobs[job_id]["progress"] = 90
        jobs[job_id]["metrics"]["merge_time"] = time.time() - start_time

        jobs[job_id]["steps"].append("Job completado")
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["metrics"].update(result["metrics"])
        jobs[job_id]["video"] = result["video"]
        jobs[job_id]["subtitles"] = result.get("subtitles") if result.get("subtitles") is not None else {}
        jobs[job_id]["error"] = None
        jobs[job_id]["error_step"] = None
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["error_step"] = "rerun_dubbing"

def clean_old_jobs():
    now = datetime.utcnow()
    expired_keys = [
        job_id for job_id, data in jobs.items()
        if data.get("created_at") and now - data["created_at"] > timedelta(minutes=30)
    ]
    for job_id in expired_keys:
        del jobs[job_id]

# Clase auxiliar para simular un UploadFile desde bytes
class DummyUploadFile:
    def __init__(self, data: bytes):
        self.data = data

    async def read(self):
        return self.data