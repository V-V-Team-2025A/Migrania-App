import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import './common/styles/normalize.css'
import "./common/styles/index.css"

import Login from './pages/Login.jsx'
import MedicalDashboard from './pages/Estadisticas-Medico.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<MedicalDashboard/>}/>
      </Routes>
    </Router>
  </StrictMode>,
)
