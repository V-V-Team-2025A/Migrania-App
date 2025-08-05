import { useState } from "react";
import styles from "../styles/ModalDisponibilidad.module.css";

export default function ModalDisponibilidad({ onClose }) {
    return (
        <div className={styles["modal__overlay"]}>
            <div className={styles["modal__contenedor"]}>
                <h2 className={styles["modal__titulo"]}>{puedeHacerAutoevaluacion ? "¡Tu autoevaluación MIDAS está disponible!" :
                    "Tu autoevaluación MIDAS aún no está disponible"}
                </h2>
                <p className={styles["modal__mensaje"]}>
                    {puedeHacerAutoevaluacion ? "Toma esta breve evaluación para descubrir tu grado de discapacidad." :
                        "Lo sentimos, pero esta es una autoevaluación trimestral. Vuelve el 23 de noviembre de 2025. "}
                </p>
                {
                    puedeHacerAutoevaluacion ? (
                        <button className="btn-primary" onClick={onClose}>
                            ¡Empezar!
                        </button>) :
                        (<button className="btn-primary" onClick={() => { navigate("/dashboard-paciente") }}>
                            ¡Entendido!
                        </button>)
                }
                <button className="btn-primary" onClick={() => { navigate("/midas/historial") }}>
                    Ver historial
                </button>
            </div>
        </div>
    );
}