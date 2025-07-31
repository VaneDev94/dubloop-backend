import subprocess
from io import BytesIO

def extract_audio_from_video_bytes(video_bytes: bytes) -> bytes:
    """
    Extrae el audio de un vídeo (en bytes) y lo devuelve como .wav (también en bytes), sin guardar nada en disco.
    """
    process = subprocess.Popen(
        ['ffmpeg', '-i', 'pipe:0', '-f', 'wav', '-ac', '1', '-ar', '16000', 'pipe:1'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL  # para no mostrar logs de ffmpeg
    )
    output, _ = process.communicate(input=video_bytes)
    return output


# --- Funciones de transcripción, traducción y simulaciones ---
import openai
import os
from dotenv import load_dotenv
import tempfile

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe un audio .wav en memoria usando Whisper de OpenAI.
    """
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.wav"  # necesario para OpenAI
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

def translate_text(text: str, target_lang: str) -> str:
    """
    Traduce el texto a otro idioma usando OpenAI (modo chat).
    """
    prompt = f"Traduce el siguiente texto al idioma '{target_lang}':\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

import requests

def clone_voice(audio_bytes: bytes) -> str:
    """
    Clona la voz desde un audio en memoria, genera el voice_id, lo usa, y luego elimina la voz clonada.
    """
    api_key = os.getenv("ELEVEN_API_KEY")
    url_add = "https://api.elevenlabs.io/v1/voices/add"

    files = {
        'name': (None, "DubloopTemp"),
        'files': ('voice.wav', BytesIO(audio_bytes), 'audio/wav')
    }

    headers = {
        "xi-api-key": api_key
    }

    # Crear la voz
    response = requests.post(url_add, headers=headers, files=files)
    if response.status_code != 200:
        raise Exception(f"Error al clonar voz: {response.status_code} - {response.text}")

    voice_id = response.json()["voice_id"]

    # Usar la voz para síntesis (por fuera de esta función)

    # Eliminar la voz
    url_delete = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    requests.delete(url_delete, headers=headers)

    return voice_id

from elevenlabs import generate, set_api_key

set_api_key(os.getenv("ELEVEN_API_KEY"))

def synthesize_audio(text: str, lang: str, voice_id: str) -> bytes:
    """
    Genera audio real desde texto usando ElevenLabs y la voz clonada o seleccionada.
    """
    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )
    return audio

from pydub import AudioSegment

def enhance_audio(audio_bytes: bytes) -> bytes:
    """
    Mejora el audio: normaliza y sube el volumen.
    """
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
    louder = audio + 6  # subir volumen
    normalized = louder.normalize()
    output = BytesIO()
    normalized.export(output, format="mp3")
    return output.getvalue()

def merge_audio_with_video(video_bytes: bytes, audio_bytes: bytes) -> bytes:
    """
    Usa ffmpeg para reemplazar el audio original del vídeo por el audio doblado.
    Todo en memoria, sin guardar en disco.
    """
    import tempfile
    import subprocess

    with tempfile.NamedTemporaryFile(suffix=".mp4") as video_tmp, \
         tempfile.NamedTemporaryFile(suffix=".mp3") as audio_tmp, \
         tempfile.NamedTemporaryFile(suffix=".mp4") as output_tmp:

        video_tmp.write(video_bytes)
        video_tmp.flush()

        audio_tmp.write(audio_bytes)
        audio_tmp.flush()

        cmd = [
            "ffmpeg", "-y",
            "-i", video_tmp.name,
            "-i", audio_tmp.name,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_tmp.name
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        output_tmp.seek(0)
        return output_tmp.read()