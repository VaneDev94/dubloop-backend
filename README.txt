# Dubloop – Sistema de Doblaje Automático con IA

**Dubloop** es una solución backend especializada en doblaje automático de vídeos, diseñada para transformar cualquier contenido audiovisual a múltiples idiomas manteniendo la voz original del hablante mediante clonación de voz y síntesis avanzada.

Este sistema está enfocado a creadores de contenido, youtubers, formadores y plataformas audiovisuales que desean expandir su alcance internacional sin perder la identidad vocal de quienes aparecen en el vídeo.

## 🧠 ¿Qué hace Dubloop?

Dubloop toma un vídeo original, identifica las voces, las transcribe, traduce su contenido, clona las voces reales de cada hablante y genera un nuevo audio doblado, manteniendo el tono, ritmo y personalidad de las voces originales, en el idioma seleccionado.

Todo este proceso se realiza sin guardar archivos en el servidor y se ejecuta íntegramente en memoria para garantizar máxima privacidad y rendimiento.

## 🔥 Funcionalidades destacadas

- 🎙 Extracción de voz directamente desde vídeos
- 🧠 Transcripción automática con inteligencia artificial (Whisper)
- 🌍 Traducción a múltiples idiomas usando modelos avanzados
- 🧬 Clonación de voz personalizada por hablante (usando ElevenLabs)
- 🗣️ Generación de audio doblado en otro idioma con la misma voz original
- 🎚 Mejora del audio: normalización y limpieza
- 🎥 Unión automática del nuevo audio al vídeo original
- ♻️ Clonación temporal: las voces se eliminan tras su uso
- 🚫 Sin almacenamiento: procesamiento 100% en memoria

## ⚙️ Tecnologías principales

- **FastAPI** para la construcción de la API REST
- **FFmpeg** para procesamiento de audio y vídeo
- **Whisper (OpenAI)** para transcripción automática
- **GPT (OpenAI)** para traducción contextual avanzada
- **ElevenLabs API** para clonación y síntesis de voz
- **Pydub** para tratamiento y mejora del audio

## 🔒 Enfoque en privacidad

Dubloop garantiza un flujo limpio y seguro. Las voces clonadas se eliminan automáticamente una vez utilizadas. No se almacena ningún archivo ni se guarda información del usuario.