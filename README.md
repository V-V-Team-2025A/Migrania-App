# Migrania-App

Una aplicación web integral para el manejo y seguimiento de migrañas, desarrollada con Django REST Framework y React.

## 📋 Descripción

Migrania-App es una plataforma digital diseñada para ayudar a los pacientes en el manejo de sus episodios de migraña y cefaleas. La aplicación permite realizar seguimiento de síntomas, autoevaluaciones, análisis de patrones, gestión de tratamientos y agendamiento de citas médicas.

## 🚀 Características Principales

- **Evaluación y Diagnóstico**: Sistema de autoevaluación MIDAS y bitácora digital de episodios
- **Gestión de Tratamientos**: Seguimiento y aseguramiento de tratamientos médicos
- **Análisis y Analíticas**: Análisis de patrones y estadísticas del historial clínico
- **Agendamiento de Citas**: Sistema de programación de citas médicas
- **Gestión de Usuarios**: Sistema completo de autenticación y perfiles

## 🛠️ Tecnologías

### Backend
- **Framework**: Django 5.x con Django REST Framework
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT con Djoser
- **Documentación API**: DRF Spectacular (Swagger/OpenAPI)
- **Testing**: Behave (BDD)

### Frontend
- **Framework**: React 19.x
- **Build Tool**: Vite
- **UI Framework**: Material-UI (MUI)
- **Routing**: React Router DOM
- **Charts**: Recharts
- **Icons**: Phosphor Icons, React Icons

## 📁 Estructura del Proyecto

```
Migrania-App/
├── backend/                    # API Django REST Framework
│   ├── migraine_app/          # Configuración principal
│   ├── usuarios/              # Gestión de usuarios
│   ├── evaluacion_diagnostico/ # Autoevaluaciones y diagnósticos
│   ├── tratamiento/           # Gestión de tratamientos
│   ├── analiticas/           # Análisis y estadísticas
│   ├── agendamiento_citas/   # Sistema de citas
│   └── features/             # Tests BDD con Behave
├── frontend/                  # Aplicación React
│   ├── src/
│   │   ├── common/          # Componentes compartidos
│   │   ├── features/        # Funcionalidades específicas
│   │   ├── pages/          # Páginas de la aplicación
│   │   └── utils/          # Utilidades
│   └── public/
└── .github/workflows/        # CI/CD
```

## 🔧 Instalación y Configuración

### Prerrequisitos
- Python 3.13+
- Node.js 18+
- PostgreSQL
- Git

### Backend Setup

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/V-V-Team-2025A/Migrania-App.git
   cd Migrania-App/backend
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con la configuración de base de datos
   ```

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navegar al directorio frontend**
   ```bash
   cd ../frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Ejecutar servidor de desarrollo**
   ```bash
   npm run dev
   ```

## 🧪 Testing

### Backend (BDD con Behave)
```bash
cd backend
behave
```

### Frontend
```bash
cd frontend
npm run lint
```

## 📚 Documentación API

Una vez ejecutando el backend, la documentación de la API estará disponible en:
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`

## 👥 Contribuidores

Este proyecto es desarrollado por el equipo V-V-Team-2025A con 19+ contribuidores activos.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🔗 Enlaces

- [Repositorio](https://github.com/V-V-Team-2025A/Migrania-App)
- [Issues](https://github.com/V-V-Team-2025A/Migrania-App/issues)
- [Pull Requests](https://github.com/V-V-Team-2025A/Migrania-App/pulls)

## 🚀 Deployment

El proyecto incluye configuración para deployment automático mediante GitHub Actions y Railway.

---

**Desarrollado con ❤️ por V-V-Team-2025A**