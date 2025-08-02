from app.utils.audio_tools import (
    extract_audio_from_video_bytes,
    transcribe_audio,
    translate_text,
    clone_voice,
    synthesize_audio,
    enhance_audio,
    merge_audio_with_video
)
from app.models.subtitle import generate_subtitles
import time

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from app.services.credits import calculate_credits
from app.models.user import User
from sqlalchemy.orm import Session

def discount_user_credits(user: User, db: Session, lip_sync: bool, subtitles: bool, enhancement: bool):
    cost = calculate_credits(
        enable_lip_sync=lip_sync,
        enable_subtitles=subtitles,
        enable_audio_enhancement=enhancement
    )
    user.credits -= cost
    db.commit()

async def process_dubbing(
    file,
    target_lang,
    user: User,
    db: Session,
    voice_source="auto",  # auto | custom
    custom_voice=None,  # UploadFile
    enable_lip_sync=False,
    enable_subtitles=False,
    enable_audio_enhancement=True
):
    video_bytes = await file.read()
    metrics = {}

    # 1. Extraer audio del vídeo
    t1 = time.perf_counter()
    audio_wav = extract_audio_from_video_bytes(video_bytes)
    metrics["audio_extraction_time"] = f"{time.perf_counter() - t1:.2f}s"

    # 2. Transcripción del audio
    t2 = time.perf_counter()
    transcript = transcribe_audio(audio_wav)
    metrics["transcription_time"] = f"{time.perf_counter() - t2:.2f}s"

    # Subtítulos (si se solicita)
    subtitles = None
    if enable_subtitles:
        subtitles = generate_subtitles(transcript)

    # 3. Traducción
    t3 = time.perf_counter()
    translated_text = translate_text(transcript, target_lang)
    metrics["translation_time"] = f"{time.perf_counter() - t3:.2f}s"
    metrics["total_tokens"] = len(translated_text.split())

    # 4. Clonación de voz (personalizada o automática)
    t4 = time.perf_counter()
    if voice_source == "custom" and custom_voice:
        custom_audio_bytes = await custom_voice.read()
        voice_id = clone_voice(custom_audio_bytes)
    else:
        voice_id = clone_voice(audio_wav)
    metrics["voice_cloning_time"] = f"{time.perf_counter() - t4:.2f}s"

    # 5. Síntesis
    t5 = time.perf_counter()
    audio_translated = synthesize_audio(translated_text, target_lang, voice_id)
    metrics["synthesis_time"] = f"{time.perf_counter() - t5:.2f}s"

    # 6. Mejora de audio
    if enable_audio_enhancement:
        t6 = time.perf_counter()
        audio_final = enhance_audio(audio_translated)
        metrics["enhancement_time"] = f"{time.perf_counter() - t6:.2f}s"
    else:
        audio_final = audio_translated

    # 7. Unión con el vídeo
    t7 = time.perf_counter()
    video_final = merge_audio_with_video(video_bytes, audio_final)
    metrics["merge_time"] = f"{time.perf_counter() - t7:.2f}s"

    # Progreso simulado
    metrics["progress"] = "100%"

    discount_user_credits(user, db, enable_lip_sync, enable_subtitles, enable_audio_enhancement)
    return {
        "video": video_final,
        "metrics": metrics,
        "subtitles": subtitles
    }


# Estimación de créditos según las opciones seleccionadas
from app.services.credits import calculate_credits

def estimate_cost(
    enable_lip_sync=False,
    enable_subtitles=False,
    enable_audio_enhancement=True
) -> int:
    """
    Estima los créditos necesarios según las funciones opcionales seleccionadas.
    """
    return calculate_credits(
        enable_lip_sync=enable_lip_sync,
        enable_subtitles=enable_subtitles,
        enable_audio_enhancement=enable_audio_enhancement
    )
