import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '@/common/components/Header.jsx';
import Tabla from '@/common/components/Tabla.jsx';
import ModalFiltro from '../components/ModalFiltro.jsx';

export default function BitacoraDigitalMedico() {
    const { pacienteId } = useParams(); // Obtener el ID del paciente desde la URL
    const [episodios, setEpisodios] = useState([]);
    const [episodiosOriginales, setEpisodiosOriginales] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModalFiltro, setShowModalFiltro] = useState(false);
    const [filtroActivo, setFiltroActivo] = useState("");
    const [nombrePaciente, setNombrePaciente] = useState("");

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

                // Obtener el token de autenticación desde localStorage
                const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MjM2MDE5LCJpYXQiOjE3NTQyMzI0MTksImp0aSI6IjQ5ODBkZmY3Mjg4MjQwMjA4Nzc3NTFhNDM0NmZkMGRiIiwidXNlcl9pZCI6IjEifQ.t6JduFMuUiLb3d7snf8ge06M-uFy-tgv89-pKjDM2EQ"
                const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

                // Obtener información del paciente
                try {
                    const pacienteUrl = `${baseUrl}/usuarios/${pacienteId}/`;
                    const pacienteResponse = await fetch(pacienteUrl, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': token ? `Bearer ${token}` : '',
                        }
                    });

                    if (pacienteResponse.ok) {
                        const pacienteData = await pacienteResponse.json();
                        console.log('Datos del paciente:', pacienteData);

                        // Usar solo el first_name del paciente
                        const nombre = pacienteData.first_name || 'Paciente';
                        setNombrePaciente(nombre);
                    }
                } catch (pacienteError) {
                    console.log('No se pudo obtener información del paciente:', pacienteError);
                    setNombrePaciente('Paciente');
                }

                // Para médicos, necesitamos especificar el paciente_id
                const url = `${baseUrl}/evaluaciones/episodios/?paciente_id=${pacienteId}`;

                console.log('Intentando conectar a:', url);
                console.log('Base URL configurada:', import.meta.env.VITE_API_BASE_URL);

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
                setEpisodiosOriginales(episodiosTransformados); // Guardar copia original para filtrado
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
        setShowModalFiltro(true);
    };

    const handleVolver = () => {
        console.log('Volver clickeado');
    };

    const handleConfirmarFiltro = (tipoFiltro) => {
        setFiltroActivo(tipoFiltro);

        if (tipoFiltro === "") {
            // Mostrar todos los episodios
            setEpisodios(episodiosOriginales);
        } else {
            // Filtrar por tipo de cefalea
            const episodiosFiltrados = episodiosOriginales.filter(episodio =>
                episodio.categoria_diagnostica === tipoFiltro
            );
            setEpisodios(episodiosFiltrados);
        }

        setShowModalFiltro(false);
    };

    const handleCancelarFiltro = () => {
        setShowModalFiltro(false);
    };

    return (
        <div>
            <Header
                title="Bitácora"
                onBack={handleVolver}
                primaryButtonText="Filtrar bitácora"
                onPrimaryClick={handleNuevoEpisodio}
                patientName={nombrePaciente}
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
            {showModalFiltro && (
                <ModalFiltro
                    message="Seleccionar filtro para la bitácora"
                    onConfirm={handleConfirmarFiltro}
                    onCancel={handleCancelarFiltro}
                />
            )}
        </div>
    );
}
