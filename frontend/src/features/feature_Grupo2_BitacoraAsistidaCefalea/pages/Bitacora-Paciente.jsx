import React, { useState } from 'react';
import Header from '@/common/components/Header.jsx';
import Tabla from '@/common/components/Tabla.jsx';

export default function BitacoraDigital() {
    const [episodios, setEpisodios] = useState([
        {
            id: 1,
            duracion_cefalea_horas: 5,
            severidad: 'Moderada',
            localizacion: 'Unilateral',
            caracter_dolor: 'Pulsátil',
            empeora_actividad: 'Sí',
            nauseas_vomitos: 'Sí',
            fotofobia: 'Sí',
            fonofobia: 'No',
            presencia_aura: 'Sí',
            sintomas_aura: 'Visual',
            duracion_aura_minutos: 30,
            en_menstruacion: 'No',
            anticonceptivos: 'No'
        },
        {
            id: 2,
            duracion_cefalea_horas: 3,
            severidad: 'Severa',
            localizacion: 'Bilateral',
            caracter_dolor: 'Opresivo',
            empeora_actividad: 'No',
            nauseas_vomitos: 'No',
            fotofobia: 'Sí',
            fonofobia: 'Sí',
            presencia_aura: 'No',
            sintomas_aura: '-',
            duracion_aura_minutos: 0,
            en_menstruacion: 'Sí',
            anticonceptivos: 'Sí'
        },
        {
            id: 3,
            duracion_cefalea_horas: 8,
            severidad: 'Moderada',
            localizacion: 'Unilateral',
            caracter_dolor: 'Pulsátil',
            empeora_actividad: 'Sí',
            nauseas_vomitos: 'Sí',
            fotofobia: 'Sí',
            fonofobia: 'No',
            presencia_aura: 'Sí',
            sintomas_aura: 'Sensitivo',
            duracion_aura_minutos: 20,
            en_menstruacion: 'No',
            anticonceptivos: 'No'
        },
        {
            id: 4,
            duracion_cefalea_horas: 2,
            severidad: 'Leve',
            localizacion: 'Frontal',
            caracter_dolor: 'Punzante',
            empeora_actividad: 'No',
            nauseas_vomitos: 'No',
            fotofobia: 'No',
            fonofobia: 'No',
            presencia_aura: 'No',
            sintomas_aura: '-',
            duracion_aura_minutos: 0,
            en_menstruacion: 'No',
            anticonceptivos: 'No'
        },
        {
            id: 5,
            duracion_cefalea_horas: 6,
            severidad: 'Severa',
            localizacion: 'Unilateral',
            caracter_dolor: 'Pulsátil',
            empeora_actividad: 'Sí',
            nauseas_vomitos: 'Sí',
            fotofobia: 'Sí',
            fonofobia: 'Sí',
            presencia_aura: 'Sí',
            sintomas_aura: 'Visual y Sensitivo',
            duracion_aura_minutos: 45,
            en_menstruacion: 'Sí',
            anticonceptivos: 'Sí'
        },
        {
            id: 6,
            duracion_cefalea_horas: 4,
            severidad: 'Moderada',
            localizacion: 'Bilateral',
            caracter_dolor: 'Opresivo',
            empeora_actividad: 'No',
            nauseas_vomitos: 'No',
            fotofobia: 'No',
            fonofobia: 'No',
            presencia_aura: 'No',
            sintomas_aura: '-',
            duracion_aura_minutos: 0,
            en_menstruacion: 'No',
            anticonceptivos: 'No'
        }
    ]);

    const columnasEpisodios = [
        { key: 'duracion_cefalea_horas', header: 'Duración Cefalea (horas)' },
        { key: 'severidad', header: 'Severidad del Dolor' },
        { key: 'localizacion', header: 'Localización del Dolor' },
        { key: 'caracter_dolor', header: 'Carácter del Dolor' },
        { key: 'empeora_actividad', header: 'Empeora con Actividad' },
        { key: 'nauseas_vomitos', header: 'Náuseas o Vómitos' },
        { key: 'fotofobia', header: 'Sensibilidad a la Luz' },
        { key: 'fonofobia', header: 'Sensibilidad al Sonido' },
        { key: 'presencia_aura', header: 'Presencia de Aura' },
        { key: 'sintomas_aura', header: 'Síntomas del Aura' },
        { key: 'duracion_aura_minutos', header: 'Duración del Aura (min)' },
        { key: 'en_menstruacion', header: 'En menstruación' },
        { key: 'anticonceptivos', header: 'Anticonceptivos' }
    ];

    const handleNuevoEpisodio = () => {
        console.log('Nuevo episodio clickeado');
    };

    const handleVolver = () => {
        console.log('Volver clickeado');
    };

    return (
        <div>
            <Header
                title="Bitácora"
                onBack={handleVolver}
                primaryButtonText="Nuevo episodio"
                onPrimaryClick={handleNuevoEpisodio}
            />
            <Tabla
                data={episodios}
                columns={columnasEpisodios}
                keyField="id"
                emptyMessage="No hay episodios de cefalea registrados"
            />
        </div>
    );
}
