import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { motion } from "framer-motion";

const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.3,
      delayChildren: 0.2,
    },
  },
};

const textVariants = {
  hidden: { opacity: 0, x: -30, filter: "blur(8px)" },
  visible: { opacity: 1, x: 0, filter: "blur(0px)", transition: { duration: 0.8 } },
};

const pVariants = {
  hidden: { opacity: 0, x: -30, filter: "blur(8px)" },
  visible: { opacity: 1, x: 0, filter: "blur(0px)", transition: { duration: 0.5 } },
};

const loginCardVariants = {
  hidden: { opacity: 0, x: 50 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.8, delay: 1 } },
};

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/dashboard");
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/auth/login`, {
        email,
        password,
      });
      localStorage.setItem("token", response.data.token);
      setLoading(false);
      navigate("/dashboard");
    } catch (error) {
      const message = error.response?.data?.message || "Error al iniciar sesión";
      alert(message);
      setLoading(false);
    }
  };

  return (
    <div
      className="flex min-h-screen bg-cover bg-center text-white"
      style={{
        backgroundImage: "url('/bg1.png')"
      }}
    >
      {/* Left side - Inspirational text */}
      <div className="w-1/2 relative flex flex-col justify-center pl-40 pr-12 pt-0 py-20 overflow-hidden">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="relative z-10 max-w-md"
        >
          <motion.h1 className="text-5xl font-extrabold mb-6 leading-tight" variants={textVariants}>
            Transforma tu voz, conecta con el mundo
          </motion.h1>
          <motion.p className="text-lg font-light max-w-sm" variants={pVariants}>
            Convierte tu contenido en cualquier idioma sin perder tu esencia única. Empieza tu viaje con Dubloop.
          </motion.p>
        </motion.div>
      </div>

      {/* Right side - Login card */}
      <motion.div
        className="w-1/2 flex items-center justify-center pt-8 pb-12 px-16"
        variants={loginCardVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="relative bg-black/20 border border-[#2ECC9A]/40 rounded-[30px] px-10 py-10 w-full max-w-sm mt-0 text-white shadow-[0_0_15px_rgba(46,204,154,0.4)] backdrop-blur-sm">
          <form className="space-y-8" onSubmit={handleSubmit}>
            <h2 className="text-3xl font-bold text-white mb-6 text-center">Accede a Dubloop</h2>
            <p className="text-sm text-gray-200 mb-6 text-center">Regístrate o inicia sesión para continuar</p>

            <div className="flex flex-col">
              <label htmlFor="email" className="mb-2 text-sm font-semibold text-white">
                Correo electrónico
              </label>
              <input
                id="email"
                type="email"
                placeholder="tu@email.com"
                className="p-3 rounded-md bg-transparent border border-[#2ECC9A] placeholder-[#2ECC9A]/70 text-white focus:outline-none focus:ring-2 focus:ring-[#33FFB5] focus:ring-opacity-75 transition"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="flex flex-col">
              <label htmlFor="password" className="mb-2 text-sm font-semibold text-white">
                Contraseña
              </label>
              <input
                id="password"
                type="password"
                placeholder="********"
                className="p-3 rounded-md bg-transparent border border-[#2ECC9A] placeholder-[#2ECC9A]/70 text-white focus:outline-none focus:ring-2 focus:ring-[#33FFB5] focus:ring-opacity-75 transition"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 rounded-md bg-transparent border border-[#2ECC9A] font-semibold text-white hover:bg-[#2ECC9A] hover:text-white transition"
              disabled={loading}
            >
              {loading ? "Cargando..." : "Iniciar Sesión"}
            </button>
          </form>

          <div className="mt-8 flex flex-col gap-4">
            <button
              type="button"
              className="w-full py-3 rounded-md bg-transparent border border-[#2ECC9A] font-semibold text-white hover:bg-[#2ECC9A] hover:text-white transition"
              onClick={() => navigate("/register")}
            >
              Regístrate
            </button>

            <button
              type="button"
              className="w-full flex items-center justify-center gap-3 py-3 rounded-md bg-white text-black font-medium hover:bg-gray-200 transition"
              onClick={() => window.location.href = `${process.env.REACT_APP_API_URL}/auth/google`}
            >
              <svg className="w-6 h-6" viewBox="0 0 48 48" aria-hidden="true" focusable="false">
                <g>
                  <path
                    fill="#4285F4"
                    d="M24 9.5c3.54 0 6.06 1.53 7.46 2.81l5.51-5.37C33.99 4.06 29.38 2 24 2 14.82 2 6.97 7.98 3.67 16.18l6.78 5.27C12.68 15.03 17.89 9.5 24 9.5z"
                  />
                  <path
                    fill="#34A853"
                    d="M46.1 24.55c0-1.54-.14-3.02-.39-4.45H24v8.44h12.43c-.54 2.9-2.18 5.36-4.64 7.01l7.19 5.6c4.18-3.86 6.62-9.56 6.62-16.6z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M10.45 28.09A14.48 14.48 0 0 1 9.5 24c0-1.42.24-2.8.66-4.09l-6.78-5.27C2.51 17.98 2 20.92 2 24c0 3.08.51 6.02 1.38 8.36l7.07-4.27z"
                  />
                  <path
                    fill="#EA4335"
                    d="M24 46c5.38 0 9.9-1.78 13.2-4.85l-7.19-5.6c-2 1.35-4.53 2.15-8.01 2.15-6.11 0-11.32-5.53-13.55-12.97l-7.07 4.27C6.97 40.02 14.82 46 24 46z"
                  />
                  <path fill="none" d="M2 2h44v44H2z" />
                </g>
              </svg>
              Continuar con Google
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}