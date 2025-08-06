import { useState } from "react"
import styles from "../styles/MidasEstadisticas.module.css"
import { BookIcon, ChartLineUpIcon, PresentationChartIcon } from "@phosphor-icons/react"
import { LinearProgress, Typography, Box } from "@mui/material"
import { PieChart, Pie, Cell, Legend, ResponsiveContainer } from "recharts"

export default function MidasEstadisticas() {

    const [categoriaComun, setCategoriaComun] = useState(3)
    const [cantidadEvaluaciones, setCantidadEvaluaciones] = useState(5)
    const [puntuacionPromedio, setPuntuacionPromedio] = useState(8)
    const datosClasificaciones = [
        { nombre: "Leve", valor: 3 },
        { nombre: "Moderado", valor: 5 },
        { nombre: "Grave", valor: 2 },
        { nombre: "Muy grave", valor: 1 },
    ]

    const colores = ["#4caf50", "#ff9800", "#f44336", "#9c27b0"]

    const respuestasPromedio = [
        { pregunta: "Dolor cabeza 1", valor: 70 },
        { pregunta: "Dolor cabeza 2", valor: 40 },
        { pregunta: "Dolor cabeza 3", valor: 90 },
        { pregunta: "Dolor cabeza 4", valor: 60 },
        { pregunta: "Dolor cabeza 5", valor: 50 },
    ]

    return <div>
        <h1>Estadísticas MIDAS</h1>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "var(--spacing-m)", marginBottom: "var(--spacing-m)" }}>
            <div className={styles["midas-estadisticas_tarjeta"]}>
                <BookIcon size={36}></BookIcon>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <p>Evaluaciones Registradas</p>
                    <p>{cantidadEvaluaciones}</p>
                </div>

            </div>
            <div className={styles["midas-estadisticas_tarjeta"]}>
                <ChartLineUpIcon size={36}></ChartLineUpIcon>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <p>Puntuación promedio</p>
                    <p>{puntuacionPromedio}</p>
                </div>
            </div>
            <div className={styles["midas-estadisticas_tarjeta"]}>
                <PresentationChartIcon size={36}></PresentationChartIcon>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <p>Categoría más común</p>
                    <p>{categoriaComun}</p>
                </div>

            </div>
        </div>
        <div style={{ display: "grid", gap: "var(--spacing-m)", gridTemplateColumns: "1fr 1fr" }}>
            <div className={styles["midas-estadisticas_tarjeta"]}>
                <h4>Respuestas promedio</h4>
                {respuestasPromedio.map((item, index) => (
                    <div className={styles["midas-estadisticas_barra-de-progreso"]}>
                        <Box key={index} sx={{ mb: 1 }}>
                            <Typography variant="body2" gutterBottom>{item.pregunta}</Typography>
                            <LinearProgress variant="determinate" value={item.valor} />
                        </Box>
                    </div>
                ))}
            </div>
            <div className={styles["midas-estadisticas_tarjeta"]} style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div style={{ width: "60%", height: 200 }}>
                    <ResponsiveContainer>
                        <PieChart>
                            <Pie
                                data={datosClasificaciones}
                                dataKey="valor"
                                nameKey="nombre"
                                cx="50%"
                                cy="50%"
                                outerRadius={80}
                                label
                            >
                                {datosClasificaciones.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={colores[index % colores.length]} />
                                ))}
                            </Pie>
                        </PieChart>
                    </ResponsiveContainer>
                </div>
                <div style={{ width: "35%" }}>
                    <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                        {datosClasificaciones.map((entry, index) => (
                            <li key={index} style={{ display: "flex", alignItems: "center", marginBottom: 8 }}>
                                <div style={{
                                    width: 12,
                                    height: 12,
                                    backgroundColor: colores[index % colores.length],
                                    marginRight: 8,
                                    borderRadius: 2
                                }}></div>
                                <span>{entry.nombre} ({entry.valor})</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

        </div>
    </div >
}