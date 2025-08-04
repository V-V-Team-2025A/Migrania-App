import "./common/styles/index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import DashboardMedicoPage from "./features/feature_Grupo5_AgendamientoCitas/pages/DashboardMedicoPage.jsx";
import AgendaSemanalPage from "./features/feature_Grupo5_AgendamientoCitas/pages/AgendaSemanalPage.jsx";
import FormularioCitaPage from "./features/feature_Grupo5_AgendamientoCitas/pages/FormularioCitaPage.jsx";
import AgendaMensualPage from "./features/feature_Grupo5_AgendamientoCitas/pages/AgendaMensualPage.jsx";
import CitasPaciente from "./features/feature_Grupo5_AgendamientoCitas/components/CitasPaciente.jsx";
import FormularioCita from "./features/feature_Grupo5_AgendamientoCitas/components/FormularioCita.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<DashboardMedicoPage />} />
        <Route path="/dashboard-medico" element={<DashboardMedicoPage />} />
        <Route path="/agenda/semana" element={<AgendaSemanalPage />} />
        <Route path="/agenda/mes" element={<AgendaMensualPage />} />
        <Route path="/citas-paciente" element={<CitasPaciente />} />
        <Route path="/formulario-cita" element={<FormularioCita />} />
        <Route path="*" element={<DashboardMedicoPage />} />
      </Routes>
    </Router>
  </StrictMode>
);
