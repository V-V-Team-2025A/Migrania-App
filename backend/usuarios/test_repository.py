# usuarios/test_repository.py
"""
Repositorio fake para testing sin dependencias de Django
"""
from typing import Dict, Any, List


class MockUser:
    """Mock de usuario para testing"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.cedula = kwargs.get('cedula')
        self.telefono = kwargs.get('telefono')
        self.tipo_usuario = kwargs.get('tipo_usuario')
        self.is_active = kwargs.get('is_active', True)
        
        # Añadir cualquier otro campo que se pase
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class MockProfile:
    """Mock de perfil para testing"""
    def __init__(self, usuario, **kwargs):
        self.usuario = usuario
        self.usuario_id = usuario.id if usuario else None
        
        # Añadir todos los campos del perfil
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestUserRepository:
    """Repositorio fake simple para testing sin dependencias de Django"""

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
        user_id = self._get_next_id()
        user_data["id"] = user_id
        user_data["tipo_usuario"] = "medico"
        user_data["is_active"] = True

        usuario = MockUser(**user_data)
        self.users[user_id] = usuario

        # Crear perfil médico
        perfil = MockProfile(usuario, **profile_data)
        self.medicos[user_id] = perfil

        return usuario

    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        user_id = self._get_next_id()
        user_data["id"] = user_id
        user_data["tipo_usuario"] = "paciente"
        user_data["is_active"] = True

        usuario = MockUser(**user_data)
        self.users[user_id] = usuario

        # Crear perfil paciente
        perfil = MockProfile(usuario, **profile_data)
        self.pacientes[user_id] = perfil

        return usuario

    def create_enfermera(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        user_id = self._get_next_id()
        user_data["id"] = user_id
        user_data["tipo_usuario"] = "enfermera"
        user_data["is_active"] = True

        usuario = MockUser(**user_data)
        self.users[user_id] = usuario

        # Crear perfil enfermera
        perfil = MockProfile(usuario, **profile_data)
        self.enfermeras[user_id] = perfil

        return usuario

    def get_all_medicos(self):
        return [perfil for perfil in self.medicos.values()]

    def get_all_pacientes(self):
        return [perfil for perfil in self.pacientes.values()]

    def get_all_enfermeras(self):
        return [perfil for perfil in self.enfermeras.values()]

    def get_medico_by_license(self, numero_licencia: str):
        for perfil in self.medicos.values():
            if hasattr(perfil, 'numero_licencia') and perfil.numero_licencia == numero_licencia:
                return perfil
        return None

    def get_enfermera_by_registro(self, numero_registro: str):
        for perfil in self.enfermeras.values():
            if hasattr(perfil, 'numero_registro') and perfil.numero_registro == numero_registro:
                return perfil
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


class TestUserService:
    """Servicio simple para testing"""
    
    def __init__(self, repository=None):
        self.repository = repository or TestUserRepository()
    
    def crear_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear paciente usando el repositorio de test"""
        return self.repository.create_paciente(user_data, profile_data)
    
    def crear_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear médico usando el repositorio de test"""
        return self.repository.create_medico(user_data, profile_data)
    
    def crear_enfermera(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crear enfermera usando el repositorio de test"""
        return self.repository.create_enfermera(user_data, profile_data)
