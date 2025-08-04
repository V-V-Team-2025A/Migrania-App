import React from "react";
import { obtenerCitasSemanalesPaciente } from "../../../common/api/agendaMedica";
import AgendaSemanalBase from "./AgendaSemanalBase";
import { useNavigate } from "react-router-dom";

export default function AgendaSemanalPaciente() {
  const navegar = useNavigate();

  return (
    <AgendaSemanalBase
      obtenerCitas={obtenerCitasSemanalesPaciente}
      titulo="Mis Citas"
      alCrearNuevaCita={() => navegar("/formulario-cita")}
    />
  );
}
