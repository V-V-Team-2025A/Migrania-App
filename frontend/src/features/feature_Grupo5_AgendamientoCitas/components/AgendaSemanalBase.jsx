import React, { useState, useEffect } from "react";
import estilos from "../styles/AgendaSemanal.module.css";
import comunes from "../styles/common.module.css";
import { obtenerFechasSemana } from "../../../common/utils/ayudantesFechas";
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
} from "@phosphor-icons/react";

const diasSemana = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"];

export default function AgendaSemanalBase({
  obtenerCitas,
  titulo,
  alCrearNuevaCita,
  renderToggle,
}) {
  const hoy = new Date();
  const [fechaActual, setFechaActual] = useState(hoy);
  const [citas, setCitas] = useState([]);

  useEffect(() => {
    const fechasSemana = obtenerFechasSemana(fechaActual);
    const lunes = fechasSemana[0];
    obtenerCitas(
      lunes.getFullYear(),
      lunes.getMonth() + 1,
      lunes.getDate()
    ).then((datos) => setCitas(datos.citas));
  }, [fechaActual, obtenerCitas]);

  const fechasSemana = obtenerFechasSemana(fechaActual);

  const manejarSemanaAnterior = () => {
    const anterior = new Date(fechaActual);
    anterior.setDate(fechaActual.getDate() - 7);
    setFechaActual(anterior);
  };

  const manejarSemanaSiguiente = () => {
    const siguiente = new Date(fechaActual);
    siguiente.setDate(fechaActual.getDate() + 7);
    setFechaActual(siguiente);
  };

  const manejarVolver = () => window.history.back();

  const inicio = fechasSemana[0];
  const fin = fechasSemana[6];
  const formatoFecha = (fecha) =>
    fecha
      .toLocaleDateString("es-ES", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      })
      .replace(".", "");

  return (
    <div className={estilos.agendaContainer}>
      <header className={estilos.headerRow}>
        <div className={estilos.toggleWrapper}>
          {renderToggle && renderToggle()}
        </div>
        <h1 className={estilos.title}>{titulo}</h1>
      </header>

      <div className={estilos.controls}>
        <div className={estilos.weekNav}>
          <button className={estilos.navBtn} onClick={manejarSemanaAnterior}>
            ‹
          </button>
          <span className={estilos.weekLabel}>
            {formatoFecha(inicio)} - {formatoFecha(fin)}
          </span>
          <button className={estilos.navBtn} onClick={manejarSemanaSiguiente}>
            ›
          </button>
        </div>
      </div>

      <div className={estilos.calendar}>
        <div className={estilos.calendarHeader}>
          {diasSemana.map((dia, idx) => (
            <div key={idx} className={estilos.headerDay}>
              {dia}
            </div>
          ))}
        </div>
        <div className={estilos.calendarBody}>
          <div className={estilos.weekRow}>
            {fechasSemana.map((fecha, idx) => {
              const fechaStr = `${fecha.getFullYear()}-${String(
                fecha.getMonth() + 1
              ).padStart(2, "0")}-${String(fecha.getDate()).padStart(2, "0")}`;
              const citasDia = citas.filter((c) => c.fecha === fechaStr);
              return (
                <div key={idx} className={estilos.dayCell}>
                  <div className={estilos.dayNumber}>{fecha.getDate()}</div>
                  {citasDia.length > 0 && (
                    <div className={estilos.citaInfo}>
                      {citasDia.map((cita, i) => (
                        <div key={i}>
                          <div className={estilos.citaDoctor}>
                            <CalendarBlankIcon
                              size={16}
                              weight="fill"
                              color="#000"
                            />{" "}
                            {cita.doctor}
                          </div>
                          <div className={estilos.citaHora}>
                            <ClockIcon size={16} weight="fill" color="#000" />{" "}
                            {cita.hora}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
