import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from "../../common/styles/dashboardPaciente.module.css";
import { BellIcon, StethoscopeIcon, ChartLineIcon, FilesIcon, PillIcon, PlusIcon, BrainIcon, SignOut } from "@phosphor-icons/react";
import { 
    parseApiResponse, 
    getApiUrl, 
    getAuthHeaders,
    fetchEpisodiosPaciente 
} from "../../features/feature_Grupo2_BitacoraAsistidaCefalea/utils/apiUtils.js";
import { transformEpisodio } from "../../features/feature_Grupo2_BitacoraAsistidaCefalea/utils/episodioUtils.js";
import { EPISODIOS_ENDPOINT } from "../../features/feature_Grupo2_BitacoraAsistidaCefalea/utils/constants.js";

const TARJETAS_DASHBOARD = [
    {
        icono: PlusIcon,
        color: "#c9525aff",
        backgroundColor: "#c42d3750",
        titulo: "Bitácora",
        descripcion: "Mira y registra un nuevo episodio de migraña."
    },
    {
        icono: FilesIcon,
        color: "#a555ebff",
        backgroundColor: "#9f58dd59",
        titulo: "Evaluación MIDAS",
        descripcion: "Evalúa el impacto de la migraña en tu vida diaria."
    },
    {
        icono: PillIcon,
        color: "#4c84f3ff",
        backgroundColor: "#3e68be50",
        titulo: "Mis tratamientos",
        descripcion: "Revisa tus tratamientos actuales."
    },
    {
        icono: ChartLineIcon,
        color: "#42b668ff",
        backgroundColor: "#3588517d",
        titulo: "Mi progreso",
        descripcion: "Visualiza tendencias y estadísticas."
    },
    {
        icono: BrainIcon,
        color: "#f39a4cff",
        backgroundColor: "#be713e50",
        titulo: "Mis patrones",
        descripcion: "Revisa tus patrones semanales."
    }
];

