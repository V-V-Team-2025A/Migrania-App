import { useEffect, useState } from "react";
import TablaExpandible from "../components/TablaExpandible";

export default function MidasMedico() {

    const [autoevaluaciones, setAutoevaluaciones] = useState()
    const token = localStorage.getItem("access");
    useEffect(() => {
        const fetchAutoevaluaciones = async () => {
            try {

                const response = await fetch('http://localhost:8000/api/evaluaciones/autoevaluaciones/', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                });
                const data = await response.json();
                setAutoevaluaciones(data.results);
            } catch (error) {
                console.error('Error al obtener preguntas:', error);
            } finally {
            }
        };
        fetchAutoevaluaciones()
    }, []);

    return <div>
        <h1>Autoevaluaciones Pasadas</h1>
        <TablaExpandible data={autoevaluaciones} />

    </div>
}