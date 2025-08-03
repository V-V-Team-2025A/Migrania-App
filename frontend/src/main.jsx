import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import './common/styles/normalize.css'
import "./common/styles/index.css"

import Login from './pages/Login.jsx'
import BDoctor from '@/features/feature_Grupo2_BitacoraAsistidaCefalea/pages/Bitacora-Medico.jsx'
import BPaciente from '@/features/feature_Grupo2_BitacoraAsistidaCefalea/pages/Bitacora-Paciente.jsx'

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/bitacora-medico/:pacienteId" element={<BDoctor />} />
                <Route path="/bitacora-paciente" element={<BPaciente />} />
            </Routes>
        </Router>
    </StrictMode>,
)
