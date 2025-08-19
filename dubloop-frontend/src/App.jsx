import { Outlet, useLocation } from "react-router-dom";
import bg1 from "./assets/bg1.png";
import bg2 from "./assets/bg2.png";
import Navbar from "./components/Navbar";

function App() {
  const location = useLocation();

  // Fondos según la página
  const backgroundImage = location.pathname === "/traducir-video" ? bg1 : bg2;

  return (
    <main
      className="min-h-screen w-full text-white relative overflow-hidden"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <Navbar />

      {/* Contenido dinámico */}
      <Outlet />
    </main>
  );
}

export default App;