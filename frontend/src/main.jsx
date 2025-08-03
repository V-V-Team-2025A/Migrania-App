import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import './common/styles/normalize.css'
import "./common/styles/index.css"

import Midas from "./features/feature_Grupo1_EvaluacionMidas/pages/Midas.jsx"
import Resultados from "./features/feature_Grupo1_EvaluacionMidas/pages/Resultados.jsx"
import Dashboard from './pages/paciente/Dashboard.jsx'

import Login from './features/feature_Grupo6_AnalisisPatrones/pages/Login'
import AnalisisPatrones from './features/feature_Grupo6_AnalisisPatrones/pages/AnalisisPatrones'

import BDoctor from '@/features/feature_Grupo2_BitacoraAsistidaCefalea/pages/Bitacora-Medico.jsx'
import BPaciente from '@/features/feature_Grupo2_BitacoraAsistidaCefalea/pages/Bitacora-Paciente.jsx'
import Registro from '@/features/feature_Grupo2_BitacoraAsistidaCefalea/pages/Registro-cefalea.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/analisis-patrones" element={<AnalisisPatrones />} />
        <Route path="/bitacora-medico/:pacienteId" element={<BDoctor />} />
        <Route path="/bitacora-paciente" element={<BPaciente />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/dashboard-paciente" element={<Dashboard />} />
        <Route path="/midas" element={<Midas />} />
        <Route path="/midas/resultados" element={<Resultados />} />
      </Routes>
    </Router>
  </StrictMode>,
)
