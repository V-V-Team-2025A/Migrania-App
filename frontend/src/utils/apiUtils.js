/**
 * Utilidades para manejo de APIs
 */

/**
 * Parsea la respuesta de la API para extraer el array de datos
 * @param {any} data - Datos recibidos de la API
 * @returns {Array} Array de datos parseados
 * @throws {Error} Si la estructura de datos es inesperada
 */
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

/**
 * Genera un mensaje de error apropiado basado en el error y respuesta
 * @param {Error} error - Error capturado
 * @param {Response} response - Respuesta HTTP (opcional)
 * @returns {string} Mensaje de error apropiado
 */
export const getErrorMessage = (error, response) => {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return 'No se puede conectar al servidor. Verifica que el backend esté ejecutándose.';
    }

    if (response) {
        switch (response.status) {
            case 401:
                return 'Sesión expirada. Por favor, inicia sesión nuevamente.';
            case 403:
                return 'No tienes permisos para ver los episodios.';
            case 404:
                return 'Episodios no encontrados.';
            default:
                return `Error ${response.status}: ${response.statusText}`;
        }
    }

    return `Error al cargar los episodios: ${error.message}`;
};
