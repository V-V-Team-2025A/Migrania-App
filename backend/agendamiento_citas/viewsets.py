# citas/viewsets.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q, Count
from datetime import date, datetime
from .models import Cita, Recordatorio, Discapacidad
from .serializers import (
    CitaListSerializer, CitaDetailSerializer, CitaCreateSerializer,
    CitaUpdateSerializer, CitaUrgenteSerializer, HorariosDisponiblesSerializer,
    RecordatorioListSerializer, RecordatorioDetailSerializer, RecordatorioCreateSerializer,
    DiscapacidadSerializer, EstadisticasCitasSerializer, ReprogramarCitaSerializer,
    CancelarCitaSerializer
)
from .services import cita_service, recordatorio_service
from usuarios.models import Usuario


class CitaViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar operaciones CRUD de citas"""
    queryset = Cita.objects.select_related('doctor', 'paciente').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'urgente', 'doctor', 'paciente', 'fecha']
    search_fields = ['paciente__first_name', 'paciente__last_name', 'doctor__first_name', 'doctor__last_name', 'motivo']
    ordering_fields = ['fecha', 'hora', 'creada_en']
    ordering = ['-fecha', '-hora']

    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'list':
            return CitaListSerializer
        elif self.action in ['create']:
            return CitaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CitaUpdateSerializer
        else:
            return CitaDetailSerializer

    def get_queryset(self):
        """Filtrar citas según el tipo de usuario"""
        user = self.request.user
        queryset = super().get_queryset()

        if hasattr(user, 'tipo_usuario'):
            if user.tipo_usuario == Usuario.TipoUsuario.PACIENTE:
                # Los pacientes solo ven sus propias citas
                queryset = queryset.filter(paciente=user)
            elif user.tipo_usuario == Usuario.TipoUsuario.MEDICO:
                # Los médicos ven sus citas asignadas
                queryset = queryset.filter(doctor=user)
            # Los administradores ven todas las citas (sin filtro adicional)

        return queryset

    def create(self, request, *args, **kwargs):
        """Crear una nueva cita usando el servicio"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Usar el servicio para crear la cita
        resultado = cita_service.crear_cita(
            doctor_id=serializer.validated_data['doctor_id'],
            paciente_id=serializer.validated_data['paciente_id'],
            fecha=serializer.validated_data['fecha'],
            hora=serializer.validated_data['hora'],
            urgente=serializer.validated_data.get('urgente', False),
            motivo=serializer.validated_data.get('motivo', '')
        )

        if resultado['success']:
            # Crear recordatorio automático
            cita_service.crear_recordatorio_automatico(resultado['cita'])

            response_serializer = CitaDetailSerializer(resultado['cita'])
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': resultado['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """Actualizar una cita existente"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Verificar permisos
        if not self._puede_modificar_cita(request.user, instance):
            return Response(
                {'error': 'No tienes permisos para modificar esta cita'},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_update(serializer)
        return Response(CitaDetailSerializer(serializer.instance).data)

    def destroy(self, request, *args, **kwargs):
        """Eliminar una cita (solo administradores)"""
        instance = self.get_object()

        if not request.user.is_staff:
            return Response(
                {'error': 'Solo los administradores pueden eliminar citas'},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def urgente(self, request):
        """Crear una cita urgente"""
        serializer = CitaUrgenteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resultado = cita_service.crear_cita_urgente(
            paciente_id=serializer.validated_data['paciente_id']
        )

        if resultado['success']:
            response_serializer = CitaDetailSerializer(resultado['cita'])
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': resultado['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def horarios_disponibles(self, request):
        """Obtener horarios disponibles para un doctor en una fecha"""
        serializer = HorariosDisponiblesSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        horarios = cita_service.obtener_horarios_disponibles(
            doctor_id=serializer.validated_data['doctor_id'],
            fecha=serializer.validated_data['fecha']
        )

        return Response({'horarios_disponibles': horarios})

    @action(detail=True, methods=['post'])
    def reprogramar(self, request, pk=None):
        """Reprogramar una cita existente"""
        cita = self.get_object()
        serializer = ReprogramarCitaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self._puede_modificar_cita(request.user, cita):
            return Response(
                {'error': 'No tienes permisos para reprogramar esta cita'},
                status=status.HTTP_403_FORBIDDEN
            )

        resultado = cita_service.reprogramar_cita(
            cita_id=cita.id,
            nueva_fecha=serializer.validated_data['nueva_fecha'],
            nueva_hora=serializer.validated_data['nueva_hora']
        )

        if resultado['success']:
            response_serializer = CitaDetailSerializer(resultado['cita'])
            return Response(response_serializer.data)
        else:
            return Response(
                {'error': resultado['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancelar una cita"""
        cita = self.get_object()
        serializer = CancelarCitaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self._puede_modificar_cita(request.user, cita):
            return Response(
                {'error': 'No tienes permisos para cancelar esta cita'},
                status=status.HTTP_403_FORBIDDEN
            )

        resultado = cita_service.cancelar_cita(
            cita_id=cita.id,
            motivo=serializer.validated_data.get('motivo', '')
        )

        if resultado['success']:
            response_serializer = CitaDetailSerializer(resultado['cita'])
            return Response(response_serializer.data)
        else:
            return Response(
                {'error': resultado['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def mis_citas(self, request):
        """Obtener citas del usuario autenticado"""
        user = request.user

        if hasattr(user, 'tipo_usuario'):
            if user.tipo_usuario == Usuario.TipoUsuario.PACIENTE:
                citas = cita_service.obtener_citas_paciente(user.id)
            elif user.tipo_usuario == Usuario.TipoUsuario.MEDICO:
                fecha_param = request.query_params.get('fecha')
                fecha = datetime.strptime(fecha_param, '%Y-%m-%d').date() if fecha_param else None
                citas = cita_service.obtener_citas_doctor(user.id, fecha)
            else:
                citas = self.get_queryset()
        else:
            citas = []

        serializer = CitaListSerializer(citas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas de citas"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Solo los administradores pueden ver estadísticas'},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = self.get_queryset()
        estadisticas = {
            'total_citas': queryset.count(),
            'citas_pendientes': queryset.filter(estado=Cita.EstadoCita.PENDIENTE).count(),
            'citas_confirmadas': queryset.filter(estado=Cita.EstadoCita.CONFIRMADA).count(),
            'citas_completadas': queryset.filter(estado=Cita.EstadoCita.COMPLETADA).count(),
            'citas_canceladas': queryset.filter(estado=Cita.EstadoCita.CANCELADA).count(),
            'citas_urgentes': queryset.filter(urgente=True).count(),
        }

        serializer = EstadisticasCitasSerializer(estadisticas)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def urgentes(self, request):
        """Obtener todas las citas urgentes"""
        citas_urgentes = cita_service.obtener_citas_urgentes()
        serializer = CitaListSerializer(citas_urgentes, many=True)
        return Response(serializer.data)

    def _puede_modificar_cita(self, user, cita):
        """Verificar si un usuario puede modificar una cita"""
        if user.is_staff:
            return True

        if hasattr(user, 'tipo_usuario'):
            if user.tipo_usuario == Usuario.TipoUsuario.PACIENTE:
                return cita.paciente == user
            elif user.tipo_usuario == Usuario.TipoUsuario.MEDICO:
                return cita.doctor == user

        return False


class RecordatorioViewSet(viewsets.ModelViewSet):
    """ViewSet para manejar operaciones CRUD de recordatorios"""
    queryset = Recordatorio.objects.select_related('paciente', 'cita').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'enviado', 'paciente', 'fecha']
    search_fields = ['paciente__first_name', 'paciente__last_name', 'mensaje']
    ordering_fields = ['fecha', 'hora', 'creado_en']
    ordering = ['-fecha', '-hora']

    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'list':
            return RecordatorioListSerializer
        elif self.action == 'create':
            return RecordatorioCreateSerializer
        else:
            return RecordatorioDetailSerializer

    def get_queryset(self):
        """Filtrar recordatorios según el tipo de usuario"""
        user = self.request.user
        queryset = super().get_queryset()

        if hasattr(user, 'tipo_usuario'):
            if user.tipo_usuario == Usuario.TipoUsuario.PACIENTE:
                # Los pacientes solo ven sus propios recordatorios
                queryset = queryset.filter(paciente=user)
            elif user.tipo_usuario == Usuario.TipoUsuario.MEDICO:
                # Los médicos ven recordatorios de sus pacientes con citas
                queryset = queryset.filter(cita__doctor=user)
            # Los administradores ven todos los recordatorios

        return queryset

    def create(self, request, *args, **kwargs):
        """Crear un nuevo recordatorio usando el servicio"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener el paciente
        from usuarios.repositories import DjangoUserRepository
        user_repo = DjangoUserRepository()
        paciente = user_repo.get_user_by_id(serializer.validated_data['paciente_id'])

        resultado = recordatorio_service.crear_recordatorio(
            paciente=paciente,
            fecha=serializer.validated_data['fecha'],
            hora=serializer.validated_data['hora'],
            mensaje=serializer.validated_data['mensaje'],
            tipo=serializer.validated_data.get('tipo', 'cita_proxima')
        )

        if resultado['success']:
            response_serializer = RecordatorioDetailSerializer(resultado['recordatorio'])
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': resultado['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def mis_recordatorios(self, request):
        """Obtener recordatorios del usuario autenticado"""
        user = request.user

        if hasattr(user, 'tipo_usuario') and user.tipo_usuario == Usuario.TipoUsuario.PACIENTE:
            recordatorios = recordatorio_service.obtener_recordatorios_paciente(user.id)
            serializer = RecordatorioListSerializer(recordatorios, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Solo los pacientes pueden consultar sus recordatorios'},
                status=status.HTTP_403_FORBIDDEN
            )

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Obtener recordatorios pendientes de envío"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Solo los administradores pueden ver recordatorios pendientes'},
                status=status.HTTP_403_FORBIDDEN
            )

        recordatorios_pendientes = recordatorio_service.obtener_recordatorios_pendientes()
        serializer = RecordatorioListSerializer(recordatorios_pendientes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def marcar_enviado(self, request, pk=None):
        """Marcar un recordatorio como enviado"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Solo los administradores pueden marcar recordatorios como enviados'},
                status=status.HTTP_403_FORBIDDEN
            )

        recordatorio = self.get_object()
        success = recordatorio_service.marcar_recordatorio_enviado(recordatorio.id)

        if success:
            response_serializer = RecordatorioDetailSerializer(recordatorio)
            recordatorio.refresh_from_db()  # Refrescar para obtener datos actualizados
            return Response(response_serializer.data)
        else:
            return Response(
                {'error': 'Error al marcar recordatorio como enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def procesar_pendientes(self, request):
        """Procesar todos los recordatorios pendientes"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Solo los administradores pueden procesar recordatorios'},
                status=status.HTTP_403_FORBIDDEN
            )

        resultado = recordatorio_service.procesar_recordatorios_pendientes()
        return Response(resultado)


class UtilsViewSet(viewsets.ViewSet):
    """ViewSet para funciones utilitarias"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def opciones_discapacidad(self, request):
        """Obtener opciones de discapacidad"""
        opciones = [{'value': choice[0], 'label': choice[1]} for choice in Discapacidad.choices]
        return Response(opciones)

    @action(detail=False, methods=['get'])
    def estados_cita(self, request):
        """Obtener estados disponibles para citas"""
        estados = [{'value': choice[0], 'label': choice[1]} for choice in Cita.EstadoCita.choices]
        return Response(estados)

    @action(detail=False, methods=['get'])
    def tipos_recordatorio(self, request):
        """Obtener tipos de recordatorio disponibles"""
        tipos = [{'value': choice[0], 'label': choice[1]} for choice in Recordatorio.TipoRecordatorio.choices]
        return Response(tipos)

    @action(detail=False, methods=['get'])
    def doctores_disponibles(self, request):
        """Obtener doctores disponibles para una fecha y hora específica"""
        fecha = request.query_params.get('fecha')
        hora = request.query_params.get('hora')

        if not fecha or not hora:
            return Response(
                {'error': 'Se requieren los parámetros fecha y hora'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doctores_disponibles = cita_service.obtener_doctores_disponibles(fecha, hora)
            doctores_data = []

            for doctor in doctores_disponibles:
                doctores_data.append({
                    'id': doctor.id,
                    'nombre': doctor.get_full_name(),
                    'email': doctor.email,
                    'especialidad': getattr(doctor, 'especialidad', None)
                })

            return Response({'doctores_disponibles': doctores_data})

        except Exception as e:
            return Response(
                {'error': f'Error al obtener doctores disponibles: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )