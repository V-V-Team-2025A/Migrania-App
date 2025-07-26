import React from 'react';
import { IoArrowBack } from 'react-icons/io5';

export default function Header({ title, onBack, primaryButtonText, onPrimaryClick, patientName }) {
    const displayTitle = patientName ? `${title} de ${patientName}` : title;

    return (
        <header>
            <button className='btn-back' onClick={onBack}>
                <IoArrowBack />
                Volver
            </button>
            <h1>{displayTitle}</h1>
            {primaryButtonText && (
                <button className='btn-primary' onClick={onPrimaryClick}>
                    {primaryButtonText}
                </button>
            )}
        </header>
    );
}
