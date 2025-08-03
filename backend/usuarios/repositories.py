# usuarios/repositories.py
import abc
from typing import Optional, List, Dict, Any
from django.db import transaction
# NO importar modelos aquí - importar solo donde es seguro


class AbstractUserRepository(abc.ABC):
    """Contrato base para todos los repositorios de usuarios"""

    @abc.abstractmethod
    def get_all_users(self):
        """Obtener todos los usuarios activos"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int):
        """Obtener usuario por ID"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_email(self, email: str):
        """Obtener usuario por email"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_cedula(self, cedula: str):
        """Obtener usuario por cédula"""
        raise NotImplementedError

    @abc.abstractmethod
    def create_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear un médico con su perfil"""
        raise NotImplementedError

    @abc.abstractmethod
    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear un paciente con su perfil"""
        raise NotImplementedError

    @abc.abstractmethod
    def create_enfermera(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear una enfermera con su perfil"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_medicos(self):
        """Obtener todos los médicos activos"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_pacientes(self):
        """Obtener todos los pacientes activos"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_enfermeras(self):
        """Obtener todas las enfermeras activas"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_medico_by_license(self, numero_licencia: str):
        """Obtener médico por número de licencia"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_enfermera_by_registro(self, numero_registro: str):
        """Obtener enfermera por número de registro"""
        raise NotImplementedError

    @abc.abstractmethod
    def update_usuario(self, user_id: int, data: Dict[str, Any]):
        """Actualizar datos de usuario"""
        raise NotImplementedError

    @abc.abstractmethod
    def deactivate_usuario(self, user_id: int) -> bool:
        """Desactivar usuario (soft delete)"""
        raise NotImplementedError

class DjangoUserRepository(AbstractUserRepository):
    """Implementación concreta usando el ORM de Django"""

    def __init__(self):
        """Importar modelos solo cuando se instancia la clase"""
        from .models import Usuario, MedicoProfile, PacienteProfile, EnfermeraProfile
        self.Usuario = Usuario
        self.MedicoProfile = MedicoProfile
        self.PacienteProfile = PacienteProfile
        self.EnfermeraProfile = EnfermeraProfile

    def get_all_users(self):
        """Obtener todos los usuarios activos con sus perfiles relacionados"""
        return (
            self.Usuario.objects.filter(is_active=True)
            .select_related("perfil_medico", "perfil_paciente", "perfil_enfermera")
            .order_by("date_joined")
        )

    def get_user_by_id(self, user_id: int):
        """Obtener usuario por ID con perfiles relacionados"""
        try:
            return self.Usuario.objects.select_related(
                "perfil_medico", "perfil_paciente", "perfil_enfermera"
            ).get(id=user_id, is_active=True)
        except self.Usuario.DoesNotExist:
            return None

    def get_user_by_email(self, email: str):
        """Obtener usuario por email"""
        try:
            return self.Usuario.objects.select_related(
                "perfil_medico", "perfil_paciente", "perfil_enfermera"
            ).get(email=email, is_active=True)
        except self.Usuario.DoesNotExist:
            return None

    def get_user_by_cedula(self, cedula: str):
        """Obtener usuario por cédula"""
        try:
            return self.Usuario.objects.select_related(
                "perfil_medico", "perfil_paciente", "perfil_enfermera"
            ).get(cedula=cedula, is_active=True)
        except self.Usuario.DoesNotExist:
            return None

    @transaction.atomic
    def create_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear médico con transacción atómica"""
        # Establecer tipo de usuario
        user_data["tipo_usuario"] = self.Usuario.TipoUsuario.MEDICO

        # Crear usuario usando el manager personalizado
        usuario = self.Usuario.objects.create_user(**user_data)

        # Crear perfil médico
        self.MedicoProfile.objects.create(usuario=usuario, **profile_data)

        return usuario

    @transaction.atomic
    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear paciente con transacción atómica"""
        # Establecer tipo de usuario
        user_data["tipo_usuario"] = self.Usuario.TipoUsuario.PACIENTE

        # Crear usuario usando el manager personalizado
        usuario = self.Usuario.objects.create_user(**user_data)

        # Crear perfil paciente
        self.PacienteProfile.objects.create(usuario=usuario, **profile_data)

        return usuario

    @transaction.atomic
    def create_enfermera(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear enfermera con transacción atómica"""
        # Establecer tipo de usuario
        user_data["tipo_usuario"] = self.Usuario.TipoUsuario.ENFERMERA

        # Crear usuario usando el manager personalizado
        usuario = self.Usuario.objects.create_user(**user_data)

        # Crear perfil enfermera
        self.EnfermeraProfile.objects.create(usuario=usuario, **profile_data)

        return usuario

    def get_all_medicos(self):
        """Obtener todos los médicos activos"""
        return (
            self.MedicoProfile.objects.filter(usuario__is_active=True)
            .select_related("usuario")
            .order_by("usuario__date_joined")
        )

    def get_all_pacientes(self):
        """Obtener todos los pacientes activos"""
        return (
            self.PacienteProfile.objects.filter(usuario__is_active=True)
            .select_related("usuario")
            .order_by("usuario__date_joined")
        )

    def get_all_enfermeras(self):
        """Obtener todas las enfermeras activas"""
        return (
            self.EnfermeraProfile.objects.filter(usuario__is_active=True)
            .select_related("usuario")
            .order_by("usuario__date_joined")
        )

    def get_medico_by_license(self, numero_licencia: str):
        """Obtener médico por número de licencia"""
        try:
            return self.MedicoProfile.objects.select_related("usuario").get(
                numero_licencia=numero_licencia, usuario__is_active=True
            )
        except self.MedicoProfile.DoesNotExist:
            return None

    def get_enfermera_by_registro(self, numero_registro: str):
        """Obtener enfermera por número de registro"""
        try:
            return self.EnfermeraProfile.objects.select_related("usuario").get(
                numero_registro=numero_registro, usuario__is_active=True
            )
        except self.EnfermeraProfile.DoesNotExist:
            return None

    @transaction.atomic
    def update_usuario(self, user_id: int, data: Dict[str, Any]):
        """Actualizar datos de usuario"""
        try:
            usuario = self.Usuario.objects.get(id=user_id, is_active=True)

            # Actualizar campos permitidos
            allowed_fields = [
                "first_name",
                "last_name",
                "telefono",
                "direccion",
                "fecha_nacimiento",
                "genero",
            ]

            for field, value in data.items():
                if field in allowed_fields and hasattr(usuario, field):
                    setattr(usuario, field, value)

            usuario.save()
            return usuario

        except self.Usuario.DoesNotExist:
            return None

    def deactivate_usuario(self, user_id: int) -> bool:
        """Desactivar usuario (soft delete)"""
        try:
            usuario = self.Usuario.objects.get(id=user_id)
            usuario.is_active = False
            usuario.save()
            return True
        except self.Usuario.DoesNotExist:
            return False

