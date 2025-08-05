import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/PrimerConsulta.css";
import ConfirmacionCancelar from "../components/ConfirmacionCancelar";

function PrimerConsulta() {
    const navigate = useNavigate();
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [doctorName, setDoctorName] = useState("");
    const [patientName, setPatientName] = useState("Paciente X");
    const [episodeData, setEpisodeData] = useState([]);

    useEffect(() => {
        setDoctorName("Dr. X");
        setPatientName("Juan Pérez");
        setEpisodeData([
            { num: 1, tipo: "Migraña", fecha: "10/08/2025" }
        ]);
    }, []);

    const handleCancel = () => {
        setIsModalVisible(true);
    };

    const handleCloseModal = () => {
        setIsModalVisible(false);
    };

    const handleNavigateHistorial = () => navigate("/bitacora-medico/:pacienteId");

    const handleNavigateCrearTratamiento = () => {
        navigate("/primerConsulta/crearTratamiento");
    };

    const hasOneEpisode = episodeData.length === 1;

    return (
        <div className="primer-consulta-container">
            <header>
                <div className="primer-consulta-user-info">
                    <span className="user-icon">👤</span>
                    <span className="user-name">{doctorName}</span>
                </div>
            </header>

            {hasOneEpisode && (
                <>
                    <div className="primer-consulta-patient-info">
                        <h1>{patientName} - Primer Consulta</h1>
                        <button className="primer-consulta-history-button" onClick={handleNavigateHistorial}>
                            Historial
                        </button>
                    </div>

                    <div className="primer-consulta-table-container">
                        <table className="primer-consulta-table">
                            <thead>
                            <tr>
                                <th>Num. Episodio</th>
                                <th>Tipo Episodio</th>
                                <th>Fecha</th>
                            </tr>
                            </thead>
                            <tbody>
                            {episodeData.map((episode) => (
                                <tr key={episode.num}>
                                    <td>{episode.num}</td>
                                    <td>{episode.tipo}</td>
                                    <td>{episode.fecha}</td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>

                    <div className="primer-consulta-actions">
                        <button className="primer-consulta-action-button-create-treatment" onClick={handleNavigateCrearTratamiento}>
                            Crear tratamiento
                        </button>
                        <button className="primer-consulta-action-button-cancel" onClick={handleCancel}>
                            Cancelar
                        </button>
                    </div>
                </>
            )}
            {isModalVisible && <ConfirmacionCancelar onClose={handleCloseModal} />}
        </div>
    );
}

export default PrimerConsulta;
