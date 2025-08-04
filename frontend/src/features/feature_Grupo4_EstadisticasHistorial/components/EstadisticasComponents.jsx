// src/components/EstadisticasComponents.jsx
import React from 'react';
import { FaClock, FaTrendingUp, FaBolt, FaClipboardList, FaCalendar, FaUser } from 'react-icons/fa';

// Componente para mostrar estadísticas generales
export const EstadisticasGenerales = ({ estadisticas, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-text">Cargando estadísticas...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-title">Error al cargar estadísticas</div>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  if (!estadisticas) {
    return (
      <div className="no-data-container">
        <div className="no-data-title">No hay datos disponibles</div>
        <div className="no-data-subtitle">
          Se requieren al menos 3 episodios para generar estadísticas
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-content">
      <div className="statistics-section">
        <h3>Estadísticas de Episodios</h3>
        <div className="statistics-grid">
          {estadisticas.duracion_promedio && (
            <div className="stat-item">
              <span className="stat-label">Duración promedio</span>
              <span className="stat-value">{estadisticas.duracion_promedio}h</span>
            </div>
          )}
          
          {estadisticas.intensidad_promedio && (
            <div className="stat-item">
              <span className="stat-label">Intensidad promedio</span>
              <span className="stat-value">{estadisticas.intensidad_promedio}</span>
            </div>
          )}
          
          <div className="stat-item">
            <span className="stat-label">Total de episodios</span>
            <span className="stat-value">{estadisticas.total_episodios || 0}</span>
          </div>
        </div>
      </div>

      <div className="statistics-section">
        <h3>Factores Hormonales</h3>
        <div className="statistics-grid">
          <div className="stat-item">
            <span className="stat-label">Episodios durante menstruación</span>
            <span className="stat-value">{estadisticas.porcentaje_menstruacion || 0}%</span>
          </div>
          
          <div className="stat-item">
            <span className="stat-label">Episodios con anticonceptivos</span>
            <span className="stat-value">{estadisticas.porcentaje_anticonceptivos || 0}%</span>
          </div>
        </div>
      </div>

      {(estadisticas.fecha_primer_episodio || estadisticas.fecha_ultimo_episodio) && (
        <div className="statistics-section">
          <h3>Período de Registro</h3>
          <div className="statistics-grid">
            {estadisticas.fecha_primer_episodio && (
              <div className="stat-item">
                <span className="stat-label">Primer episodio</span>
                <span className="stat-value">
                  {new Date(estadisticas.fecha_primer_episodio).toLocaleDateString('es-ES')}
                </span>
              </div>
            )}
            
            {estadisticas.fecha_ultimo_episodio && (
              <div className="stat-item">
                <span className="stat-label">Último episodio</span>
                <span className="stat-value">
                  {new Date(estadisticas.fecha_ultimo_episodio).toLocaleDateString('es-ES')}
                </span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Componente para mostrar análisis de patrones
export const AnalisisPatrones = ({ analisisPatrones, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-text">Cargando análisis de patrones...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-title">Error al cargar análisis</div>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  if (!analisisPatrones) {
    return (
      <div className="no-data-container">
        <div className="no-data-title">No hay análisis disponible</div>
        <div className="no-data-subtitle">
          Se requieren datos suficientes para generar el análisis
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-content">
      {analisisPatrones.conclusion_clinica && (
        <div className="statistics-section">
          <h3>Conclusión Clínica</h3>
          <p style={{ color: 'var(--color-text)', lineHeight: '1.5' }}>
            {analisisPatrones.conclusion_clinica}
          </p>
        </div>
      )}

      {analisisPatrones.conclusiones_sintomas && (
        <div className="statistics-section">
          <h3>Análisis de Síntomas</h3>
          <div className="statistics-grid">
            {analisisPatrones.conclusiones_sintomas.map((sintoma, index) => (
              <div key={index} className="stat-item">
                <span className="stat-label">{sintoma.sintoma}</span>
                <span className="stat-value">{sintoma.frecuencia}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {analisisPatrones.conclusion_aura && (
        <div className="statistics-section">
          <h3>Patrón de Aura</h3>
          <p style={{ color: 'var(--color-text)', lineHeight: '1.5' }}>
            {analisisPatrones.conclusion_aura}
          </p>
        </div>
      )}

      {analisisPatrones.dias_recurrentes && analisisPatrones.dias_recurrentes.length > 0 && (
        <div className="statistics-section">
          <h3>Días Recurrentes</h3>
          <div className="statistics-grid">
            {analisisPatrones.dias_recurrentes.map((dia, index) => (
              <div key={index} className="stat-item">
                <span className="stat-label">{dia.dia}</span>
                <span className="stat-value">{dia.frecuencia} episodios</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {analisisPatrones.conclusion_hormonal && (
        <div className="statistics-section">
          <h3>Patrón Hormonal</h3>
          <p style={{ color: 'var(--color-text)', lineHeight: '1.5' }}>
            {analisisPatrones.conclusion_hormonal}
          </p>
        </div>
      )}
    </div>
  );
};

// Componente para selector de pacientes
export const PacienteSelector = ({ 
  pacientes, 
  selectedPacienteId, 
  onPacienteChange, 
  loading, 
  error 
}) => {
  return (
    <div className="patient-selector">
      <label htmlFor="paciente-select">Seleccionar Paciente:</label>
      <select
        id="paciente-select"
        value={selectedPacienteId || ''}
        onChange={(e) => onPacienteChange(e.target.value || null)}
        disabled={loading}
      >
        <option value="">-- Seleccionar paciente --</option>
        {pacientes.map((paciente) => (
          <option key={paciente.id} value={paciente.id}>
            {paciente.nombre} {paciente.apellido} - {paciente.email}
          </option>
        ))}
      </select>
      {error && (
        <div className="error-message" style={{ marginTop: 'var(--spacing-xs)' }}>
          Error cargando pacientes: {error}
        </div>
      )}
    </div>
  );
};

// Componente para tarjetas de resumen
export const SummaryCards = ({ estadisticas, promedioSemanal }) => {
  const summaryCards = [
    {
      icon: FaClock,
      title: 'Frecuencia semanal',
      value: promedioSemanal ? `${promedioSemanal.promedio_semanal}` : '--',
      subtitle: 'promedio'
    },
    {
      icon: FaTrendingUp,
      title: 'Duración promedio',
      value: estadisticas?.duracion_promedio ? `${estadisticas.duracion_promedio}h` : '--',
      subtitle: 'por episodio'
    },
    {
      icon: FaBolt,
      title: 'Intensidad promedio',
      value: estadisticas?.intensidad_promedio || '--',
      subtitle: 'del dolor'
    },
    {
      icon: FaClipboardList,
      title: 'Total episodios',
      value: estadisticas?.total_episodios || '--',
      subtitle: 'registrados'
    }
  ];

  return (
    <div className="summary-grid">
      {summaryCards.map((card, index) => (
        <div key={index} className="summary-card">
          <div className="card-icon">
            <card.icon size={24} color="#9CA3AF" />
          </div>
          <div className="card-title">{card.title}</div>
          <div className="card-value">{card.value}</div>
          <div className="card-subtitle">{card.subtitle}</div>
        </div>
      ))}
    </div>
  );
};