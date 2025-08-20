import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import bg2 from "../assets/bg1.png";
import axios from "axios";
import { API } from "../api"; // o el path correcto si ya tienes un wrapper configurado

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
      setStatus("Procesando...");
      const formData = new FormData();
      if (videoFile) formData.append("file", videoFile);
      formData.append("lipSync", lipSync || "");
      formData.append("addSubtitles", addSubtitles || "");
      formData.append("improveAudio", improveAudio || "");
      formData.append("outputLang", outputLang || "");
      formData.append("cloneVoice", cloneVoice || "");

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
    // Example toggle between two options, can be expanded as needed
    if (outputLang === "Español") {
      setOutputLang("Inglés");
    } else {
      setOutputLang("Español");
    }
  };

  const handleToggleCloneVoice = () => {
    // Example toggle between two options, can be expanded as needed
    if (cloneVoice === "Sí") {
      setCloneVoice("No");
    } else {
      setCloneVoice("Sí");
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setVideoFile(e.target.files[0]);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-cover bg-center px-4"
      style={{ backgroundImage: `url(${bg2})` }}>
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1, ease: "easeOut" }}
        className="inline-flex items-center gap-2 bg-gradient-to-r from-black/30 via-black/40 to-black/30 border border-[#2ECC9A]/70 shadow-[0_0_15px_rgba(46,204,154,0.4)] backdrop-blur-sm rounded-full px-4 py-1 text-white mt-12 animate-fadeDown"
      >
        <span>✨</span>
        <span>Nuestra IA integrada de alta precisión</span>
      </motion.div>
      <motion.h1
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, ease: "easeOut", delay: 0.3 }}
        className="text-4xl md:text-6xl font-bold text-white text-center mt-10 mb-2 whitespace-pre-line font-satoshi"
      >
        Toma El Control Del Idioma{'\n'}De Tus Videos
      </motion.h1>
      <motion.p
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, ease: "easeOut", delay: 0.5 }}
        className="text-lg md:text-xl text-gray-200 text-center max-w-3xl mt-6 mb-10 font-grotesk"
      >
        Traduce, sincroniza y descarga el video prácticamente en tiempo real y aumenta el alcance de tu público
      </motion.p>
      {/* Recuadro de arrastrar video */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, ease: "easeOut", delay: 0.7 }}
        className="relative overflow-hidden w-full max-w-3xl mx-auto mt-12"
      >
        <label
          className="flex flex-col items-center justify-center border-2 border-[#2ECC9A] rounded-lg p-10 
                     bg-black/30 text-center text-[#2ECC9A] hover:border-[#33FFB5] transition 
                     shadow-[0_0_25px_rgba(46,204,154,0.5)] cursor-pointer
                     before:absolute before:inset-0 before:bg-[radial-gradient(circle,_rgba(51,255,181,0.15)_0%,_transparent_90%)] before:rounded-full before:z-0 z-10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-12 h-12 mb-4 text-[#2ECC9A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <p className="text-lg text-white font-grotesk">
            {videoFile ? `Archivo seleccionado: ${videoFile.name}` : "Arrastra un video o haz click para abrir el explorador de archivos"}
          </p>
          <span className="text-sm text-gray-400 mt-2">(MP4 · MOV · AVI · MKV)</span>
          <input type="file" accept="video/*" onChange={handleFileChange} className="hidden" />
        </label>
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, ease: "easeOut", delay: 0.9 }}
        className="relative bg-black/20 border border-[#2ECC9A]/40 rounded-[30px] px-10 py-12 w-full max-w-3xl mt-16 text-white shadow-[0_0_15px_rgba(46,204,154,0.4)] backdrop-blur-sm"
      >
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-4">
            <div 
              onClick={handleToggleOutputLang}
              className={`flex items-center justify-between w-full rounded-full border px-6 py-4 text-white text-lg cursor-pointer transition ${
                outputLang ? "border-[#33FFB5]" : "border-[#2ECC9A] hover:border-[#33FFB5]"
              } bg-transparent`}
            >
              <span>Idioma de salida del video {outputLang ? `- ${outputLang}` : ""}</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            <div 
              onClick={handleToggleCloneVoice}
              className={`flex items-center justify-between w-full rounded-full border px-6 py-4 text-white text-lg cursor-pointer transition ${
                cloneVoice ? "border-[#33FFB5]" : "border-[#2ECC9A] hover:border-[#33FFB5]"
              } bg-transparent`}
            >
              <span>Clonar voz desde el video {cloneVoice ? `- ${cloneVoice}` : ""}</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>

          <div className="flex justify-between mt-6">
            <div className="flex flex-col items-center gap-2">
              <span>Sincronización de labios</span>
              <div className="flex gap-3">
                <button
                  onClick={() => setLipSync(lipSync === "sí" ? null : "sí")}
                  className={`px-6 py-2 rounded-full border text-white transition duration-300 ease-out active:scale-95 active:bg-[#33FFB5]/20 ${
                    lipSync === "sí"
                      ? "bg-[#33FFB5]/20 border-[#33FFB5]"
                      : "border-[#2ECC9A] hover:border-[#33FFB5] hover:bg-[#33FFB5]/10"
                  }`}
                >
                  Sí
                </button>
                <button
                  onClick={() => setLipSync(lipSync === "no" ? null : "no")}
                  className={`px-6 py-2 rounded-full border text-white transition duration-300 ease-out active:scale-95 active:bg-[#33FFB5]/20 ${
                    lipSync === "no"
                      ? "bg-[#33FFB5]/20 border-[#33FFB5]"
                      : "border-[#2ECC9A] hover:border-[#33FFB5] hover:bg-[#33FFB5]/10"
                  }`}
                >
                  No
                </button>
              </div>
            </div>
            <div className="flex flex-col items-center gap-2">
              <span>Añadir subtítulos</span>
              <div className="flex gap-3">
                <button
                  onClick={() => setAddSubtitles(addSubtitles === "sí" ? null : "sí")}
                  className={`px-6 py-2 rounded-full border text-white transition duration-300 ease-out active:scale-95 active:bg-[#33FFB5]/20 ${
                    addSubtitles === "sí"
                      ? "bg-[#33FFB5]/20 border-[#33FFB5]"
                      : "border-[#2ECC9A] hover:border-[#33FFB5] hover:bg-[#33FFB5]/10"
                  }`}
                >
                  Sí
                </button>
                <button
                  onClick={() => setAddSubtitles(addSubtitles === "no" ? null : "no")}
                  className={`px-6 py-2 rounded-full border text-white transition duration-300 ease-out active:scale-95 active:bg-[#33FFB5]/20 ${
                    addSubtitles === "no"
                      ? "bg-[#33FFB5]/20 border-[#33FFB5]"
                      : "border-[#2ECC9A] hover:border-[#33FFB5] hover:bg-[#33FFB5]/10"
                  }`}
                >
                  No
                </button>
              </div>
            </div>
          </div>

          <div className="flex flex-col items-center gap-2 mt-6">
            <span>Mejorar calidad del audio del video</span>
            <div className="flex gap-3">
              <button
                onClick={() => setImproveAudio(improveAudio === "sí" ? null : "sí")}
                className={`px-6 py-2 rounded-full border text-white transition duration-300 ease-out active:scale-95 active:bg-[#33FFB5]/20 ${
                  improveAudio === "sí"
                    ? "bg-[#33FFB5]/20 border-[#33FFB5]"
                    : "border-[#2ECC9A] hover:border-[#33FFB5] hover:bg-[#33FFB5]/10"
                }`}
              >
                Sí
              </button>
              <button
                onClick={() => setImproveAudio(improveAudio === "no" ? null : "no")}
                className={`px-6 py-2 rounded-full border text-white transition duration-300 ease-out active:scale-95 active:bg-[#33FFB5]/20 ${
                  improveAudio === "no"
                    ? "bg-[#33FFB5]/20 border-[#33FFB5]"
                    : "border-[#2ECC9A] hover:border-[#33FFB5] hover:bg-[#33FFB5]/10"
                }`}
              >
                No
              </button>
            </div>
          </div>

          <motion.button
            onClick={handleSubmit}
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 20 }}
            className="mt-10 w-full bg-transparent border border-[#2ECC9A] rounded-full px-10 py-4 text-lg font-bold text-white hover:bg-[#33FFB5]/20 transition duration-500 ease-out active:scale-95 active:bg-[#33FFB5]/20"
          >
            ENVIAR
          </motion.button>
          {status && <p className="mt-4 text-center text-white">{status}</p>}
          {resultUrl && (
            <div className="mt-6 flex flex-col items-center gap-4">
              <video
                src={resultUrl}
                controls
                className="w-full max-w-2xl rounded-lg border border-[#2ECC9A] shadow-lg"
              />
              <a
                href={`${import.meta.env.VITE_API_URL}/dubbing/download/${jobId}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-center text-[#33FFB5] underline"
              >
                Descargar video procesado
              </a>
              <a
                href={`${import.meta.env.VITE_API_URL}/dubbing/subtitles/${jobId}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-center text-[#33FFB5] underline"
              >
                Descargar subtítulos
              </a>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default TraducirVideo;
