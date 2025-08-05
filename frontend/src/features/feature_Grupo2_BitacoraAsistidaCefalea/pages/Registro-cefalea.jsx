import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header.jsx';
import styles from '../styles/bitacora.module.css';
import { INITIAL_FORM_DATA } from '../utils/constants.js';
import { fetchUserInfoPaciente, createEpisodioPaciente, getErrorMessage } from '../utils/apiUtils.js';
import { transformFormDataForAPI, validateEpisodioForm } from '../utils/episodioUtils.js';

export default function IngresarCefalea() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState(INITIAL_FORM_DATA);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const [userInfo, setUserInfo] = useState(null);
    const [loadingUser, setLoadingUser] = useState(true);

    useEffect(() => {
        const loadUserInfo = async () => {
            try {
                setLoadingUser(true);
                const userData = await fetchUserInfoPaciente();
                setUserInfo(userData);
            } catch (err) {
                console.error('Error al obtener información del usuario:', err);
                setUserInfo({ genero: 'F', nombre_completo: 'Usuario' });
            } finally {
                setLoadingUser(false);
            }
        };

        loadUserInfo();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;

        let updatedFormData = { ...formData, [name]: value };

        if (name === 'presencia_aura' && value === 'No') {
            updatedFormData = {
                ...updatedFormData,
                sintomas_aura: '',
                duracion_aura_minutos: ''
            };
        }

        setFormData(updatedFormData);

        if (error && error.includes(name)) {
            setError(null);
        }
    };

    const resetForm = () => {
        setFormData(INITIAL_FORM_DATA);
    };

    const showSuccessAndReset = () => {
        setSuccess(true);
        resetForm();
        setTimeout(() => {
            setSuccess(false);
        }, 3000);
    };

    const validateForm = () => {
        const errors = [];

        if (!formData.duracion_cefalea_horas) {
            errors.push('La duración es requerida');
        } else if (formData.duracion_cefalea_horas < 1 || formData.duracion_cefalea_horas > 72) {
            errors.push('La duración debe estar entre 1 y 72 horas');
        }

        if (!formData.severidad) {
            errors.push('La severidad es requerida');
        }

        if (!formData.caracter_dolor) {
            errors.push('El carácter del dolor es requerido');
        }

        if (!formData.localizacion) {
            errors.push('La localización es requerida');
        }

        if (!formData.empeora_actividad) {
            errors.push('El campo "Empeora con actividad" es requerido');
        }

        if (!formData.nauseas_vomitos) {
            errors.push('El campo "Náuseas o vómitos" es requerido');
        }

        if (!formData.fotofobia) {
            errors.push('El campo "Sensibilidad a la luz" es requerido');
        }

        if (!formData.fonofobia) {
            errors.push('El campo "Sensibilidad al sonido" es requerido');
        }

        if (!formData.presencia_aura) {
            errors.push('El campo "Presencia de aura" es requerido');
        }

        if (formData.presencia_aura === 'Sí') {
            if (!formData.sintomas_aura) {
                errors.push('Los síntomas del aura son requeridos cuando hay presencia de aura');
            }
            if (!formData.duracion_aura_minutos) {
                errors.push('La duración del aura es requerida cuando hay presencia de aura');
            } else if (formData.duracion_aura_minutos < 0 || formData.duracion_aura_minutos > 120) {
                errors.push('La duración del aura debe estar entre 0 y 120 minutos');
            }
        }

        if (userInfo?.genero !== 'M') {
            if (!formData.en_menstruacion) {
                errors.push('El campo "En menstruación" es requerido');
            }

            if (!formData.anticonceptivos) {
                errors.push('El campo "Anticonceptivos" es requerido');
            }
        }

        if (formData.duracion_aura_minutos && (isNaN(formData.duracion_aura_minutos) || formData.duracion_aura_minutos < 0)) {
            errors.push('La duración del aura debe ser un número positivo');
        }

        if (isNaN(formData.duracion_cefalea_horas) || formData.duracion_cefalea_horas <= 0) {
            errors.push('La duración de la cefalea debe ser un número positivo');
        }

        return errors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const validationErrors = validateForm();
        if (validationErrors.length > 0) {
            setError(validationErrors.join('. '));
            return;
        }

        try {
            setLoading(true);
            setError(null);
            setSuccess(false);

            validateEpisodioForm(formData);
            const apiData = transformFormDataForAPI(formData, userInfo);

            console.log('Datos del formulario original:', formData);
            console.log('Datos transformados para la API:', apiData);

            const responseData = await createEpisodioPaciente(apiData);
            console.log('Episodio creado exitosamente:', responseData);
            showSuccessAndReset();

        } catch (err) {
            console.error('Error al crear episodio:', err);
            setError(getErrorMessage(err));
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        navigate('/bitacora-paciente');
    };

    const renderLoadingState = () => (
        <div className={styles.loading}>
            Cargando información del usuario...
        </div>
    );

    const renderSubmissionState = () => (
        <>
            {loading && (
                <div className={styles.loading}>
                    Guardando episodio...
                </div>
            )}

            {error && (
                <div className={styles.error}>
                    {error}
                </div>
            )}

            {success && (
                <div className={styles.success}>
                    ¡Episodio registrado exitosamente!
                </div>
            )}
        </>
    );

    return (
        <div>
            <Header
                title="Bitácora"
                onBack={() => navigate('/bitacora-paciente')}
            />

            <div className={styles.formContainer}>
                <h2 className={styles.formTitle}>
                    Registrar nuevo episodio
                </h2>

                {loadingUser && renderLoadingState()}
                {renderSubmissionState()}

                {!loadingUser && userInfo && (
                    <form onSubmit={handleSubmit}>
                        <div className={styles.formGrid}>

                            <div className={styles.formField}>
                                <label htmlFor="duracion_cefalea_horas" className={styles.labelStyled}>Duración (h)</label>
                                <input
                                    type="number"
                                    id="duracion_cefalea_horas"
                                    name="duracion_cefalea_horas"
                                    placeholder="Ej: 5"
                                    min="1"
                                    max="72"
                                    value={formData.duracion_cefalea_horas}
                                    onChange={handleInputChange}
                                    className={styles.inputDefault}
                                    required
                                />
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="severidad" className={styles.labelStyled}>Severidad</label>
                                <select
                                    id="severidad"
                                    name="severidad"
                                    value={formData.severidad}
                                    onChange={handleInputChange}
                                    className={styles.selectDefault}
                                    required
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Leve">Leve</option>
                                    <option value="Moderada">Moderada</option>
                                    <option value="Severa">Severa</option>
                                </select>
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="caracter_dolor" className={styles.labelStyled}>Carácter</label>
                                <select
                                    id="caracter_dolor"
                                    name="caracter_dolor"
                                    value={formData.caracter_dolor}
                                    onChange={handleInputChange}
                                    className={styles.selectDefault}
                                    required
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Pulsátil">Pulsátil</option>
                                    <option value="Opresivo">Opresivo</option>
                                    <option value="Punzante">Punzante</option>
                                </select>
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="localizacion" className={styles.labelStyled}>Localización</label>
                                <select
                                    id="localizacion"
                                    name="localizacion"
                                    value={formData.localizacion}
                                    onChange={handleInputChange}
                                    className={styles.selectDefault}
                                    required
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Unilateral">Unilateral</option>
                                    <option value="Bilateral">Bilateral</option>
                                </select>
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="empeora_actividad" className={styles.labelStyled}>Empeora con actividad</label>
                                <select
                                    id="empeora_actividad"
                                    name="empeora_actividad"
                                    value={formData.empeora_actividad}
                                    onChange={handleInputChange}
                                    className={`${styles.selectDefault} ${formData.empeora_actividad === '' ? styles.selectPlaceholder : ''}`}
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="nauseas_vomitos" className={styles.labelStyled}>Náuseas o vómitos</label>
                                <select
                                    id="nauseas_vomitos"
                                    name="nauseas_vomitos"
                                    value={formData.nauseas_vomitos}
                                    onChange={handleInputChange}
                                    className={`${styles.selectDefault} ${formData.nauseas_vomitos === '' ? styles.selectPlaceholder : ''}`}
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="fotofobia" className={styles.labelStyled}>Sensibilidad a la luz</label>
                                <select
                                    id="fotofobia"
                                    name="fotofobia"
                                    value={formData.fotofobia}
                                    onChange={handleInputChange}
                                    className={`${styles.selectDefault} ${formData.fotofobia === '' ? styles.selectPlaceholder : ''}`}
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="fonofobia" className={styles.labelStyled}>Sensibilidad al sonido</label>
                                <select
                                    id="fonofobia"
                                    name="fonofobia"
                                    value={formData.fonofobia}
                                    onChange={handleInputChange}
                                    className={`${styles.selectDefault} ${formData.fonofobia === '' ? styles.selectPlaceholder : ''}`}
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            <div className={styles.formField}>
                                <label htmlFor="presencia_aura" className={styles.labelStyled}>Presencia de aura</label>
                                <select
                                    id="presencia_aura"
                                    name="presencia_aura"
                                    value={formData.presencia_aura}
                                    onChange={handleInputChange}
                                    className={`${styles.selectDefault} ${formData.presencia_aura === '' ? styles.selectPlaceholder : ''}`}
                                >
                                    <option value="" disabled>Seleccione una opción</option>
                                    <option value="Sí">Sí</option>
                                    <option value="No">No</option>
                                </select>
                            </div>

                            {formData.presencia_aura === 'Sí' && (
                                <>
                                    <div className={styles.formField}>
                                        <label htmlFor="sintomas_aura" className={styles.labelStyled}>Síntomas del aura</label>
                                        <select
                                            id="sintomas_aura"
                                            name="sintomas_aura"
                                            value={formData.sintomas_aura}
                                            onChange={handleInputChange}
                                            className={`${styles.selectDefault} ${formData.sintomas_aura === '' ? styles.selectPlaceholder : ''}`}
                                        >
                                            <option value="" disabled>Seleccione una opción</option>
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

                                    <div className={styles.formField}>
                                        <label htmlFor="duracion_aura_minutos" className={styles.labelStyled}>Duración del aura (min)</label>
                                        <input
                                            type="number"
                                            id="duracion_aura_minutos"
                                            name="duracion_aura_minutos"
                                            placeholder="Ej: 30"
                                            min="0"
                                            max="120"
                                            value={formData.duracion_aura_minutos}
                                            onChange={handleInputChange}
                                            className={styles.inputDefault}
                                            required
                                        />
                                    </div>
                                </>
                            )}

                            {userInfo?.genero !== 'M' && userInfo?.genero === 'F' && (
                                <>
                                    <div className={styles.formField}>
                                        <label htmlFor="en_menstruacion" className={styles.labelStyled}>En menstruación</label>
                                        <select
                                            id="en_menstruacion"
                                            name="en_menstruacion"
                                            value={formData.en_menstruacion}
                                            onChange={handleInputChange}
                                            className={`${styles.selectDefault} ${formData.en_menstruacion === '' ? styles.selectPlaceholder : ''}`}
                                        >
                                            <option value="" disabled>Seleccione una opción</option>
                                            <option value="Sí">Sí</option>
                                            <option value="No">No</option>
                                        </select>
                                    </div>

                                    <div className={styles.formField}>
                                        <label htmlFor="anticonceptivos" className={styles.labelStyled}>Anticonceptivos</label>
                                        <select
                                            id="anticonceptivos"
                                            name="anticonceptivos"
                                            value={formData.anticonceptivos}
                                            onChange={handleInputChange}
                                            className={`${styles.selectDefault} ${formData.anticonceptivos === '' ? styles.selectPlaceholder : ''}`}
                                        >
                                            <option value="" disabled>Seleccione una opción</option>
                                            <option value="Sí">Sí</option>
                                            <option value="No">No</option>
                                        </select>
                                    </div>
                                </>
                            )}
                        </div>

                        <div className={styles.formButtons}>
                            <button type="submit" className={styles.btnPrimary} disabled={loading}>
                                {loading ? 'Guardando...' : 'Registrar'}
                            </button>
                            <button type="button" className={styles.btnCancel} onClick={handleCancel} disabled={loading}>
                                Cancelar
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
}
