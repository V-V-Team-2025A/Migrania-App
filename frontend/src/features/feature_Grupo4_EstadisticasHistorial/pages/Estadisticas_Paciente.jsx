import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '@/common/components/Header.jsx';
import {
  useEstadisticasCompletas,
  useEpisodiosPaciente,
  usePromedioSemanalPaciente
} from '../hooks/useEstadisticasPaciente';
import {
  SummaryCardsPaciente,
  BitacoraStatistics,
  PatronesStatistics,
  BitacoraHistory,
  PatronesHistory
} from '../components/EstadisticasPacienteComponents';
import '../styles/EstadisticasPaciente.css';
import MidasEstadisticas from '../../feature_Grupo1_EvaluacionMidas/pages/MidasEstadisticas';
import MidasMedico from '../../feature_Grupo1_EvaluacionMidas/pages/MidasMedico';

const EstadisticasPaciente = () => {
  const navigate = useNavigate();

  // Estados locales
  const [activeCategory, setActiveCategory] = useState('Bitácora');
  const [activeSubcategory, setActiveSubcategory] = useState('Ver Estadísticas');

  // Hooks para datos
  const {
    estadisticas,
    analisisPatrones,
    user,
    loading: loadingMain,
    error: errorMain,
    fetchPromedioReciente
  } = useEstadisticasCompletas();

  const { episodios, loading: loadingEpisodios, error: errorEpisodios } = useEpisodiosPaciente();
  const { promedioSemanal, fetchPromedioSemanal } = usePromedioSemanalPaciente();

  const categories = ['Bitácora', 'Patrones', 'MIDAS'];
  const subcategories = ['Ver Estadísticas', 'Ver Historial'];

  // Obtener promedio semanal al montar el componente
  useEffect(() => {
    const fetchPromedio = async () => {
      const fechaFin = new Date();
      const fechaInicio = new Date();
      fechaInicio.setMonth(fechaInicio.getMonth() - 3);

      await fetchPromedioSemanal(
        fechaInicio.toISOString().split('T')[0],
        fechaFin.toISOString().split('T')[0]
      );
    };

    fetchPromedio();
  }, [fetchPromedioSemanal]);

  const handleVolver = () => {
    navigate(-1);
  };

  const renderContent = () => {
    if (activeCategory === 'Bitácora') {
      if (activeSubcategory === 'Ver Estadísticas') {
        return (
          <BitacoraStatistics
            estadisticas={estadisticas}
            episodios={episodios}
            loading={loadingMain || loadingEpisodios}
            error={errorMain || errorEpisodios}
          />
        );
      } else {
        return (
          <BitacoraHistory
            episodios={episodios}
            loading={loadingEpisodios}
            error={errorEpisodios}
          />
        );
      }
    } else if (activeCategory === 'Patrones') {
      if (activeSubcategory === 'Ver Estadísticas') {
        return (
          <PatronesStatistics
            analisisPatrones={analisisPatrones}
            loading={loadingMain}
            error={errorMain}
          />
        );
      } else {
        return (
          <PatronesHistory
            analisisPatrones={analisisPatrones}
            estadisticas={estadisticas}
            loading={loadingMain}
            error={errorMain}
          />
        );
      }
    } else if (activeCategory === 'MIDAS') {
      if (activeSubcategory === 'Ver Estadísticas') {
        return (
         <MidasEstadisticas/>
        );
      } else {
        return (
          <MidasMedico/>
        );
      }
    }
  };

  // Loading state para la carga inicial
  if (loadingMain && !estadisticas) {
    return (
      <div className="estadisticas-paciente-container">
        <Header
          title="Historial y Estadísticas"
          onBack={handleVolver}
        />
        <div className="loading-container">
          <div className="loading-content">
            <div className="loading-spinner"></div>
            Cargando tus datos...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="estadisticas-paciente-container">
      <Header
        title="Historial y Estadísticas"
        onBack={handleVolver}
      />

      {/* Header con información del usuario */}
      <div className="header-section">
        <h1 className="welcome-text">
          Hola, {user?.nombre || 'Usuario'}
        </h1>
        <p className="subtitle">
          Aquí puedes ver el resumen de tus episodios y patrones de migraña
        </p>
      </div>

      {/* Mostrar error si existe pero no bloquear toda la interfaz */}
      {errorMain && (
        <div className="error-container" style={{ marginBottom: 'var(--spacing-l)' }}>
          <div className="error-title">Advertencia</div>
          <div className="error-message">
            Algunos datos pueden no estar actualizados: {errorMain}
          </div>
        </div>
      )}

      {/* Summary Cards */}
      <SummaryCardsPaciente
        estadisticas={estadisticas}
        promedioSemanal={promedioSemanal}
        user={user}
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

      {/* Subcategory Buttons */}
      <div className="subcategory-container">
        {subcategories.map((subcategory) => (
          <button
            key={subcategory}
            onClick={() => setActiveSubcategory(subcategory)}
            className={`subcategory-button ${activeSubcategory === subcategory ? 'active' : 'inactive'}`}
          >
            {subcategory}
          </button>
        ))}
      </div>

      {/* Content Area */}
      <div className="content-area">
        {renderContent()}
      </div>
    </div>
  );
};

export default EstadisticasPaciente;