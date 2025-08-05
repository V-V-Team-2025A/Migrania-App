import DashboardMedico from "../components/DashboardMedico";
import { getDashboardMedico } from "../../../common/api/dashboardMedico";

const dashinfo = getDashboardMedico()

console.log(getDashboardMedico)
const DashboardMedicoPage = () => <DashboardMedico
    estadisticas={dashinfo.estadisticas}
    alertasRecientes={dashinfo.alertasRecientes}
    citasProximas={dashinfo.citasProximas} />;

export default DashboardMedicoPage;
