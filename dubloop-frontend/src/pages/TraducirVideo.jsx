import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import bg2 from "../assets/bg1.png";
import { API } from "../api/api"; // asegúrate de que este path es correcto

const TraducirVideo = () => {
  const [lipSync, setLipSync] = useState(null);
  const [addSubtitles, setAddSubtitles] = useState(null);
  const [improveAudio, setImproveAudio] = useState(null);
  const [outputLang, setOutputLang] = useState(null);
  const [cloneVoice, setCloneVoice] = useState(null);

  const [videoFile, setVideoFile] = useState(null);
  const [status, setStatus] = useState("");
  const [resultUrl, setResultUrl] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [progress, setProgress] = useState(0);

  const handleSubmit = async () => {
    try {
      if (!videoFile) {
        setStatus("Selecciona un video primero ❌");
        return;
      }

      setStatus("Procesando...");

      const formData = new FormData();
      formData.append("file", videoFile);
      formData.append("target_language", outputLang || "en"); 
      formData.append("voice_cloning", cloneVoice === "Sí" ? "true" : "false");
      formData.append("enable_lip_sync", lipSync === "Sí" ? "true" : "false");
      formData.append("enable_subtitles", addSubtitles === "Sí" ? "true" : "false");
      formData.append("enable_audio_enhancement", improveAudio === "Sí" ? "true" : "false");

      const response = await API.post(`/dubbing/start-dubbing/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("Respuesta del backend:", response.data);
      setJobId(response.data.job_id);
      setStatus("Procesando...");
      setProgress(0);
    } catch (error) {
      console.error("Error al enviar datos:", error);
      setStatus("Error ❌");
    }
  };

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        const response = await API.get(`/dubbing/result/${jobId}`);
        if (response.data.progress !== undefined) {
          setProgress(response.data.progress);
        }
        if (response.data.status === "completed") {
          setResultUrl(response.data.result_url);
          setStatus("Completado ✅");
          clearInterval(interval);
        } else if (response.data.status === "error") {
          setStatus("Error ❌");
          clearInterval(interval);
        } else {
          setStatus("Procesando...");
        }
      } catch (error) {
        console.error("Error al obtener el resultado:", error);
        setStatus("Error ❌");
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [jobId]);

  const handleToggleOutputLang = () => {
    setOutputLang(outputLang === "es" ? "en" : "es");
  };

  const handleToggleCloneVoice = () => {
    setCloneVoice(cloneVoice === "Sí" ? "No" : "Sí");
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setVideoFile(e.target.files[0]);
    }
  };

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen bg-cover bg-center px-4"
      style={{ backgroundImage: `url(${bg2})` }}
    >
      {/* ... resto de tu JSX igual */}
      {jobId && (
        <div className="w-full max-w-lg mt-4">
          <div className="w-full bg-gray-300 rounded-full h-4 mb-2">
            <div
              className="bg-green-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="text-center font-medium">{progress}%</p>
        </div>
      )}
      {status && (
        <p className="mt-2 font-semibold text-center">{status}</p>
      )}
      {resultUrl && (
        <div className="mt-4 flex flex-col gap-2">
          <video controls src={resultUrl} className="w-full max-w-lg rounded-lg shadow-lg" />

          {/* Descargar vídeo final */}
          <a
            href={`${API.defaults.baseURL}/dubbing/download/${jobId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-center"
          >
            Descargar vídeo final
          </a>

          {/* Descargar subtítulos */}
          <a
            href={`${API.defaults.baseURL}/dubbing/subtitles/${jobId}?format=srt`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-center"
          >
            Descargar subtítulos (.srt)
          </a>

          {/* Ver métricas */}
          <button
            onClick={async () => {
              try {
                const response = await API.get(`/dubbing/metrics/${jobId}`);
                alert(JSON.stringify(response.data, null, 2));
              } catch (error) {
                console.error("Error al obtener métricas:", error);
                alert("No se pudieron cargar las métricas ❌");
              }
            }}
            className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
          >
            Ver métricas
          </button>
        </div>
      )}
    </div>
  );
};

export default TraducirVideo;