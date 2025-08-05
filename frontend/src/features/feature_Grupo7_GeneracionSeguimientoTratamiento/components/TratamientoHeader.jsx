import React from 'react';
import { useNavigate } from 'react-router-dom';
import { IoArrowBack, IoHome } from 'react-icons/io5';
import '../styles/tratamientoHeader.css';

export default function TratamientoHeader({ 
    title, 
    showBackButton = true, 
    customBackAction = null,
    showHomeButton = false,
    userName = "Dr. X",
    patientName = null 
}) {
    const navigate = useNavigate();

    const handleBack = () => {
        if (customBackAction) {
            customBackAction();
        } else {
            navigate(-1);
        }
    };

    const handleHome = () => {
        navigate('/tratamientos');
    };

    const handleDashboard = () => {
        navigate('/dashboard-paciente');
    };

    return (
        <header className="tratamiento-header">
            <div className="tratamiento-header__navigation">
                {showBackButton && (
                    <button 
                        className="tratamiento-header__back-btn"
                        onClick={handleBack}
                        title="Volver"
                    >
                        <IoArrowBack size={20} />
                        Volver
                    </button>
                )}
                
                {showHomeButton && (
                    <button 
                        className="tratamiento-header__home-btn"
                        onClick={handleHome}
                        title="Ir a Tratamientos"
                    >
                        <IoHome size={20} />
                        Tratamientos
                    </button>
                )}
            </div>

            <div className="tratamiento-header__title">
                <h1>{title}</h1>
                {patientName && (
                    <p className="tratamiento-header__patient">Paciente: {patientName}</p>
                )}
            </div>

            <div className="tratamiento-header__user">
                <div className="user-info">
                    <span className="user-icon">👤</span>
                    <span className="user-name">{userName}</span>
                </div>
                <button 
                    className="tratamiento-header__dashboard-btn"
                    onClick={handleDashboard}
                    title="Ir al Dashboard"
                >
                    Dashboard
                </button>
            </div>
        </header>
    );
}
