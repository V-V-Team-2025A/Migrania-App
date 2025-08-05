// src/components/EstadisticasPacienteComponents.jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { 
  Brain, 
  Activity, 
  FileText, 
  Pill,
  Clock,
  Zap
} from 'lucide-react';

// Componente para las tarjetas de resumen del paciente
export const SummaryCardsPaciente = ({ estadisticas, promedioSemanal, user }) => {
  const summaryCards = [
    {
      icon: Activity,
      title: 'Total episodios',
      value: estadisticas?.total_episodios || '0',
      subtitle: 'registrados',
      color: 'var(--color-action)'
    },
    {
      icon: Clock,
      title: 'Duración promedio',
      value: estadisticas?.duracion_promedio ? `${estadisticas.duracion_promedio}h` : '--',
      subtitle: 'por episodio',
      color: '#F59E0B'
    },
    {
      icon: Zap,
      title: 'Intensidad promedio',
      value: estadisticas?.intensidad_promedio || '--',
      subtitle: 'del dolor',
      color: 'var(--color-error)'
    },
    {
      icon: Activity,
      title: 'Frecuencia semanal',
      value: promedioSemanal?.promedio_semanal || '--',
      subtitle: 'episodios/semana',
      color: 'var(--color-action)'
    }
  ];

  return (
    <div className="summary-grid">
      {summaryCards.map((card, index) => (
        <div key={index} className="summary-card">
          <div className="card-icon" style={{ backgroundColor: card.color + '20' }}>
            <card.icon size={24} color={card.color} />
          </div>
          <div className="card-title">{card.title}</div>
          <div className="card-value">{card.value}</div>
          <div className="card-subtitle">{card.subtitle}</div>
        </div>
      ))}
    </div>
  );
};

// Componente para estadísticas de bitácora
export const BitacoraStatistics = ({ estadisticas, episodios, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          Cargando estadísticas de bitácora...
        </div>
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
          Registra algunos episodios para ver tus estadísticas
        </div>
      </div>
    );
  }

  // Procesar datos para gráficos
  const processMonthlyData = () => {
    if (!episodios || episodios.length === 0) return [];
    
    const monthlyData = {};
    
    episodios.forEach(episode => {
      const date = new Date(episode.fecha_creacion);
      const monthKey = date.toLocaleDateString('es-ES', { month: 'short', year: 'numeric' });
      
      if (!monthlyData[monthKey]) {
        monthlyData[monthKey] = {
          mes: monthKey,
          episodios: 0,
          intensidad_total: 0,
          duracion_total: 0,
          count: 0
        };
      }
      
      monthlyData[monthKey].episodios++;
      monthlyData[monthKey].intensidad_total += episode.severidad_numerica || 0;
      monthlyData[monthKey].duracion_total += episode.duracion_cefalea_horas || 0;
      monthlyData[monthKey].count++;
    });

    return Object.values(monthlyData).map(month => ({
      ...month,
      intensidad_avg: month.count > 0 ? (month.intensidad_total / month.count).toFixed(1) : 0,
      duracion_avg: month.count > 0 ? (month.duracion_total / month.count).toFixed(1) : 0
    }));
  };

  const processIntensityDistribution = () => {
    if (!episodios || episodios.length === 0) return [];
    
    const distribution = {
      '1-3': 0,
      '4-6': 0,
      '7-8': 0,
      '9-10': 0
    };
    
    episodios.forEach(episode => {
      const intensity = episode.severidad_numerica || 0;
      if (intensity >= 1 && intensity <= 3) distribution['1-3']++;
      else if (intensity >= 4 && intensity <= 6) distribution['4-6']++;
      else if (intensity >= 7 && intensity <= 8) distribution['7-8']++;
      else if (intensity >= 9 && intensity <= 10) distribution['9-10']++;
    });

    const total = episodios.length;
    return Object.entries(distribution).map(([range, count]) => ({
      intensidad: range,
      episodios: count,
      porcentaje: total > 0 ? Math.round((count / total) * 100) : 0
    }));
  };

  const monthlyData = processMonthlyData();
  const intensityData = processIntensityDistribution();

  return (
    <div className="statistics-content">
      {/* Episodios por mes */}
      <div className="chart-container">
        <h3 className="chart-title">
          <Activity size={20} color="var(--color-action)" />
          Episodios por Mes
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={monthlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis dataKey="mes" stroke="#6B7280" />
            <YAxis stroke="#6B7280" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'var(--color-background)', 
                border: 'none', 
                borderRadius: 'var(--border-radius)',
                color: 'white'
              }}
              formatter={(value) => [`${value} episodios`, 'Episodios']}
            />
            <Bar dataKey="episodios" fill="var(--color-action)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Distribución de intensidad */}
      <div className="chart-container">
        <h3 className="chart-title">Distribución de Intensidad</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={intensityData} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis type="number" stroke="#6B7280" />
            <YAxis dataKey="intensidad" type="category" stroke="#6B7280" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'var(--color-background)', 
                border: 'none', 
                borderRadius: 'var(--border-radius)',
                color: 'white'
              }}
              formatter={(value) => [`${value} episodios`, 'Cantidad']}
            />
            <Bar dataKey="episodios" fill="var(--color-action)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Resumen estadístico */}
      <div className="chart-container">
        <h3 className="chart-title">Resumen Estadístico</h3>
        <div className="breakdown-container">
          <div className="breakdown-item">
            <span className="breakdown-label">Duración promedio</span>
            <span className="breakdown-value">{estadisticas.duracion_promedio || 0}h</span>
          </div>
          <div className="breakdown-item">
            <span className="breakdown-label">Intensidad promedio</span>
            <span className="breakdown-value">{estadisticas.intensidad_promedio || 'N/A'}</span>
          </div>
          <div className="breakdown-item">
            <span className="breakdown-label">Episodios durante menstruación</span>
            <span className="breakdown-value">{estadisticas.porcentaje_menstruacion || 0}%</span>
          </div>
          <div className="breakdown-item">
            <span className="breakdown-label">Episodios con anticonceptivos</span>
            <span className="breakdown-value">{estadisticas.porcentaje_anticonceptivos || 0}%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Componente para análisis de patrones (equivalente a MIDAS estadísticas)
