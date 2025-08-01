import React, { useState } from 'react';
import Header from '@/common/components/Header.jsx';
import { ArrowLeft, Search, Clock, TrendingUp, Zap, ClipboardList } from 'lucide-react';

const MedicalDashboard = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('General');
  const [activeSubcategory, setActiveSubcategory] = useState('Ver Historial');

  const categories = ['General', 'MIDAS', 'Bitácora'];
  
  const summaryCards = [
    {
      icon: Clock,
      title: 'Frecuencia semanal',
      value: '3.2',
      subtitle: 'promedio'
    },
    {
      icon: TrendingUp,
      title: 'Duración promedio',
      value: '2.5h',
      subtitle: 'por episodio'
    },
    {
      icon: Zap,
      title: 'Intensidad promedio',
      value: '7/10',
      subtitle: 'escala dolor'
    },
    {
      icon: ClipboardList,
      title: 'Última MIDAS',
      value: '15',
      subtitle: 'puntos'
    }
  ];

  const handleVolver = () => {
    console.log('Volver clickeado');
  };

  const styles = {
    container: {
      fontFamily: 'var(--font-main)',
      backgroundColor: 'var(--color-body-background)',
      color: 'var(--color-text)',
      padding: 'var(--spacing-m)',
      minHeight: '100vh'
    },
    searchContainer: {
      position: 'relative',
      maxWidth: '300px',
      marginBottom: 'var(--spacing-l)'
    },
    searchInput: {
      width: '100%',
      paddingLeft: '40px',
      paddingRight: 'var(--spacing-m)',
      paddingTop: 'var(--spacing-s)',
      paddingBottom: 'var(--spacing-s)',
      backgroundColor: 'var(--color-background)',
      border: '1px solid #4A5A69',
      borderRadius: 'var(--border-radius)',
      color: 'var(--color-text)',
      fontSize: '14px',
      outline: 'none'
    },
    searchIcon: {
      position: 'absolute',
      left: '12px',
      top: '50%',
      transform: 'translateY(-50%)',
      color: '#9CA3AF'
    },
    patientTitle: {
      fontSize: '18px',
      fontWeight: '600',
      marginBottom: 'var(--spacing-m)',
      color: 'var(--color-text)'
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
      backgroundColor: '#4A5A69',
      borderRadius: 'var(--border-radius)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      margin: '0 auto var(--spacing-s) auto'
    },
    cardTitle: {
      fontSize: '12px',
      color: '#9CA3AF',
      marginBottom: 'var(--spacing-xs)'
    },
    cardValue: {
      fontSize: '20px',
      fontWeight: '700',
      color: 'var(--color-text)',
      marginBottom: 'var(--spacing-xs)'
    },
    cardSubtitle: {
      fontSize: '10px',
      color: '#9CA3AF'
    },
    categoryButtons: {
      display: 'flex',
      gap: 'var(--spacing-s)',
      marginBottom: 'var(--spacing-m)'
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
    categoryButtonActive: {
      backgroundColor: 'var(--color-action)',
      color: 'var(--color-text)'
    },
    categoryButtonInactive: {
      backgroundColor: 'var(--color-background)',
      color: '#9CA3AF'
    },
    subcategoryContainer: {
      display: 'flex',
      gap: 'var(--spacing-s)',
      alignItems: 'center',
      marginBottom: 'var(--spacing-l)'
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
    subcategoryButtonActive: {
      backgroundColor: 'var(--secondary-light)',
      color: 'var(--color-background)'
    },
    subcategoryButtonInactive: {
      backgroundColor: 'var(--color-background)',
      color: '#9CA3AF'
    },
    exportButton: {
      padding: 'var(--spacing-s) var(--spacing-m)',
      backgroundColor: 'var(--color-background)',
      color: '#9CA3AF',
      borderRadius: 'var(--border-radius)',
      border: 'none',
      fontFamily: 'var(--font-main)',
      fontSize: '12px',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--spacing-xs)',
      transition: 'all 0.2s ease'
    },
    contentArea: {
      backgroundColor: '#E5E7EB',
      borderRadius: 'var(--border-radius)',
      padding: 'var(--spacing-xxl)',
      minHeight: '400px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    },
    noDataContainer: {
      textAlign: 'center'
    },
    noDataTitle: {
      fontSize: '18px',
      fontWeight: '600',
      color: '#6B7280',
      marginBottom: 'var(--spacing-s)'
    },
    noDataSubtitle: {
      fontSize: '14px',
      color: '#9CA3AF'
    }
  };

  return (
    <div style={styles.container}>
      <Header
        title="Historial y Estadísticas"
        onBack={handleVolver}
      />

      {/* Search Bar */}
      <div style={styles.searchContainer}>
        <Search style={styles.searchIcon} size={18} />
        <input
          type="text"
          placeholder="Buscar paciente"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={styles.searchInput}
        />
      </div>

      {/* Patient Summary Section */}
      <div>
        <h2 style={styles.patientTitle}>Resumen de: nombrepaciente</h2>
        
        {/* Summary Cards */}
        <div style={styles.summaryGrid}>
          {summaryCards.map((card, index) => (
            <div key={index} style={styles.summaryCard}>
              <div style={styles.cardIcon}>
                <card.icon size={24} color="#9CA3AF" />
              </div>
              <div style={styles.cardTitle}>{card.title}</div>
              <div style={styles.cardValue}>{card.value}</div>
              <div style={styles.cardSubtitle}>{card.subtitle}</div>
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
                ...(activeCategory === category 
                  ? styles.categoryButtonActive 
                  : styles.categoryButtonInactive
                )
              }}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Subcategory Buttons */}
        <div style={styles.subcategoryContainer}>
          {['Ver Historial', 'Ver Estadísticas'].map((subcategory) => (
            <button
              key={subcategory}
              onClick={() => setActiveSubcategory(subcategory)}
              style={{
                ...styles.subcategoryButton,
                ...(activeSubcategory === subcategory 
                  ? styles.subcategoryButtonActive 
                  : styles.subcategoryButtonInactive
                )
              }}
            >
              {subcategory}
            </button>
          ))}
          
          {/* Export Button */}
          <button style={styles.exportButton}>
            <ClipboardList size={16} />
            <span>Exportar</span>
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div style={styles.contentArea}>
        <div style={styles.noDataContainer}>
          <div style={styles.noDataTitle}>
            No se encuentran registros
          </div>
          <div style={styles.noDataSubtitle}>
            Mostrando {activeSubcategory.toLowerCase()} de {activeCategory}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicalDashboard;