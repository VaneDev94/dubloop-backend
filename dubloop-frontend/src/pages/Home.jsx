import React, { useState } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import videodemo from "../assets/videodemo.gif";
import bg2 from "../assets/bg2.png";

// Variantes de animación para letras
const fadeInBlurLeft = {
  hidden: { opacity: 0, x: -40, filter: "blur(4px)" },
  visible: (custom = 0) => ({
    opacity: 1,
    x: 0,
    filter: "blur(0px)",
    transition: { duration: 0.8, delay: custom },
  }),
};
const fadeInUpButton = {
  hidden: { opacity: 0, y: 20, filter: "blur(4px)" },
  visible: (custom = 0) => ({
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: { duration: 0.8, delay: custom },
  }),
};
const containerStagger = {
  visible: {
    transition: {
      staggerChildren: 0.08,
    },
  },
};
const containerSequential = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.4,
    },
  },
};

// Nueva variante revealCharBlur para animar cada letra con opacidad y blur con retraso escalonado
const revealCharBlur = {
  hidden: { opacity: 0, filter: "blur(4px)" },
  visible: (custom) => ({
    opacity: 1,
    filter: "blur(0px)",
    transition: {
      duration: 0.6,
      delay: custom * 0.05,
    },
  }),
};
// Nueva variante revealCharBlurFast para subtítulo con delay más rápido
const revealCharBlurFast = {
  hidden: { opacity: 0, filter: "blur(4px)" },
  visible: (custom) => ({
    opacity: 1,
    filter: "blur(0px)",
    transition: {
      duration: 0.6,
      delay: custom * 0.03,
    },
  }),
};

const titleLines = [
  "Rompe Las Barreras",
  "Del Idioma Sin Perder",
  "Tu Esencia",
];
const subtitle = "Sube tu video y en minutos tendrás una versión traducida al idioma que quieras y que suena exactamente como tú.";

