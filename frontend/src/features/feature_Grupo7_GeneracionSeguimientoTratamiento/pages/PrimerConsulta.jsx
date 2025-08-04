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

    const handleCancel = () => setIsModalVisible(true);
    const handleCloseModal = () => setIsModalVisible(false);
    const handleNavigateHistorial = () => navigate("/historial");
    const handleNavigateCrearTratamiento = () => navigate("/primerConsulta/crearTratamiento");

    const hasOneEpisode = episodeData.length === 1;

    return (
        <div className="primerConsulta__container">
            <header className="primerConsulta__header">
                <div className="primerConsulta__user-info">
                    <span className="primerConsulta__user-icon">👤</span>
                    <span className="primerConsulta__user-name">{doctorName}</span>
                </div>
            </header>

            {hasOneEpisode && (
                <>
                    <div className="primerConsulta__patient-info">
                        <h1>{patientName} - Primer Consulta</h1>
                        <button className="primerConsulta__history-button" onClick={handleNavigateHistorial}>
                            Historial
                        </button>
                    </div>

                    <div className="primerConsulta__table-container">
                        <table className="primerConsulta__table">
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

                    <div className="primerConsulta__actions">
                        <button className="primerConsulta__crear" onClick={handleNavigateCrearTratamiento}>
                            Crear tratamiento
                        </button>
                        <button className="primerConsulta__cancelar" onClick={handleCancel}>
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
