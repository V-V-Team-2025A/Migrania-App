// src/hooks/useEstadisticas.js
import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/apiService';

export const useEstadisticas = (pacienteId = null) => {
  const [estadisticas, setEstadisticas] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchEstadisticas = useCallback(async () => {
    if (!pacienteId) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getEstadisticasHistorial(pacienteId);
      setEstadisticas(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching estadísticas:', err);
    } finally {
      setLoading(false);
    }
  }, [pacienteId]);

  useEffect(() => {
    fetchEstadisticas();
  }, [fetchEstadisticas]);

  const refetch = useCallback(() => {
    fetchEstadisticas();
  }, [fetchEstadisticas]);

  return {
    estadisticas,
    loading,
    error,
    refetch
  };
};

export const usePromedioSemanal = () => {
  const [promedioSemanal, setPromedioSemanal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPromedioSemanal = useCallback(async (pacienteId, fechaInicio, fechaFin) => {
    if (!pacienteId || !fechaInicio || !fechaFin) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getPromedioSemanal(pacienteId, fechaInicio, fechaFin);
      setPromedioSemanal(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching promedio semanal:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    promedioSemanal,
    loading,
    error,
    fetchPromedioSemanal
  };
};

export const usePacientes = () => {
  const [pacientes, setPacientes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPacientes = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getPacientes();
      setPacientes(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching pacientes:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPacientes();
  }, [fetchPacientes]);

  return {
    pacientes,
    loading,
    error,
    refetch: fetchPacientes
  };
};

export const useAnalisisPatrones = (pacienteId = null) => {
  const [analisisPatrones, setAnalisisPatrones] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAnalisisPatrones = useCallback(async () => {
    if (!pacienteId) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getAnalisisPatrones(pacienteId);
      setAnalisisPatrones(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching análisis de patrones:', err);
    } finally {
      setLoading(false);
    }
  }, [pacienteId]);

  useEffect(() => {
    fetchAnalisisPatrones();
  }, [fetchAnalisisPatrones]);

  const refetch = useCallback(() => {
    fetchAnalisisPatrones();
  }, [fetchAnalisisPatrones]);

  return {
    analisisPatrones,
    loading,
    error,
    refetch
  };
};