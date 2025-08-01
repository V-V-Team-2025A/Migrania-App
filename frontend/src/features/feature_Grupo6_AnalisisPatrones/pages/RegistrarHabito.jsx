import React, { useState } from 'react';
import styles from '../styles/RegistrarHabito.module.css';
import { ArrowLeft, CalendarBlank } from '@phosphor-icons/react';

export default function RegistrarHabito() {
    const [formData, setFormData] = useState({
        duracion: '',
        fecha: '',
        severidad1: '', 
        caracter: '',
        localizacion: '',
        severidad2: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Datos del formulario a enviar:', formData);
        
    };

    const opcionesSeveridad = ['Leve', 'Moderada', 'Severa'];
    const opcionesCaracter = ['Pulsátil', 'Opresivo', 'Constante'];
    const opcionesLocalizacion = ['Unilateral', 'Bilateral', 'Occipital'];

    return (
        <div className={styles.episodio}>
            <header className={styles.episodio__cabecera}>
                <button className={styles.episodio__botonVolver}>
                    <ArrowLeft size={32} />
                    Volver
                </button>
                <h1 className={styles.episodio__tituloPrincipal}>Bitácora</h1>
            </header>

            <main className={styles.episodio__contenido}>
                <div className={styles.formularioContenedor}>
                    <h2 className={styles.formularioContenedor__titulo}>Registrar nuevo habito</h2>
                    
                    <form onSubmit={handleSubmit} className={styles.formulario}>
                        
                        <div className={styles.formulario__grupo}>
                            <label htmlFor="duracion">Duración (h)</label>
                            <input type="number" id="duracion" name="duracion" value={formData.duracion} onChange={handleChange} placeholder="Ej: 5" />
                        </div>

                      
                        <div className={styles.formulario__grupo}>
                            <label htmlFor="fecha">Fecha del episodio</label>
                            <div className={styles.inputConIcono}>
                                <input type="date" id="fecha" name="fecha" value={formData.fecha} onChange={handleChange} />
                                <CalendarBlank size={20} className={styles.inputConIcono__icono} />
                            </div>
                        </div>

                        
                        <div className={styles.formulario__grupo}>
                            <label htmlFor="severidad1">Severidad</label>
                            <select id="severidad1" name="severidad1" value={formData.severidad1} onChange={handleChange}>
                                <option value="" disabled>Seleccione una opción</option>
                                {opcionesSeveridad.map(op => <option key={op} value={op}>{op}</option>)}
                            </select>
                        </div>
                        
                        
                        <div className={styles.formulario__grupo}>
                            <label htmlFor="caracter">Carácter</label>
                            <select id="caracter" name="caracter" value={formData.caracter} onChange={handleChange}>
                                <option value="" disabled>Seleccione una opción</option>
                                {opcionesCaracter.map(op => <option key={op} value={op}>{op}</option>)}
                            </select>
                        </div>

                        
                        <div className={styles.formulario__grupo}>
                            <label htmlFor="localizacion">Localización</label>
                            <select id="localizacion" name="localizacion" value={formData.localizacion} onChange={handleChange}>
                                <option value="" disabled>Seleccione una opción</option>
                                {opcionesLocalizacion.map(op => <option key={op} value={op}>{op}</option>)}
                            </select>
                        </div>

                        
                        <div className={styles.formulario__grupo}>
                            <label htmlFor="severidad2">Severidad</label>
                            <select id="severidad2" name="severidad2" value={formData.severidad2} onChange={handleChange}>
                                <option value="" disabled>Seleccione una opción</option>
                                {opcionesSeveridad.map(op => <option key={op} value={op}>{op}</option>)}
                            </select>
                        </div>
                        
                        <div className={styles.formulario__acciones}>
                            <button type="submit" className={styles.formulario__boton}>Registrar</button>
                            <button type="button" className={`${styles.formulario__boton} ${styles['formulario__boton--cancelar']}`}>Cancelar</button>
                        </div>
                    </form>
                </div>
            </main>
        </div>
    );
}