import React, { useState } from 'react';
import Header from '@/common/components/Header.jsx';

export default function IngresarCefalea() {
    const [formData, setFormData] = useState({
        duracion_cefalea_horas: '',
        fecha_episodio: '',
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

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Datos del episodio:', formData);
        // Aquí iría la lógica para enviar los datos
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

                <form onSubmit={handleSubmit}>
                    <div className="form-grid">

                        <div className="form-field">
                            <label htmlFor="duracion_cefalea_horas" className="label-styled">Duración (h)</label>
                            <input
                                type="text"
                                id="duracion_cefalea_horas"
                                name="duracion_cefalea_horas"
                                placeholder="Ej: 5"
                                value={formData.duracion_cefalea_horas}
                                onChange={handleInputChange}
                                className="input-default"
                            />
                        </div>

                        <div className="form-field">
                            <label htmlFor="fecha_episodio" className="label-styled">Fecha del episodio</label>
                            <input
                                type="date"
                                id="fecha_episodio"
                                name="fecha_episodio"
                                value={formData.fecha_episodio}
                                onChange={handleInputChange}
                                className="input-default input-date"
                            />
                        </div>

                        <div className="form-field">
                            <label htmlFor="severidad" className="label-styled">Severidad</label>
                            <select
                                id="severidad"
                                name="severidad"
                                value={formData.severidad}
                                onChange={handleInputChange}
                                className="select-default"
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Leve">Leve</option>
                                <option value="Moderada">Moderada</option>
                                <option value="Severa">Severa</option>
                            </select>
                        </div>

                        <div className="form-field">
                            <label htmlFor="caracter_dolor" className="label-styled">Carácter</label>
                            <select
                                id="caracter_dolor"
                                name="caracter_dolor"
                                value={formData.caracter_dolor}
                                onChange={handleInputChange}
                                className="select-default"
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Pulsátil">Pulsátil</option>
                                <option value="Opresivo">Opresivo</option>
                            </select>
                        </div>

                        <div className="form-field">
                            <label htmlFor="localizacion" className="label-styled">Localización</label>
                            <select
                                id="localizacion"
                                name="localizacion"
                                value={formData.localizacion}
                                onChange={handleInputChange}
                                className="select-default"
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
                                <option value="Visuales, Sensitivos">Visuales, Sensitivos</option>
                            </select>
                        </div>

                        <div className="form-field">
                            <label htmlFor="duracion_aura_minutos" className="label-styled">Duración del aura (min)</label>
                            <input
                                type="text"
                                id="duracion_aura_minutos"
                                name="duracion_aura_minutos"
                                placeholder="Ej: 30"
                                value={formData.duracion_aura_minutos}
                                onChange={handleInputChange}
                                className="input-default"
                            />
                        </div>

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
                                <option value="Si">Si</option>
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
                                <option value="Si">Si</option>
                                <option value="No">No</option>
                            </select>
                        </div>
                    </div>

                    <div className="form-buttons">
                        <button type="submit" className="btn-primary">
                            Registrar
                        </button>
                        <button type="button" className="btn-cancel" onClick={handleCancel}>
                            Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
