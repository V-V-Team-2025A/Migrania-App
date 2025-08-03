import React, { useState, useEffect } from 'react';
import Header from '@/common/components/Header.jsx';
import Tabla from '@/common/components/Tabla.jsx';

export default function BitacoraDigital() {
    const [episodios, setEpisodios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchEpisodios = async () => {
            try {
                setLoading(true);
                setError(null);

                // URL para que el paciente vea sus propios episodios
                const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/evaluaciones/episodios/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': localStorage.getItem('access_token') ? `Bearer ${localStorage.getItem('access_token')}` : '',
                    }
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('No autorizado. Por favor, inicia sesión nuevamente.');
                    } else {
                        throw new Error(`Error ${response.status}: ${response.statusText}`);
                    }
                }

                const data = await response.json();

                // Transformar los datos booleanos a strings para la tabla
                const episodiosTransformados = data.map(episodio => ({
                    ...episodio,
                    empeora_actividad: episodio.empeora_actividad ? 'Sí' : 'No',
                    nauseas_vomitos: episodio.nauseas_vomitos ? 'Sí' : 'No',
                    fotofobia: episodio.fotofobia ? 'Sí' : 'No',
                    fonofobia: episodio.fonofobia ? 'Sí' : 'No',
                    presencia_aura: episodio.presencia_aura ? 'Sí' : 'No',
                    en_menstruacion: episodio.en_menstruacion ? 'Sí' : 'No',
                    anticonceptivos: episodio.anticonceptivos ? 'Sí' : 'No',
                    sintomas_aura: episodio.sintomas_aura || '-'
                }));

                setEpisodios(episodiosTransformados);
            } catch (err) {
                console.error('Error al cargar episodios:', err);
                setError('Error al cargar los episodios de cefalea');
            } finally {
                setLoading(false);
            }
        };

        fetchEpisodios();
    }, []);

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
            {loading && (
                <div style={{ padding: '20px', textAlign: 'center' }}>
                    Cargando episodios...
                </div>
            )}
            {error && (
                <div style={{ padding: '20px', color: 'red', textAlign: 'center' }}>
                    {error}
                </div>
            )}
            {!loading && !error && (
                <Tabla
                    data={episodios}
                    columns={columnasEpisodios}
                    keyField="id"
                    emptyMessage="No hay episodios de cefalea registrados"
                />
            )}
        </div>
    );
}