export default function Dashboard() {
    const navigate = useNavigate();
    const [episodiosRecientes, setEpisodiosRecientes] = useState([]);
    const [cargandoEpisodios, setCargandoEpisodios] = useState(true);
    const [errorEpisodios, setErrorEpisodios] = useState(null);

    const procesarEpisodios = (episodios) => {
        if (!Array.isArray(episodios)) {
            throw new Error('Formato de datos incorrecto recibido de la API');
        }

        return episodios
            .filter(episodio => episodio && episodio.creado_en)
            .sort((a, b) => new Date(b.creado_en) - new Date(a.creado_en))
            .slice(0, 4);
    };

    useEffect(() => {
        const cargarEpisodiosRecientes = async () => {
            try {
                setCargandoEpisodios(true);
                setErrorEpisodios(null);

                const episodiosArray = await fetchEpisodiosPaciente();
                const episodiosTransformados = episodiosArray.map(transformEpisodio);
                const episodiosOrdenados = procesarEpisodios(episodiosTransformados);
                
                setEpisodiosRecientes(episodiosOrdenados);
            } catch (error) {
                console.error('Error al cargar episodios recientes:', error);
                setErrorEpisodios(error.message || 'Error al cargar episodios');
            } finally {
                setCargandoEpisodios(false);
            }
        };

        cargarEpisodiosRecientes();
    }, []);

    const handleNavegacion = (ruta) => {
        navigate(ruta);
    };

    const handleNavegacionMidas = async () => {
    const token = localStorage.getItem("access");

    try {
        const response = await fetch("https://migrania-app-pruebas-production.up.railway.app/api/evaluaciones/autoevaluaciones/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({}),
        });

        const data = await response.json();

        if (!response.ok) {
            if (data.detail === "No disponible") {
                navigate("/midas", {
                    state: {
                        puedeHacerAutoevaluacion: false,
                        idAutoevaluacion: null
                    }
                });
                return;
            } else {
                console.error("Error inesperado:", data);
                return;
            }
        }

        // Si llegamos aquí, la respuesta fue exitosa
        const idAutoevaluacion = data.id;

        navigate("/midas", {
            state: {
                puedeHacerAutoevaluacion: true,
                idAutoevaluacion: idAutoevaluacion,
            }
        });

    } catch (error) {
        console.error("Error en la petición:", error);
    }
};

    const handleLogout = () => {
        // Eliminar tokens del localStorage
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        
        // Opcional: también eliminar cualquier otro dato de sesión
        localStorage.removeItem("user");
        localStorage.removeItem("userType");
        
        // Redirigir al login
        navigate("/login", { replace: true });
    };


    const TarjetaDashboard = ({ icono: Icono, color, backgroundColor, titulo, descripcion, onClick }) => (
        <div
            className={styles["dashboard__tarjeta"]}
            onClick={onClick}
            style={{ cursor: onClick ? 'pointer' : 'default' }}
        >
            <div className={styles["dashboard__icono"]} style={{ backgroundColor }}>
                <Icono size={32} color={color} />
            </div>
            <h4>{titulo}</h4>
            <p>{descripcion}</p>
        </div>
    );

    const EstadoCarga = ({ cargando, error, vacio, textoVacio = "No hay datos disponibles" }) => {
        if (cargando) {
            return <div style={{ textAlign: 'center', padding: '20px', color: 'var(--color-secondary-dark)' }}>Cargando...</div>;
        }

        if (error) {
            return <div style={{ textAlign: 'center', padding: '20px', color: '#e74c3c' }}>Error: {error}</div>;
        }

        if (vacio) {
            return <div style={{ textAlign: 'center', padding: '20px', color: 'var(--color-secondary-dark)' }}>{textoVacio}</div>;
        }

        return null;
    };

    const DetalleEpisodio = ({ icono, texto }) => (
        <div className={styles["dashboard__episodio-detalle"]}>
            <div className={styles["dashboard__episodio-detalle-icono"]}>{icono}</div>
            <span className={styles["dashboard__episodio-detalle-texto"]}>{texto}</span>
        </div>
    );

    const EpisodioItem = ({ episodio, index }) => {
        // Usar directamente la fecha formateada que viene de transformEpisodio
        const fechaFormateada = episodio.creado_en;
        const severidadClass = episodio.severidad
            ? styles[`dashboard__episodio-severidad--${episodio.severidad.toLowerCase()}`]
            : '';

        return (
            <div key={episodio.id || index} className={styles["dashboard__episodio-item"]}>
                <div className={styles["dashboard__episodio-fecha"]}>{fechaFormateada}</div>
                <div className={styles["dashboard__episodio-contenido"]}>
                    <div className={styles["dashboard__episodio-header"]}>
                        <div className={`${styles["dashboard__episodio-severidad"]} ${severidadClass}`}>
                            {episodio.severidad || 'N/A'}
                        </div>
                    </div>
                    <div className={styles["dashboard__episodio-detalles"]}>
                        <DetalleEpisodio icono="⏱" texto={episodio.duracion_cefalea_horas ? `${episodio.duracion_cefalea_horas}h` : 'N/A'} />
                        {episodio.localizacion && <DetalleEpisodio icono="📍" texto={episodio.localizacion} />}
                        {episodio.caracter_dolor && (
                            <DetalleEpisodio icono="💫" texto={episodio.caracter_dolor} />
                        )}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <>
            <div className={styles["dashboard__cabecera"]}>
                <div>
                    <h2>¿Cómo te sientes hoy?</h2>
                    <p>¡Vas 5 días sin episodios! Sigue cuidándote y registrando tus síntomas.</p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <BellIcon size={32} color="var(--color-text)" />
                    <button 
                        onClick={handleLogout}
                        style={{
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            padding: '8px',
                            borderRadius: '6px',
                            transition: 'background-color 0.2s',
                            backgroundColor: 'transparent'
                        }}
                        onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--color-background-light)'}
                        onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                        title="Cerrar sesión"
                    >
                        <SignOut size={32} color="var(--color-text)" />
                    </button>
                </div>
            </div>

            <section className={styles["dashboard__contenedor-tarjetas"]}>
                <TarjetaDashboard {...TARJETAS_DASHBOARD[0]} onClick={() => handleNavegacion('/bitacora-paciente')} />

                <TarjetaDashboard {...TARJETAS_DASHBOARD[1]} onClick={() => handleNavegacionMidas()} />
                <TarjetaDashboard {...TARJETAS_DASHBOARD[2]} onClick={() => handleNavegacion('/tratamientos')} />
                <TarjetaDashboard {...TARJETAS_DASHBOARD[3]} onClick={() => handleNavegacion('/estadisticas')} />
                <TarjetaDashboard {...TARJETAS_DASHBOARD[4]} onClick={() => handleNavegacion('/analisis-patrones')} />
            </section>

            <div className={styles["dashboard__seccion-inferior"]}>
                <section className={styles["dashboard__episodios-recientes"]}>
                    <h4>Episodios recientes</h4>

                    <EstadoCarga
                        cargando={cargandoEpisodios}
                        error={errorEpisodios}
                        vacio={episodiosRecientes.length === 0}
                        textoVacio="No hay episodios registrados"
                    />

                    {!cargandoEpisodios && !errorEpisodios && episodiosRecientes.length > 0 && (
                        <div className={styles["dashboard__lista-episodios"]}>
                            {episodiosRecientes.map((episodio, index) => (
                                <EpisodioItem key={episodio.id || index} episodio={episodio} index={index} />
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

                    <button className="btn-primary" onClick={() => navigate("/formulario-cita")}>Agendar</button>
                </section>
            </div>
        </>
    );
}
