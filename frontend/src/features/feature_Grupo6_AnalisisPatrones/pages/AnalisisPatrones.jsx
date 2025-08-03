import React from 'react';
import { useNavigate } from 'react-router-dom';
import TarjetaResumen from '../components/TarjetaResumen';
import TarjetaAnalisis from '../components/TarjetaAnalisis';
import styles from '../styles/AnalisisPatrones.module.css';
import { ArrowLeft, ChartLineUp, Warning } from '@phosphor-icons/react';

export default function AnalisisPatrones() {
    const navigate = useNavigate();


    const handleVolver = () => {

        navigate(-1);
    };
    return (
        <div className={styles.patrones}>
            { }
            { }
            <div className={styles.patrones__cabecera}>
                <button onClick={handleVolver} className={styles.patrones__botonVolver}>
                    <ArrowLeft size={24} />
                    Volver
                </button>
            </div>

            <main className={styles.patrones__contenido}>
                <section className={styles.patrones__resumen}>
                    <TarjetaResumen
                        titulo="Factores Identificados"
                        valor={15}
                        subtitulo="3 nuevos esta semana"
                        icono={<ChartLineUp size={48} weight="light" />}
                        color="secondary-light"
                    />
                    <TarjetaResumen
                        titulo="Alertas Preventivas"
                        valor={5}
                        subtitulo="Activas ahora"
                        icono={<Warning size={48} weight="light" />}
                        color="secondary-dark"
                        iconColor="var(--color-error)"
                    />
                </section>

                <section className={styles.patrones__analisis}>
                    <TarjetaAnalisis
                        icono={<Warning size={32} />}
                        titulo="Factores médicos"
                        descripcion="Tus episodios presentan síntomas clínicos frecuentes como sensibilidad a la luz y al sonido."
                        recomendacion="Considera consultar a un profesional de salud para una evaluación médica."
                    />
                    <TarjetaAnalisis
                        icono={<Warning size={32} />}
                        titulo="Recurrencia semanal"
                        descripcion="Se ha detectado un aumento de episodios de migraña severa los días martes, con dolor bilateral y pulsátil."
                        recomendacion="Evalúa tu rutina de lunes por la noche y martes por la mañana (sueño, alimentación, estrés)."
                    />
                </section>
            </main>
        </div>
    );
}