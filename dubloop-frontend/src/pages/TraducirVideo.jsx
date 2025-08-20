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

  const handleSubmit = async () => {
    try {
      if (!videoFile) {
        setStatus("Selecciona un video primero ❌");
        return;
      }

      setStatus("Procesando...");

      const formData = new FormData();
      formData.append("file", videoFile); // 👈 obligatorio
      formData.append("target_language", "es"); // 👈 asegúrate de usar el mismo nombre que en backend
      formData.append("voice_cloning", cloneVoice === "Sí" ? "true" : "false"); 
      formData.append("enable_lip_sync", lipSync === "sí" ? "true" : "false");
      formData.append("enable_subtitles", addSubtitles === "sí" ? "true" : "false");
      formData.append("enable_audio_enhancement", improveAudio === "sí" ? "true" : "false");

      const response = await API.post(`/dubbing/start-dubbing/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("Respuesta del backend:", response.data);
      setJobId(response.data.job_id);
      setStatus("Procesando...");
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
    setOutputLang(outputLang === "Español" ? "Inglés" : "Español");
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
    </div>
  );
};

export default TraducirVideo;