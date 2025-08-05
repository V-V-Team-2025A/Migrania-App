// src/services/apiService.js

// Configuración de la API con fallback seguro
const getApiBaseUrl = () => {
  if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_BASE_URL) {
    return process.env.REACT_APP_API_BASE_URL;
  }
  // Fallback para desarrollo local
  return 'https://migrania-app-pruebas-production.up.railway.app/api';
};

const API_BASE_URL = getApiBaseUrl();

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Helper para obtener el token de autenticación
  getAuthToken() {
    return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
  }

  // Helper para crear headers de autenticación
  getAuthHeaders() {
    const token = this.getAuthToken();
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  // Helper para manejar respuestas HTTP
  async handleResponse(response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  // Helper para hacer peticiones HTTP
  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    try {
      const response = await fetch(url, config);
      return await this.handleResponse(response);
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Obtener lista de pacientes (para personal médico)
  async getPacientes() {
    return this.makeRequest('/usuarios/pacientes/', {
      method: 'GET'
    });
  }

  // Obtener estadísticas del historial
  async getEstadisticasHistorial(pacienteId = null) {
    const queryParams = pacienteId ? `?paciente_id=${pacienteId}` : '';
    return this.makeRequest(`/analiticas/estadisticas/${queryParams}`, {
      method: 'GET'
    });
  }

  // Obtener promedio semanal
  async getPromedioSemanal(pacienteId, fechaInicio, fechaFin) {
    const queryParams = new URLSearchParams({
      ...(pacienteId && { paciente_id: pacienteId }),
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin
    });
    
    return this.makeRequest(`/analiticas/promedio-semanal/?${queryParams}`, {
      method: 'GET'
    });
  }

  // Obtener análisis de patrones
  async getAnalisisPatrones(pacienteId = null) {
    const queryParams = pacienteId ? `?paciente_id=${pacienteId}` : '';
    return this.makeRequest(`/analiticas/patrones/${queryParams}`, {
      method: 'GET'
    });
  }

  // Obtener información del usuario actual
  async getCurrentUser() {
    return this.makeRequest('/usuarios/me/', {
      method: 'GET'
    });
  }

  // Obtener episodios de bitácora (si necesitas mostrar historial detallado)
  async getEpisodiosBitacora(pacienteId = null, fechaInicio = null, fechaFin = null) {
    const queryParams = new URLSearchParams();
    if (pacienteId) queryParams.append('paciente_id', pacienteId);
    if (fechaInicio) queryParams.append('fecha_inicio', fechaInicio);
    if (fechaFin) queryParams.append('fecha_fin', fechaFin);
    
    const queryString = queryParams.toString();
    return this.makeRequest(`/bitacora/episodios/${queryString ? '?' + queryString : ''}`, {
      method: 'GET'
    });
  }

  // Obtener un episodio específico
  async getEpisodio(episodioId) {
    return this.makeRequest(`/bitacora/episodios/${episodioId}/`, {
      method: 'GET'
    });
  }

  // Crear un nuevo episodio
  async createEpisodio(episodioData) {
    return this.makeRequest('/bitacora/episodios/', {
      method: 'POST',
      body: JSON.stringify(episodioData)
    });
  }

  // Actualizar un episodio
  async updateEpisodio(episodioId, episodioData) {
    return this.makeRequest(`/bitacora/episodios/${episodioId}/`, {
      method: 'PUT',
      body: JSON.stringify(episodioData)
    });
  }

  // Eliminar un episodio
  async deleteEpisodio(episodioId) {
    return this.makeRequest(`/bitacora/episodios/${episodioId}/`, {
      method: 'DELETE'
    });
  }
}

// Exportar instancia singleton
export const apiService = new ApiService();
export default apiService;