import React, { useState } from 'react';
import { motion } from 'framer-motion';
import bg2 from '../assets/bg2.png';

const Profile = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState('Juan Pérez');
  const email = 'juan.perez@example.com';

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleLogout = () => {
    // Aquí iría la lógica para cerrar sesión
    alert('Sesión cerrada');
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center"
      style={{ backgroundImage: `url(${bg2})` }}
    >
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white bg-opacity-20 backdrop-blur-md rounded-xl shadow-lg p-8 max-w-4xl w-full border-4 border-gradient-to-r from-aqua-400 via-green-400 to-aqua-400 space-y-10"
      >
        <h1 className="text-3xl font-semibold text-white mb-6 text-center">Mi Perfil</h1>

        {/* Sección de datos de perfil */}
        <section>
          <h2 className="text-2xl font-semibold text-white mb-4">Datos de perfil</h2>
          <form className="space-y-6 max-w-md">
            <div>
              <label className="block text-white mb-1 font-medium" htmlFor="name">
                Nombre
              </label>
              <input
                type="text"
                id="name"
                className={`w-full px-4 py-2 rounded-md focus:outline-none ${
                  isEditing ? 'bg-white text-gray-900' : 'bg-white bg-opacity-50 text-gray-700 cursor-not-allowed'
                } border border-transparent focus:border-green-400 transition`}
                value={name}
                onChange={(e) => setName(e.target.value)}
                readOnly={!isEditing}
              />
            </div>
            <div>
              <label className="block text-white mb-1 font-medium" htmlFor="email">
                Email
              </label>
              <input
                type="email"
                id="email"
                className="w-full px-4 py-2 rounded-md bg-white bg-opacity-50 text-gray-700 cursor-not-allowed border border-transparent"
                value={email}
                readOnly
              />
            </div>
            <div className="flex justify-between max-w-xs mt-4">
              <motion.button
                type="button"
                onClick={handleEditToggle}
                whileTap={{ scale: 0.95 }}
                whileHover={{ scale: 1.05 }}
                className="px-6 py-2 rounded-md font-semibold bg-gradient-to-r from-aqua-400 to-green-400 text-white hover:from-green-400 hover:to-aqua-400 transition"
              >
                {isEditing ? 'Guardar' : 'Editar perfil'}
              </motion.button>
              <motion.button
                type="button"
                onClick={handleLogout}
                whileTap={{ scale: 0.95 }}
                whileHover={{ scale: 1.05 }}
                className="px-6 py-2 rounded-md font-semibold bg-gradient-to-r from-green-400 to-aqua-400 text-white hover:from-aqua-400 hover:to-green-400 transition"
              >
                Cerrar sesión
              </motion.button>
            </div>
          </form>
        </section>

        {/* Sección de plan activo */}
        <section>
          <h2 className="text-2xl font-semibold text-white mb-4">Plan activo</h2>
          <div className="max-w-md bg-white bg-opacity-30 rounded-md p-6 border border-green-400 text-white font-medium">
            Plan actual: <span className="font-bold">Pro</span>
          </div>
        </section>
      </motion.div>
    </div>
  );
};

export default Profile;
