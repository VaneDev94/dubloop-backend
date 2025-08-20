// src/pages/GoogleCallback.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const GoogleCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleGoogleLogin = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');

      if (!code) {
        navigate('/login'); // si no hay code, lo mandamos a login
        return;
      }

      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/google/callback`, { code });

        const token = response.data.token;
        localStorage.setItem('token', token);
        navigate('/dashboard'); // redirigimos al dashboard o donde quieras
      } catch (error) {
        console.error('Error al iniciar sesión con Google:', error);
        navigate('/login');
      }
    };

    handleGoogleLogin();
  }, [navigate]);

  return (
    <div className="flex items-center justify-center h-screen">
      <p className="text-xl text-[#2da59c]">Procesando inicio de sesión con Google...</p>
    </div>
  );
};

export default GoogleCallback;