from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from .models import EpisodioCefalea
from .serializers import EpisodioCefaleaSerializer, CrearEpisodioCefaleaSerializer
from .permissions import EsPaciente, EsPropietarioDelEpisodioOPersonalMedico
from .episodio_cefalea_service import episodio_cefalea_service


class EpisodioCefaleaViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet para la gestión de la bitácora de episodios de cefalea.

    Permite a los pacientes registrar sus episodios y a todo el personal
    (paciente, médico, enfermera) visualizar los registros con los
    permisos adecuados.

    Endpoints:
    - POST /api/evaluaciones/episodios/ - Crear un nuevo episodio (Solo Pacientes)
    - GET /api/evaluaciones/episodios/ - Lista los episodios (Paciente ve los suyos, Personal Médico puede filtrar por paciente)
    - GET /api/evaluaciones/episodios/{id}/ - Detalle de un episodio específico
    """
    queryset = EpisodioCefalea.objects.all().select_related('paciente').order_by('-creado_en')

    def get_serializer_class(self):
        """
        Selecciona el serializer adecuado según la acción.
        """
        if self.action == 'create':
            return CrearEpisodioCefaleaSerializer
        return EpisodioCefaleaSerializer

    def get_permissions(self):
        """
        Asigna los permisos adecuados según la acción.
        """
        if self.action == 'create':
            # Solo los pacientes autenticados pueden crear
            return [permissions.IsAuthenticated(), EsPaciente()]

        # Para 'list' y 'retrieve'
        return [permissions.IsAuthenticated(), EsPropietarioDelEpisodioOPersonalMedico()]

    def get_serializer_context(self):
        """
        Inyecta el 'request' en el contexto del serializer.
        Esencial para que el serializer de creación pueda acceder al usuario
        y aplicar la lógica condicional de género.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        """
        Filtra los episodios de manera inteligente según el rol del usuario.
        """
        usuario = self.request.user
        queryset = super().get_queryset()

        # Si el usuario es médico o enfermera
        if usuario.es_medico or usuario.es_enfermera:
            # Pueden filtrar los episodios de un paciente específico usando un query param
            paciente_id = self.request.query_params.get('paciente_id', None)
            if paciente_id:
                return queryset.filter(paciente_id=paciente_id)
            # Si no especifican un paciente, no devolvemos nada para no exponer datos masivos.
            return queryset.none()

            # Si el usuario es paciente, solo puede ver sus propios episodios
        if usuario.es_paciente:
            return queryset.filter(paciente=usuario)

        # En cualquier otro caso, no devolver nada.
        return queryset.none()

    def perform_create(self, serializer):
        """
        Personaliza el proceso de guardado de un nuevo episodio.
        """
        episodio_cefalea_service.registrar_nuevo_episodio(
            paciente=self.request.user,
            datos_validados=serializer.validated_data
        )
