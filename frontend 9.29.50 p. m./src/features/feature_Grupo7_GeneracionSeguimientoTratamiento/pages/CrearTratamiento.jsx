import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/crearTratamiento.css";

const recomendacionesHombre = [
    "Mantener una rutina regular de sueño",
    "Realizar ejercicio de forma moderada",
    "Controlar los niveles de estrés",
    "Mantener una hidratación adecuada",
    "Buscar un ambiente oscuro y silencioso para descansar durante el episodio",
    "Realizar una compresión fría o tibia sobre la zona afectada",
    "Evitar cualquier tipo de esfuerzo físico mientras dure el episodio",
    "Ingerir líquidos en pequeñas cantidades y evitar alimentos pesados"
];

const recomendacionesMujer = [
    ...recomendacionesHombre,
    "Utilizar analgésicos adecuados durante el periodo menstrual",
    "Consultar con un ginecólogo sobre anticonceptivos hormonales"
];

function CrearTratamiento({ genero = "hombre" }) {
    const navigate = useNavigate();
    const [tratamientos, setTratamientos] = useState([
        { cantidad: 1, medicamento: "", caracteristica: "", frecuencia: "", duracion: "" }
    ]);
    const [recomendacionesSeleccionadas, setRecomendacionesSeleccionadas] = useState([]);

    const recomendaciones = genero === "mujer" ? recomendacionesMujer : recomendacionesHombre;

    const handleAddFila = () => {
        setTratamientos([
            ...tratamientos,
            { cantidad: 1, medicamento: "", caracteristica: "", frecuencia: "", duracion: "" }
        ]);
    };

    const handleRemoveFila = (index) => {
        const nuevos = tratamientos.filter((_, i) => i !== index);
        setTratamientos(nuevos);
    };

    const handleInputChange = (index, field, value) => {
        const nuevos = [...tratamientos];
        nuevos[index][field] = value;
        setTratamientos(nuevos);
    };

    const handleToggleRecomendacion = (texto) => {
        setRecomendacionesSeleccionadas((prev) =>
            prev.includes(texto)
                ? prev.filter((r) => r !== texto)
                : [...prev, texto]
        );
    };

    return (
        <div className="crear-tratamiento-container">
            <header className="crear-tratamiento-header">
                <div className="crear-tratamiento-user-info">
                    <span className="crear-tratamiento-user-icon">👤</span>
                    <span className="crear-tratamiento-user-name">Dr. X</span>
                </div>
            </header>

            <div className="crear-tratamiento-patient-info">
                <h1>Paciente X – Crear Tratamiento</h1>
            </div>

            <div className="crear-tratamiento-tabla-container">
                <table className="crear-tratamiento-tabla">
                    <thead>
                        <tr>
                            <th>Cantidad</th>
                            <th>Medicamento</th>
                            <th>Característica</th>
                            <th>Frecuencia</th>
                            <th>Duración Tratamiento</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tratamientos.map((fila, index) => (
                            <tr key={index}>
                                <td>
                                    <input
                                        type="number"
                                        placeholder="1"
                                        min="1"
                                        value={fila.cantidad}
                                        onChange={(e) => handleInputChange(index, "cantidad", parseInt(e.target.value))}
                                    />
                                </td>
                                <td>
                                    <input
                                        type="text"
                                        placeholder="Ej: Analgésicos"
                                        value={fila.medicamento}
                                        onChange={(e) => handleInputChange(index, "medicamento", e.target.value)}
                                    />
                                </td>
                                <td>
                                    <input
                                        type="text"
                                        placeholder="Ej: 500mg"
                                        value={fila.caracteristica}
                                        onChange={(e) => handleInputChange(index, "caracteristica", e.target.value)}
                                    />
                                </td>
                                <td>
                                    <input
                                        type="text"
                                        placeholder="Ej: C/8h"
                                        value={fila.frecuencia}
                                        onChange={(e) => handleInputChange(index, "frecuencia", e.target.value)}
                                    />
                                </td>
                                <td>
                                    <input
                                        type="text"
                                        placeholder="Ej: 3 días"
                                        value={fila.duracion}
                                        onChange={(e) => handleInputChange(index, "duracion", e.target.value)}
                                    />
                                </td>
                                <td className="crear-tratamiento-botones">
                                    <button className="crear-tratamiento-add" onClick={handleAddFila}>+</button>
                                    {tratamientos.length > 1 && (
                                        <button className="crear-tratamiento-remove" onClick={() => handleRemoveFila(index)}>-</button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <div className="crear-tratamiento-recomendaciones">
                    <h3>Recomendaciones</h3>
                    <div className="crear-tratamiento-lista-recomendaciones">
                        {recomendaciones.map((texto, i) => (
                            <label key={i}>
                                <input
                                    type="checkbox"
                                    checked={recomendacionesSeleccionadas.includes(texto)}
                                    onChange={() => handleToggleRecomendacion(texto)}
                                />
                                {" "}{texto}
                            </label>
                        ))}
                    </div>
                </div>
            </div>

            <div className="crear-tratamiento-acciones">
                <button className="crear-tratamiento-enviar">Enviar tratamiento</button>
                <button className="crear-tratamiento-cancelar" onClick={() => navigate(-1)}>↩ Regresar</button>
            </div>
        </div>
    );
}

export default CrearTratamiento;
