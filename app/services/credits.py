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


def get_total_credits_for_user(user) -> int:
    """
    Devuelve la cantidad total de créditos que tiene un usuario.
    """
    return user.credits if hasattr(user, "credits") else 0


#función para deducir créditos
def deduct_credits(user, amount: int):
    """
    Resta créditos al usuario si tiene suficientes.
    Lanza excepción si no tiene créditos suficientes.
    """
    if user.credits < amount:
        raise ValueError("No tienes suficientes créditos.")
    user.credits -= amount
def check_and_consume_credits(user, cost: int):
    """
    Verifica si el usuario tiene créditos suficientes y los descuenta.
    Lanza una excepción si no tiene suficientes créditos.
    """
    if get_total_credits_for_user(user) < cost:
        raise ValueError("No tienes créditos suficientes.")
    deduct_credits(user, cost)

def estimate_credits(
    enable_lip_sync: bool,
    enable_subtitles: bool,
    enable_audio_enhancement: bool
) -> int:
    """
    Estima los créditos que se usarán para una operación dada sin aplicarlos.
    """
    return calculate_credits(
        enable_lip_sync=enable_lip_sync,
        enable_subtitles=enable_subtitles,
        enable_audio_enhancement=enable_audio_enhancement
    )

def add_credits_to_user(user, amount: int):
    """
    Añade una cantidad específica de créditos al usuario.
    """
    if not hasattr(user, "credits"):
        raise AttributeError("El usuario no tiene atributo 'credits'")
    user.credits += amount