class FakeUserRepository(AbstractUserRepository):
    """
    Repositorio fake que usa modelos REALES de Django para testing BDD
    pero con modelos Django manejados en memoria sin tocar la base de datos
    """
    
    def __init__(self):
        self._usuarios = []
        self._pacientes = []
        self._medicos = []
        self._enfermeras = []
        self._models_loaded = False
        # Referencias a los modelos (se cargan lazy)
        self.Usuario = None
        self.PacienteProfile = None
        self.MedicoProfile = None
        self.EnfermeraProfile = None
        self._next_id = 1

    def _load_models(self):
        """Cargar modelos Django solo cuando se necesiten (lazy loading)"""
        if not self._models_loaded:
            # Importar AQUÍ, no al nivel del módulo para evitar problemas de configuración
            from .models import Usuario, MedicoProfile, PacienteProfile, EnfermeraProfile
            self.Usuario = Usuario
            self.PacienteProfile = PacienteProfile
            self.MedicoProfile = MedicoProfile
            self.EnfermeraProfile = EnfermeraProfile
            self._models_loaded = True

    def _get_next_id(self):
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def get_all_users(self):
        return [u for u in self._usuarios if u.is_active]

    def get_user_by_id(self, user_id: int):
        return next((u for u in self._usuarios if u.id == user_id and u.is_active), None)

    def get_user_by_email(self, email: str):
        return next((u for u in self._usuarios if u.email == email and u.is_active), None)

    def get_user_by_cedula(self, cedula: str):
        return next((u for u in self._usuarios if u.cedula == cedula and u.is_active), None)

    def create_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear médico usando modelos REALES de Django pero en memoria"""
        self._load_models()
        
        user_data['tipo_usuario'] = self.Usuario.TipoUsuario.MEDICO
        user_data['is_active'] = True
        user_data['id'] = self._get_next_id()
        
        # Crear usuario REAL usando el modelo de Django
        usuario = self.Usuario(**user_data)
        usuario.pk = user_data['id']  # Simular que tiene ID
        self._usuarios.append(usuario)
        
        # Crear perfil médico REAL
        profile_data['usuario'] = usuario
        profile_data['id'] = self._get_next_id()
        medico_profile = self.MedicoProfile(**profile_data)
        medico_profile.pk = profile_data['id']
        self._medicos.append(medico_profile)
        
        return usuario

    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear paciente usando modelos REALES de Django pero en memoria"""
        self._load_models()
        
        user_data['tipo_usuario'] = self.Usuario.TipoUsuario.PACIENTE
        user_data['is_active'] = True
        user_data['id'] = self._get_next_id()
        
        # Crear usuario REAL usando el modelo de Django
        usuario = self.Usuario(**user_data)
        usuario.pk = user_data['id']  # Simular que tiene ID
        self._usuarios.append(usuario)
        
        # Crear perfil paciente REAL
        profile_data['usuario'] = usuario
        profile_data['id'] = self._get_next_id()
        paciente_profile = self.PacienteProfile(**profile_data)
        paciente_profile.pk = profile_data['id']
        self._pacientes.append(paciente_profile)
        
        return usuario

    def create_enfermera(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear enfermera usando modelos REALES de Django pero en memoria"""
        self._load_models()
        
        user_data['tipo_usuario'] = self.Usuario.TipoUsuario.ENFERMERA
        user_data['is_active'] = True
        user_data['id'] = self._get_next_id()
        
        # Crear usuario REAL usando el modelo de Django
        usuario = self.Usuario(**user_data)
        usuario.pk = user_data['id']  # Simular que tiene ID
        self._usuarios.append(usuario)
        
        # Crear perfil enfermera REAL
        profile_data['usuario'] = usuario
        profile_data['id'] = self._get_next_id()
        enfermera_profile = self.EnfermeraProfile(**profile_data)
        enfermera_profile.pk = profile_data['id']
        self._enfermeras.append(enfermera_profile)
        
        return usuario

    def get_all_medicos(self):
        return self._medicos

    def get_all_pacientes(self):
        return self._pacientes

    def get_all_enfermeras(self):
        return self._enfermeras

    def get_medico_by_license(self, numero_licencia: str):
        return next((m for m in self._medicos if m.numero_licencia == numero_licencia), None)

    def get_enfermera_by_registro(self, numero_registro: str):
        return next((e for e in self._enfermeras if e.numero_registro == numero_registro), None)

    def update_usuario(self, user_id: int, data: Dict[str, Any]):
        usuario = self.get_user_by_id(user_id)
        if usuario:
            for key, value in data.items():
                setattr(usuario, key, value)
            return usuario
        return None

    def deactivate_usuario(self, user_id: int) -> bool:
        usuario = self.get_user_by_id(user_id)
        if usuario:
            usuario.is_active = False
            return True
        return False
