import time
from datetime import datetime, timedelta
from app.services.dubbing_service import process_dubbing
from app.services.credits import check_and_consume_credits
from app.services.credits import estimate_credits

# Diccionario para almacenar los jobs en memoria
jobs = {}

def create_job(job_id):
    jobs[job_id] = {
        "status": "processing",
        "progress": 0,
        "metrics": {},
        "video": None,
        "error": None,
        "estimated_credits": None,
        "subtitles": None,
        "created_at": datetime.utcnow()
    }

async def run_dubbing_job(
    job_id,
    user_id,
    file_bytes,
    target_lang,
    enable_lip_sync,
    enable_subtitles,
    enable_audio_enhancement
):
    try:
        estimated_credits = estimate_credits(file_bytes, enable_lip_sync, enable_subtitles, enable_audio_enhancement)
        if not check_and_consume_credits(user_id, estimated_credits):
            raise Exception("Créditos insuficientes")
        jobs[job_id]["estimated_credits"] = estimated_credits

        result = await process_dubbing(
            file=DummyUploadFile(file_bytes),
            target_lang=target_lang,
            enable_lip_sync=enable_lip_sync,
            enable_subtitles=enable_subtitles,
            enable_audio_enhancement=enable_audio_enhancement
        )
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["metrics"] = result["metrics"]
        jobs[job_id]["video"] = result["video"]
        jobs[job_id]["subtitles"] = result.get("subtitles")
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)

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
    enable_audio_enhancement
):
    try:
        file_bytes = get_job_video(job_id)
        if not file_bytes:
            raise ValueError("No se encontró el vídeo original para este job.")

        result = await process_dubbing(
            file=DummyUploadFile(file_bytes),
            target_lang=target_lang,
            enable_lip_sync=enable_lip_sync,
            enable_subtitles=enable_subtitles,
            enable_audio_enhancement=enable_audio_enhancement
        )
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["metrics"] = result["metrics"]
        jobs[job_id]["video"] = result["video"]
        jobs[job_id]["subtitles"] = result.get("subtitles")
        jobs[job_id]["error"] = None
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)

def clean_old_jobs():
    now = datetime.utcnow()
    expired_keys = [
        job_id for job_id, data in jobs.items()
        if data.get("created_at") and now - data["created_at"] > timedelta(minutes=30)
    ]
    for job_id in expired_keys:
        del jobs[job_id]

def estimate_credits(file_bytes, enable_lip_sync, enable_subtitles, enable_audio_enhancement):
    base_cost = len(file_bytes) / (1024 * 1024)  # 1 crédito por MB
    if enable_lip_sync:
        base_cost += 2
    if enable_subtitles:
        base_cost += 1
    if enable_audio_enhancement:
        base_cost += 1
    return int(base_cost)

# Clase auxiliar para simular un UploadFile desde bytes
class DummyUploadFile:
    def __init__(self, data: bytes):
        self.data = data

    async def read(self):
        return self.data