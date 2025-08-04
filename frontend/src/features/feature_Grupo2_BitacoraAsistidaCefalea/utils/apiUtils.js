
import { BASE_URL, getAuthToken, MI_PERFIL_ENDPOINT, EPISODIOS_ENDPOINT } from './constants.js';

export const parseApiResponse = (data) => {
    if (Array.isArray(data)) {
        return data;
    }

    const possibleArrayPaths = ['results', 'episodios', 'data'];
    for (const path of possibleArrayPaths) {
        if (data && Array.isArray(data[path])) {
            return data[path];
        }
    }

    console.error('Estructura de datos inesperada:', data);
    throw new Error('La respuesta del servidor no tiene el formato esperado');
};

export const getErrorMessage = (error, response, context = 'paciente') => {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return 'No se puede conectar al servidor. Verifica que el backend esté ejecutándose.';
    }

    if (response) {
        switch (response.status) {
            case 401:
                return context === 'medico'
                    ? 'No autorizado. Por favor, inicia sesión nuevamente.'
                    : 'Sesión expirada. Por favor, inicia sesión nuevamente.';
            case 403:
                return context === 'medico'
                    ? 'No tienes permisos para ver los episodios de este paciente.'
                    : 'No tienes permisos para ver los episodios.';
            case 404:
                return context === 'medico'
                    ? 'Paciente no encontrado.'
                    : 'Episodios no encontrados.';
            default:
                return `Error ${response.status}: ${response.statusText}`;
        }
    }

    return `Error al cargar los episodios: ${error.message}`;
};

export const getErrorMessageMedico = (error, response) => {
    return getErrorMessage(error, response, 'medico');
};

export const getApiUrl = (endpoint) => {
    return `${BASE_URL}${endpoint}`;
};

export const getAuthHeaders = (token = null, userType = 'paciente') => {
    const defaultToken = token || getAuthToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': defaultToken ? `Bearer ${defaultToken}` : '',
    };
};

export const fetchUserInfo = async (token = null, userType = 'paciente') => {
    const response = await fetch(getApiUrl(MI_PERFIL_ENDPOINT), {
        method: 'GET',
        headers: getAuthHeaders(token, userType)
    });

    if (!response.ok) {
        console.error(`Error al obtener información del usuario:`, response.status);
        return { genero: 'F', nombre_completo: 'Usuario' };
    }

    const userData = await response.json();
    console.log('Información del usuario:', userData);
    return userData;
};

export const handleApiError = (response, errorData) => {
    if (response.status === 401) {
        throw new Error('No autorizado. Por favor, inicia sesión nuevamente.');
    } else if (response.status === 403) {
        throw new Error('No tienes permisos para crear episodios.');
    } else if (response.status === 400) {
        const errorMessages = Object.entries(errorData).map(([field, messages]) =>
            `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
        ).join('; ');
        throw new Error(`Error de validación: ${errorMessages}`);
    } else {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
};

export const createEpisodio = async (episodioData, token = null, userType = 'paciente') => {
    const response = await fetch(getApiUrl(EPISODIOS_ENDPOINT), {
        method: 'POST',
        headers: getAuthHeaders(token, userType),
        body: JSON.stringify(episodioData)
    });

    if (!response.ok) {
        const errorData = await response.json();
        handleApiError(response, errorData);
    }

    return await response.json();
};


export const fetchUserInfoPaciente = async (token = null) => {
    return fetchUserInfo(token, 'paciente');
};

export const createEpisodioPaciente = async (episodioData, token = null) => {
    return createEpisodio(episodioData, token, 'paciente');
};


export const fetchUserInfoMedico = async (token = null) => {
    return fetchUserInfo(token, 'medico');
};

export const createEpisodioMedico = async (episodioData, token = null) => {
    return createEpisodio(episodioData, token, 'medico');
};


export const fetchPacienteInfo = async (pacienteId, baseUrl, token = null) => {
    try {
        const pacienteUrl = `${baseUrl}/usuarios/${pacienteId}/`;
        console.log('Intentando obtener información del paciente desde:', pacienteUrl);

        const response = await fetch(pacienteUrl, {
            method: 'GET',
            headers: getAuthHeaders(token, 'medico')
        });

        console.log('Respuesta del API para paciente:', response.status, response.statusText);

        if (response.ok) {
            const pacienteData = await response.json();
            console.log('Datos completos del paciente:', pacienteData);

            const nombre = pacienteData.first_name ||
                pacienteData.nombre ||
                pacienteData.username ||
                'Paciente';

            console.log('Nombre del paciente obtenido:', nombre);
            return nombre;
        } else {
            console.error('Error en la respuesta del API:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('Detalles del error:', errorText);
            return 'Paciente';
        }
    } catch (error) {
        console.error('Error al obtener información del paciente:', error);
        return 'Paciente';
    }
};

export const fetchPacienteInfoCompleta = async (pacienteId, baseUrl, token = null) => {
    try {
        const pacienteUrl = `${baseUrl}/usuarios/${pacienteId}/`;
        console.log('Intentando obtener información completa del paciente desde:', pacienteUrl);

        const response = await fetch(pacienteUrl, {
            method: 'GET',
            headers: getAuthHeaders(token, 'medico')
        });

        console.log('Respuesta del API para paciente completo:', response.status, response.statusText);

        if (response.ok) {
            const pacienteData = await response.json();
            console.log('Datos completos del paciente:', pacienteData);

            return {
                nombre: pacienteData.first_name || pacienteData.nombre || pacienteData.username || 'Paciente',
                genero: pacienteData.genero || pacienteData.gender || 'F',
                ...pacienteData
            };
        } else {
            console.error('Error en la respuesta del API:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('Detalles del error:', errorText);
            return { nombre: 'Paciente', genero: 'F' };
        }
    } catch (error) {
        console.error('Error al obtener información completa del paciente:', error);
        return { nombre: 'Paciente', genero: 'F' };
    }
};
