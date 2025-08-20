import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import "./styles/globals.css";
import App from "./App.jsx";

// Importar páginas mínimas
import Home from "./pages/Home.jsx";
import TraducirVideo from "./pages/TraducirVideo.jsx";
import Precios from "./pages/Precios.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import GoogleCallback from "./pages/GoogleCallback.jsx";
import Profile from "./pages/Profile.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<Home />} />
          <Route path="traducir-video" element={<TraducirVideo />} />
          <Route path="precios" element={<Precios />} />
          <Route path="iniciar-sesion" element={<Login />} />
          <Route path="registro" element={<Register />} />
          <Route path="auth/google/callback" element={<GoogleCallback />} />
          <Route path="profile" element={<Profile />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
