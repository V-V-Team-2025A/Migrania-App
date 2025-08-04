import styles from "../styles/Midas.module.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ModalDisponibilidad from "../components/ModalDisponibilidad";
import { useLocation } from "react-router-dom";

export default function Midas() {

    const navigate = useNavigate();
    const [indice, setIndice] = useState(0);
    const [preguntas, setPreguntas] = useState([]);
    const [respuestas, setRespuestas] = useState([]);
    const [valorRespuesta, setValorRespuesta] = useState("");
    const [mostrarModal, setMostrarModal] = useState(true);
    const [loading, setLoading] = useState(true);

    const token = localStorage.getItem("access");
    const location = useLocation();
    const idAutoevaluacion = location.state?.idAutoevaluacion;
    useEffect(() => {
        const fetchPreguntas = async () => {
            try {
                setLoading(true);
                const response = await fetch('http://localhost:8000/api/evaluaciones/preguntas/', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                });

                const data = await response.json();

                const preguntasOrdenadas = data.results
                    .sort((a, b) => a.orden_pregunta - b.orden_pregunta)
                    .map(p => ({
                        id: p.id, 
                        enunciado: p.enunciado_pregunta
                    }));


                setPreguntas(preguntasOrdenadas);
                setRespuestas(Array(preguntasOrdenadas.length).fill(""));
            } catch (error) {
                console.error('Error al obtener preguntas:', error);
            } finally {
                setLoading(false);
            }
        };
        console.log(idAutoevaluacion)
        fetchPreguntas();
        setMostrarModal(true);
    }, []);

    const enviarRespuesta = async (idPregunta, valor) => {
        try {
            console.log(idPregunta, "fsdhuyhbjfwb ")
            await fetch("http://localhost:8000/api/evaluaciones/respuestas/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    autoevaluacion: idAutoevaluacion,
                    pregunta: idPregunta,
                    valor_respuesta: valor,
                })
            });
        } catch (error) {
            console.error("Error al enviar respuesta:", error);
        }
    };

    const responderPregunta = async () => {
        const nuevasRespuestas = [...respuestas];
        nuevasRespuestas[indice] = valorRespuesta;
        setRespuestas(nuevasRespuestas);

        // Enviar la respuesta actual al backend
        const preguntaActual = preguntas[indice];
        await enviarRespuesta(preguntaActual.id, valorRespuesta);

        setValorRespuesta("");

        if (indice < preguntas.length - 1) {
            setIndice(indice + 1);
        } else {
            alert("Respuestas registradas: " + JSON.stringify(nuevasRespuestas));
        }
    };

    const finalizarEvaluacion = async () => {
        const nuevasRespuestas = [...respuestas];
        nuevasRespuestas[indice] = valorRespuesta;
        setRespuestas(nuevasRespuestas);

        const preguntaActual = preguntas[indice];
        await enviarRespuesta(preguntaActual.id, valorRespuesta);

        navigate("/midas/resultados", {
            state: {
                respuestas: nuevasRespuestas,
                preguntas: preguntas.map(p => p.enunciado)
            }
        });
    };

    return (
        <div className={styles["midas__contenedor"]}>
            {mostrarModal && <ModalDisponibilidad onClose={() => setMostrarModal(false)} />}
            <h1>Autoevaluación MIDAS</h1>
            {loading ? (
                <p>Cargando preguntas...</p>
            ) : (
                <div className={styles["midas__tarjeta-pregunta"]}>
                    <h2>Pregunta {indice + 1}</h2>
                    <p>{preguntas[indice]?.enunciado}</p>

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
                        {indice < preguntas.length - 1 ? (
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
                                onClick={finalizarEvaluacion}
                                disabled={valorRespuesta === ""}
                            >
                                Finalizar
                            </button>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
