import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import TratamientoHeader from "../components/TratamientoHeader";
import "../styles/tratamientosHub.css";

function TratamientosHub() {
    const navigate = useNavigate();
    const [tratamientos, setTratamientos] = useState([]);
    const [userInfo, setUserInfo] = useState({
        doctorName: "Dr. X",
        patientName: "Juan Pérez"
    });

    useEffect(() => {
        // Aquí cargarías los datos reales de tratamientos
        setTratamientos([
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
        ]);
    }, []);

    const navegacionOpciones = [
        {
            title: "Primera Consulta",
            description: "Registrar primera consulta médica",
            path: "/primera-consulta",
            icon: "🩺",
            color: "#4CAF50"
        },
        {
            title: "Crear Tratamiento",
            description: "Generar nuevo plan de tratamiento",
            path: "/crear-tratamiento",
            icon: "➕",
            color: "#2196F3"
        },
        {
            title: "Historial de Tratamientos",
            description: "Ver todos los tratamientos anteriores",
            path: "/historial-tratamientos",
            icon: "📋",
            color: "#FF9800"
        },
        {
            title: "Seguimiento",
            description: "Monitorear progreso del tratamiento",
            path: "/seguimiento",
            icon: "📊",
            color: "#9C27B0"
        }
    ];

    const handleNavigation = (path) => {
        navigate(path);
    };

    const handleEditarTratamiento = (tratamientoId) => {
        navigate(`/editar-tratamiento/${tratamientoId}`);
    };

    const handleSuspenderTratamiento = (tratamientoId) => {
        navigate(`/suspender-tratamiento/${tratamientoId}`);
    };

    return (
        <div className="tratamientos-hub">
            <TratamientoHeader 
                title="Gestión de Tratamientos"
                showBackButton={true}
                customBackAction={() => navigate('/dashboard-paciente')}
                userName={userInfo.doctorName}
                patientName={userInfo.patientName}
            />

            <div className="tratamientos-hub__content">
                {/* Sección de acciones principales */}
                <section className="tratamientos-hub__actions">
                    <h2>Acciones Disponibles</h2>
                    <div className="actions-grid">
                        {navegacionOpciones.map((opcion, index) => (
                            <div 
                                key={index}
                                className="action-card"
                                onClick={() => handleNavigation(opcion.path)}
                                style={{ borderLeftColor: opcion.color }}
                            >
                                <div className="action-card__icon" style={{ color: opcion.color }}>
                                    {opcion.icon}
                                </div>
                                <div className="action-card__content">
                                    <h3>{opcion.title}</h3>
                                    <p>{opcion.description}</p>
                                </div>
                                <div className="action-card__arrow">→</div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Sección de tratamientos activos */}
                <section className="tratamientos-hub__current">
                    <h2>Tratamientos Actuales</h2>
                    {tratamientos.length > 0 ? (
                        <div className="tratamientos-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Episodio</th>
                                        <th>Medicamento</th>
                                        <th>Fecha Inicio</th>
                                        <th>Estado</th>
                                        <th>Cumplimiento</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {tratamientos.map((tratamiento) => (
                                        <tr key={tratamiento.id}>
                                            <td>#{tratamiento.episodio}</td>
                                            <td>{tratamiento.medicamento}</td>
                                            <td>{tratamiento.fecha}</td>
                                            <td>
                                                <span className={`estado ${tratamiento.estado.toLowerCase()}`}>
                                                    {tratamiento.estado}
                                                </span>
                                            </td>
                                            <td>{tratamiento.cumplimiento}</td>
                                            <td>
                                                <div className="acciones">
                                                    <button 
                                                        className="btn-editar"
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            handleEditarTratamiento(tratamiento.id);
                                                        }}
                                                    >
                                                        Editar
                                                    </button>
                                                    {tratamiento.estado === 'Activo' && (
                                                        <button 
                                                            className="btn-suspender"
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                handleSuspenderTratamiento(tratamiento.id);
                                                            }}
                                                        >
                                                            Suspender
                                                        </button>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <div className="no-tratamientos">
                            <p>No hay tratamientos registrados</p>
                            <button 
                                className="btn-primary"
                                onClick={() => handleNavigation('/primera-consulta')}
                            >
                                Iniciar Primera Consulta
                            </button>
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
}

export default TratamientosHub;
