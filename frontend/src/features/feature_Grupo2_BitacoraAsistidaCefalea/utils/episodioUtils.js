export const transformEpisodio = (episodio) => ({
    ...episodio,
    creado_en: episodio.creado_en ? new Date(episodio.creado_en).toLocaleString() : '-',
    empeora_actividad: episodio.empeora_actividad ? 'Sí' : 'No',
    nauseas_vomitos: episodio.nauseas_vomitos ? 'Sí' : 'No',
    fotofobia: episodio.fotofobia ? 'Sí' : 'No',
    fonofobia: episodio.fonofobia ? 'Sí' : 'No',
    presencia_aura: episodio.presencia_aura ? 'Sí' : 'No',
    en_menstruacion: episodio.en_menstruacion ? 'Sí' : 'No',
    anticonceptivos: episodio.anticonceptivos ? 'Sí' : 'No',
    sintomas_aura: episodio.sintomas_aura || '-'
});

export const COLUMNAS_EPISODIOS = [
    { key: 'creado_en', header: 'Fecha de Registro' },
    { key: 'categoria_diagnostica', header: 'Categoría Diagnóstica' },
    { key: 'duracion_cefalea_horas', header: 'Duración Cefalea (horas)' },
    { key: 'severidad', header: 'Severidad del Dolor' },
    { key: 'localizacion', header: 'Localización del Dolor' },
    { key: 'caracter_dolor', header: 'Carácter del Dolor' },
    { key: 'empeora_actividad', header: 'Empeora con Actividad' },
    { key: 'nauseas_vomitos', header: 'Náuseas o Vómitos' },
    { key: 'fotofobia', header: 'Sensibilidad a la Luz' },
    { key: 'fonofobia', header: 'Sensibilidad al Sonido' },
    { key: 'presencia_aura', header: 'Presencia de Aura' },
    { key: 'sintomas_aura', header: 'Síntomas del Aura' },
    { key: 'duracion_aura_minutos', header: 'Duración del Aura (min)' },
    { key: 'en_menstruacion', header: 'En menstruación' },
    { key: 'anticonceptivos', header: 'Anticonceptivos' }
];
