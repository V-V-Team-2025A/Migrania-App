/**
 * Constantes de configuración para la aplicación
 */

// URLs y endpoints de la API
export const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
export const EPISODIOS_ENDPOINT = '/evaluaciones/episodios/';

// Token temporal - TODO: Implementar sistema de autenticación apropiado
export const TEMP_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MjQ2MjM5LCJpYXQiOjE3NTQyNDI2MzksImp0aSI6ImIzOGE1NjgwYmE4ZTRmNTFiYmExZTI3YzRhNGY4YzdmIiwidXNlcl9pZCI6IjU4In0.3g1egaoaw4XbkELqqub1nvKuCTM0rw2gFCUHdF8otb4";
