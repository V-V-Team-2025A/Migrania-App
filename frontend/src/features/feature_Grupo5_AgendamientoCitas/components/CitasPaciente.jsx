import React, { useEffect, useState } from "react";
import estilos from "../styles/CitasPaciente.module.css";
import comunes from "../styles/common.module.css";
import { useNavigate } from "react-router-dom";
import { getCitasPaciente } from "../../../common/api/citasPaciente";
import {
  Users,
  Stethoscope,
  Warning,
  Clock,
  Calendar,
  UserCircle,
  Siren,
  FirstAidIcon,
  CalendarBlankIcon,
  ClockAfternoonIcon,
  ClockIcon,
  CalendarIcon,
} from "@phosphor-icons/react";

const meses = [
  "ENE",
  "FEB",
  "MAR",
  "ABR",
  "MAY",
  "JUN",
  "JUL",
  "AGO",
  "SEP",
  "OCT",
  "NOV",
  "DIC",
];

function formatearFecha(fechaStr) {
  const [a, m, d] = fechaStr.split("-").map(Number);
  const date = new Date(a, m - 1, d);
  return {
    dia: String(date.getDate()).padStart(2, "0"),
    mes: meses[date.getMonth()],
    anio: date.getFullYear(),
  };
}

const CitasPaciente = () => {
  const navegar = useNavigate();
  const [citas, setCitas] = useState([]);
  const [citasHistorial, setCitasHistorial] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCitasPaciente().then((data) => {
      setCitas(data.proximas || []);
      setCitasHistorial(data.historial || []);
      setLoading(false);
    });
  }, []);

  const manejarNuevaCita = () => navegar("/formulario-cita");
  const manejarEditarCita = (cita) => navegar("/formulario-cita");
  const manejarVolver = () => navegar(-1);

  if (loading) {
    return <div className={estilos.citasContainer}>Cargando...</div>;
  }

  return (
    <div className={estilos.citasContainer}>
      <header className={comunes.header}>
        <button
          className={comunes["btn-back"]}
          onClick={manejarVolver}
          aria-label="Volver"
        >
          ← Volver
        </button>
        <h1 className={comunes.title}>Citas Médicas</h1>
        <button className={comunes["btn-primary"]} onClick={manejarNuevaCita}>
          + Nueva Cita
        </button>
      </header>

      <div className={estilos.citasBox}>
        <h2>Próximas Citas</h2>
        {citas.length === 0 ? (
          <div>No tienes citas próximas.</div>
        ) : (
          citas.map((cita) => {
            const { dia, mes } = formatearFecha(cita.fecha);
            return (
              <div key={cita.id} className={estilos.citaCard}>
                <div className={estilos.citaFecha}>
                  <div className={estilos.citaDia}>{dia}</div>
                  <div className={estilos.citaMes}>{mes}</div>
                </div>
                <div className={estilos.citaInfo}>
                  <div className={estilos.citaDoctor}>{cita.doctor}</div>
                  <div className={estilos.citaDetalles}>
                    <span>
                      <CalendarBlankIcon size={20} weight="fill" color="#fff" />{" "}
                      {cita.fecha}
                    </span>
                    <span>
                      <ClockIcon size={20} weight="fill" color="#fff" />{" "}
                      {cita.hora}
                    </span>
                  </div>
                </div>
                <div className={estilos.citaAcciones}>
                  <button
                    className={comunes["btn-primary"]}
                    onClick={() => manejarEditarCita(cita)}
                  >
                    Editar
                  </button>
                  <button className={comunes["btn-cancel"]}>Cancelar</button>
                </div>
              </div>
            );
          })
        )}
      </div>

      <div className={estilos.citasBox}>
        <h2>Historial de Citas</h2>
        {citasHistorial.length === 0 ? (
          <div>No tienes historial de citas.</div>
        ) : (
          citasHistorial.map((cita) => {
            const { dia, mes } = formatearFecha(cita.fecha);
            return (
              <div key={cita.id} className={estilos.citaCardHistorial}>
                <div className={estilos.citaFecha}>
                  <div className={estilos.citaDia}>{dia}</div>
                  <div className={estilos.citaMes}>{mes}</div>
                </div>
                <div className={estilos.citaInfo}>
                  <div className={estilos.citaDoctor}>{cita.doctor}</div>
                  <div className={estilos.citaDetalles}>
                    <span>
                      <CalendarBlankIcon size={20} weight="fill" color="#fff" />{" "}
                      {cita.fecha}
                    </span>
                    <span>
                      <ClockIcon size={20} weight="fill" color="#fff" />{" "}
                      {cita.hora}
                    </span>
                  </div>
                </div>
                <div className={estilos.citaEstado}>{cita.estado}</div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default CitasPaciente;
