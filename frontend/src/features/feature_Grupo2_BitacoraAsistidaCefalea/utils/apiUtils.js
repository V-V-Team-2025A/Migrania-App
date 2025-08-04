
// Importaciones de constantes y funciones auxiliares
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const EPISODIOS_ENDPOINT = '/evaluaciones/episodios/';

// Funciones auxiliares
export const getApiUrl = (endpoint) => {
    return `${BASE_URL}${endpoint}`;
};

export const isTokenExpired = (token) => {
    if (!token) return true;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentTime = Math.floor(Date.now() / 1000);
        return payload.exp < currentTime;
    } catch (error) {
        console.error('Error al verificar token:', error);
        return true;
    }
};

export const getAuthHeaders = (token = null, userType = 'paciente') => {
    const defaultToken = token || localStorage.getItem("access");

    if (isTokenExpired(defaultToken)) {
        console.warn(`Token ha expirado`);
    }

    return {
        'Content-Type': 'application/json',
        'Authorization': defaultToken ? `Bearer ${defaultToken}` : '',
    };
};

export const parseApiResponse = (data) => {
    console.log('Parseando respuesta API:', data);

    if (Array.isArray(data)) {
        console.log('Data es array directo, devolviendo:', data);
        return data;
    }

    const possibleArrayPaths = ['results', 'episodios', 'data'];
    for (const path of possibleArrayPaths) {
        if (data && Array.isArray(data[path])) {
            console.log(`Encontrado array en ${path}:`, data[path]);
            return data[path];
        }
    }

    console.error('Estructura de datos inesperada:', data);
    console.error('Tipo de data:', typeof data);
    console.error('Keys disponibles:', Object.keys(data || {}));

    // Si no encontramos un array, pero data existe, intentar devolverlo tal como está
    if (data) {
        console.warn('Devolviendo data sin parsear:', data);
        return data;
    }

    throw new Error('La respuesta del servidor no tiene el formato esperado');
};

export const fetchEpisodiosPaciente = async (token = null) => {
    return fetchEpisodios(token, 'paciente');
};

export const fetchEpisodios = async (token = null, userType = 'paciente') => {
    try {
        const url = getApiUrl(EPISODIOS_ENDPOINT);
        const headers = getAuthHeaders(token, userType);
        const defaultToken = token || localStorage.getItem("access");

        // Verificar si el token ha expirado antes de hacer la petición
        if (isTokenExpired(defaultToken)) {
            console.warn('Token expirado detectado, retornando datos de prueba');
            return getMockEpisodios();
        }

        console.log('Haciendo request a:', url);
        console.log('Con headers:', headers);

        const response = await fetch(url, {
            method: 'GET',
            headers: headers
        });

        console.log('Response status:', response.status);
        console.log('Response OK:', response.ok);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response body:', errorText);

            if (response.status === 401) {
                console.warn('Error 401: Token expirado o inválido, retornando datos de prueba');
                return getMockEpisodios();
            }

            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Raw data from API:', data);

        const parsedData = parseApiResponse(data);
        console.log('Parsed data:', parsedData);

        return parsedData;
    } catch (error) {
        console.error('Error al obtener episodios:', error);

        // Si hay error de red o token, retornar datos de prueba
        if (error.message.includes('401') || error.message.includes('fetch')) {
            console.warn('Retornando datos de prueba debido a error de autenticación');
            return getMockEpisodios();
        }

        throw error;
    }
};

export const fetchEpisodiosMedico = async (token = null) => {
    return fetchEpisodios(token, 'medico');
};

