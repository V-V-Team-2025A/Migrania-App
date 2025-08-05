import { useEffect, useState } from "react";
import TablaExpandible from "../components/TablaExpandible";

export default function MidasMedico() {

    return <div>
        <h1>Autoevaluaciones Pasadas</h1>
        <TablaExpandible data={autoevaluaciones} />

    </div>
}