const Home = () => {
  const [lipSync, setLipSync] = useState(null);
  const [audioQuality, setAudioQuality] = useState(null);

  return (
    <section
      className="relative bg-cover bg-center text-white pt-[2rem] pb-[5rem] px-[3rem]"
      style={{ backgroundImage: `url(${bg2})` }}
    >
      <div className="max-w-[1200px] mx-auto">
        
        <div className="flex flex-col md:flex-row items-center justify-between gap-10">
          {/* Textos alineados a la izquierda */}
          <motion.div
            className="text-left max-w-[650px] ml-[1rem]"
            initial="hidden"
            animate="visible"
            variants={containerSequential}
          >
            {/* Título principal animado */}
            <motion.h1
              className="text-[3.2rem] font-bold leading-[1.1] text-white max-w-[650px] min-h-[10.5rem] flex flex-col justify-start"
              variants={fadeInBlurLeft}
              style={{ overflow: "hidden" }}
            >
              {titleLines.map((line, i) => (
                <span key={i} className="block">
                  {line.split("").map((char, idx) => (
                    <motion.span
                      key={idx}
                      variants={revealCharBlur}
                      initial="hidden"
                      animate="visible"
                      custom={idx}
                      style={{ display: "inline-block", minWidth: char === " " ? "0.7ch" : undefined }}
                    >
                      {char === " " ? "\u00A0" : char}
                    </motion.span>
                  ))}
                  {i !== titleLines.length - 1 && <br />}
                </span>
              ))}
            </motion.h1>

            {/* Subtexto animado */}
            <motion.p
              className="mt-[1.5rem] text-[1.05rem] text-[#d1d5db] max-w-[500px] leading-[1.5] min-h-[3.2rem]"
              variants={fadeInBlurLeft}
              style={{ overflow: "hidden" }}
            >
              {subtitle.split("").map((char, idx) => (
                <motion.span
                  key={idx}
                  variants={revealCharBlurFast}
                  initial="hidden"
                  animate="visible"
                  custom={idx}
                  style={{ display: "inline-block", minWidth: char === " " ? "0.5ch" : undefined }}
                >
                  {char === " " ? "\u00A0" : char}
                </motion.span>
              ))}
            </motion.p>

            {/* Botón */}
            <motion.div variants={fadeInUpButton} custom={2.5}>
              <Link
                to="/traducir-video"
                className="mt-[2.2rem] inline-block px-[2rem] py-[0.8rem] rounded-full border border-[var(--color-accent,#8fefee)] bg-transparent text-white text-[1rem] font-medium hover:bg-[var(--color-accent,#8fefee)] hover:text-black transition-all shadow-[0_0_10px_var(--color-accent,#8fefee)] backdrop-blur-sm"
              >
                Traduce tu vídeo
              </Link>
            </motion.div>
          </motion.div>

          {/* Video alineado a la derecha */}
          <motion.img
            src={videodemo}
            alt="Demo"
            initial={{ opacity: 0, x: 60, filter: "blur(4px)" }}
            animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
            transition={{ duration: 1, delay: 1 }}
            style={{
              width: "var(--video-demo-width, 35rem)",
              height: "var(--video-demo-height, 25rem)",
              maxWidth: "var(--video-demo-max-width, 40rem)",
              transform: "scale(1.2)",
              transformOrigin: "center center",
              marginLeft: "-3rem",
            }}
            className="rounded-lg flex-shrink-0 ml-[auto] mr-[-3rem] video-transparent"
          />
        </div>
        
        {/* DEMO GRATUITA nueva sección */}
        <motion.section 
          className="py-12"
          initial="hidden"
          animate="visible"
          custom={0.45}
          variants={fadeInUpButton}
        >
          <motion.h2 className="text-2xl font-bold text-center text-white mb-8" variants={fadeInUpButton} custom={0.5}>
            DEMO GRATUITA
          </motion.h2>

          <motion.div 
            className="w-full max-w-[900px] mx-auto bg-black bg-opacity-10 border border-[#2ECC9A]/30 shadow-[0_0_15px_rgba(46,204,154,0.4)] backdrop-blur-md rounded-xl p-6 flex flex-col md:flex-row items-center justify-center gap-8"
            variants={fadeInUpButton}
            custom={0.55}
          >
            {/* Contenedor del video (placeholder con imagen por ahora) */}
            <div className="w-full md:w-1/2 flex justify-center">
              <img
                src="/demo-placeholder.jpg" 
                alt="Video demo"
                className="rounded-xl shadow-lg w-full md:w-[450px] h-[250px] object-cover"
              />
            </div>

            {/* Contenedor del formulario */}
            <div className="w-full md:w-1/2 max-w-md rounded-xl p-6 shadow-lg">
              <label className="block mb-4 text-white">Traducir a:</label>
              <select className="w-full p-2 mb-4 rounded-md bg-black text-white border border-[var(--color-accent,#8fefee)]">
                <option>Seleccionar idioma</option>
                <option>Inglés</option>
                <option>Francés</option>
              </select>

              <div className="mb-4">
                <p className="text-white mb-2">Sincronización de labios</p>
                <div className="flex gap-3">
                  <button
                    onClick={() => setLipSync(lipSync === true ? null : true)}
                    className={`px-4 py-1 border rounded-full transition-transform active:scale-95 hover:bg-[var(--color-accent,#8fefee)] ${
                      lipSync === true
                        ? "bg-[var(--color-accent,#8fefee)] text-black border-[var(--color-accent,#8fefee)]"
                        : "text-white border-[var(--color-accent,#8fefee)]"
                    }`}
                  >
                    Sí
                  </button>
                  <button
                    onClick={() => setLipSync(lipSync === false ? null : false)}
                    className={`px-4 py-1 border rounded-full transition-transform active:scale-95 hover:bg-[var(--color-accent,#8fefee)] ${
                      lipSync === false
                        ? "bg-[var(--color-accent,#8fefee)] text-black border-[var(--color-accent,#8fefee)]"
                        : "text-white border-[var(--color-accent,#8fefee)]"
                    }`}
                  >
                    No
                  </button>
                </div>
              </div>

              <div className="mb-6">
                <p className="text-white mb-2">Mejor calidad de audio</p>
                <div className="flex gap-3">
                  <button
                    onClick={() => setAudioQuality(audioQuality === true ? null : true)}
                    className={`px-4 py-1 border rounded-full transition-transform active:scale-95 hover:bg-[var(--color-accent,#8fefee)] ${
                      audioQuality === true
                        ? "bg-[var(--color-accent,#8fefee)] text-black border-[var(--color-accent,#8fefee)]"
                        : "text-white border-[var(--color-accent,#8fefee)]"
                    }`}
                  >
                    Sí
                  </button>
                  <button
                    onClick={() => setAudioQuality(audioQuality === false ? null : false)}
                    className={`px-4 py-1 border rounded-full transition-transform active:scale-95 hover:bg-[var(--color-accent,#8fefee)] ${
                      audioQuality === false
                        ? "bg-[var(--color-accent,#8fefee)] text-black border-[var(--color-accent,#8fefee)]"
                        : "text-white border-[var(--color-accent,#8fefee)]"
                    }`}
                  >
                    No
                  </button>
                </div>
              </div>

              <button className="w-full px-6 py-2 border border-[var(--color-accent,#8fefee)] rounded-full text-white hover:bg-[var(--color-accent,#8fefee)] active:scale-95 active:bg-[var(--color-accent,#8fefee)]/20 transition-transform">
                ENVIAR
              </button>
            </div>
          </motion.div>
        </motion.section>

      </div>
    </section>
  );
};

export default Home;

<style jsx>{`
  .video-transparent {
    mix-blend-mode: screen;
  }
`}</style>