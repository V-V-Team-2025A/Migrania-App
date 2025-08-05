import { useEffect, useState } from "react";
import TablaExpandible from "../components/TablaExpandible";

export default function MidasMedico() {

    const [autoevaluaciones, setAutoevaluaciones] = useState()
    const token = localStorage.getItem("access");
    useEffect(() => {
        const fetchAutoevaluaciones = async () => {
            try {

                const response = await fetch('https://migrania-app-pruebas-production-1be5.up.railway.app/api/evaluaciones/autoevaluaciones/', {
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