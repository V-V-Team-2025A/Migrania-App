import React, { useState } from "react";
import estilos from "../styles/FormularioCita.module.css";
import comunes from "../styles/common.module.css";
import { crearCitaPaciente } from "../../../common/api/citasPaciente";
import { useNavigate } from "react-router-dom";

export default function FormularioCita() {
  const navegar = useNavigate();
  const [medico, setMedico] = useState("");
  const [fecha, setFecha] = useState("");
  const [hora, setHora] = useState("");
  const [observaciones, setObservaciones] = useState("");
  const [cargando, setCargando] = useState(false);

  const medicos = ["Dr. Juan Pérez", "Dra. Ana López", "Dr. Carlos Ruiz"];
  const horas = [
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
  ];

  const manejarVolver = () => navegar(-1);

  const manejarEnvio = async (e) => {
    e.preventDefault();
    setCargando(true);
    await crearCitaPaciente({ medico, fecha, hora, observaciones });
    setCargando(false);
    navegar("/agenda-paciente/semana");
  };

  const manejarCancelar = () => navegar("/agenda-paciente/semana");

  return (
    <div className={estilos.formularioWrapper}>
      <div className={estilos.formularioContainer}>
        <div className={estilos.headerRow}>
          <button
            className={comunes["btn-back"]}
            onClick={manejarVolver}
            aria-label="Volver"
          >
            ← Volver
          </button>
          <h1 className={estilos.mainTitle}>Citas Médicas</h1>
          <div style={{ width: 80 }} />
        </div>
        <form className={estilos.formBox} onSubmit={manejarEnvio}>
          <div className={estilos.formTitle}>Agendar Nueva Cita</div>
          <div className={estilos.formRow}>
            <div className={estilos.formColFull}>
              <label className={estilos.label}>Médico:</label>
              <select
                className={estilos.input}
                value={medico}
                onChange={(e) => setMedico(e.target.value)}
                required
              >
                <option value="">Seleccione un médico</option>
                {medicos.map((m) => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className={estilos.formRow}>
            <div className={estilos.formColHalf}>
              <label className={estilos.label}>Fecha:</label>
              <input
                className={estilos.input}
                type="date"
                value={fecha}
                onChange={(e) => setFecha(e.target.value)}
                required
              />
            </div>
            <div className={estilos.formColHalf}>
              <label className={estilos.label}>Hora:</label>
              <select
                className={estilos.input}
                value={hora}
                onChange={(e) => setHora(e.target.value)}
                required
              >
                <option value="">Seleccione una hora</option>
                {horas.map((h) => (
                  <option key={h} value={h}>
                    {h}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className={estilos.formRow}>
            <div className={estilos.formColFull}>
              <label className={estilos.label}>Observaciones:</label>
              <textarea
                className={estilos.textarea}
                value={observaciones}
                onChange={(e) => setObservaciones(e.target.value)}
                rows={3}
              />
            </div>
          </div>
          <div className={estilos.formButtons}>
            <button
              type="submit"
              className={estilos.btnAgendar}
              disabled={cargando}
            >
              {cargando ? "Guardando..." : "Agendar"}
            </button>
            <button
              type="button"
              className={estilos.btnCancelar}
              onClick={manejarCancelar}
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