// Función para obtener información del paciente
export const fetchPacienteInfo = async (pacienteId) => {
    try {
        const url = `${BASE_URL}/usuarios/${pacienteId}/`;
        const headers = getAuthHeaders(null, 'medico');

        const response = await fetch(url, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener información del paciente:', error);
        throw error;
    }
};

// Función para obtener información completa del paciente
export const fetchPacienteInfoCompleta = async (pacienteId, baseUrl = null) => {
    try {
        const url = `${baseUrl || BASE_URL}/usuarios/${pacienteId}/`;
        const headers = getAuthHeaders(null, 'medico');

        const response = await fetch(url, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener información completa del paciente:', error);
        throw error;
    }
};

// Función para obtener información del paciente actual
export const fetchUserInfoPaciente = async () => {
    try {
        const url = `${BASE_URL}/usuarios/mi_perfil/`;
        const headers = getAuthHeaders(null, 'paciente');

        const response = await fetch(url, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener información del paciente:', error);
        // Retornar datos de prueba en caso de error
        return {
            id: 1,
            nombre: "Paciente de Prueba",
            genero: "F",
            email: "paciente@test.com"
        };
    }
};

// Función para crear un nuevo episodio
export const createEpisodioPaciente = async (episodioData) => {
    try {
        const url = getApiUrl(EPISODIOS_ENDPOINT);
        const headers = getAuthHeaders(null, 'paciente');

        console.log('Creando episodio con datos:', episodioData);
        console.log('URL:', url);

        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(episodioData)
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response body:', errorText);
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Episodio creado exitosamente:', data);
        return data;
    } catch (error) {
        console.error('Error al crear episodio:', error);
        throw error;
    }
};

// Función para manejo de errores del médico
export const getErrorMessageMedico = (error) => {
    if (error.message.includes('401')) {
        return 'Error de autenticación. Por favor, inicie sesión nuevamente.';
    }
    if (error.message.includes('403')) {
        return 'No tiene permisos para acceder a esta información.';
    }
    if (error.message.includes('404')) {
        return 'Paciente no encontrado.';
    }
    if (error.message.includes('500')) {
        return 'Error interno del servidor. Intente nuevamente más tarde.';
    }
    return error.message || 'Ha ocurrido un error inesperado.';
};

// Función para manejo de errores general
export const getErrorMessage = (error) => {
    if (error.message.includes('401')) {
        return 'Error de autenticación. Por favor, inicie sesión nuevamente.';
    }
    if (error.message.includes('403')) {
        return 'No tiene permisos para realizar esta acción.';
    }
    if (error.message.includes('500')) {
        return 'Error interno del servidor. Intente nuevamente más tarde.';
    }
    return error.message || 'Ha ocurrido un error inesperado.';
};

// Datos de prueba para cuando no hay tokens válidos
export const getMockEpisodios = () => {
    console.log('Retornando datos de prueba de episodios');
    return [
        {
            id: 1,
            creado_en: "2025-08-03T14:30:00.000Z",
            categoria_diagnostica: "Migraña sin aura",
            severidad: "Leve",
            duracion_cefalea_horas: 6,
            localizacion: "Unilateral",
            caracter_dolor: "Pulsátil",
            empeora_actividad: true,
            nauseas_vomitos: true,
            fotofobia: false,
            fonofobia: false,
            presencia_aura: false,
            sintomas_aura: "",
            duracion_aura_minutos: 0,
            en_menstruacion: false,
            anticonceptivos: false
        },
        {
            id: 2,
            creado_en: "2025-08-03T10:15:00.000Z",
            categoria_diagnostica: "Migraña con aura",
            severidad: "Moderado",
            duracion_cefalea_horas: 8,
            localizacion: "Bilateral",
            caracter_dolor: "Pulsátil",
            empeora_actividad: true,
            nauseas_vomitos: false,
            fotofobia: true,
            fonofobia: true,
            presencia_aura: true,
            sintomas_aura: "Luces brillantes",
            duracion_aura_minutos: 30,
            en_menstruacion: false,
            anticonceptivos: false
        },
        {
            id: 3,
            creado_en: "2025-08-02T16:45:00.000Z",
            categoria_diagnostica: "Cefalea de tipo tensional",
            severidad: "Leve",
            duracion_cefalea_horas: 4,
            localizacion: "Bilateral",
            caracter_dolor: "Opresivo",
            empeora_actividad: false,
            nauseas_vomitos: false,
            fotofobia: false,
            fonofobia: false,
            presencia_aura: false,
            sintomas_aura: "",
            duracion_aura_minutos: 0,
            en_menstruacion: false,
            anticonceptivos: false
        },
        {
            id: 4,
            creado_en: "2025-08-01T09:20:00.000Z",
            categoria_diagnostica: "Migraña sin aura",
            severidad: "Severo",
            duracion_cefalea_horas: 12,
            localizacion: "Unilateral",
            caracter_dolor: "Pulsátil",
            empeora_actividad: true,
            nauseas_vomitos: true,
            fotofobia: true,
            fonofobia: true,
            presencia_aura: false,
            sintomas_aura: "",
            duracion_aura_minutos: 0,
            en_menstruacion: false,
            anticonceptivos: false
        }
    ];
};
