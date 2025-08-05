import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import styles from "../styles/AgendaMedicaToggle.module.css";

export default function ToggleAgendaView() {
  const navigate = useNavigate();
  const location = useLocation();
  const isSemana = location.pathname.endsWith("/semana");
  const isMes = location.pathname.endsWith("/mes");

  return (
    <div className={styles.toggleContainer}>
      <button
        className={`${styles.toggleBtn} ${isSemana ? styles.active : ""}`}
        onClick={() => navigate("/agenda/semana")}
      >
        Día
      </button>
      <button
        className={`${styles.toggleBtn} ${isMes ? styles.active : ""}`}
        onClick={() => navigate("/agenda/mes")}
      >
        Mes
      </button>
    </div>
  );
}
