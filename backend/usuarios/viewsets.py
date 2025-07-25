# usuarios/viewsets.py 
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import MedicoProfile, PacienteProfile, EnfermeraProfile
from .serializers import (
    UsuarioCompletoSerializer, 
    RegistroMedicoSerializer, 
    RegistroPacienteSerializer, 
    RegistroEnfermeraSerializer
)
from .permissions import EsMedicoOEnfermera

Usuario = get_user_model()

#  VIEWSET PROTEGIDO - Solo para usuarios autenticados
class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """Gestión de usuarios - Solo lectura y acciones específicas"""
    serializer_class = UsuarioCompletoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Usuarios ven solo su info, personal médico ve todo"""
        user = self.request.user
        if user.es_medico or user.es_enfermera:
            return Usuario.objects.all().select_related(
                'perfil_medico', 'perfil_paciente', 'perfil_enfermera'
            )
        else:
            return Usuario.objects.filter(id=user.id).select_related(
                'perfil_medico', 'perfil_paciente', 'perfil_enfermera'
            )
    
    @action(detail=False, methods=['get'])
    def mi_perfil(self, request):
        """ GET /api/usuarios/mi-perfil/ - Perfil del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """ GET /api/usuarios/dashboard/ - Dashboard según rol"""
        user = request.user
        
        base_data = {
            'usuario': {
                'id': user.id,
                'nombre_completo': user.get_full_name(),
                'email': user.email,
                'tipo_usuario': user.tipo_usuario,
            }
        }
        
        if user.es_medico:
            perfil = getattr(user, 'perfil_medico', None)
            base_data.update({
                'tipo_usuario': 'medico',
                'especializacion': perfil.especializacion if perfil else None,
                'numero_licencia': perfil.numero_licencia if perfil else None,
                'permisos': {
                    'puede_ver_todos_pacientes': True,
                    'puede_crear_diagnosticos': True,
                    'puede_prescribir_tratamientos': True,
                    'puede_agendar_citas': True,
                }
            })
        
        elif user.es_enfermera:
            perfil = getattr(user, 'perfil_enfermera', None)
            base_data.update({
                'tipo_usuario': 'enfermera',
                'departamento': perfil.departamento if perfil else None,
                'permisos': {
                    'puede_ver_pacientes_asignados': True,
                    'puede_registrar_vitales': True,
                    'puede_administrar_medicamentos': True,
                    'puede_agendar_citas': True,
                }
            })
        
        else:  # paciente
            perfil = getattr(user, 'perfil_paciente', None)
            base_data.update({
                'tipo_usuario': 'paciente',
                'grupo_sanguineo': perfil.grupo_sanguineo if perfil else None,
                'permisos': {
                    'puede_agendar_citas': True,
                    'puede_ver_historial_propio': True,
                    'puede_completar_evaluaciones': True,
                    'puede_registrar_episodios': True,
                }
            })
        
        return Response(base_data)
    
    @action(detail=False, methods=['get'], permission_classes=[EsMedicoOEnfermera])
    def medicos(self, request):
        """ GET /api/usuarios/medicos/ - Lista médicos (solo personal médico)"""
        medicos = MedicoProfile.objects.filter(
            usuario__is_active=True
        ).select_related('usuario')
        
        data = []
        for medico in medicos:
            data.append({
                'id': medico.usuario.id,
                'nombre_completo': medico.usuario.get_full_name(),
                'email': medico.usuario.email,
                'especializacion': medico.get_especializacion_display(),
                'numero_licencia': medico.numero_licencia,
                'anos_experiencia': medico.anos_experiencia,
            })
        
        return Response({'medicos': data, 'count': len(data)})
    
    @action(detail=False, methods=['get'], permission_classes=[EsMedicoOEnfermera])
    def pacientes(self, request):
        """ GET /api/usuarios/pacientes/ - Lista pacientes (solo personal médico)"""
        pacientes = PacienteProfile.objects.filter(
            usuario__is_active=True
        ).select_related('usuario')
        
        data = []
        for paciente in pacientes:
            data.append({
                'id': paciente.usuario.id,
                'nombre_completo': paciente.usuario.get_full_name(),
                'email': paciente.usuario.email,
                'grupo_sanguineo': paciente.grupo_sanguineo,
                'contacto_emergencia': paciente.contacto_emergencia_nombre,
                'telefono_emergencia': paciente.contacto_emergencia_telefono,
            })
        
        return Response({'pacientes': data, 'count': len(data)})
    
    @action(detail=False, methods=['get'], permission_classes=[EsMedicoOEnfermera])
    def enfermeras(self, request):
        """ GET /api/usuarios/enfermeras/ - Lista enfermeras (solo personal médico)"""
        enfermeras = EnfermeraProfile.objects.filter(
            usuario__is_active=True
        ).select_related('usuario')
        
        data = []
        for enfermera in enfermeras:
            data.append({
                'id': enfermera.usuario.id,
                'nombre_completo': enfermera.usuario.get_full_name(),
                'email': enfermera.usuario.email,
                'numero_registro': enfermera.numero_registro,
                'departamento': enfermera.departamento,
            })
        
        return Response({'enfermeras': data, 'count': len(data)})

