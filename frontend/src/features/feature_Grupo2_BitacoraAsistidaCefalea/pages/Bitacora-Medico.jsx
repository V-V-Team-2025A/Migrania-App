
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/Header.jsx';
import Tabla from '../components/Table.jsx';
import ModalFiltro from '../components/ModalFiltro.jsx';
import { parseApiResponse, getErrorMessageMedico, fetchPacienteInfo, fetchPacienteInfoCompleta, getAuthHeaders } from '../utils/apiUtils.js';
import { transformEpisodioMedico, getColumnasSegunGenero } from '../utils/episodioUtils.js';
import { BASE_URL, EPISODIOS_ENDPOINT } from '../utils/constants.js';
import styles from '../styles/bitacora.module.css';

export default function BitacoraDigitalMedico() {
    const { pacienteId } = useParams();
    const [episodios, setEpisodios] = useState([]);
    const [episodiosOriginales, setEpisodiosOriginales] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModalFiltro, setShowModalFiltro] = useState(false);
    const [nombrePaciente, setNombrePaciente] = useState("");
    const [pacienteInfo, setPacienteInfo] = useState(null);
    const [columnas, setColumnas] = useState([]);
    const [filtroActivo, setFiltroActivo] = useState("");

    useEffect(() => {
        const fetchEpisodios = async () => {
            if (!pacienteId) {
                setError('ID de paciente no proporcionado');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                const pacienteData = await fetchPacienteInfoCompleta(pacienteId, BASE_URL);
                setPacienteInfo(pacienteData);
                setNombrePaciente(pacienteData.nombre);
                console.log('Información del paciente:', pacienteData);

                const columnasAMostrar = getColumnasSegunGenero(pacienteData.genero);
                setColumnas(columnasAMostrar);

                const url = `${BASE_URL}${EPISODIOS_ENDPOINT}?paciente_id=${pacienteId}`;
                console.log('Intentando conectar a:', url);
                console.log('Base URL configurada:', BASE_URL);

                const response = await fetch(url, {
                    method: 'GET',
                    headers: getAuthHeaders(null, 'medico')
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();
                console.log('Datos recibidos de la API:', data);

                const episodiosArray = parseApiResponse(data);
                const episodiosTransformados = episodiosArray.map(transformEpisodioMedico);

                setEpisodios(episodiosTransformados);
                setEpisodiosOriginales(episodiosTransformados);
            } catch (err) {
                console.error('Error al cargar episodios:', err);
                setError(getErrorMessageMedico(err));
            } finally {
                setLoading(false);
            }
        };

        fetchEpisodios();
    }, [pacienteId]);

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
                <div className={styles.loading}>
                    Cargando episodios...
                </div>
            )}
            {error && (
                <div className={styles.error}>
                    {error}
                </div>
            )}
            {!loading && !error && (
                <Tabla
                    data={episodios}
                    columns={columnas}
                    keyField="id"
                    className={styles.tableContainer}
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
