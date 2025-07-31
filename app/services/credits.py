


def calculate_credits(
    enable_lip_sync: bool,
    enable_subtitles: bool,
    enable_audio_enhancement: bool
) -> int:
    """
    Calcula los créditos necesarios según las funciones opcionales seleccionadas.
    """
    credits = 0

    if enable_lip_sync:
        credits += 100  # 💋 Sincronización labial

    if enable_subtitles:
        credits += 50   # 📝 Generación de subtítulos

    if enable_audio_enhancement:
        credits += 30   # 🎧 Mejora de audio

    return credits