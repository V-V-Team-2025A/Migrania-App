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

// Función específica para médicos (mantiene compatibilidad)
export const getErrorMessageMedico = (error, response) => {
    return getErrorMessage(error, response, 'medico');
};

export const fetchPacienteInfo = async (pacienteId, baseUrl, token) => {
    try {
        const pacienteUrl = `${baseUrl}/usuarios/${pacienteId}/`;
        const response = await fetch(pacienteUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : '',
            }
        });

        if (response.ok) {
            const pacienteData = await response.json();
            return pacienteData.first_name || 'Paciente';
        }
        return 'Paciente';
    } catch (error) {
        console.log('No se pudo obtener información del paciente:', error);
        return 'Paciente';
    }
};
