import React, { useState, useEffect } from 'react';
import Header from '@/common/components/Header.jsx';

export default function IngresarCefalea() {
    const [formData, setFormData] = useState({
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
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const [userInfo, setUserInfo] = useState(null);
    const [loadingUser, setLoadingUser] = useState(true);

    // Obtener información del usuario para verificar el género
    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                setLoadingUser(true);

                const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
                const url = `${baseUrl}/usuarios/mi_perfil/`;

                const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MTk1MzE3LCJpYXQiOjE3NTQxOTE3MTcsImp0aSI6ImE5Yjg2NDI1ZTQ0ZjQxNzhhNWIxNzU0ZWE3ODQ3Y2E5IiwidXNlcl9pZCI6IjE1NyJ9.mosOa4Qd8O-w-sT0Yzo2sH94FOj3W6aTFpKNS4LAmck";

                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': token ? `Bearer ${token}` : '',
                    }
                });

                if (!response.ok) {
                    console.error(`Error al obtener información del usuario desde ${url}:`, response.status);
                    // Si no se puede obtener la info del usuario, asumir mujer para mostrar todos los campos
                    setUserInfo({ genero: 'F', nombre_completo: 'Usuario' });
                    return;
                }

                const userData = await response.json();
                console.log('Información del usuario obtenida desde:', url);
                console.log('Información del usuario:', userData);
                console.log('Género del usuario:', userData.genero);
                setUserInfo(userData);


            } catch (err) {
                console.error('Error al obtener información del usuario:', err);
                // Si hay error, asumir mujer para mostrar todos los campos
                setUserInfo({ genero: 'F', nombre_completo: 'Usuario' });
            } finally {
                setLoadingUser(false);
            }
        };

        fetchUserInfo();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const transformFormDataForAPI = (data) => {
        // Transformar strings "Sí"/"No" a booleanos
        const booleanFields = ['empeora_actividad', 'nauseas_vomitos', 'fotofobia', 'fonofobia', 'presencia_aura', 'en_menstruacion', 'anticonceptivos'];

        const transformedData = { ...data };

        booleanFields.forEach(field => {
            if (transformedData[field] === 'Sí' || transformedData[field] === 'Si') {
                transformedData[field] = true;
            } else if (transformedData[field] === 'No') {
                transformedData[field] = false;
            } else {
                // Si no se seleccionó nada, por defecto false
                transformedData[field] = false;
            }
        });

        // Si el usuario es hombre, establecer campos específicos de mujeres como false
        if (userInfo && userInfo.genero === 'M') {
            transformedData.en_menstruacion = false;
            transformedData.anticonceptivos = false;
        }

        // Convertir campos numéricos
        if (transformedData.duracion_cefalea_horas) {
            transformedData.duracion_cefalea_horas = parseInt(transformedData.duracion_cefalea_horas);
        }

        if (transformedData.duracion_aura_minutos) {
            transformedData.duracion_aura_minutos = parseInt(transformedData.duracion_aura_minutos);
        } else {
            transformedData.duracion_aura_minutos = 0;
        }

        // Manejar síntomas del aura
        if (!transformedData.presencia_aura || transformedData.presencia_aura === false) {
            transformedData.sintomas_aura = "";
            transformedData.duracion_aura_minutos = 0;
        } else if (!transformedData.sintomas_aura || transformedData.sintomas_aura === "") {
            transformedData.sintomas_aura = "";
        }

        return transformedData;
    };

    const validateForm = (data) => {
        const requiredFields = ['duracion_cefalea_horas', 'severidad', 'localizacion', 'caracter_dolor'];
        const missingFields = requiredFields.filter(field => !data[field]);

        if (missingFields.length > 0) {
            throw new Error(`Campos requeridos faltantes: ${missingFields.join(', ')}`);
        }

        // Validar duración de cefalea
        const duracion = parseInt(data.duracion_cefalea_horas);
        if (isNaN(duracion) || duracion < 1 || duracion > 72) {
            throw new Error('La duración de la cefalea debe estar entre 1 y 72 horas.');
        }

        // Validar coherencia de aura
        if (data.presencia_aura === 'Sí' && data.duracion_aura_minutos && parseInt(data.duracion_aura_minutos) === 0) {
            throw new Error('Si hay presencia de aura, debe especificar una duración mayor a 0 minutos.');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            setLoading(true);
            setError(null);
            setSuccess(false);

            // Validar formulario
            validateForm(formData);

            // Transformar datos para la API
            const apiData = transformFormDataForAPI(formData);

            console.log('Datos del formulario original:', formData);
            console.log('Datos transformados para la API:', apiData);
            console.log('Campos enviados:', Object.keys(apiData));

            // Construir URL de la API
            const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
            const url = `${baseUrl}/evaluaciones/episodios/`;

            // Obtener token de autenticación

            const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MTk0Mjg3LCJpYXQiOjE3NTQxOTA2ODcsImp0aSI6IjZjZjA3Yjg3Y2QwNDQ3NTY5Y2MwYTA4Y2M1NjRjOGU1IiwidXNlcl9pZCI6IjIifQ.tb9AKkSOiS45A9eer6FnJAKzd2Mn3aNI_dYdHc5WitE"

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : '',
                },
                body: JSON.stringify(apiData)
            });

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('No autorizado. Por favor, inicia sesión nuevamente.');
                } else if (response.status === 403) {
                    throw new Error('No tienes permisos para crear episodios.');
                } else if (response.status === 400) {
                    const errorData = await response.json();
                    const errorMessages = Object.entries(errorData).map(([field, messages]) =>
                        `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
                    ).join('; ');
                    throw new Error(`Error de validación: ${errorMessages}`);
                } else {
                    throw new Error(`Error ${response.status}: ${response.statusText}`);
                }
            }

            const responseData = await response.json();
            console.log('Episodio creado exitosamente:', responseData);

            setSuccess(true);

            // Limpiar formulario
            setFormData({
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
            });

            // Opcional: redirigir después de un tiempo
            setTimeout(() => {
                setSuccess(false);
                // Aquí podrías agregar navegación de vuelta a la bitácora
            }, 3000);

        } catch (err) {
            console.error('Error al crear episodio:', err);

            if (err.name === 'TypeError' && err.message.includes('fetch')) {
                setError('No se puede conectar al servidor. Verifica que el backend esté ejecutándose.');
            } else {
                setError(err.message);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        // Lógica para cancelar y volver
        console.log('Cancelar registro');
    };

    return (
        <div>
            <Header
                title="Bitácora"
                onBack={() => console.log('Volver')}
            />

            <div className="form-container">
                <h2 className="form-title">
                    Registrar nuevo episodio
                </h2>

                {/* Mostrar loading mientras se obtiene información del usuario */}
                {loadingUser && (
                    <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
                        Cargando información del usuario...
                    </div>
                )}

                {/* Mostrar estados de loading, error o éxito */}
                {loading && (
                    <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
                        Guardando episodio...
                    </div>
                )}

                {error && (
                    <div style={{ padding: '20px', color: 'red', textAlign: 'center', background: '#ffebee', border: '1px solid #ffcdd2', borderRadius: '4px', margin: '20px 0' }}>
                        {error}
                    </div>
                )}

                {success && (
                    <div style={{ padding: '20px', color: 'green', textAlign: 'center', background: '#e8f5e8', border: '1px solid #c8e6c9', borderRadius: '4px', margin: '20px 0' }}>
                        ¡Episodio registrado exitosamente!
                    </div>
                )}

                {!loadingUser && userInfo && (
                    <form onSubmit={handleSubmit}>
                        <div className="form-grid">

                            <div className="form-field">
                                <label htmlFor="duracion_cefalea_horas" className="label-styled">Duración (h) *</label>
                                <input
                                    type="number"
                                    id="duracion_cefalea_horas"
                                    name="duracion_cefalea_horas"
                                    placeholder="Ej: 5"
                                    min="1"
                                    max="72"
                                    value={formData.duracion_cefalea_horas}
                                    onChange={handleInputChange}
                                    className="input-default"
                                    required
                                />
                            </div>

                            <div className="form-field">
                                <label htmlFor="severidad" className="label-styled">Severidad *</label>
                                <select
                                    id="severidad"
                                    name="severidad"
                                    value={formData.severidad}
                                    onChange={handleInputChange}
                                    className="select-default"
                                    required
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Leve">Leve</option>
                                    <option value="Moderada">Moderada</option>
                                    <option value="Severa">Severa</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="caracter_dolor" className="label-styled">Carácter *</label>
                                <select
                                    id="caracter_dolor"
                                    name="caracter_dolor"
                                    value={formData.caracter_dolor}
                                    onChange={handleInputChange}
                                    className="select-default"
                                    required
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Pulsátil">Pulsátil</option>
                                    <option value="Opresivo">Opresivo</option>
                                    <option value="Punzante">Punzante</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="localizacion" className="label-styled">Localización *</label>
                                <select
                                    id="localizacion"
                                    name="localizacion"
                                    value={formData.localizacion}
                                    onChange={handleInputChange}
                                    className="select-default"
                                    required
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Unilateral">Unilateral</option>
                                    <option value="Bilateral">Bilateral</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="empeora_actividad" className="label-styled">Empeora con actividad</label>
                                <select
                                    id="empeora_actividad"
                                    name="empeora_actividad"
                                    value={formData.empeora_actividad}
                                    onChange={handleInputChange}
                                    className="select-default"
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="nauseas_vomitos" className="label-styled">Náuseas o vómitos</label>
                                <select
                                    id="nauseas_vomitos"
                                    name="nauseas_vomitos"
                                    value={formData.nauseas_vomitos}
                                    onChange={handleInputChange}
                                    className="select-default"
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="fotofobia" className="label-styled">Sensibilidad a la luz</label>
                                <select
                                    id="fotofobia"
                                    name="fotofobia"
                                    value={formData.fotofobia}
                                    onChange={handleInputChange}
                                    className="select-default"
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="fonofobia" className="label-styled">Sensibilidad al sonido</label>
                                <select
                                    id="fonofobia"
                                    name="fonofobia"
                                    value={formData.fonofobia}
                                    onChange={handleInputChange}
                                    className="select-default"
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="presencia_aura" className="label-styled">Presencia de aura</label>
                                <select
                                    id="presencia_aura"
                                    name="presencia_aura"
                                    value={formData.presencia_aura}
                                    onChange={handleInputChange}
                                    className="select-default"
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="sintomas_aura" className="label-styled">Síntomas del aura</label>
                                <select
                                    id="sintomas_aura"
                                    name="sintomas_aura"
                                    value={formData.sintomas_aura}
                                    onChange={handleInputChange}
                                    className="select-default"
                                >
                                    <option value="">Seleccione una opción</option>
                                    <option value="Ninguno">Ninguno</option>
                                    <option value="Visuales">Visuales</option>
                                    <option value="Sensitivos">Sensitivos</option>
                                    <option value="De habla o lenguaje">De habla o lenguaje</option>
                                    <option value="Motores">Motores</option>
                                    <option value="Troncoencefálicos">Troncoencefálicos</option>
                                    <option value="Retinianos">Retinianos</option>
                                    <option value="Visuales, Sensitivos">Visuales, Sensitivos</option>
                                </select>
                            </div>

                            <div className="form-field">
                                <label htmlFor="duracion_aura_minutos" className="label-styled">Duración del aura (min)</label>
                                <input
                                    type="number"
                                    id="duracion_aura_minutos"
                                    name="duracion_aura_minutos"
                                    placeholder="Ej: 30"
                                    min="0"
                                    max="120"
                                    value={formData.duracion_aura_minutos}
                                    onChange={handleInputChange}
                                    className="input-default"
                                />
                            </div>

                            {/* Campos específicos para mujeres */}
                            {userInfo && userInfo.genero === 'F' && (
                                <>
                                    <div className="form-field">
                                        <label htmlFor="en_menstruacion" className="label-styled">En menstruación</label>
                                        <select
                                            id="en_menstruacion"
                                            name="en_menstruacion"
                                            value={formData.en_menstruacion}
                                            onChange={handleInputChange}
                                            className="select-default"
                                        >
                                            <option value="">Seleccione una opción</option>
                                            <option value="Sí">Sí</option>
                                            <option value="No">No</option>
                                        </select>
                                    </div>

                                    <div className="form-field">
                                        <label htmlFor="anticonceptivos" className="label-styled">Anticonceptivos</label>
                                        <select
                                            id="anticonceptivos"
                                            name="anticonceptivos"
                                            value={formData.anticonceptivos}
                                            onChange={handleInputChange}
                                            className="select-default"
                                        >
                                            <option value="">Seleccione una opción</option>
                                            <option value="Sí">Sí</option>
                                            <option value="No">No</option>
                                        </select>
                                    </div>
                                </>
                            )}
                        </div>

                        <div className="form-buttons">
                            <button type="submit" className="btn-primary" disabled={loading}>
                                {loading ? 'Guardando...' : 'Registrar'}
                            </button>
                            <button type="button" className="btn-cancel" onClick={handleCancel} disabled={loading}>
                                Cancelar
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
}
