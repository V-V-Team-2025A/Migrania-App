import styles from "../styles/Midas.module.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Midas() {
    const preguntasMock = [
        "¿Cuántos días en los últimos 3 meses faltaste al trabajo o a la escuela debido a tus dolores de cabeza?",
        "¿Cuántos días en los últimos 3 meses redujiste tu productividad a la mitad o menos en el trabajo o la escuela?",
        "¿Cuántos días no realizaste tareas del hogar debido a los dolores de cabeza?",
        "¿Cuántos días tuviste que reducir a la mitad o más tu rendimiento en tareas del hogar?",
        "¿Cuántos días evitaste actividades sociales o familiares por dolores de cabeza?"
    ];
    const navigate = useNavigate();
    const [indice, setIndice] = useState(0);
    const [respuestas, setRespuestas] = useState(Array(preguntasMock.length).fill(""));
    const [valorRespuesta, setValorRespuesta] = useState("");

    const responderPregunta = () => {
        const nuevasRespuestas = [...respuestas];
        nuevasRespuestas[indice] = valorRespuesta;
        setRespuestas(nuevasRespuestas);
        setValorRespuesta("");

        if (indice < preguntasMock.length - 1) {
            setIndice(indice + 1);
        } else {
            alert("Respuestas registradas: " + JSON.stringify(nuevasRespuestas));
        }
    };

    return (
        <div className={styles["midas__contenedor"]}>
            <h1>Autoevaluación MIDAS</h1>

            <div className={styles["midas__tarjeta-pregunta"]}>
                <h2>Pregunta {indice + 1}</h2>
                <p>{preguntasMock[indice]}</p>

                <p style={{ color: "var(--color-secondary-dark)" }}>Número de días</p>
                <input
                    type="number"
                    placeholder="Ej: 5"
                    min={0}
                    max={90}
                    value={valorRespuesta}
                    onChange={(e) => setValorRespuesta(e.target.value)}
                />

                <div className={styles["midas__contenedor-botones"]}>
                    <button
                        className="btn-secondary"
                        disabled={indice === 0}
                        onClick={() => {
                            const nuevaRespuesta = respuestas[indice - 1] || "";
                            setIndice(indice - 1);
                            setValorRespuesta(nuevaRespuesta);
                        }}
                    >
                        Regresar
                    </button>
                    {
                        indice < preguntasMock.length - 1 ? (
                            <button
                                className="btn-primary"
                                onClick={responderPregunta}
                                disabled={valorRespuesta === ""}
                            >
                                Siguiente
                            </button>
                        ) : (
                            <button
                                className="btn-primary"
                                onClick={() => {
                                    const nuevasRespuestas = [...respuestas];
                                    nuevasRespuestas[indice] = valorRespuesta;
                                    setRespuestas(nuevasRespuestas);

                                    navigate("/midas/resultados", {
                                        state: {
                                            respuestas: nuevasRespuestas
                                        }
                                    });
                                }}
                                disabled={valorRespuesta === ""}
                            >
                                Finalizar
                            </button>

                        )
                    }
                </div>
            </div>
        </div>
    );
}
