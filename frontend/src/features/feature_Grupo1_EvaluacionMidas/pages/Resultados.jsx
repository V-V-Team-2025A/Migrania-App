import midasStyles from "../styles/Midas.module.css";
import styles from "../styles/Resultados.module.css";

function ResultadosRow({ pregunta, puntuacion }) {
    return (
        <div className={styles["resultados__resultado"]}>
            <span>{pregunta}</span>
            <span>{puntuacion}</span>
        </div>
    );
}

export default function Resultados() {
    return (
        <div className={midasStyles["midas__contenedor"]}>
            <div className={styles["resultados__tarjeta-resultados"]}>
                <div className={styles["resultados__seccion-superior"]}>
                    <h1>Resultados</h1>
                    <h4>Puntuación: 21</h4>
                    <p>
                        Sus dolores de cabeza causan una discapacidad moderada. Se recomienda evaluación médica y tratamiento especializado.
                    </p>
                </div>

                <div className={styles["resultados__seccion-inferior"]}>
                    <h3>Tus respuestas</h3>
                    <div className={styles["resultados__lista"]}>
                        <div>
                            <ResultadosRow
                                pregunta={"¿Cuántos días en los últimos 3 meses faltaste al trabajo o a la escuela debido a tus dolores de cabeza?"}
                                puntuacion={2}
                            />
                            <ResultadosRow
                                pregunta={"¿Cuántos días en los últimos 3 meses faltaste al trabajo o a la escuela debido a tus dolores de cabeza?"}
                                puntuacion={11}
                            />
                            <ResultadosRow
                                pregunta={"¿Cuántos días en los últimos 3 meses faltaste al trabajo o a la escuela debido a tus dolores de cabeza?"}
                                puntuacion={8}
                            />
                        </div>
                        <div>
                            <ResultadosRow
                                pregunta={"¿Cuántos días en los últimos 3 meses faltaste al trabajo o a la escuela debido a tus dolores de cabeza?"}
                                puntuacion={6}
                            />
                            <ResultadosRow
                                pregunta={"¿Cuántos días en los últimos 3 meses faltaste al trabajo o a la escuela debido a tus dolores de cabeza?"}
                                puntuacion={12}
                            />
                        </div>
                    </div>
                </div>

                <div className={styles["resultados__boton-inferior"]}>
                    <button className="btn-primary">¡Listo!</button>
                </div>
            </div>
        </div>
    );
}
