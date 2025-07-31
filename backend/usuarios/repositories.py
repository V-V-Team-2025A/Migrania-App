# usuarios/repositories.py
import abc
from typing import Optional, List, Dict, Any
from django.db import transaction
from .models import Usuario, MedicoProfile, PacienteProfile, EnfermeraProfile


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

    def get_all_users(self):
        """Obtener todos los usuarios activos con sus perfiles relacionados"""
        return (
            Usuario.objects.filter(is_active=True)
            .select_related("perfil_medico", "perfil_paciente", "perfil_enfermera")
            .order_by("date_joined")
        )

    def get_user_by_id(self, user_id: int):
        """Obtener usuario por ID con perfiles relacionados"""
        try:
            return Usuario.objects.select_related(
                "perfil_medico", "perfil_paciente", "perfil_enfermera"
            ).get(id=user_id, is_active=True)
        except Usuario.DoesNotExist:
            return None

    def get_user_by_email(self, email: str):
        """Obtener usuario por email"""
        try:
            return Usuario.objects.select_related(
                "perfil_medico", "perfil_paciente", "perfil_enfermera"
            ).get(email=email, is_active=True)
        except Usuario.DoesNotExist:
            return None

    def get_user_by_cedula(self, cedula: str):
        """Obtener usuario por cédula"""
        try:
            return Usuario.objects.select_related(
                "perfil_medico", "perfil_paciente", "perfil_enfermera"
            ).get(cedula=cedula, is_active=True)
        except Usuario.DoesNotExist:
            return None

    @transaction.atomic
    def create_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear médico con transacción atómica"""
        # Establecer tipo de usuario
        user_data["tipo_usuario"] = Usuario.TipoUsuario.MEDICO

        # Crear usuario usando el manager personalizado
        usuario = Usuario.objects.create_user(**user_data)

        # Crear perfil médico
        MedicoProfile.objects.create(usuario=usuario, **profile_data)

        return usuario

    @transaction.atomic
    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear paciente con transacción atómica"""
        # Establecer tipo de usuario
        user_data["tipo_usuario"] = Usuario.TipoUsuario.PACIENTE

        # Crear usuario usando el manager personalizado
        usuario = Usuario.objects.create_user(**user_data)

        # Crear perfil paciente
        PacienteProfile.objects.create(usuario=usuario, **profile_data)

        return usuario

    @transaction.atomic
    def create_enfermera(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear enfermera con transacción atómica"""
        # Establecer tipo de usuario
        user_data["tipo_usuario"] = Usuario.TipoUsuario.ENFERMERA

        # Crear usuario usando el manager personalizado
        usuario = Usuario.objects.create_user(**user_data)

        # Crear perfil enfermera
        EnfermeraProfile.objects.create(usuario=usuario, **profile_data)

        return usuario

    def get_all_medicos(self):
        """Obtener todos los médicos activos"""
        return (
            MedicoProfile.objects.filter(usuario__is_active=True)
            .select_related("usuario")
            .order_by("usuario__date_joined")
        )

    def get_all_pacientes(self):
        """Obtener todos los pacientes activos"""
        return (
            PacienteProfile.objects.filter(usuario__is_active=True)
            .select_related("usuario")
            .order_by("usuario__date_joined")
        )

    def get_all_enfermeras(self):
        """Obtener todas las enfermeras activas"""
        return (
            EnfermeraProfile.objects.filter(usuario__is_active=True)
            .select_related("usuario")
            .order_by("usuario__date_joined")
        )

    def get_medico_by_license(self, numero_licencia: str):
        """Obtener médico por número de licencia"""
        try:
            return MedicoProfile.objects.select_related("usuario").get(
                numero_licencia=numero_licencia, usuario__is_active=True
            )
        except MedicoProfile.DoesNotExist:
            return None

    def get_enfermera_by_registro(self, numero_registro: str):
        """Obtener enfermera por número de registro"""
        try:
            return EnfermeraProfile.objects.select_related("usuario").get(
                numero_registro=numero_registro, usuario__is_active=True
            )
        except EnfermeraProfile.DoesNotExist:
            return None

    @transaction.atomic
    def update_usuario(self, user_id: int, data: Dict[str, Any]):
        """Actualizar datos de usuario"""
        try:
            usuario = Usuario.objects.get(id=user_id, is_active=True)

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

        except Usuario.DoesNotExist:
            return None

    def deactivate_usuario(self, user_id: int) -> bool:
        """Desactivar usuario (soft delete)"""
        try:
            usuario = Usuario.objects.get(id=user_id)
            usuario.is_active = False
            usuario.save()
            return True
        except Usuario.DoesNotExist:
            return False

class InMemoryUserRepository(AbstractUserRepository):
    """Implementación en memoria para pruebas"""

    def __init__(self):
        self.users = {}
        self.medicos = {}
        self.pacientes = {}
        self.enfermeras = {}
        self._next_id = 1

    def _get_next_id(self):
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def get_all_users(self):
        return [user for user in self.users.values() if user.is_active]

    def get_user_by_id(self, user_id: int):
        user = self.users.get(user_id)
        return user if user and user.is_active else None

    def get_user_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email and user.is_active:
                return user
        return None

    def get_user_by_cedula(self, cedula: str):
        for user in self.users.values():
            if user.cedula == cedula and user.is_active:
                return user
        return None

    def create_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        # Simular creación de médico en memoria
        user_id = self._get_next_id()
        user_data["id"] = user_id
        user_data["tipo_usuario"] = "medico"

        # Crear mock de usuario (en una implementación real usarías factories o mocks)
        usuario = type("Usuario", (), user_data)()
        self.users[user_id] = usuario

        # Simular perfil médico
        profile_data["usuario_id"] = user_id
        self.medicos[user_id] = profile_data

        return usuario

    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        # Implementación similar para pacientes
        user_id = self._get_next_id()
        user_data["id"] = user_id
        user_data["tipo_usuario"] = "paciente"

        usuario = type("Usuario", (), user_data)()
        self.users[user_id] = usuario

        profile_data["usuario_id"] = user_id
        self.pacientes[user_id] = profile_data

        return usuario

    def create_enfermera(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        # Implementación similar para enfermeras
        user_id = self._get_next_id()
        user_data["id"] = user_id
        user_data["tipo_usuario"] = "enfermera"

        usuario = type("Usuario", (), user_data)()
        self.users[user_id] = usuario

        profile_data["usuario_id"] = user_id
        self.enfermeras[user_id] = profile_data

        return usuario

    def get_all_medicos(self):
        return [profile for profile in self.medicos.values()]

    def get_all_pacientes(self):
        return [profile for profile in self.pacientes.values()]

    def get_all_enfermeras(self):
        return [profile for profile in self.enfermeras.values()]

    def get_medico_by_license(self, numero_licencia: str):
        for profile in self.medicos.values():
            if profile.get("numero_licencia") == numero_licencia:
                return profile
        return None

    def get_enfermera_by_registro(self, numero_registro: str):
        for profile in self.enfermeras.values():
            if profile.get("numero_registro") == numero_registro:
                return profile
        return None

    def update_usuario(self, user_id: int, data: Dict[str, Any]):
        user = self.users.get(user_id)
        if user and user.is_active:
            for key, value in data.items():
                setattr(user, key, value)
            return user
        return None

    def deactivate_usuario(self, user_id: int) -> bool:
        user = self.users.get(user_id)
        if user:
            user.is_active = False
            return True
        return False
