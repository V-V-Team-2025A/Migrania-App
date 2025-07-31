# usuarios/fake_repository.py
"""
Repositorio fake EXACTAMENTE como en el ejemplo - usa modelos reales pero los maneja en memoria
"""
import abc
from typing import Dict, Any

# NO IMPORTAR MODELOS AQUÍ - usar lazy loading como en tu ejemplo funcional


class AbstractUserRepository(abc.ABC):
    """Contrato base - misma interfaz que repositories.py"""
    
    @abc.abstractmethod
    def get_user_by_email(self, email: str):
        raise NotImplementedError

    @abc.abstractmethod
    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        raise NotImplementedError

    @abc.abstractmethod
    def create_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        raise NotImplementedError


class FakeUserRepository(AbstractUserRepository):
    """
    Repositorio fake IGUAL que en tu ejemplo - usa modelos REALES pero en memoria
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

    def _load_models(self):
        """Cargar modelos solo cuando se necesiten - IGUAL que en tu ejemplo"""
        if not self._models_loaded:
            # Importar AQUÍ, no al nivel del módulo
            from .models import Usuario, MedicoProfile, PacienteProfile, EnfermeraProfile
            self.Usuario = Usuario
            self.PacienteProfile = PacienteProfile
            self.MedicoProfile = MedicoProfile
            self.EnfermeraProfile = EnfermeraProfile
            self._models_loaded = True

    def get_user_by_email(self, email: str):
        return next((u for u in self._usuarios if u.email == email), None)

    def create_paciente(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        # Cargar modelos solo cuando se necesiten
        self._load_models()
        
        # Crear usuario REAL usando el modelo de Django IGUAL que en tu ejemplo
        user_data['tipo_usuario'] = self.Usuario.TipoUsuario.PACIENTE
        user_data['is_active'] = True
        
        # Crear el usuario usando el modelo REAL - no se guarda en BD
        usuario = self.Usuario(
            id=len(self._usuarios) + 1,
            **user_data
        )
        self._usuarios.append(usuario)
        
        # Crear perfil REAL usando el modelo de Django
        perfil = self.PacienteProfile(
            id=len(self._pacientes) + 1,
            usuario=usuario,
            **profile_data
        )
        self._pacientes.append(perfil)
        
        return usuario

    def create_medico(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        # Cargar modelos solo cuando se necesiten
        self._load_models()
        
        # Crear usuario REAL usando el modelo de Django IGUAL que en tu ejemplo
        user_data['tipo_usuario'] = self.Usuario.TipoUsuario.MEDICO
        user_data['is_active'] = True
        
        # Crear el usuario usando el modelo REAL - no se guarda en BD
        usuario = self.Usuario(
            id=len(self._usuarios) + 1,
            **user_data
        )
        self._usuarios.append(usuario)
        
        # Crear perfil REAL usando el modelo de Django
        perfil = self.MedicoProfile(
            id=len(self._medicos) + 1,
            usuario=usuario,
            **profile_data
        )
        self._medicos.append(perfil)
        
        return usuario
