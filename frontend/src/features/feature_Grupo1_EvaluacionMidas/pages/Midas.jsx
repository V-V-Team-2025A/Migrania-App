import styles from "../styles/Midas.module.css";

export default function Midas() {
    return (
        <div className={styles["midas__contenedor"]}>
            <h1>Autoevaluación MIDAS</h1>

            <div className={styles["midas__tarjeta-pregunta"]}>
                <h2>Ausencias Laborales/Escolares</h2>
                <p>
                    ¿Cuántos días en los últimos 3 meses faltaste al trabajo o a la escuela
                    debido a tus dolores de cabeza?
                </p>
                <p style={{ color: "var(--color-secondary-dark)" }}>Número de días</p>
                <input type="text" placeholder="Ej: 5" />

                <div className={styles["midas__contenedor-botones"]}>
                    <button disabled className="btn-secondary">Regresar</button>
                    <a href="/midas/resultados">
                        <button className="btn-primary">Siguiente</button>
                    </a>
                </div>
            </div>
        </div>
    );
}
