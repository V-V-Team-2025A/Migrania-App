import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import TratamientoHeader from "../components/TratamientoHeader";
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
    const [mostrarModal, setMostrarModal] = useState(false);  // Estado para mostrar el modal

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

    const handleEnviarTratamiento = () => {
        setMostrarModal(true);  // Mostrar el modal cuando se envíe el tratamiento
    };

    const handleCerrarModal = () => {
        setMostrarModal(false);  // Cerrar el modal
        navigate("/home");  // Redirigir a la página anterior
    };

    return (
        <div className="crear-tratamiento-container">
            <TratamientoHeader 
                title="Crear Tratamiento"
                showBackButton={true}
                customBackAction={() => navigate('/tratamientos')}
                userName="Dr. X"
                patientName="Juan Pérez"
            />

            <div className="crear-tratamiento-table-container">
                <table className="crear-tratamiento-table">
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
                                    className="crear-tratamiento-input"
                                />
                            </td>
                            <td>
                                <input
                                    type="text"
                                    placeholder="Ej: Analgésicos"
                                    value={fila.medicamento}
                                    onChange={(e) => handleInputChange(index, "medicamento", e.target.value)}
                                    className="crear-tratamiento-input"
                                />
                            </td>
                            <td>
                                <input
                                    type="text"
                                    placeholder="Ej: 500mg"
                                    value={fila.caracteristica}
                                    onChange={(e) => handleInputChange(index, "caracteristica", e.target.value)}
                                    className="crear-tratamiento-input"
                                />
                            </td>
                            <td>
                                <input
                                    type="text"
                                    placeholder="Ej: C/8h"
                                    value={fila.frecuencia}
                                    onChange={(e) => handleInputChange(index, "frecuencia", e.target.value)}
                                    className="crear-tratamiento-input"
                                />
                            </td>
                            <td>
                                <input
                                    type="text"
                                    placeholder="Ej: 3 días"
                                    value={fila.duracion}
                                    onChange={(e) => handleInputChange(index, "duracion", e.target.value)}
                                    className="crear-tratamiento-input"
                                />
                            </td>
                            <td className="crear-tratamiento-acciones-botones">
                                <button className="crear-tratamiento-add-button" onClick={handleAddFila}>+</button>
                                {tratamientos.length > 1 && (
                                    <button className="crear-tratamiento-remove-button" onClick={() => handleRemoveFila(index)}>-</button>
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

            <div className="crear-tratamiento-actions">
                <button className="crear-tratamiento-create-button" onClick={handleEnviarTratamiento}>
                    Enviar tratamiento
                </button>
                <button className="crear-tratamiento-cancel-button" onClick={() => navigate(-1)}>Regresar</button>
            </div>

            {/* Modal para confirmación */}
            {mostrarModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>Tratamiento enviado</h2>
                        <button onClick={handleCerrarModal}>Aceptar</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CrearTratamiento;
