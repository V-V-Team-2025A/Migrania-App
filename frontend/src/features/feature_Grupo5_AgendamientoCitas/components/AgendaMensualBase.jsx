import React, { useState, useEffect } from "react";
import estilos from "../styles/AgendaMensual.module.css";
import comunes from "../styles/common.module.css";
import ToggleAgendaView from "./ToggleAgendaView";
import { generarMatrizMes } from "../../../common/utils/ayudantesFechas";
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

const diasSemana = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"];
const meses = [
  "Enero",
  "Febrero",
  "Marzo",
  "Abril",
  "Mayo",
  "Junio",
  "Julio",
  "Agosto",
  "Septiembre",
  "Octubre",
  "Noviembre",
  "Diciembre",
];

export default function AgendaMensualBase({
  obtenerCitas,
  titulo,
  alCrearNuevaCita,
}) {
  const hoy = new Date();
  const [anio, setAnio] = useState(hoy.getFullYear());
  const [mes, setMes] = useState(hoy.getMonth());
  const [filaInicio, setFilaInicio] = useState(0);
  const [citas, setCitas] = useState([]);

  useEffect(() => {
    obtenerCitas(anio, mes + 1).then((datos) => setCitas(datos.citas));
  }, [anio, mes, obtenerCitas]);

  const matriz = generarMatrizMes(anio, mes, citas);
  const filasVisibles = matriz;

  const manejarMesAnterior = () => {
    if (mes === 0) {
      setMes(11);
      setAnio(anio - 1);
    } else {
      setMes(mes - 1);
    }
    setFilaInicio(0);
  };

  const manejarMesSiguiente = () => {
    if (mes === 11) {
      setMes(0);
      setAnio(anio + 1);
    } else {
      setMes(mes + 1);
    }
    setFilaInicio(0);
  };

  const manejarScrollArriba = () => {
    if (filaInicio > 0) setFilaInicio(filaInicio - 1);
  };

  const manejarScrollAbajo = () => {
    if (filaInicio < matriz.length - 5) setFilaInicio(filaInicio + 1);
  };

  const manejarVolver = () => window.history.back();

  return (
    <div className={estilos.agendaContainer}>
      <div style={{ width: "100%", marginBottom: 24 }}>
        <ToggleAgendaView />
      </div>
      <header className={estilos.headerRow}>
        <div className={estilos.headerLeft}>
          <button
            className={comunes["btn-back"]}
            onClick={manejarVolver}
            aria-label="Volver"
          >
            ← Volver
          </button>
        </div>
        <div className={estilos.headerCenter}>
          <h1 className={comunes.title}>{titulo}</h1>
        </div>
        <div className={estilos.headerRight}>
          <button className={comunes["btn-primary"]} onClick={alCrearNuevaCita}>
            + Nueva Cita
          </button>
        </div>
      </header>

      <div className={estilos.controls}>
        <div className={estilos.monthNav}>
          <button className={estilos.navBtn} onClick={manejarMesAnterior}>
            ‹
          </button>
          <span className={estilos.monthLabel}>
            {meses[mes]} {anio}
          </span>
          <button className={estilos.navBtn} onClick={manejarMesSiguiente}>
            ›
          </button>
        </div>
      </div>

      <div className={estilos.calendarGridWrapper}>
        <div className={estilos.calendar}>
          <div className={estilos.calendarHeader}>
            {diasSemana.map((dia, idx) => (
              <div key={idx} className={estilos.headerDay}>
                {dia}
              </div>
            ))}
          </div>
          <div className={estilos.calendarBody}>
            {filasVisibles.map((semana, filaIdx) => (
              <div key={filaIdx} className={estilos.weekRow}>
                {semana.map((dia, colIdx) => (
                  <div
                    key={colIdx}
                    className={
                      estilos.dayCell +
                      (dia.tipo === "anterior" || dia.tipo === "siguiente"
                        ? " " + estilos.prevMonth
                        : "")
                    }
                  >
                    <div className={estilos.dayNumber}>{dia.numero}</div>
                    {dia.citas && dia.citas.length > 0 && (
                      <div className={estilos.citaInfo}>
                        {dia.citas.map((cita, i) => (
                          <div key={i}>
                            <div className={estilos.citaDoctor}>
                              <CalendarBlankIcon
                                size={32}
                                weight="fill"
                                color="#000"
                              />{" "}
                              {cita.doctor}
                            </div>
                            <div className={estilos.citaHora}>
                              <ClockIcon size={20} weight="fill" color="#000" />{" "}
                              {cita.hora}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
