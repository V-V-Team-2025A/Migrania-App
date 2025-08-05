import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/seguimiento.css";
import ConfirmacionCancelar from "@/features/feature_Grupo7_GeneracionSeguimientoTratamiento/components/ConfirmacionCancelar.jsx";

function Seguimiento() {
    const navigate = useNavigate();
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [doctorName, setDoctorName] = useState("");
    const [patientName, setPatientName] = useState("Paciente X");
    const [episodeData, setEpisodeData] = useState([]);

    useEffect(() => {
        setDoctorName("Dr. X");
        setPatientName("Juan Pérez");
        setEpisodeData([
            { num: 1, tipo: "Migraña", fecha: "10/08/2025", tratamiento: "Activo" },
            { num: 2, tipo: "Cefalea tensional", fecha: "12/08/2025", tratamiento: "S/T" },
        ]);
    }, []);

    const handleCancel = () => setIsModalVisible(true);
    const handleCloseModal = () => setIsModalVisible(false);

    const handleNavigateHistorial = () => navigate("/bitacora-medico/:pacienteId");
    const handleNavigateCrearTratamiento = () => navigate("/seguimiento/crearTratamiento");
    const handleNavigateTratamientos = () => navigate("/seguimiento/tratamientos");

    return (
        <div className="seguimiento">
            <header>
                <div className="user-info">
                    <span className="user-icon">👤</span>
                    <span className="user-name">{doctorName}</span>
                </div>
            </header>

            <div className="seguimiento__patient-info">
                <h1>{patientName} - Seguimiento</h1>
                <button className="seguimiento__history-button" onClick={handleNavigateHistorial}>Historial</button>
                <button className="seguimiento__tratamiento-button" onClick={handleNavigateTratamientos}>Tratamiento</button>
            </div>

            <div className="seguimiento__table-container">
                <table>
                    <thead>
                    <tr>
                        <th>Num. Episodio</th>
                        <th>Tipo Episodio</th>
                        <th>Fecha</th>
                        <th>Tratamiento</th>
                    </tr>
                    </thead>
                    <tbody>
                    {episodeData.map((episode) => (
                        <tr key={episode.num}>
                            <td>{episode.num}</td>
                            <td>{episode.tipo}</td>
                            <td>{episode.fecha}</td>
                            <td>{episode.tratamiento}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>

            <div className="seguimiento__actions">
                <button className="seguimiento__create-treatment" onClick={handleNavigateCrearTratamiento}>Crear tratamiento</button>
                <button className="seguimiento__cancel" onClick={handleCancel}>Cancelar</button>
            </div>

            {isModalVisible && <ConfirmacionCancelar onClose={handleCloseModal} />}
        </div>
    );
}

export default Seguimiento;