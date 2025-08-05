import React from "react";
import { obtenerCitasMensuales } from "../../../common/api/agendaMedica";
import AgendaMensualBase from "./AgendaMensualBase";
import { useNavigate } from "react-router-dom";

export default function AgendaMensualMedico() {
  const navegar = useNavigate();

  return (
    <AgendaMensualBase
      obtenerCitas={obtenerCitasMensuales}
      titulo="Agenda Médica"
      alCrearNuevaCita={() => navegar("/formulario-cita")}
    />
  );
}
