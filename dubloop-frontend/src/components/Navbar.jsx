import React from 'react';
import { NavLink } from 'react-router-dom';
import logo from '../assets/logodubloop.png';

const Navbar = () => {
  return (
    <header className="flex items-center" style={{ height: "5rem" }}>
      <div className="max-w-7xl mx-auto w-full flex items-center justify-between px-8">
        <img src={logo} alt="Dubloop Logo" className="h-[4rem] md:h-[12rem] w-auto mt-2" />
        <nav className="flex items-center justify-between w-full">
          <div className="flex-1 flex justify-center gap-[3rem] md:gap-[4rem]">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `text-[1rem] md:text-[1.2rem] font-medium transition-colors duration-200 ease-out relative after:content-[''] after:absolute after:left-0 after:-bottom-1 after:w-0 after:h-[2px] after:bg-[#2ECC9A] after:transition-all after:duration-300 hover:after:w-full hover:text-[#33FFB5] text-[#2ECC9A]${
                  isActive
                    ? ' font-semibold'
                    : ''
                }`
              }
            >
              Inicio
            </NavLink>
            <NavLink
              to="/traducir-video"
              className={({ isActive }) =>
                `text-[1rem] md:text-[1.2rem] font-medium transition-colors duration-200 ease-out relative after:content-[''] after:absolute after:left-0 after:-bottom-1 after:w-0 after:h-[2px] after:bg-[#2ECC9A] after:transition-all after:duration-300 hover:after:w-full hover:text-[#33FFB5] text-[#2ECC9A]${
                  isActive
                    ? ' font-semibold'
                    : ''
                }`
              }
            >
              Traducir Video
            </NavLink>
            <NavLink
              to="/precios"
              className={({ isActive }) =>
                `text-[1rem] md:text-[1.2rem] font-medium transition-colors duration-200 ease-out relative after:content-[''] after:absolute after:left-0 after:-bottom-1 after:w-0 after:h-[2px] after:bg-[#2ECC9A] after:transition-all after:duration-300 hover:after:w-full hover:text-[#33FFB5] text-[#2ECC9A]${
                  isActive
                    ? ' font-semibold'
                    : ''
                }`
              }
            >
              Precios
            </NavLink>
          </div>
          <NavLink
            to="/iniciar-sesion"
            className="text-[1rem] md:text-[1.1rem] rounded-full border border-[#2ECC9A]/70 bg-transparent text-white font-medium transition-all duration-200 ease-out shadow-[0_0_8px_2px_rgba(46,204,154,0.4)] backdrop-blur-sm hover:bg-[#2ECC9A] hover:text-white hover:scale-105 hover:shadow-[0_0_12px_3px_rgba(46,204,154,0.6)]"
            style={{ padding: "0.5rem 1.25rem" }}
          >
            Iniciar Sesión
          </NavLink>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;