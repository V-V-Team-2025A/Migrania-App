# usuarios/serializers.py
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from .models import MedicoProfile, PacienteProfile, EnfermeraProfile
from datetime import date

Usuario = get_user_model()

class MedicoProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicoProfile
        fields = '__all__'
        extra_kwargs = {'usuario': {'read_only': True}}

class PacienteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteProfile
        fields = '__all__'
        extra_kwargs = {'usuario': {'read_only': True}}

class EnfermeraProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnfermeraProfile
        fields = '__all__'
        extra_kwargs = {'usuario': {'read_only': True}}

class UsuarioCompletoSerializer(BaseUserSerializer):
    nombre_completo = serializers.CharField(source='get_full_name', read_only=True)
    edad = serializers.ReadOnlyField()
    perfil_medico = MedicoProfileSerializer(read_only=True)
    perfil_paciente = PacienteProfileSerializer(read_only=True)
    perfil_enfermera = EnfermeraProfileSerializer(read_only=True)
    
    class Meta(BaseUserSerializer.Meta):
        model = Usuario
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'nombre_completo',
            'cedula', 'telefono', 'fecha_nacimiento', 'edad', 'direccion', 'genero',
            'tipo_usuario', 'date_joined', 'creado_en',
            'perfil_medico', 'perfil_paciente', 'perfil_enfermera'
        )

# =================================================
# SERIALIZERS DE REGISTRO ESPECÍFICOS
# =================================================

class RegistroMedicoSerializer(BaseUserCreateSerializer):
    # Campos del perfil médico
    numero_licencia = serializers.CharField(max_length=50)
    especializacion = serializers.CharField(max_length=100)
    anos_experiencia = serializers.IntegerField()
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = Usuario
        fields = (
            'email', 'username', 'password',
            'first_name', 'last_name', 'cedula', 'telefono', 'fecha_nacimiento',
            'direccion', 'genero',
            'numero_licencia', 'especializacion', 'anos_experiencia',
        )
    
    def validate(self, attrs):
        perfil_data = {
            'numero_licencia': attrs.pop('numero_licencia'),
            'especializacion': attrs.pop('especializacion'),
            'anos_experiencia': attrs.pop('anos_experiencia')
        }
        
        validated_attrs = super().validate(attrs)
        validated_attrs.update(perfil_data)
        
        return validated_attrs

    def create(self, validated_data):
        # Separamos los datos del perfil de los datos del usuario
        perfil_data = {
            'numero_licencia': validated_data.pop('numero_licencia'),
            'especializacion': validated_data.pop('especializacion'),
            'anos_experiencia': validated_data.pop('anos_experiencia'),
        }
        
        # Asignamos el tipo de usuario
        validated_data['tipo_usuario'] = 'medico'
        
        # Creamos el usuario usando el manager, que maneja el hash de la contraseña.
        usuario = Usuario.objects.create_user(**validated_data)
        
        # Creamos el perfil del médico asociado
        MedicoProfile.objects.create(usuario=usuario, **perfil_data)
        
        return usuario

class RegistroPacienteSerializer(BaseUserCreateSerializer):
    # Campos del perfil paciente
    numero_seguro = serializers.CharField(max_length=50, required=False, allow_blank=True)
    contacto_emergencia_nombre = serializers.CharField(max_length=100)
    contacto_emergencia_telefono = serializers.CharField(max_length=15)
    contacto_emergencia_relacion = serializers.CharField(max_length=50)
    alergias = serializers.CharField(required=False, allow_blank=True)
    grupo_sanguineo = serializers.CharField(max_length=5, required=False, allow_blank=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = Usuario
        fields = (
            'email', 'username', 'password',
            'first_name', 'last_name', 'cedula', 'telefono', 'fecha_nacimiento',
            'direccion', 'genero',
            'numero_seguro', 'contacto_emergencia_nombre', 'contacto_emergencia_telefono',
            'contacto_emergencia_relacion', 'alergias', 'grupo_sanguineo'
        )

    def validate(self, attrs):
        perfil_data = {
            'numero_seguro': attrs.pop('numero_seguro', None),
            'contacto_emergencia_nombre': attrs.pop('contacto_emergencia_nombre'),
            'contacto_emergencia_telefono': attrs.pop('contacto_emergencia_telefono'),
            'contacto_emergencia_relacion': attrs.pop('contacto_emergencia_relacion'),
            'alergias': attrs.pop('alergias', None),
            'grupo_sanguineo': attrs.pop('grupo_sanguineo', None)
        }
        
        validated_attrs = super().validate(attrs)
        validated_attrs.update(perfil_data)
        return validated_attrs

    def create(self, validated_data):
        perfil_data = {
            'numero_seguro': validated_data.pop('numero_seguro', ''),
            'contacto_emergencia_nombre': validated_data.pop('contacto_emergencia_nombre'),
            'contacto_emergencia_telefono': validated_data.pop('contacto_emergencia_telefono'),
            'contacto_emergencia_relacion': validated_data.pop('contacto_emergencia_relacion'),
            'alergias': validated_data.pop('alergias', ''),
            'grupo_sanguineo': validated_data.pop('grupo_sanguineo', ''),
        }
        
        validated_data['tipo_usuario'] = 'paciente'
        usuario = Usuario.objects.create_user(**validated_data)
        
        PacienteProfile.objects.create(usuario=usuario, **perfil_data)
        
        return usuario

class RegistroEnfermeraSerializer(BaseUserCreateSerializer):
    # Campos del perfil enfermera
    numero_registro = serializers.CharField(max_length=50)
    departamento = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = Usuario
        fields = (
            'email', 'username', 'password',
            'first_name', 'last_name', 'cedula', 'telefono', 'fecha_nacimiento',
            'direccion', 'genero',
            'numero_registro', 'departamento'
        )

    def validate(self, attrs):
        perfil_data = {
            'numero_registro': attrs.pop('numero_registro'),
            'departamento': attrs.pop('departamento', None)
        }
        
        validated_attrs = super().validate(attrs)
        validated_attrs.update(perfil_data)
        return validated_attrs

    def create(self, validated_data):
        perfil_data = {
            'numero_registro': validated_data.pop('numero_registro'),
            'departamento': validated_data.pop('departamento', ''),
        }
        
        validated_data['tipo_usuario'] = 'enfermera'
        usuario = Usuario.objects.create_user(**validated_data)
        
        EnfermeraProfile.objects.create(usuario=usuario, **perfil_data)
        
        return usuario

# =================================================
# OTROS SERIALIZERS
# =================================================

class MedicoCompletoSerializer(serializers.ModelSerializer):
    usuario = UsuarioCompletoSerializer(read_only=True)
    
    class Meta:
        model = MedicoProfile
        fields = '__all__'

class PacienteCompletoSerializer(serializers.ModelSerializer):
    usuario = UsuarioCompletoSerializer(read_only=True)
    
    class Meta:
        model = PacienteProfile
        fields = '__all__'

class EnfermeraCompletoSerializer(serializers.ModelSerializer):
    usuario = UsuarioCompletoSerializer(read_only=True)
    
    class Meta:
        model = EnfermeraProfile
        fields = '__all__'

# Serializer base para creación general
class CrearUsuarioSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = Usuario
        fields = (
            'email', 'username', 'password',
            'first_name', 'last_name', 'cedula', 'telefono', 'fecha_nacimiento',
            'direccion', 'genero', 'tipo_usuario'
        )
