import React from "react";
import ToggleAgendaView from "../components/ToggleAgendaView";
import { Outlet } from "react-router-dom";

const AgendaMedicaPage = () => {
  return (
    <div>
      <ToggleAgendaView basePath="/agenda" />
      <Outlet />
    </div>
  );
};

export default AgendaMedicaPage;
