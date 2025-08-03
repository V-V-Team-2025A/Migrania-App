import styles from "../../common/styles/dashboardPaciente.module.css";
import { BellIcon,StethoscopeIcon, ChartLineIcon, FilesIcon, PillIcon, PlusIcon } from "@phosphor-icons/react";

export default function Dashboard() {
    return (
        <>
            <div className={styles["dashboard__cabecera"]}>
                <div>
                    <h2>¿Cómo te sientes hoy?</h2>
                    <p>¡Vas 5 días sin episodios! Sigue cuidándote y registrando tus síntomas.</p>
                </div>
                <BellIcon size={32} color={"var(--color-text)"} />
            </div>
            <section className={styles["dashboard__contenedor-tarjetas"]}>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#c42d3750",
                        }}>
                        <PlusIcon size={32} color={"#c9525aff"} />
                    </div>
                    <h4>Registrar episodio</h4>
                    <p>Documenta un nuevo episodio de migraña.</p>
                </div>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#9f58dd59",
                        }}>
                        <FilesIcon size={32} color={"#a555ebff"} />
                    </div>
                    <h4>Evaluación MIDAS</h4>
                    <p>Evalúa el impacto de la migraña en tu vida diaria.</p>
                </div>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#3e68be50",
                        }}>
                        <PillIcon size={32} color={"#4c84f3ff"} />
                    </div>
                    <h4>Mis tratamientos</h4>
                    <p>Revisa tus tratamientos actuales.</p>
                </div>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#3588517d",
                        }}>
                        <ChartLineIcon size={32} color={"#42b668ff"} />
                    </div>
                    <h4>Mi progreso</h4>
                    <p>Visualiza tendencias y estadísticas.</p>
                </div>
            </section>

            <div className={styles["dashboard__seccion-inferior"]}>
                <section className={styles["dashboard__episodios-recientes"]}>
                    <h4>Episodios recientes</h4>

                </section>

                <section className={styles["dashboard__mi-medico"]}>
                    <h4>Mi médico</h4>

                    <div className={styles["dashboard__medico-info"]}>
                        <StethoscopeIcon size={64} />
                        <h4>Dr. Juan Pérez</h4>
                        <p>Especialista en Neurología</p>
                    </div>

                    <div>
                        <h4>Próxima cita:</h4>
                        <div style={{color: "var(--color-secondary-dark)"}}>2025-10-22 - 10:00 AM</div>
                    </div>

                    <div>
                        <h4>Tratamiento actual:</h4>
                        <div style={{color: "var(--color-secondary-dark)"}}>Propranolol 40mg</div>
                    </div>

                    <button className="btn-primary">Agendar</button>
                </section>
            </div>

        </>
    );
}