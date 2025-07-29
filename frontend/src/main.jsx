import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import "./common/styles/index.css"
import Midas from "./features/feature_Grupo1_EvaluacionMidas/pages/Midas.jsx"
import Resultados from "./features/feature_Grupo1_EvaluacionMidas/pages/Resultados.jsx"
import Dashboard from './pages/paciente/Dashboard.jsx'
import Login from './pages/Login.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Login />}/>
        <Route path="/dashboard-paciente" element={<Dashboard />}/>
        <Route path="/midas" element={<Midas />}/>
        <Route path="/midas/resultados" element={<Resultados />}/>
      </Routes>
    </Router>
  </StrictMode>,
)
