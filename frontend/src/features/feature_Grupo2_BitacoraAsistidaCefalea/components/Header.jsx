
import React from 'react';
import { IoArrowBack, IoAdd, IoFilter, IoClose } from 'react-icons/io5';

export default function Header({ 
    title, 
    onBack, 
    primaryButtonText, 
    onPrimaryClick, 
    secondaryButtonText, 
    onSecondaryClick, 
    patientName 
}) {
    const displayTitle = patientName ? `${title} de ${patientName}` : title;

    const getPrimaryButtonIcon = () => {
        if (primaryButtonText?.includes('Nuevo episodio')) {
            return <IoAdd />;
        }
        if (primaryButtonText?.includes('Filtrar bitácora')) {
            return <IoFilter />;
        }
        return null;
    };

    const getSecondaryButtonIcon = () => {
        if (secondaryButtonText?.includes('Filtrar')) {
            return <IoFilter />;
        }
        if (secondaryButtonText?.includes('Limpiar')) {
            return <IoClose />;
        }
        return null;
    };

    return (
        <header>
            <button className='btn-back' onClick={onBack}>
                <IoArrowBack />
                Volver
            </button>
            <h1>{displayTitle}</h1>
            <div style={{ display: 'flex', gap: '10px' }}>
                {secondaryButtonText && (
                    <button 
                        className={secondaryButtonText?.includes('Limpiar') ? 'btn-secondary' : 'btn-filter'} 
                        onClick={onSecondaryClick}
                    >
                        {getSecondaryButtonIcon()}
                        {secondaryButtonText}
                    </button>
                )}
                {primaryButtonText && (
                    <button className='btn-primary' onClick={onPrimaryClick}>
                        {getPrimaryButtonIcon()}
                        {primaryButtonText}
                    </button>
                )}
            </div>
        </header>
    );
}