# VIEWSETS PÚBLICOS DE REGISTRO (sin autenticación)

class RegistroMedicoViewSet(viewsets.GenericViewSet):
    """ Registro de médicos - Público con formulario DRF"""
    serializer_class = RegistroMedicoSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Usuario.objects.none()
    
    def list(self, request):
        """GET /api/registro-medico/ - Muestra formulario de registro"""
        return Response({
            'message': 'Registro de médicos',
            'instruction': 'Complete el formulario para registrar un nuevo médico',
            'endpoint_info': {
                'method': 'POST',
                'url': '/api/registro-medico/',
                'content_type': 'application/json'
            }
        })
    
    def create(self, request):
        """POST /api/registro-medico/ - Crear médico"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'Médico registrado exitosamente',
                'usuario': {
                    'id': user.id,
                    'email': user.email,
                    'nombre_completo': user.get_full_name(),
                    'tipo_usuario': user.tipo_usuario
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Error en el registro',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RegistroPacienteViewSet(viewsets.GenericViewSet):
    """ Registro de pacientes - Público con formulario DRF"""
    serializer_class = RegistroPacienteSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Usuario.objects.none()
    
    def list(self, request):
        """GET /api/registro-paciente/ - Muestra formulario de registro"""
        return Response({
            'message': 'Registro de pacientes',
            'instruction': 'Complete el formulario para registrar un nuevo paciente',
            'endpoint_info': {
                'method': 'POST',
                'url': '/api/registro-paciente/',
                'content_type': 'application/json'
            }
        })
    
    def create(self, request):
        """POST /api/registro-paciente/ - Crear paciente"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'Paciente registrado exitosamente',
                'usuario': {
                    'id': user.id,
                    'email': user.email,
                    'nombre_completo': user.get_full_name(),
                    'tipo_usuario': user.tipo_usuario
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Error en el registro',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RegistroEnfermeraViewSet(viewsets.GenericViewSet):
    """ Registro de enfermeras - Público con formulario DRF"""
    serializer_class = RegistroEnfermeraSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Usuario.objects.none()
    
    def list(self, request):
        """GET /api/registro-enfermera/ - Muestra formulario de registro"""
        return Response({
            'message': 'Registro de enfermeras',
            'instruction': 'Complete el formulario para registrar una nueva enfermera',
            'endpoint_info': {
                'method': 'POST',
                'url': '/api/registro-enfermera/',
                'content_type': 'application/json'
            }
        })
    
    def create(self, request):
        """POST /api/registro-enfermera/ - Crear enfermera"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'Enfermera registrada exitosamente',
                'usuario': {
                    'id': user.id,
                    'email': user.email,
                    'nombre_completo': user.get_full_name(),
                    'tipo_usuario': user.tipo_usuario
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Error en el registro',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)