
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header.jsx';
import Tabla from '../components/Table.jsx';
import ModalFiltroPaciente from '../components/ModalFiltroPaciente.jsx';
import { parseApiResponse, getErrorMessage, getApiUrl, getAuthHeaders, fetchUserInfoPaciente } from '../utils/apiUtils.js';
import { transformEpisodio, getColumnasSegunGenero } from '../utils/episodioUtils.js';
import { EPISODIOS_ENDPOINT } from '../utils/constants.js';
import '../styles/bitacora.module.css';

export default function BitacoraDigital() {
    const navigate = useNavigate();
    const [episodios, setEpisodios] = useState([]);
    const [episodiosOriginales, setEpisodiosOriginales] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userInfo, setUserInfo] = useState(null);
    const [columnas, setColumnas] = useState([]);
    const [showModalFiltro, setShowModalFiltro] = useState(false);
    const [filtroActivo, setFiltroActivo] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);

                const userData = await fetchUserInfoPaciente();
                setUserInfo(userData);

                const columnasAMostrar = getColumnasSegunGenero(userData.genero);
                setColumnas(columnasAMostrar);

                const url = getApiUrl(EPISODIOS_ENDPOINT);
                console.log('Intentando conectar a:', url);

                const response = await fetch(url, {
                    method: 'GET',
                    headers: getAuthHeaders(null, 'paciente')
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();
                console.log('Datos recibidos de la API:', data);

                const episodiosArray = parseApiResponse(data);
                const episodiosTransformados = episodiosArray.map(transformEpisodio);

                setEpisodios(episodiosTransformados);
                setEpisodiosOriginales(episodiosTransformados);
            } catch (err) {
                console.error('Error al cargar datos:', err);
                setError(getErrorMessage(err));
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleNuevoEpisodio = () => {
        navigate('/registro');
    };

    const handleFiltrar = () => {
        setShowModalFiltro(true);
    };

    const handleConfirmarFiltro = (filtros) => {
        let episodiosFiltrados = [...episodiosOriginales];

        // Aplicar filtros
        if (filtros.categoria && filtros.categoria !== "") {
            episodiosFiltrados = episodiosFiltrados.filter(episodio =>
                episodio.categoria_diagnostica === filtros.categoria
            );
        }

        if (filtros.severidad && filtros.severidad !== "") {
            episodiosFiltrados = episodiosFiltrados.filter(episodio =>
                episodio.severidad === filtros.severidad
            );
        }

        if (filtros.conAura !== null) {
            episodiosFiltrados = episodiosFiltrados.filter(episodio =>
                filtros.conAura ? episodio.presencia_aura === 'Sí' : episodio.presencia_aura === 'No'
            );
        }

        setEpisodios(episodiosFiltrados);
        setFiltroActivo(Object.values(filtros).some(v => v !== "" && v !== null) ? "activo" : "");
        setShowModalFiltro(false);
    };

    const handleCancelarFiltro = () => {
        setShowModalFiltro(false);
    };

    const handleLimpiarFiltros = () => {
        setEpisodios(episodiosOriginales);
        setFiltroActivo("");
    };

    const handleVolver = () => {
        navigate('/dashboard-paciente');
    };

    return (
        <div>
            <Header
                title="Bitácora"
                onBack={handleVolver}
                primaryButtonText="Nuevo episodio"
                onPrimaryClick={handleNuevoEpisodio}
                secondaryButtonText={filtroActivo ? "Limpiar filtros" : "Filtrar"}
                onSecondaryClick={filtroActivo ? handleLimpiarFiltros : handleFiltrar}
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
                    columns={columnas}
                    keyField="id"
                    emptyMessage="No hay episodios de cefalea registrados"
                />
            )}
            {showModalFiltro && (
                <ModalFiltroPaciente
                    onConfirm={handleConfirmarFiltro}
                    onCancel={handleCancelarFiltro}
                />
            )}
        </div>
    );
}
