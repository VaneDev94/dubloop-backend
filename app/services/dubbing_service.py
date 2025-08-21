from app.utils.audio_tools import (
    extract_audio_from_video_bytes,
    transcribe_audio,
    translate_text,
    clone_voice,
    synthesize_audio,
    enhance_audio,
    merge_audio_with_video,
    apply_lip_sync
)
from app.models.subtitle import generate_subtitles
import time

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from app.models.user import User
from sqlalchemy.orm import Session


async def process_dubbing(
    file,
    target_language,
    user: User,
    db: Session,
    voice_source="auto",  # auto | custom
    custom_voice=None,  # UploadFile
    enable_lip_sync=False,
    enable_subtitles=False,
    enable_audio_enhancement=True,
    voice_cloning: bool = True
):
    video_bytes = await file.read()
    metrics = {}

    # 1. Extraer audio del vídeo
    try:
        t1 = time.perf_counter()
        audio_wav = extract_audio_from_video_bytes(video_bytes)
        metrics["audio_extraction_time"] = f"{time.perf_counter() - t1:.2f}s"
    except Exception as e:
        raise Exception(f"Error en extracción de audio: {str(e)}")

    # 2. Transcripción del audio
    try:
        t2 = time.perf_counter()
        transcript = transcribe_audio(audio_wav)
        metrics["transcription_time"] = f"{time.perf_counter() - t2:.2f}s"
    except Exception as e:
        raise Exception(f"Error en transcripción: {str(e)}")

    # Subtítulos (si se solicita)
    subtitles = None
    if enable_subtitles:
        try:
            subtitles = generate_subtitles(transcript)
        except Exception as e:
            raise Exception(f"Error en generación de subtítulos: {str(e)}")

    # 3. Traducción
    try:
        t3 = time.perf_counter()
        translated_text = translate_text(transcript, target_language)
        metrics["translation_time"] = f"{time.perf_counter() - t3:.2f}s"
        metrics["total_tokens"] = len(translated_text.split())
    except Exception as e:
        raise Exception(f"Error en traducción: {str(e)}")

    # 4. Clonación de voz (personalizada o automática)
    try:
        t4 = time.perf_counter()
        if voice_cloning:
            if voice_source == "custom" and custom_voice:
                custom_audio_bytes = await custom_voice.read()
                voice_id = clone_voice(custom_audio_bytes)
            else:
                voice_id = clone_voice(audio_wav)
        else:
            voice_id = None
        metrics["voice_cloning_time"] = f"{time.perf_counter() - t4:.2f}s"
    except Exception as e:
        raise Exception(f"Error en clonación de voz: {str(e)}")

    # 5. Síntesis
    try:
        t5 = time.perf_counter()
        audio_translated = synthesize_audio(translated_text, target_language, voice_id)
        metrics["synthesis_time"] = f"{time.perf_counter() - t5:.2f}s"
    except Exception as e:
        raise Exception(f"Error en síntesis: {str(e)}")

    # 6. Mejora de audio
    if enable_audio_enhancement:
        try:
            t6 = time.perf_counter()
            audio_final = enhance_audio(audio_translated)
            metrics["enhancement_time"] = f"{time.perf_counter() - t6:.2f}s"
        except Exception as e:
            raise Exception(f"Error en mejora de audio: {str(e)}")
    else:
        audio_final = audio_translated

    # Aplicar lip sync si está habilitado
    if enable_lip_sync:
        try:
            t_lip = time.perf_counter()
            video_bytes = apply_lip_sync(video_bytes, audio_final)
            metrics["lip_sync_time"] = f"{time.perf_counter() - t_lip:.2f}s"
        except Exception as e:
            raise Exception(f"Error en lip sync: {str(e)}")

    # 7. Unión con el vídeo
    try:
        t7 = time.perf_counter()
        video_final = merge_audio_with_video(video_bytes, audio_final)
        metrics["merge_time"] = f"{time.perf_counter() - t7:.2f}s"
    except Exception as e:
        raise Exception(f"Error en unión con el vídeo: {str(e)}")

    # Progreso simulado
    metrics["progress"] = "100%"

    return {
        "video": video_final,
        "metrics": metrics,
        "subtitles": subtitles
    }
