import React, { useState, useEffect } from 'react';
import { FaSearch } from 'react-icons/fa';
import Header from '@/common/components/Header.jsx';
import { 
  useEstadisticas, 
  usePacientes, 
  useAnalisisPatrones, 
  usePromedioSemanal 
} from '../hooks/useEstadisticas';
import { 
  EstadisticasGenerales, 
  AnalisisPatrones, 
  PacienteSelector, 
  SummaryCards 
} from '../components/EstadisticasComponents';
import '../styles/EstadisticasMedico.css';

const EstadisticasMedico = () => {
  // Estados locales
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('General');
  const [activeSubcategory, setActiveSubcategory] = useState('Ver Estadísticas');
  const [selectedPacienteId, setSelectedPacienteId] = useState(null);
  const [selectedPaciente, setSelectedPaciente] = useState(null);

  // Hooks para datos
  const { pacientes, loading: loadingPacientes, error: errorPacientes } = usePacientes();
  const { estadisticas, loading: loadingEstadisticas, error: errorEstadisticas } = useEstadisticas(selectedPacienteId);
  const { analisisPatrones, loading: loadingPatrones, error: errorPatrones } = useAnalisisPatrones(selectedPacienteId);
  const { promedioSemanal, fetchPromedioSemanal } = usePromedioSemanal();

  const categories = ['General', 'MIDAS', 'Bitácora'];

  // Filtrar pacientes según término de búsqueda
  const filteredPacientes = pacientes.filter(paciente => 
    `${paciente.nombre} ${paciente.apellido}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    paciente.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Manejar selección de paciente
  const handlePacienteChange = (pacienteId) => {
    setSelectedPacienteId(pacienteId);
    const paciente = pacientes.find(p => p.id === parseInt(pacienteId));
    setSelectedPaciente(paciente);
  };

  // Calcular promedio semanal para los últimos 3 meses cuando se selecciona un paciente
  useEffect(() => {
    if (selectedPacienteId) {
      const fechaFin = new Date();
      const fechaInicio = new Date();
      fechaInicio.setMonth(fechaInicio.getMonth() - 3);
      
      fetchPromedioSemanal(
        selectedPacienteId,
        fechaInicio.toISOString().split('T')[0],
        fechaFin.toISOString().split('T')[0]
      );
    }
  }, [selectedPacienteId, fetchPromedioSemanal]);

  const handleVolver = () => {
    console.log('Volver clickeado');
  };

  const renderContent = () => {
    if (!selectedPacienteId) {
      return (
        <div className="no-data-container">
          <div className="no-data-title">Seleccione un paciente</div>
          <div className="no-data-subtitle">
            Seleccione un paciente para ver sus estadísticas y análisis
          </div>
        </div>
      );
    }

    if (activeCategory === 'General') {
      if (activeSubcategory === 'Ver Estadísticas') {
        return (
          <EstadisticasGenerales 
            estadisticas={estadisticas}
            loading={loadingEstadisticas}
            error={errorEstadisticas}
          />
        );
      } else if (activeSubcategory === 'Ver Historial') {
        return (
          <AnalisisPatrones 
            analisisPatrones={analisisPatrones}
            loading={loadingPatrones}
            error={errorPatrones}
          />
        );
      }
    } else if (activeCategory === 'MIDAS') {
      return (
        <div className="no-data-container">
          <div className="no-data-title">Funcionalidad MIDAS</div>
          <div className="no-data-subtitle">
            En desarrollo - Próximamente disponible
          </div>
        </div>
      );
    } else if (activeCategory === 'Bitácora') {
      return (
        <div className="no-data-container">
          <div className="no-data-title">Historial de Bitácora</div>
          <div className="no-data-subtitle">
            En desarrollo - Próximamente disponible
          </div>
        </div>
      );
    }

    return (
      <div className="no-data-container">
        <div className="no-data-title">No se encuentran registros</div>
        <div className="no-data-subtitle">
          Mostrando {activeSubcategory.toLowerCase()} de {activeCategory}
        </div>
      </div>
    );
  };

  return (
    <div className="estadisticas-container">
      <Header
        title="Historial y Estadísticas"
        onBack={handleVolver}
      />

      {/* Selector de Paciente */}
      <PacienteSelector
        pacientes={filteredPacientes}
        selectedPacienteId={selectedPacienteId}
        onPacienteChange={handlePacienteChange}
        loading={loadingPacientes}
        error={errorPacientes}
      />

      {/* Search Bar */}
      <div className="search-container">
        <FaSearch className="search-icon" size={18} />
        <input
          type="text"
          placeholder="Buscar paciente"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {/* Patient Summary Section */}
      {selectedPaciente && (
        <div>
          <h2 className="patient-title">
            Resumen de: {selectedPaciente.nombre} {selectedPaciente.apellido}
          </h2>
          
          {/* Summary Cards */}
          <SummaryCards 
            estadisticas={estadisticas}
            promedioSemanal={promedioSemanal}
          />

          {/* Category Buttons */}
          <div className="category-buttons">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setActiveCategory(category)}
                className={`category-button ${activeCategory === category ? 'active' : 'inactive'}`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* Subcategory Buttons - Solo para categoría General */}
          {activeCategory === 'General' && (
            <div className="subcategory-container">
              {['Ver Estadísticas', 'Ver Historial'].map((subcategory) => (
                <button
                  key={subcategory}
                  onClick={() => setActiveSubcategory(subcategory)}
                  className={`subcategory-button ${activeSubcategory === subcategory ? 'active' : 'inactive'}`}
                >
                  {subcategory}
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Content Area */}
      <div className="content-area">
        {renderContent()}
      </div>
    </div>
  );
};

export default EstadisticasMedico;