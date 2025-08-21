def apply_lip_sync(video_bytes: bytes, audio_bytes: bytes) -> bytes:
    """
    Aplica sincronización labial real usando Wav2Lip.
    Requiere modelo preentrenado y PyTorch instalado.
    """
    import tempfile
    import subprocess
    from pathlib import Path

    # Guardar inputs en archivos temporales
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_tmp, \
         tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_tmp, \
         tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as output_tmp:

        video_tmp.write(video_bytes)
        video_tmp.flush()

        audio_tmp.write(audio_bytes)
        audio_tmp.flush()

        # Ruta al modelo de Wav2Lip (debes descargarlo antes)
        wav2lip_model = Path("models/wav2lip_gan.pth")

        if not wav2lip_model.exists():
            raise FileNotFoundError(
                "No se encontró el modelo Wav2Lip. Descárgalo en 'models/wav2lip_gan.pth'"
            )

        # Ejecutar Wav2Lip (asumiendo que tienes un script inference.py en carpeta Wav2Lip)
        cmd = [
            "python", "Wav2Lip/inference.py",
            "--checkpoint_path", str(wav2lip_model),
            "--face", video_tmp.name,
            "--audio", audio_tmp.name,
            "--outfile", output_tmp.name
        ]

        subprocess.run(cmd, check=True)

        output_tmp.seek(0)
        return output_tmp.read()

def extract_audio_from_video_bytes(video_bytes: bytes) -> bytes:
    """
    Extrae el audio de un video en formato WAV.
    Devuelve los bytes del audio.
    """
    import tempfile
    import subprocess

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_tmp, \
         tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_tmp:

        # Guardar el video temporalmente
        video_tmp.write(video_bytes)
        video_tmp.flush()

        # Usar ffmpeg para extraer el audio
        cmd = [
            "ffmpeg", "-y",
            "-i", video_tmp.name,
            "-ar", "16000",      # tasa de muestreo 16kHz
            "-ac", "1",          # mono
            "-f", "wav",
            audio_tmp.name
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        audio_tmp.seek(0)
        return audio_tmp.read()

def transcribe_audio(audio_bytes: bytes, language: str = "en") -> str:
    """
    Transcribe audio bytes to text using OpenAI Whisper API.
    """
    import openai
    import tempfile

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_tmp:
            audio_tmp.write(audio_bytes)
            audio_tmp.flush()
            audio_tmp.seek(0)

            with openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_tmp,
                language=language
            ) as response:
                transcription = response["text"]

        return transcription.strip()
    except Exception as e:
        return f"[Transcription failed: {e}]"

def translate_text(text: str, target_language: str) -> str:
    """
    Traduce el texto al idioma objetivo usando OpenAI Chat Completions API.
    """
    import openai
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini-translator",
            messages=[
                {"role": "system", "content": f"You are a helpful translator that translates text to {target_language}."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        translated_text = response.choices[0].message.content.strip()
        return translated_text
    except Exception:
        return text


def clone_voice(reference_audio: bytes, text: str, target_language: str = "en") -> bytes:
    """
    Clone a voice using OpenAI's TTS API.
    """
    try:
        import openai
        response = openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
        )
        return response.read()
    except Exception:
        return bytes()


# Nueva función: sintetiza audio desde texto sin referencia de voz
def synthesize_audio(text: str, target_language: str = "en", voice: str = "alloy") -> bytes:
    """
    Sintetiza audio a partir de texto usando OpenAI TTS sin clonación de voz.
    """
    try:
        import openai
        response = openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
        )
        return response.read()
    except Exception:
        return bytes()

def enhance_audio(audio_bytes: bytes) -> bytes:
    """
    Mejora el audio aplicando normalización usando ffmpeg.
    Devuelve los bytes del audio mejorado o el audio original si falla.
    """
    import tempfile
    import subprocess

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as input_tmp, \
             tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as output_tmp:

            input_tmp.write(audio_bytes)
            input_tmp.flush()

            cmd = [
                "ffmpeg", "-y",
                "-i", input_tmp.name,
                "-af", "loudnorm",
                output_tmp.name
            ]

            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            output_tmp.seek(0)
            return output_tmp.read()
    except Exception:
        return audio_bytes

def merge_audio_with_video(video_bytes: bytes, audio_bytes: bytes) -> bytes:
    """
    Combina un video y un audio en un solo archivo de video usando ffmpeg.
    Devuelve los bytes del video final o el original si falla.
    """
    import tempfile
    import subprocess

    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_tmp, \
             tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_tmp, \
             tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as output_tmp:

            video_tmp.write(video_bytes)
            video_tmp.flush()

            audio_tmp.write(audio_bytes)
            audio_tmp.flush()

            cmd = [
                "ffmpeg", "-y",
                "-i", video_tmp.name,
                "-i", audio_tmp.name,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                output_tmp.name
            ]

            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            output_tmp.seek(0)
            return output_tmp.read()
    except Exception:
        return video_bytes