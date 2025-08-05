import React from "react";
import { useNavigate } from "react-router-dom";
import TratamientoHeader from "../components/TratamientoHeader";
import "../styles/tratamientos.css";

function Tratamientos() {
    const navigate = useNavigate();

    const tratamientos = [
        {
            id: 1,
            episodio: 2,
            fecha: "03/08/2025",
            estado: "Activo",
            cumplimiento: "75%",
            medicamento: "Propranolol 40mg"
        },
        {
            id: 2,
            episodio: 1,
            fecha: "01/08/2025",
            estado: "Finalizado",
            cumplimiento: "90%",
            medicamento: "Sumatriptán 50mg"
        },
    ];

    return (
        <div className="tratamientos">
            <TratamientoHeader 
                title="Gestión de Tratamientos"
                showBackButton={true}
                customBackAction={() => navigate('/dashboard-paciente')}
                userName="Dr. X"
                patientName="Juan Pérez"
            />

            <div className="patient-info">
                <button
                    className="history-button"
                    onClick={() => navigate("/historial-tratamientos")}
                >
                    Historial
                </button>
            </div>

            <div className="table-container-PC">
                <table>
                    <thead>
                    <tr>
                        <th># Tratamiento</th>
                        <th>Episodio</th>
                        <th>Fecha</th>
                        <th>Estado</th>
                        <th>% Cumplimiento</th>
                        <th>Acciones</th>
                    </tr>
                    </thead>
                    <tbody>
                    {tratamientos.map((t) => (
                        <tr key={t.id}>
                            <td>{t.id}</td>
                            <td>{t.episodio}</td>
                            <td>{t.fecha}</td>
                            <td>{t.estado}</td>
                            <td>{t.cumplimiento}</td>
                            <td className="acciones">
                                <button
                                    className="edit-button"
                                    onClick={() => navigate("/seguimiento/tratamientos/crearTratamiento/editarTratamiento")}
                                >
                                    Editar
                                </button>
                                <button
                                    className="delete-button"
                                    onClick={() => navigate("/seguimiento/tratamientos/crearTratamiento/suspenderTratamiento")}
                                >
                                    Suspender
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>

            <div className="actions">
                <button
                    className="create-treatment"
                    onClick={() => navigate("/seguimiento/tratamientos/crearTratamiento")}
                >
                    Nuevo tratamiento
                </button>
                <button className="cancel" onClick={() => navigate(-1)}>
                    Cancelar
                </button>
            </div>
        </div>
    );
}

export default Tratamientos;
