import React, { useState, useEffect } from 'react';
import Header from '@/common/components/Header.jsx';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { 
  Calendar, 
  Clock, 
  TrendingUp, 
  Zap, 
  ClipboardList, 
  Pill, 
  FileText,
  Activity,
  AlertCircle,
  CheckCircle,
  Brain,
  Target
} from 'lucide-react';

const PatientDashboard = ({ patientId = 1 }) => {
  const [activeCategory, setActiveCategory] = useState('MIDAS');
  const [activeSubcategory, setActiveSubcategory] = useState('Ver Estadísticas');
  const [patientData, setPatientData] = useState(null);
  const [loading, setLoading] = useState(false);

  const categories = ['MIDAS', 'Bitácora'];
  const subcategories = ['Ver Historial', 'Ver Estadísticas'];

  // Datos mock - en producción vendrían de tu API Django
  const mockPatientData = {
    name: "María González",
    summary: {
      episodios_mes: 8,
      promedio_intensidad: 6.5,
      dias_sin_episodios: 12,
      ultima_midas: 15,
      midas_categoria: "Moderada",
      frecuencia_semanal: 2.1
    },
    midas_data: {
      timeline_scores: [
        { fecha: 'Ene 2024', score: 18, categoria: 'Moderada' },
        { fecha: 'Mar 2024', score: 22, categoria: 'Severa' },
        { fecha: 'Jun 2024', score: 15, categoria: 'Moderada' },
      ],
      breakdown: [
        { pregunta: 'Días perdidos trabajo', valor: 3 },
        { pregunta: 'Días productividad reducida', valor: 5 },
        { pregunta: 'Días perdidos hogar', valor: 2 },
        { pregunta: 'Días productividad hogar reducida', valor: 4 },
        { pregunta: 'Días actividades familiares', valor: 1 }
      ]
    },
    bitacora_data: {
      monthly_episodes: [
        { mes: 'Ene', episodios: 12, intensidad_avg: 7.2, duracion_avg: 2.8 },
        { mes: 'Feb', episodios: 8, intensidad_avg: 6.1, duracion_avg: 2.1 },
        { mes: 'Mar', episodios: 15, intensidad_avg: 8.0, duracion_avg: 3.5 },
        { mes: 'Abr', episodios: 6, intensidad_avg: 5.5, duracion_avg: 1.8 },
        { mes: 'May', episodios: 10, intensidad_avg: 6.8, duracion_avg: 2.3 },
        { mes: 'Jun', episodios: 8, intensidad_avg: 6.5, duracion_avg: 2.0 }
      ],
      intensity_distribution: [
        { intensidad: '1-3', episodios: 2, porcentaje: 5 },
        { intensidad: '4-6', episodios: 15, porcentaje: 38 },
        { intensidad: '7-8', episodios: 18, porcentaje: 45 },
        { intensidad: '9-10', episodios: 5, porcentaje: 12 }
      ]
    },
    midas_history: [
      {
        id: 1,
        fecha: '2024-06-01',
        score: 15,
        categoria: 'Moderada',
        q1: 3, q2: 5, q3: 2, q4: 4, q5: 1
      },
      {
        id: 2,
        fecha: '2024-03-01',
        score: 22,
        categoria: 'Severa',
        q1: 5, q2: 7, q3: 3, q4: 5, q5: 2
      },
      {
        id: 3,
        fecha: '2024-01-01',
        score: 18,
        categoria: 'Moderada',
        q1: 4, q2: 6, q3: 2, q4: 4, q5: 2
      }
    ],
    bitacora_history: [
      {
        id: 1,
        fecha: '2024-06-15',
        hora_inicio: '14:30',
        duracion: 3.5,
        intensidad: 8,
        sintomas: ['Náusea', 'Fotofobia'],
        medicacion: 'Sumatriptán 50mg'
      },
      {
        id: 2,
        fecha: '2024-06-12',
        hora_inicio: '09:15',
        duracion: 2.0,
        intensidad: 6,
        sintomas: ['Dolor pulsátil'],
        medicacion: 'Ibuprofeno 600mg'
      },
      {
        id: 3,
        fecha: '2024-06-08',
        hora_inicio: '18:45',
        duracion: 4.0,
        intensidad: 9,
        sintomas: ['Náusea', 'Vómito', 'Fotofobia'],
        medicacion: 'Sumatriptán 100mg'
      },
      {
        id: 4,
        fecha: '2024-06-05',
        hora_inicio: '11:20',
        duracion: 1.5,
        intensidad: 4,
        sintomas: ['Dolor leve'],
        medicacion: 'Paracetamol 500mg'
      }
    ]
  };

  useEffect(() => {
    setPatientData(mockPatientData);
  }, []);

  const handleVolver = () => {
    console.log('Volver clickeado');
  };

  const summaryCards = [
    {
      icon: Target,
      title: 'Score MIDAS actual',
      value: patientData?.summary.ultima_midas || '0',
      subtitle: patientData?.summary.midas_categoria || 'Sin datos',
      color: patientData?.summary.ultima_midas >= 21 ? 'var(--color-error)' : 
             patientData?.summary.ultima_midas >= 11 ? '#F59E0B' : 'var(--color-action)'
    },
    {
      icon: Activity,
      title: 'Episodios este mes',
      value: patientData?.summary.episodios_mes || '0',
      subtitle: 'últimos 30 días',
      color: '#F59E0B'
    },
    {
      icon: Zap,
      title: 'Intensidad promedio',
      value: `${patientData?.summary.promedio_intensidad || '0'}/10`,
      subtitle: 'este mes',
      color: 'var(--color-error)'
    },
    {
      icon: TrendingUp,
      title: 'Frecuencia semanal',
      value: patientData?.summary.frecuencia_semanal || '0',
      subtitle: 'episodios/semana',
      color: 'var(--color-action)'
    }
  ];

  const renderMIDASStatistics = () => (
    <div style={{ display: 'grid', gap: 'var(--spacing-l)' }}>
      {/* Evolución Score MIDAS */}
      <div style={{ backgroundColor: 'white', padding: 'var(--spacing-l)', borderRadius: 'var(--border-radius)' }}>
        <h3 style={{ color: '#374151', marginBottom: 'var(--spacing-m)', display: 'flex', alignItems: 'center', gap: 'var(--spacing-s)' }}>
          <Brain size={20} color="var(--color-action)" />
          Evolución Score MIDAS
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={patientData?.midas_data.timeline_scores || []}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis dataKey="fecha" stroke="#6B7280" />
            <YAxis domain={[0, 50]} stroke="#6B7280" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'var(--color-background)', 
                border: 'none', 
                borderRadius: 'var(--border-radius)',
                color: 'white'
              }}
              formatter={(value) => [`${value} puntos`, 'Score MIDAS']}
            />
            <Line 
              type="monotone" 
              dataKey="score" 
              stroke="var(--color-action)" 
              strokeWidth={3}
              dot={{ fill: 'var(--color-action)', strokeWidth: 2, r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
        
        {/* Leyenda de categorías */}
        <div style={{ marginTop: 'var(--spacing-m)', display: 'flex', justifyContent: 'center', gap: 'var(--spacing-l)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
            <div style={{ width: '12px', height: '12px', backgroundColor: 'var(--color-action)', borderRadius: '50%' }}></div>
            <span style={{ fontSize: '12px', color: '#6B7280' }}>Leve (0-5)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
            <div style={{ width: '12px', height: '12px', backgroundColor: '#F59E0B', borderRadius: '50%' }}></div>
            <span style={{ fontSize: '12px', color: '#6B7280' }}>Moderada (6-10)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
            <div style={{ width: '12px', height: '12px', backgroundColor: 'var(--color-error)', borderRadius: '50%' }}></div>
            <span style={{ fontSize: '12px', color: '#6B7280' }}>Severa (11+)</span>
          </div>
        </div>
      </div>

      {/* Desglose último MIDAS */}
      <div style={{ backgroundColor: 'white', padding: 'var(--spacing-l)', borderRadius: 'var(--border-radius)' }}>
        <h3 style={{ color: '#374151', marginBottom: 'var(--spacing-m)' }}>Desglose Última Evaluación MIDAS</h3>
        <div style={{ display: 'grid', gap: 'var(--spacing-s)' }}>
          {patientData?.midas_data.breakdown.map((item, index) => (
            <div key={index} style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: 'var(--spacing-s)',
              backgroundColor: '#F9FAFB',
              borderRadius: 'var(--border-radius)'
            }}>
              <span style={{ color: '#374151', fontSize: '14px' }}>{item.pregunta}</span>
              <span style={{ 
                color: 'var(--color-action)', 
                fontWeight: '600',
                fontSize: '16px'
              }}>
                {item.valor} días
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderBitacoraStatistics = () => (
    <div style={{ display: 'grid', gap: 'var(--spacing-l)' }}>
      {/* Episodios por mes */}
      <div style={{ backgroundColor: 'white', padding: 'var(--spacing-l)', borderRadius: 'var(--border-radius)' }}>
        <h3 style={{ color: '#374151', marginBottom: 'var(--spacing-m)' }}>Episodios por Mes</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={patientData?.bitacora_data.monthly_episodes || []}>
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
              formatter={(value, name) => [
                name === 'episodios' ? `${value} episodios` : `${value}/10`,
                name === 'episodios' ? 'Episodios' : 'Intensidad Promedio'
              ]}
            />
            <Bar dataKey="episodios" fill="var(--color-action)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Distribución de intensidad */}
      <div style={{ backgroundColor: 'white', padding: 'var(--spacing-l)', borderRadius: 'var(--border-radius)' }}>
        <h3 style={{ color: '#374151', marginBottom: 'var(--spacing-m)' }}>Distribución de Intensidad</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={patientData?.bitacora_data.intensity_distribution || []} layout="horizontal">
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
            <Bar dataKey="episodios" fill="var(--color-action)" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  const renderMIDASHistory = () => (
    <div style={{ backgroundColor: 'white', padding: 'var(--spacing-l)', borderRadius: 'var(--border-radius)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-l)' }}>
        <h3 style={{ color: '#374151' }}>Historial de Evaluaciones MIDAS</h3>
        <button style={{
          padding: 'var(--spacing-s) var(--spacing-m)',
          backgroundColor: 'var(--color-action)',
          color: 'white',
          border: 'none',
          borderRadius: 'var(--border-radius)',
          cursor: 'pointer',
          fontSize: '12px',
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--spacing-xs)'
        }}>
          <FileText size={16} />
          Exportar
        </button>
      </div>

      <div style={{ display: 'grid', gap: 'var(--spacing-m)' }}>
        {patientData?.midas_history.map((evaluation) => (
          <div key={evaluation.id} style={{
            padding: 'var(--spacing-m)',
            backgroundColor: '#F9FAFB',
            borderRadius: 'var(--border-radius)',
            border: '1px solid #E5E7EB'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-s)' }}>
              <div>
                <div style={{ fontWeight: '600', color: '#374151', marginBottom: '4px' }}>
                  {new Date(evaluation.fecha).toLocaleDateString('es-ES', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}
                </div>
                <div style={{ fontSize: '12px', color: '#6B7280' }}>
                  Evaluación MIDAS
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ 
                  fontSize: '24px', 
                  fontWeight: '700', 
                  color: evaluation.score >= 21 ? 'var(--color-error)' : 
                         evaluation.score >= 11 ? '#F59E0B' : 'var(--color-action)'
                }}>
                  {evaluation.score}
                </div>
                <div style={{ 
                  fontSize: '12px', 
                  color: evaluation.score >= 21 ? 'var(--color-error)' : 
                         evaluation.score >= 11 ? '#F59E0B' : 'var(--color-action)',
                  fontWeight: '600'
                }}>
                  {evaluation.categoria}
                </div>
              </div>
            </div>
            
            {/* Desglose de respuestas */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 'var(--spacing-xs)', marginTop: 'var(--spacing-s)' }}>
              {[evaluation.q1, evaluation.q2, evaluation.q3, evaluation.q4, evaluation.q5].map((value, idx) => (
                <div key={idx} style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '10px', color: '#6B7280' }}>P{idx + 1}</div>
                  <div style={{ fontSize: '14px', fontWeight: '600', color: '#374151' }}>{value}</div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderBitacoraHistory = () => (
    <div style={{ backgroundColor: 'white', padding: 'var(--spacing-l)', borderRadius: 'var(--border-radius)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-l)' }}>
        <h3 style={{ color: '#374151' }}>Historial de Episodios</h3>
        <button style={{
          padding: 'var(--spacing-s) var(--spacing-m)',
          backgroundColor: 'var(--color-action)',
          color: 'white',
          border: 'none',
          borderRadius: 'var(--border-radius)',
          cursor: 'pointer',
          fontSize: '12px',
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--spacing-xs)'
        }}>
          <FileText size={16} />
          Exportar
        </button>
      </div>

      <div style={{ display: 'grid', gap: 'var(--spacing-s)' }}>
        {patientData?.bitacora_history.map((episode) => (
          <div key={episode.id} style={{
            display: 'grid',
            gridTemplateColumns: '1fr auto auto',
            alignItems: 'center',
            padding: 'var(--spacing-m)',
            backgroundColor: '#F9FAFB',
            borderRadius: 'var(--border-radius)',
            border: '1px solid #E5E7EB',
            gap: 'var(--spacing-m)'
          }}>
            <div>
              <div style={{ fontWeight: '600', color: '#374151', marginBottom: '4px' }}>
                {new Date(episode.fecha).toLocaleDateString('es-ES', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </div>
              <div style={{ fontSize: '12px', color: '#6B7280', marginBottom: '4px' }}>
                {episode.hora_inicio} • {episode.duracion}h de duración
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginBottom: '4px' }}>
                {episode.sintomas.map((sintoma, idx) => (
                  <span key={idx} style={{
                    padding: '2px 6px',
                    backgroundColor: '#E5E7EB',
                    color: '#374151',
                    borderRadius: '4px',
                    fontSize: '10px'
                  }}>
                    {sintoma}
                  </span>
                ))}
              </div>
              <div style={{ fontSize: '11px', color: '#6B7280', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Pill size={12} />
                {episode.medicacion}
              </div>
            </div>
            
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '12px', color: '#6B7280', marginBottom: '4px' }}>Intensidad</div>
              <span style={{
                padding: '6px 10px',
                borderRadius: '6px',
                backgroundColor: episode.intensidad >= 7 ? 'var(--color-error)' : 
                               episode.intensidad >= 4 ? '#F59E0B' : 'var(--color-action)',
                color: 'white',
                fontSize: '14px',
                fontWeight: '600'
              }}>
                {episode.intensidad}/10
              </span>
            </div>

            <button style={{
              padding: 'var(--spacing-xs) var(--spacing-s)',
              backgroundColor: 'transparent',
              color: 'var(--color-action)',
              border: '1px solid var(--color-action)',
              borderRadius: 'var(--border-radius)',
              cursor: 'pointer',
              fontSize: '12px'
            }}>
              Ver detalles
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderContent = () => {
    if (activeCategory === 'MIDAS') {
      return activeSubcategory === 'Ver Estadísticas' ? renderMIDASStatistics() : renderMIDASHistory();
    } else {
      return activeSubcategory === 'Ver Estadísticas' ? renderBitacoraStatistics() : renderBitacoraHistory();
    }
  };

  const styles = {
    container: {
      fontFamily: 'var(--font-main)',
      backgroundColor: 'var(--color-body-background)',
      color: 'var(--color-text)',
      padding: 'var(--spacing-m)',
      minHeight: '100vh'
    },
    header: {
      textAlign: 'center',
      marginBottom: 'var(--spacing-l)'
    },
    welcomeText: {
      fontSize: '24px',
      fontWeight: '700',
      marginBottom: 'var(--spacing-s)'
    },
    subtitle: {
      fontSize: '14px',
      color: '#9CA3AF'
    },
    summaryGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: 'var(--spacing-m)',
      marginBottom: 'var(--spacing-l)'
    },
    summaryCard: {
      backgroundColor: 'var(--color-background)',
      borderRadius: 'var(--border-radius)',
      padding: 'var(--spacing-m)',
      textAlign: 'center',
      border: '1px solid #4A5A69'
    },
    cardIcon: {
      width: '48px',
      height: '48px',
      borderRadius: 'var(--border-radius)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      margin: '0 auto var(--spacing-s) auto'
    },
    categoryButtons: {
      display: 'flex',
      gap: 'var(--spacing-s)',
      marginBottom: 'var(--spacing-m)',
      justifyContent: 'center'
    },
    categoryButton: {
      padding: 'var(--spacing-s) var(--spacing-l)',
      borderRadius: 'var(--border-radius)',
      border: 'none',
      fontFamily: 'var(--font-main)',
      fontSize: '14px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    subcategoryContainer: {
      display: 'flex',
      gap: 'var(--spacing-s)',
      alignItems: 'center',
      marginBottom: 'var(--spacing-l)',
      justifyContent: 'center'
    },
    subcategoryButton: {
      padding: 'var(--spacing-s) var(--spacing-l)',
      borderRadius: 'var(--border-radius)',
      border: 'none',
      fontFamily: 'var(--font-main)',
      fontSize: '14px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    contentArea: {
      minHeight: '400px'
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '400px' 
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-s)' }}>
            <div style={{ 
              width: '20px', 
              height: '20px', 
              border: '2px solid var(--color-action)', 
              borderTop: '2px solid transparent', 
              borderRadius: '50%', 
              animation: 'spin 1s linear infinite' 
            }}></div>
            Cargando tus datos...
          </div>
        </div>
      </div>
    );
  }

  return (
     <div style={styles.container}>
          <Header
            title="Historial y Estadísticas"
            onBack={handleVolver}
          />

      {/* Summary Cards */}
      <div style={styles.summaryGrid}>
        {summaryCards.map((card, index) => (
          <div key={index} style={styles.summaryCard}>
            <div style={{...styles.cardIcon, backgroundColor: card.color + '20'}}>
              <card.icon size={24} color={card.color} />
            </div>
            <div style={{ fontSize: '12px', color: '#9CA3AF', marginBottom: 'var(--spacing-xs)' }}>
              {card.title}
            </div>
            <div style={{ fontSize: '20px', fontWeight: '700', marginBottom: 'var(--spacing-xs)' }}>
              {card.value}
            </div>
            <div style={{ fontSize: '10px', color: '#9CA3AF' }}>
              {card.subtitle}
            </div>
          </div>
        ))}
      </div>

      {/* Category Buttons */}
      <div style={styles.categoryButtons}>
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            style={{
              ...styles.categoryButton,
              backgroundColor: activeCategory === category ? 'var(--color-action)' : 'var(--color-background)',
              color: activeCategory === category ? 'var(--color-text)' : '#9CA3AF'
            }}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Subcategory Buttons */}
      <div style={styles.subcategoryContainer}>
        {subcategories.map((subcategory) => (
          <button
            key={subcategory}
            onClick={() => setActiveSubcategory(subcategory)}
            style={{
              ...styles.subcategoryButton,
              backgroundColor: activeSubcategory === subcategory ? 'var(--secondary-light)' : 'var(--color-background)',
              color: activeSubcategory === subcategory ? 'var(--color-background)' : '#9CA3AF'
            }}
          >
            {subcategory}
          </button>
        ))}
      </div>

      {/* Content Area */}
      <div style={styles.contentArea}>
        {renderContent()}
      </div>
    </div>
  );
};

export default PatientDashboard;