export const PatronesStatistics = ({ analisisPatrones, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          Cargando análisis de patrones...
        </div>
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
          Se requieren más datos para generar el análisis de patrones
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-content">
      {/* Conclusión clínica */}
      {analisisPatrones.conclusion_clinica && (
        <div className="chart-container">
          <h3 className="chart-title">
            <Brain size={20} color="var(--color-action)" />
            Conclusión Clínica
          </h3>
          <p style={{ color: '#374151', lineHeight: '1.6', fontSize: '14px' }}>
            {analisisPatrones.conclusion_clinica}
          </p>
        </div>
      )}

      {/* Análisis de síntomas */}
      {analisisPatrones.conclusiones_sintomas && analisisPatrones.conclusiones_sintomas.length > 0 && (
        <div className="chart-container">
          <h3 className="chart-title">Frecuencia de Síntomas</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analisisPatrones.conclusiones_sintomas}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey="sintoma" stroke="#6B7280" angle={-45} textAnchor="end" height={80} />
              <YAxis stroke="#6B7280" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'var(--color-background)', 
                  border: 'none', 
                  borderRadius: 'var(--border-radius)',
                  color: 'white'
                }}
                formatter={(value) => [`${value}%`, 'Frecuencia']}
              />
              <Bar dataKey="frecuencia" fill="var(--color-action)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Patrón de aura */}
      {analisisPatrones.conclusion_aura && (
        <div className="chart-container">
          <h3 className="chart-title">Patrón de Aura</h3>
          <p style={{ color: '#374151', lineHeight: '1.6', fontSize: '14px' }}>
            {analisisPatrones.conclusion_aura}
          </p>
        </div>
      )}

      {/* Días recurrentes */}
      {analisisPatrones.dias_recurrentes && analisisPatrones.dias_recurrentes.length > 0 && (
        <div className="chart-container">
          <h3 className="chart-title">Días de Mayor Recurrencia</h3>
          <div className="breakdown-container">
            {analisisPatrones.dias_recurrentes.map((dia, index) => (
              <div key={index} className="breakdown-item">
                <span className="breakdown-label">{dia.dia}</span>
                <span className="breakdown-value">{dia.frecuencia} episodios</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Patrón hormonal */}
      {analisisPatrones.conclusion_hormonal && (
        <div className="chart-container">
          <h3 className="chart-title">Patrón Hormonal</h3>
          <p style={{ color: '#374151', lineHeight: '1.6', fontSize: '14px' }}>
            {analisisPatrones.conclusion_hormonal}
          </p>
        </div>
      )}
    </div>
  );
};

// Componente para historial de bitácora
export const BitacoraHistory = ({ episodios, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          Cargando historial de episodios...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-title">Error al cargar historial</div>
        <div className="error-message">{error}</div>
        <button className="retry-button" onClick={() => window.location.reload()}>
          Reintentar
        </button>
      </div>
    );
  }

  if (!episodios || episodios.length === 0) {
    return (
      <div className="no-data-container">
        <div className="no-data-title">No hay episodios registrados</div>
        <div className="no-data-subtitle">
          Comienza a registrar tus episodios para ver tu historial aquí
        </div>
      </div>
    );
  }

  const getIntensityClass = (intensidad) => {
    if (intensidad >= 7) return 'intensity-high';
    if (intensidad >= 4) return 'intensity-medium';
    return 'intensity-low';
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h3 className="history-title">Historial de Episodios</h3>
        <button className="export-button">
          <FileText size={16} />
          Exportar
        </button>
      </div>

      <div className="history-grid">
        {episodios.slice(0, 10).map((episode) => (
          <div key={episode.id} className="episode-item">
            <div className="episode-details">
              <div className="episode-date">
                {new Date(episode.fecha_creacion).toLocaleDateString('es-ES', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </div>
              <div className="episode-time">
                {episode.hora_inicio ? `${episode.hora_inicio} • ` : ''}{episode.duracion_cefalea_horas || 0}h de duración
              </div>
              
              {/* Síntomas */}
              {episode.sintomas_asociados && (
                <div className="symptoms-container">
                  {episode.sintomas_asociados.split(',').map((sintoma, idx) => (
                    <span key={idx} className="symptom-tag">
                      {sintoma.trim()}
                    </span>
                  ))}
                </div>
              )}
              
              {/* Medicación */}
              {episode.medicacion_tomada && (
                <div className="medication-info">
                  <Pill size={12} />
                  {episode.medicacion_tomada}
                </div>
              )}
            </div>
            
            <div className="intensity-display">
              <div className="intensity-label">Intensidad</div>
              <span className={`intensity-badge ${getIntensityClass(episode.severidad_numerica || 0)}`}>
                {episode.severidad_numerica || 0}/10
              </span>
            </div>

            <button className="details-button">
              Ver detalles
            </button>
          </div>
        ))}
      </div>
      
      {episodios.length > 10 && (
        <div style={{ textAlign: 'center', marginTop: 'var(--spacing-m)' }}>
          <button className="details-button">
            Ver más episodios ({episodios.length - 10} restantes)
          </button>
        </div>
      )}
    </div>
  );
};

// Componente para análisis de patrones como historial
export const PatronesHistory = ({ analisisPatrones, estadisticas, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          Cargando análisis histórico...
        </div>
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

  if (!analisisPatrones && !estadisticas) {
    return (
      <div className="no-data-container">
        <div className="no-data-title">No hay análisis disponible</div>
        <div className="no-data-subtitle">
          Se requieren más datos para generar análisis históricos
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h3 className="history-title">Resumen de Análisis</h3>
        <button className="export-button">
          <FileText size={16} />
          Exportar
        </button>
      </div>

      <div className="history-grid">
        {/* Información general */}
        {estadisticas && (
          <div className="history-item">
            <div className="history-item-header">
              <div>
                <div className="history-date">
                  Estadísticas Generales
                </div>
                <div className="history-type">
                  Período: {estadisticas.fecha_primer_episodio && estadisticas.fecha_ultimo_episodio ? 
                    `${new Date(estadisticas.fecha_primer_episodio).toLocaleDateString('es-ES')} - ${new Date(estadisticas.fecha_ultimo_episodio).toLocaleDateString('es-ES')}` :
                    'Datos disponibles'
                  }
                </div>
              </div>
              <div className="score-display">
                <div className="score-value" style={{ color: 'var(--color-action)' }}>
                  {estadisticas.total_episodios || 0}
                </div>
                <div className="score-category" style={{ color: 'var(--color-action)' }}>
                  episodios
                </div>
              </div>
            </div>
            
            <div className="breakdown-container">
              <div className="breakdown-item">
                <span className="breakdown-label">Duración promedio</span>
                <span className="breakdown-value">{estadisticas.duracion_promedio || 0}h</span>
              </div>
              <div className="breakdown-item">
                <span className="breakdown-label">Intensidad promedio</span>
                <span className="breakdown-value">{estadisticas.intensidad_promedio || 'N/A'}</span>
              </div>
            </div>
          </div>
        )}

        {/* Conclusiones clínicas */}
        {analisisPatrones?.conclusion_clinica && (
          <div className="history-item">
            <div className="history-item-header">
              <div>
                <div className="history-date">Conclusión Clínica</div>
                <div className="history-type">Análisis de patrones</div>
              </div>
            </div>
            <p style={{ color: '#374151', lineHeight: '1.5', fontSize: '14px', margin: 0 }}>
              {analisisPatrones.conclusion_clinica}
            </p>
          </div>
        )}

        {/* Patrón hormonal */}
        {analisisPatrones?.conclusion_hormonal && (
          <div className="history-item">
            <div className="history-item-header">
              <div>
                <div className="history-date">Patrón Hormonal</div>
                <div className="history-type">Análisis de correlaciones</div>
              </div>
            </div>
            <p style={{ color: '#374151', lineHeight: '1.5', fontSize: '14px', margin: 0 }}>
              {analisisPatrones.conclusion_hormonal}
            </p>
          </div>
        )}

        {/* Patrón de aura */}
        {analisisPatrones?.conclusion_aura && (
          <div className="history-item">
            <div className="history-item-header">
              <div>
                <div className="history-date">Patrón de Aura</div>
                <div className="history-type">Análisis de síntomas</div>
              </div>
            </div>
            <p style={{ color: '#374151', lineHeight: '1.5', fontSize: '14px', margin: 0 }}>
              {analisisPatrones.conclusion_aura}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};