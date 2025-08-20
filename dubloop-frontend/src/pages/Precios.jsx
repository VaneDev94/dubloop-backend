import React from "react";
import { motion } from "framer-motion";
import axios from "axios";
const API_BASE_URL = import.meta.env.VITE_API_URL;
import { BASE_URL } from "../config";

export default function Precios() {
  const planes = [
    {
      nombre: "Gratis",
      precio: "0€ / mes",
      descripcion: "Perfecto para empezar a probar Dubloop con funciones limitadas.",
      caracteristicas: [
        "Vídeos de hasta 2 minutos",
        "1 voz clonada",
        "Subtítulos automáticos",
        "Exportación máxima en 720p",
        "Procesamiento limitado por vídeo",
      ],
    },
    {
      nombre: "Creador",
      precio: "29€ / mes",
      descripcion: "Ideal para creadores que suben contenido cada semana.",
      caracteristicas: [
        "Vídeos de hasta 20 minutos",
        "Detección y clonación multivoz",
        "Subtítulos editables",
        "Exportación máxima en 1080p",
        "Procesamiento ilimitado por vídeo",
      ],
    },
    {
      nombre: "Premium",
      precio: "39€ / mes",
      descripcion: "Para creadores profesionales que necesitan gran capacidad.",
      caracteristicas: [
        "Vídeos de hasta 1 hora",
        "Clonación ilimitada de voces",
        "Soporte prioritario",
        "Exportación máxima en 4K",
        "Procesamiento ilimitado por vídeo",
      ],
    },
  ];

  const containerVariants = {
    hidden: { x: 100, opacity: 0 },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        staggerChildren: 0.5,
        delayChildren: 0.5,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0,
        ease: "easeOut",
      },
    },
  };

  const badgeVariants = {
    hidden: { scale: 0, opacity: 0 },
    visible: {
      scale: 1,
      opacity: 1,
      transition: { type: "spring", stiffness: 100, damping: 10, delay: 0.8 },
    },
  };

  const titleContainerVariants = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0,
      },
    },
  };

  const letterVariants = {
    hidden: { opacity: 1, filter: "blur(4px)" },
    visible: {
      opacity: 1,
      filter: "blur(0px)",
      transition: { duration: 1.2, ease: "easeInOut" },
    },
  };

  const subtitleLetterVariants = {
    hidden: { opacity: 1, filter: "blur(4px)" },
    visible: {
      opacity: 1,
      filter: "blur(0px)",
      transition: { duration: 0.6, ease: "easeInOut" },
    },
  };

  const handleSubscribe = async (plan) => {
    try {
      const res = await axios.post(`${API_BASE_URL}/subscriptions/create`, {
        plan: plan,
      });
      alert(`Suscripción creada con el plan: ${plan}`);
      console.log(res.data);
      // If backend returns a checkout URL, redirect
      if (res.data && (res.data.checkout_url || res.data.url)) {
        const redirectUrl = res.data.checkout_url || res.data.url;
        window.location.href = redirectUrl;
      }
    } catch (err) {
      console.error(err);
      alert("Error al crear suscripción");
    }
  };

  return (
    <div className="min-h-screen bg-[url('/src/assets/fondo.png')] bg-cover bg-center text-white flex flex-col items-center justify-start pt-10 px-6">
      {/* Animated title: simple motion, fade in from above */}
      <motion.h1
        className="text-5xl font-bold mb-2 mt-0 text-center"
        style={{ display: "block" }}
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, ease: "easeOut" }}
      >
        Planes y Precios
      </motion.h1>
      <motion.h2
        className="text-xl mb-10 text-center"
        style={{ display: "block" }}
        variants={{
          hidden: { opacity: 0, y: 30 },
          visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 1, ease: "easeOut", delay: 0.6 },
          },
        }}
        initial="hidden"
        animate="visible"
      >
        {(() => {
          const text = "Elige el plan que mejor se adapte a ti";
          const letters = text.split("");
          return letters.map((letter, i) => (
            <span key={i} style={{ display: "inline-block" }}>
              {letter === " " ? "\u00A0" : letter}
            </span>
          ));
        })()}
      </motion.h2>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid md:grid-cols-3 gap-8 w-full max-w-6xl mt-10"
      >
        {planes.map((plan, index) => (
          <motion.div
            key={index}
            variants={cardVariants}
            className="relative bg-gray-950/60 bg-gradient-to-br from-[#2ECC9A]/5 via-transparent to-[#33FFB5]/5 p-8 rounded-xl border border-[#2ECC9A]/30 hover:border-[#33FFB5]/50 shadow-[0_0_15px_rgba(46,204,154,0.4)] transition"
          >
            <motion.h2
              className="text-2xl font-semibold mb-4"
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0 },
              }}
            >
              {plan.nombre}
            </motion.h2>
            <motion.p
              className="text-[#2ECC9A] text-3xl font-bold mb-2"
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0 },
              }}
            >
              {plan.precio}
            </motion.p>
            <motion.p
              className="mb-6 text-[#2ECC9A]"
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0 },
              }}
            >
              {plan.descripcion}
            </motion.p>
            <motion.ul
              className="mb-6 space-y-2"
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0 },
              }}
            >
              {plan.caracteristicas.map((caracteristica, i) => (
                <li key={i} className="flex items-start">
                  <span className="text-[#2ECC9A] mr-2">✔</span>
                  {caracteristica}
                </li>
              ))}
            </motion.ul>
            <motion.button
              className="w-full bg-[#2ECC9A] hover:bg-[#33FFB5] text-white font-bold py-2 px-4 rounded"
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0 },
              }}
              onClick={() => handleSubscribe(plan.nombre)}
            >
              Empezar
            </motion.button>
            {plan.nombre === "Creador" && (
              <motion.div
                initial={{ scale: 0, opacity: 0 }}
                animate={{
                  scale: [0, 1.3, 1],
                  opacity: 1,
                  x: [0, -8, 8, -4, 4, 0],
                }}
                transition={{
                  duration: 1.2,
                  ease: "easeOut",
                  delay: 1.5,
                }}
                className="absolute top-4 right-4 bg-gradient-to-r from-[#2ECC9A] to-[#33FFB5] text-white text-ml rounded px-2 py-1"
              >
                Más popular
              </motion.div>
            )}
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}