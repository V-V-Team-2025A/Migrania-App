import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '@/common/components/Header.jsx';
import Tabla from '@/common/components/Tabla.jsx';

export default function BitacoraDigitalMedico() {
    const { pacienteId } = useParams(); // Obtener el ID del paciente desde la URL
    const [episodios, setEpisodios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchEpisodios = async () => {
            // Validar que tengamos un ID de paciente
            if (!pacienteId) {
                setError('ID de paciente no proporcionado');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                // Para médicos, necesitamos especificar el paciente_id
                const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
                const url = `${baseUrl}/evaluaciones/episodios/?paciente_id=${pacienteId}`;

                console.log('Intentando conectar a:', url);
                console.log('Base URL configurada:', import.meta.env.VITE_API_BASE_URL);

                // Obtener el token de autenticación desde localStorage
                const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MTg5NDU0LCJpYXQiOjE3NTQxODU4NTQsImp0aSI6Ijc5YThlNTcxMzk4ZjQ5OWY5ZGJjNmQ0ZTFiOThjODg5IiwidXNlcl9pZCI6IjU4In0.vGZieu_vT30hyM6Z0H71shBfqCG9MJb6yx6yXOSvWmg"

                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': token ? `Bearer ${token}` : '',
                    }
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('No autorizado. Por favor, inicia sesión nuevamente.');
                    } else if (response.status === 403) {
                        throw new Error('No tienes permisos para ver los episodios de este paciente.');
                    } else if (response.status === 404) {
                        throw new Error('Paciente no encontrado.');
                    } else {
                        throw new Error(`Error ${response.status}: ${response.statusText}`);
                    }
                }

                const data = await response.json();
                console.log('Datos recibidos de la API:', data);
                console.log('Tipo de datos:', typeof data);
                console.log('Es array:', Array.isArray(data));

                // Verificar si data es un array o tiene una propiedad que contenga el array
                let episodiosArray = [];
                if (Array.isArray(data)) {
                    episodiosArray = data;
                } else if (data && Array.isArray(data.results)) {
                    episodiosArray = data.results;
                } else if (data && Array.isArray(data.episodios)) {
                    episodiosArray = data.episodios;
                } else if (data && Array.isArray(data.data)) {
                    episodiosArray = data.data;
                } else {
                    console.error('Estructura de datos inesperada:', data);
                    throw new Error('La respuesta del servidor no tiene el formato esperado');
                }

                // Transformar los datos booleanos a strings para la tabla
                const episodiosTransformados = episodiosArray.map(episodio => ({
                    ...episodio,
                    creado_en: episodio.creado_en ? new Date(episodio.creado_en).toLocaleString() : '-',
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

                if (err.name === 'TypeError' && err.message.includes('fetch')) {
                    setError('No se puede conectar al servidor. Verifica que el backend esté ejecutándose.');
                } else if (err.message.includes('No autorizado')) {
                    setError('Sesión expirada. Por favor, inicia sesión nuevamente.');
                } else if (err.message.includes('No tienes permisos')) {
                    setError('No tienes permisos para ver los episodios de este paciente.');
                } else if (err.message.includes('Paciente no encontrado')) {
                    setError('Paciente no encontrado.');
                } else {
                    setError(`Error al cargar los episodios: ${err.message}`);
                }
            } finally {
                setLoading(false);
            }
        };

        fetchEpisodios();
    }, [pacienteId]); // Recargar cuando cambie el paciente

    const columnasEpisodios = [
        { key: 'creado_en', header: 'Fecha de Registro' },
        { key: 'categoria_diagnostica', header: 'Categoría Diagnóstica' },
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
                primaryButtonText="Filtrar bitácora"
                onPrimaryClick={handleNuevoEpisodio}
                patientName="Juan Pérez"
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
