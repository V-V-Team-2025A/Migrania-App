import React from "react";
import { useNavigate } from "react-router-dom";
import AgendaSemanalBase from "./AgendaSemanalBase";
import ToggleAgendaView from "./ToggleAgendaView";
import { obtenerCitasSemanales } from "../../../common/api/agendaMedica";

export default function AgendaSemanalMedico() {
  const navegar = useNavigate();

  return (
    <AgendaSemanalBase
      obtenerCitas={obtenerCitasSemanales}
      titulo="Agenda Médica"
      alCrearNuevaCita={() => navegar("/formulario-cita")}
      renderToggle={() => <ToggleAgendaView />}
    />
  );
}
