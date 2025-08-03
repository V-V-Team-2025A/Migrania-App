import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import './common/styles/normalize.css'
import "./common/styles/index.css"

import Login from './pages/Login.jsx'
import PatientDashboard from './features/feature_Grupo4_EstadisticasHistorial/pages/Estadisticas-Paciente.jsx'
import MedicalDashboard from './features/feature_Grupo4_EstadisticasHistorial/pages/Estadisticas-Medico.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/medico" element={<MedicalDashboard/>}/>
        <Route path="/paciente" element={<PatientDashboard/>}/>
      </Routes>
    </Router>
  </StrictMode>,
)
