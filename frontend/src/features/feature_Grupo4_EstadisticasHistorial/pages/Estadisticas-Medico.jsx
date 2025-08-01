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

  return (
    <div className="min-h-screen bg-slate-700 text-white p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="text-sm text-gray-400 mb-4">
          Historial y Estadísticas - Médico (sin registros)
        </div>
        
        <div className="flex items-center gap-4 mb-6">
          <button className="flex items-center gap-2 text-white hover:text-gray-300 transition-colors">
            <ArrowLeft size={20} />
            <span className="font-medium">Volver</span>
          </button>
          
          <h1 className="text-2xl font-bold">Historial y Estadísticas</h1>
        </div>

        {/* Search Bar */}
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
          <input
            type="text"
            placeholder="Buscar paciente"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-600 border border-slate-500 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
          />
        </div>
      </div>

      {/* Patient Summary Section */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">Resumen de: nombrepaciente</h2>
        
        {/* Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {summaryCards.map((card, index) => (
            <div key={index} className="bg-slate-600 rounded-lg p-4 border border-slate-500">
              <div className="flex items-center justify-center w-12 h-12 bg-slate-500 rounded-lg mb-3 mx-auto">
                <card.icon size={24} className="text-gray-300" />
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-400 mb-1">{card.title}</div>
                <div className="text-xl font-bold">{card.value}</div>
                <div className="text-xs text-gray-400">{card.subtitle}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Category Buttons */}
        <div className="flex gap-4 mb-6">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                activeCategory === category
                  ? 'bg-cyan-500 text-white'
                  : 'bg-slate-600 text-gray-300 hover:bg-slate-500'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Subcategory Buttons */}
        <div className="flex gap-4 mb-6">
          {['Ver Historial', 'Ver Estadísticas'].map((subcategory) => (
            <button
              key={subcategory}
              onClick={() => setActiveSubcategory(subcategory)}
              className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                activeSubcategory === subcategory
                  ? 'bg-yellow-600 text-white'
                  : 'bg-slate-600 text-gray-300 hover:bg-slate-500'
              }`}
            >
              {subcategory}
            </button>
          ))}
          
          {/* Export Button */}
          <button className="px-4 py-2 bg-slate-600 text-gray-300 hover:bg-slate-500 rounded-lg transition-colors flex items-center gap-2">
            <ClipboardList size={16} />
            <span className="text-sm">Exportar</span>
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="bg-gray-100 rounded-lg p-8 min-h-96 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-600 text-lg font-medium mb-2">
            No se encuentran registros
          </div>
          <div className="text-gray-500 text-sm">
            Mostrando {activeSubcategory.toLowerCase()} de {activeCategory}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicalDashboard;