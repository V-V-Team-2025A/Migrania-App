// src/hooks/useEstadisticasPaciente.js
import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/apiService';

// Hook para estadísticas del paciente autenticado
export const useEstadisticasPaciente = () => {
  const [estadisticas, setEstadisticas] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchEstadisticas = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Para pacientes, no se pasa paciente_id ya que se obtiene del token
      const data = await apiService.getEstadisticasHistorial();
      setEstadisticas(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching estadísticas del paciente:', err);
    } finally {
      setLoading(false);
    }
  }, []);

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

// Hook para análisis de patrones del paciente autenticado
export const useAnalisisPatronesPaciente = () => {
  const [analisisPatrones, setAnalisisPatrones] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAnalisisPatrones = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getAnalisisPatrones();
      setAnalisisPatrones(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching análisis de patrones del paciente:', err);
    } finally {
      setLoading(false);
    }
  }, []);

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

// Hook para promedio semanal del paciente
export const usePromedioSemanalPaciente = () => {
  const [promedioSemanal, setPromedioSemanal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPromedioSemanal = useCallback(async (fechaInicio, fechaFin) => {
    if (!fechaInicio || !fechaFin) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // Para pacientes, no se pasa paciente_id
      const data = await apiService.getPromedioSemanal(null, fechaInicio, fechaFin);
      setPromedioSemanal(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching promedio semanal del paciente:', err);
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

// Hook para episodios de bitácora del paciente
export const useEpisodiosPaciente = (fechaInicio = null, fechaFin = null) => {
  const [episodios, setEpisodios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchEpisodios = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getEpisodiosBitacora(null, fechaInicio, fechaFin);
      setEpisodios(data.results || data || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching episodios del paciente:', err);
    } finally {
      setLoading(false);
    }
  }, [fechaInicio, fechaFin]);

  useEffect(() => {
    fetchEpisodios();
  }, [fetchEpisodios]);

  const refetch = useCallback(() => {
    fetchEpisodios();
  }, [fetchEpisodios]);

  return {
    episodios,
    loading,
    error,
    refetch
  };
};

// Hook para información del usuario actual
export const useCurrentUser = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUser = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await apiService.getCurrentUser();
      setUser(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching current user:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const refetch = useCallback(() => {
    fetchUser();
  }, [fetchUser]);

  return {
    user,
    loading,
    error,
    refetch
  };
};

// Hook combinado para todas las estadísticas del paciente
export const useEstadisticasCompletas = () => {
  const { estadisticas, loading: loadingEstadisticas, error: errorEstadisticas, refetch: refetchEstadisticas } = useEstadisticasPaciente();
  const { analisisPatrones, loading: loadingPatrones, error: errorPatrones, refetch: refetchPatrones } = useAnalisisPatronesPaciente();
  const { user, loading: loadingUser, error: errorUser } = useCurrentUser();
  const { fetchPromedioSemanal } = usePromedioSemanalPaciente();

  // Función para obtener promedio semanal de los últimos 3 meses
  const fetchPromedioReciente = useCallback(() => {
    const fechaFin = new Date();
    const fechaInicio = new Date();
    fechaInicio.setMonth(fechaInicio.getMonth() - 3);
    
    return fetchPromedioSemanal(
      fechaInicio.toISOString().split('T')[0],
      fechaFin.toISOString().split('T')[0]
    );
  }, [fetchPromedioSemanal]);

  // Función para refrescar todos los datos
  const refetchAll = useCallback(() => {
    refetchEstadisticas();
    refetchPatrones();
    fetchPromedioReciente();
  }, [refetchEstadisticas, refetchPatrones, fetchPromedioReciente]);

  const loading = loadingEstadisticas || loadingPatrones || loadingUser;
  const error = errorEstadisticas || errorPatrones || errorUser;

  return {
    estadisticas,
    analisisPatrones,
    user,
    loading,
    error,
    refetchAll,
    fetchPromedioReciente
  };
};