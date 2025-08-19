import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import bg2 from '../assets/bg2.png';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden.');
      return;
    }
    try {
      const response = await axios.post('http://localhost:8000/auth/register', {
        email,
        password,
      });
      localStorage.setItem('token', response.data.token);
      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError('Error al registrar. Inténtalo de nuevo.');
      }
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center"
      style={{ backgroundImage: `url(${bg2})` }}
    >
      <form
        onSubmit={handleSubmit}
        className="bg-white bg-opacity-80 border border-gradient-to-r from-[#3ee6c1] to-[#2da59c] rounded-lg shadow-lg p-10 max-w-md w-full backdrop-blur-sm"
      >
        <h2 className="text-center text-2xl font-semibold mb-6">Crear cuenta</h2>
        <div className="mb-5">
          <label htmlFor="email" className="block mb-2 font-medium text-gray-700">
            Correo electrónico
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#3ee6c1] focus:ring-opacity-75 transition-shadow"
          />
        </div>
        <div className="mb-5">
          <label htmlFor="password" className="block mb-2 font-medium text-gray-700">
            Contraseña
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#3ee6c1] focus:ring-opacity-75 transition-shadow"
          />
        </div>
        <div className="mb-5">
          <label htmlFor="confirmPassword" className="block mb-2 font-medium text-gray-700">
            Confirmar contraseña
          </label>
          <input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={e => setConfirmPassword(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#3ee6c1] focus:ring-opacity-75 transition-shadow"
          />
        </div>
        {error && (
          <div className="text-red-600 mb-5 text-center font-medium">
            {error}
          </div>
        )}
        <button
          type="submit"
          className="w-full py-3 rounded-md bg-gradient-to-r from-[#3ee6c1] to-[#2da59c] text-white font-bold hover:from-[#2ac4a6] hover:to-[#23866f] transition duration-300 ease-in-out animate-pulse-slow"
        >
          Registrarse
        </button>
        <div className="mt-6 text-center text-[#2da59c] font-medium">
          ¿Ya tienes una cuenta?{' '}
          <Link to="/login" className="hover:underline">
            Inicia sesión
          </Link>
        </div>
      </form>
    </div>
  );
};

export default Register;