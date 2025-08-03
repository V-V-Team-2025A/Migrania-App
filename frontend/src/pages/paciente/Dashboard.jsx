import { useState, useEffect } from 'react';
import styles from "../../common/styles/dashboardPaciente.module.css";
import { BellIcon,StethoscopeIcon, ChartLineIcon, FilesIcon, PillIcon, PlusIcon, BrainIcon} from "@phosphor-icons/react";
import { fetchEpisodiosPaciente } from "../../utils/apiUtils.js";
export default function Dashboard() {
    const [episodiosRecientes, setEpisodiosRecientes] = useState([]);
    const [cargandoEpisodios, setCargandoEpisodios] = useState(true);
    const [errorEpisodios, setErrorEpisodios] = useState(null);

    useEffect(() => {
        const cargarEpisodiosRecientes = async () => {
            try {
                setCargandoEpisodios(true);
                setErrorEpisodios(null);

                console.log('Iniciando carga de episodios...');
                const episodios = await fetchEpisodiosPaciente();
                console.log('Episodios recibidos de la API:', episodios);
                console.log('Tipo de datos recibidos:', typeof episodios);
                console.log('Es array?:', Array.isArray(episodios));
                console.log('Longitud:', episodios?.length);

                if (!Array.isArray(episodios)) {
                    console.error('Los episodios no son un array:', episodios);
                    setErrorEpisodios('Formato de datos incorrecto recibido de la API');
                    return;
                }

                // Ordenar por fecha más reciente y tomar solo los 4 primeros
                const episodiosOrdenados = episodios
                    .filter(episodio => {
                        console.log('Evaluando episodio:', episodio);
                        const tieneFecha = episodio && (
                            episodio.fecha_inicio ||
                            episodio.creado_en ||
                            episodio.fecha
                        );
                        console.log('Tiene fecha válida:', tieneFecha);
                        return tieneFecha;
                    })
                    .sort((a, b) => {
                        try {
                            // Obtener fechas con múltiples respaldos
                            let fechaA = a.fecha_inicio || a.creado_en || a.fecha;
                            let fechaB = b.fecha_inicio || b.creado_en || b.fecha;

                            console.log('Fecha A original:', fechaA);
                            console.log('Fecha B original:', fechaB);

                            // Limpiar fechas si tienen formato con coma
                            if (fechaA && typeof fechaA === 'string' && fechaA.includes(',')) {
                                fechaA = fechaA.split(',')[0].trim();
                            }
                            if (fechaB && typeof fechaB === 'string' && fechaB.includes(',')) {
                                fechaB = fechaB.split(',')[0].trim();
                            }

                            console.log('Fecha A limpia:', fechaA);
                            console.log('Fecha B limpia:', fechaB);

                            // Convertir a objetos Date
                            const dateA = new Date(fechaA);
                            const dateB = new Date(fechaB);

                            console.log('Date A:', dateA);
                            console.log('Date B:', dateB);

                            // Si alguna fecha es inválida, ponerla al final
                            if (isNaN(dateA.getTime())) {
                                console.log('Fecha A inválida');
                                return 1;
                            }
                            if (isNaN(dateB.getTime())) {
                                console.log('Fecha B inválida');
                                return -1;
                            }

                            const resultado = dateB.getTime() - dateA.getTime(); // Más reciente primero
                            console.log('Resultado comparación:', resultado);
                            return resultado;
                        } catch (error) {
                            console.error('Error al ordenar fechas:', error);
                            return 0;
                        }
                    })
                    .slice(0, 4);

                console.log('Episodios ordenados y filtrados:', episodiosOrdenados);
                setEpisodiosRecientes(episodiosOrdenados);
            } catch (error) {
                console.error('Error al cargar episodios recientes:', error);
                setErrorEpisodios(error.message);
            } finally {
                setCargandoEpisodios(false);
            }
        };

        cargarEpisodiosRecientes();
    }, []);

    const formatearFecha = (fechaString) => {
        if (!fechaString) {
            return 'Fecha no disponible';
        }

        try {
            // Manejar diferentes formatos de fecha
            let fechaLimpia = fechaString;

            // Si la fecha viene en formato "3/8/2025, 2:02:02 p. m.", extraer solo la parte de la fecha
            if (fechaString.includes(',')) {
                fechaLimpia = fechaString.split(',')[0].trim();
            }

            // Si es formato ISO (2025-08-03T19:02:02.165994Z), usarlo directamente
            const fecha = new Date(fechaLimpia);

            // Verificar si la fecha es válida
            if (isNaN(fecha.getTime())) {
                console.warn('Fecha inválida recibida:', fechaString);
                return 'Fecha inválida';
            }

            return fecha.toLocaleDateString('es-ES', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
        } catch (error) {
            console.error('Error al formatear fecha:', error, fechaString);
            return 'Error en fecha';
        }
    };

    const formatearFechaCompleta = (fechaString) => {
        if (!fechaString) {
            return 'Fecha no disponible';
        }

        try {
            // Manejar el formato "3/8/2025, 2:02:02 p. m."
            let fechaLimpia = fechaString.trim();

            // Si contiene coma, es probable que tenga formato de fecha y hora
            if (fechaString.includes(',')) {
                const [fechaParte, horaParte] = fechaString.split(',').map(s => s.trim());
                fechaLimpia = fechaParte;

                const fecha = new Date(fechaParte);
                if (isNaN(fecha.getTime())) {
                    return 'Fecha inválida';
                }

                return `${fecha.toLocaleDateString('es-ES')} ${horaParte}`;
            }

            const fecha = new Date(fechaLimpia);
            if (isNaN(fecha.getTime())) {
                return 'Fecha inválida';
            }

            return fecha.toLocaleDateString('es-ES', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
        } catch (error) {
            console.error('Error al formatear fecha completa:', error, fechaString);
            return 'Error en fecha';
        }
    };

    return (
        <>
            <div className={styles["dashboard__cabecera"]}>
                <div>
                    <h2>¿Cómo te sientes hoy?</h2>
                    <p>¡Vas 5 días sin episodios! Sigue cuidándote y registrando tus síntomas.</p>
                </div>
                <BellIcon size={32} color={"var(--color-text)"} />
            </div>
            <section className={styles["dashboard__contenedor-tarjetas"]}>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#c42d3750",
                        }}>
                        <PlusIcon size={32} color={"#c9525aff"} />
                    </div>
                    <h4>Registrar episodio</h4>
                    <p>Documenta un nuevo episodio de migraña.</p>
                </div>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#9f58dd59",
                        }}>
                        <FilesIcon size={32} color={"#a555ebff"} />
                    </div>
                    <h4>Evaluación MIDAS</h4>
                    <p>Evalúa el impacto de la migraña en tu vida diaria.</p>
                </div>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#3e68be50",
                        }}>
                        <PillIcon size={32} color={"#4c84f3ff"} />
                    </div>
                    <h4>Mis tratamientos</h4>
                    <p>Revisa tus tratamientos actuales.</p>
                </div>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#3588517d",
                        }}>
                        <ChartLineIcon size={32} color={"#42b668ff"} />
                    </div>
                    <h4>Mi progreso</h4>
                    <p>Visualiza tendencias y estadísticas.</p>
                </div>
                <div className={styles["dashboard__tarjeta"]}>
                    <div
                        className={styles["dashboard__icono"]}
                        style={{
                            backgroundColor: "#be713e50",
                        }}>
                        <BrainIcon size={32} color={"#f39a4cff"} />
                    </div>
                    <h4>Mis patrones</h4>
                    <p>Revisa tus patrones semanales.</p>
                </div>

            </section>

            <div className={styles["dashboard__seccion-inferior"]}>
                <section className={styles["dashboard__episodios-recientes"]}>
                    <h4>Episodios recientes</h4>

                    {cargandoEpisodios ? (
                        <div style={{ textAlign: 'center', padding: '20px', color: 'var(--color-secondary-dark)' }}>
                            Cargando episodios...
                        </div>
                    ) : errorEpisodios ? (
                        <div style={{ textAlign: 'center', padding: '20px', color: '#e74c3c' }}>
                            Error: {errorEpisodios}
                        </div>
                    ) : episodiosRecientes.length === 0 ? (
                        <div style={{ textAlign: 'center', padding: '20px', color: 'var(--color-secondary-dark)' }}>
                            No hay episodios registrados
                        </div>
                    ) : (
                        <div className={styles["dashboard__lista-episodios"]}>
                            {episodiosRecientes.map((episodio, index) => (
                                <div key={episodio.id || index} className={styles["dashboard__episodio-item"]}>
                                    <div className={styles["dashboard__episodio-fecha"]}>
                                        {formatearFecha(episodio.fecha_inicio || episodio.creado_en || episodio.fecha)}
                                    </div>
                                    <div className={styles["dashboard__episodio-contenido"]}>
                                        <div className={styles["dashboard__episodio-header"]}>
                                            <div
                                                className={`${styles["dashboard__episodio-severidad"]} ${episodio.severidad ?
                                                    styles[`dashboard__episodio-severidad--${episodio.severidad.toLowerCase()}`] :
                                                    ''
                                                    }`}
                                            >
                                                {episodio.severidad || 'N/A'}
                                            </div>
                                        </div>
                                        <div className={styles["dashboard__episodio-detalles"]}>
                                            <div className={styles["dashboard__episodio-detalle"]}>
                                                <div className={styles["dashboard__episodio-detalle-icono"]}>⏱</div>
                                                <span className={styles["dashboard__episodio-detalle-texto"]}>
                                                    {episodio.duracion_cefalea_horas ? `${episodio.duracion_cefalea_horas}h` : 'N/A'}
                                                </span>
                                            </div>
                                            {episodio.localizacion && (
                                                <div className={styles["dashboard__episodio-detalle"]}>
                                                    <div className={styles["dashboard__episodio-detalle-icono"]}>📍</div>
                                                    <span className={styles["dashboard__episodio-detalle-texto"]}>
                                                        {episodio.localizacion}
                                                    </span>
                                                </div>
                                            )}
                                            {episodio.caracter_dolor && (
                                                <div className={styles["dashboard__episodio-detalle"]}>
                                                    <div className={styles["dashboard__episodio-detalle-icono"]}>💫</div>
                                                    <span className={styles["dashboard__episodio-detalle-texto"]}>
                                                        {episodio.caracter_dolor}
                                                    </span>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </section>

                <section className={styles["dashboard__mi-medico"]}>
                    <h4>Mi médico</h4>

                    <div className={styles["dashboard__medico-info"]}>
                        <StethoscopeIcon size={64} />
                        <h4>Dr. Juan Pérez</h4>
                        <p>Especialista en Neurología</p>
                    </div>

                    <div>
                        <h4>Próxima cita:</h4>
                        <div style={{ color: "var(--color-secondary-dark)" }}>2025-10-22 - 10:00 AM</div>
                    </div>

                    <div>
                        <h4>Tratamiento actual:</h4>
                        <div style={{ color: "var(--color-secondary-dark)" }}>Propranolol 40mg</div>
                    </div>

                    <button className="btn-primary">Agendar</button>
                </section>
            </div>

        </>
    );
}
