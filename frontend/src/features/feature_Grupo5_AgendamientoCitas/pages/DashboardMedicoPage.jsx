import React, { useEffect, useState } from "react";
import DashboardMedico from "../components/DashboardMedico";
import { getDashboardMedico } from "../../../common/api/dashboardMedico";

const DashboardMedicoPage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    getDashboardMedico().then(setData);
  }, []);

  if (!data) return <div>Cargando...</div>;

  return (
    <DashboardMedico
      estadisticas={data.estadisticas}
      alertasRecientes={data.alertasRecientes}
      citasProximas={data.citasProximas}
    />
  );
};

export default DashboardMedicoPage;
