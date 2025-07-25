import React from 'react';
import { IoArrowBack } from 'react-icons/io5';

export default function Header({ title, onBack, primaryButtonText, onPrimaryClick }) {
    return (
        <header>
            <button className='btn-back' onClick={onBack}>
                <IoArrowBack />
                Volver
            </button>
            <h1>{title}</h1>
            {primaryButtonText && (
                <button className='btn-primary' onClick={onPrimaryClick}>
                    {primaryButtonText}
                </button>
            )}
        </header>
    );
}