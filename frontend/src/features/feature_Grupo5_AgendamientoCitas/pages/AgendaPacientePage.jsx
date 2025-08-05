import React from "react";
import ToggleAgendaView from "../components/ToggleAgendaView";
import { Outlet } from "react-router-dom";

const AgendaPacientePage = () => {
  return (
    <div>
      <ToggleAgendaView basePath="/agenda-paciente" />
      <Outlet />
    </div>
  );
};

export default AgendaPacientePage;
