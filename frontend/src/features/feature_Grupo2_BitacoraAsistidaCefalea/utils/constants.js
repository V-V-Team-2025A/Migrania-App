export const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
export const EPISODIOS_ENDPOINT = '/evaluaciones/episodios/';
export const USUARIOS_ENDPOINT = '/usuarios/';
export const MI_PERFIL_ENDPOINT = '/usuarios/mi_perfil/';

// Token de autenticación obtenido del localStorage
export const getAuthToken = () => localStorage.getItem("access");

// Constantes del formulario de registro de cefalea
export const INITIAL_FORM_DATA = {
    duracion_cefalea_horas: '',
    severidad: '',
    localizacion: '',
    caracter_dolor: '',
    empeora_actividad: '',
    nauseas_vomitos: '',
    fotofobia: '',
    fonofobia: '',
    presencia_aura: '',
    sintomas_aura: '',
    duracion_aura_minutos: '',
    en_menstruacion: '',
    anticonceptivos: ''
};

export const BOOLEAN_FIELDS = [
    'empeora_actividad',
    'nauseas_vomitos',
    'fotofobia',
    'fonofobia',
    'presencia_aura',
    'en_menstruacion',
    'anticonceptivos'
];

export const REQUIRED_FIELDS = [
    'duracion_cefalea_horas',
    'severidad',
    'localizacion',
    'caracter_dolor'
];
