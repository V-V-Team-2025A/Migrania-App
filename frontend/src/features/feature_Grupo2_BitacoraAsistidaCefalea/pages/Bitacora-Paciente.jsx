
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header.jsx';
import Tabla from '../components/Table.jsx';
import { parseApiResponse, getErrorMessage, getApiUrl, getAuthHeaders, fetchUserInfoPaciente } from '../utils/apiUtils.js';
import { transformEpisodio, getColumnasSegunGenero } from '../utils/episodioUtils.js';
import { EPISODIOS_ENDPOINT } from '../utils/constants.js';
import '../styles/bitacora.module.css';

export default function BitacoraDigital() {
    const navigate = useNavigate();
    const [episodios, setEpisodios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userInfo, setUserInfo] = useState(null);
    const [columnas, setColumnas] = useState([]);

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
        </div>
    );
}
