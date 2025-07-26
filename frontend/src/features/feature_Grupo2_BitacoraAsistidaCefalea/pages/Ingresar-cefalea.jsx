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

            <div style={{
                backgroundColor: 'var(--color-background)',
                padding: 'var(--spacing-xl)',
                borderRadius: 'var(--border-radius)',
                marginTop: 'var(--spacing-l)'
            }}>
                <h2 style={{ marginBottom: 'var(--spacing-l)', textAlign: 'center' }}>
                    Registrar nuevo episodio
                </h2>

                <form onSubmit={handleSubmit}>
                    <div style={{ display: 'grid', gap: 'var(--spacing-m)' }}>

                        <div>
                            <label htmlFor="duracion_cefalea_horas">Duración (h)</label>
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

                        <div>
                            <label htmlFor="fecha_episodio">Fecha del episodio</label>
                            <input
                                type="date"
                                id="fecha_episodio"
                                name="fecha_episodio"
                                value={formData.fecha_episodio}
                                onChange={handleInputChange}
                                className="input-default"
                                style={{ padding: 'var(--spacing-s)', borderRadius: 'var(--border-radius)', border: 'none' }}
                            />
                        </div>

                        <div>
                            <label htmlFor="severidad">Severidad</label>
                            <select
                                id="severidad"
                                name="severidad"
                                value={formData.severidad}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Leve">Leve</option>
                                <option value="Moderada">Moderada</option>
                                <option value="Severa">Severa</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="caracter_dolor">Carácter</label>
                            <select
                                id="caracter_dolor"
                                name="caracter_dolor"
                                value={formData.caracter_dolor}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Pulsátil">Pulsátil</option>
                                <option value="Opresivo">Opresivo</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="localizacion">Localización</label>
                            <select
                                id="localizacion"
                                name="localizacion"
                                value={formData.localizacion}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Unilateral">Unilateral</option>
                                <option value="Bilateral">Bilateral</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="empeora_actividad">Empeora con actividad</label>
                            <select
                                id="empeora_actividad"
                                name="empeora_actividad"
                                value={formData.empeora_actividad}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Sí">Sí</option>
                                <option value="No">No</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="nauseas_vomitos">Náuseas o vómitos</label>
                            <select
                                id="nauseas_vomitos"
                                name="nauseas_vomitos"
                                value={formData.nauseas_vomitos}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Sí">Sí</option>
                                <option value="No">No</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="fotofobia">Sensibilidad a la luz</label>
                            <select
                                id="fotofobia"
                                name="fotofobia"
                                value={formData.fotofobia}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Sí">Sí</option>
                                <option value="No">No</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="fonofobia">Sensibilidad al sonido</label>
                            <select
                                id="fonofobia"
                                name="fonofobia"
                                value={formData.fonofobia}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Sí">Sí</option>
                                <option value="No">No</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="presencia_aura">Presencia de aura</label>
                            <select
                                id="presencia_aura"
                                name="presencia_aura"
                                value={formData.presencia_aura}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Sí">Sí</option>
                                <option value="No">No</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="sintomas_aura">Síntomas del aura</label>
                            <select
                                id="sintomas_aura"
                                name="sintomas_aura"
                                value={formData.sintomas_aura}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Ninguno">Ninguno</option>
                                <option value="Visuales, Sensitivos">Visuales, Sensitivos</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="duracion_aura_minutos">Duración del aura (min)</label>
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

                        <div>
                            <label htmlFor="en_menstruacion">En menstruación</label>
                            <select
                                id="en_menstruacion"
                                name="en_menstruacion"
                                value={formData.en_menstruacion}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Si">Si</option>
                                <option value="No">No</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="anticonceptivos">Anticonceptivos</label>
                            <select
                                id="anticonceptivos"
                                name="anticonceptivos"
                                value={formData.anticonceptivos}
                                onChange={handleInputChange}
                                style={{
                                    width: '100%',
                                    padding: 'var(--spacing-s)',
                                    borderRadius: 'var(--border-radius)',
                                    border: 'none',
                                    backgroundColor: '#fff'
                                }}
                            >
                                <option value="">Seleccione una opción</option>
                                <option value="Si">Si</option>
                                <option value="No">No</option>
                            </select>
                        </div>
                    </div>

                    <div style={{
                        display: 'flex',
                        gap: 'var(--spacing-m)',
                        marginTop: 'var(--spacing-xl)',
                        justifyContent: 'center'
                    }}>
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
