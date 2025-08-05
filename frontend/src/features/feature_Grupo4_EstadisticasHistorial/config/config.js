// src/config/config.js

// Helper para acceso seguro a variables de entorno
const getEnvVar = (key, defaultValue = '') => {
  if (typeof process !== 'undefined' && process.env) {
    return process.env[key] || defaultValue;
  }
  return defaultValue;
};

export const API_CONFIG = {
  // URL base de la API - ajustar según el entorno
  BASE_URL: getEnvVar('REACT_APP_API_BASE_URL', 'https://migrania-app-pruebas-production.up.railway.app/api'),
  
  // Endpoints específicos
  ENDPOINTS: {
    // Usuarios
    PACIENTES: '/usuarios/pacientes/',
    CURRENT_USER: '/usuarios/me/',
    
    // Analíticas
    ESTADISTICAS: '/analiticas/estadisticas/',
    PROMEDIO_SEMANAL: '/analiticas/promedio-semanal/',
    PATRONES: '/analiticas/patrones/',
    
    // Bitácora (para futuras implementaciones)
    EPISODIOS: '/bitacora/episodios/',
    
    // MIDAS (para futuras implementaciones)
    MIDAS: '/midas/',
  },
  
  // Configuración de autenticación
  AUTH: {
    TOKEN_KEY: 'authToken',
    REFRESH_TOKEN_KEY: 'refreshToken',
  },
  
  // Configuraciones por defecto
  DEFAULTS: {
    // Número mínimo de episodios para mostrar estadísticas
    MIN_EPISODES_FOR_STATS: 3,
    
    // Período por defecto para promedio semanal (meses)
    DEFAULT_PERIOD_MONTHS: 3,
    
    // Formato de fecha
    DATE_FORMAT: 'YYYY-MM-DD',
    
    // Configuración de paginación
    PAGE_SIZE: 20,
  }
};

export const UI_CONFIG = {
  // Configuraciones de la interfaz
  DEBOUNCE_DELAY: 300, // ms para búsquedas
  ANIMATION_DURATION: 200, // ms para animaciones
  
  // Mensajes por defecto
  MESSAGES: {
    LOADING: 'Cargando...',
    NO_DATA: 'No hay datos disponibles',
    ERROR_GENERIC: 'Ha ocurrido un error',
    NO_PATIENTS: 'No se encontraron pacientes',
    SELECT_PATIENT: 'Seleccione un paciente',
    MIN_EPISODES_ERROR: 'Se requieren al menos 3 episodios para generar estadísticas',
  }
};

export default {
  API_CONFIG,
  UI_CONFIG
};