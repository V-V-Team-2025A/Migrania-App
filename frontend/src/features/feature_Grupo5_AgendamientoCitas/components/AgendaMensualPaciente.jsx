import React from "react";
import { obtenerCitasMensualesPaciente } from "../../../common/api/agendaMedica";
import AgendaMensualBase from "./AgendaMensualBase";
import { useNavigate } from "react-router-dom";

export default function AgendaMensualPaciente() {
  const navegar = useNavigate();

  return (
    <AgendaMensualBase
      obtenerCitas={obtenerCitasMensualesPaciente}
      titulo="Mis Citas"
      alCrearNuevaCita={() => navegar("/formulario-cita")}
    />
  );
}
