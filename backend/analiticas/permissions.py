from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth import get_user_model


User = get_user_model()


class EstadisticaHistorialPermission(BasePermission):
    """
    Permisos para acceder a estadísticas historial.
    Solo usuarios autenticados pueden ver sus propias estadísticas.
    """
    
    def has_permission(self, request, view):
        """Verificar que el usuario esté autenticado"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Verificar que el usuario solo acceda a sus propios datos"""
        # Si el objeto tiene un campo usuario, verificar que sea el mismo
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        return True


class AnalisisEstadisticaPermission(BasePermission):
    """
    Permisos específicos para análisis estadísticos.
    Permite lectura a usuarios autenticados y escritura solo al propietario.
    """
    
    def has_permission(self, request, view):
        """Verificar permisos generales"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Métodos de lectura permitidos para usuarios autenticados
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Métodos de escritura requieren validación adicional
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Verificar permisos específicos del objeto"""
        # Lectura permitida para el propietario
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            if hasattr(obj, 'usuario'):
                return obj.usuario == request.user
            return True
        
        # Escritura solo para el propietario
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        
        return True


class PromedioSemanalPermission(EstadisticaHistorialPermission):
    """Permisos específicos para promedio semanal de episodios"""
    pass


class DuracionPromedioPermission(EstadisticaHistorialPermission):
    """Permisos específicos para duración promedio de episodios"""
    pass


class IntensidadPromedioPermission(EstadisticaHistorialPermission):
    """Permisos específicos para intensidad promedio del dolor"""
    pass


class AsociacionHormonalPermission(EstadisticaHistorialPermission):
    """Permisos específicos para asociación hormonal"""
    pass


class EvolucionMIDASPermission(EstadisticaHistorialPermission):
    """Permisos específicos para evolución MIDAS"""
    pass


class DesencadenantesComunesPermission(EstadisticaHistorialPermission):
    """Permisos específicos para desencadenantes comunes"""
    pass


class EstadisticaCombinadaPermission(BasePermission):
    """
    Permisos para análisis combinados de estadísticas.
    Permite acceso a múltiples tipos de estadísticas simultáneamente.
    """
    
    def has_permission(self, request, view):
        """Verificar que el usuario esté autenticado para análisis combinados"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Verificar permisos para análisis combinados"""
        return request.user and request.user.is_authenticated
