# Migrania-App

Plataforma full‑stack para gestión integral de migrañas: permite a médicos, pacientes y personal de enfermería registrar episodios de cefalea, evaluar discapacidad (MIDAS), sugerir tratamientos y recordatorios, agendar citas y consultar analíticas desde una sola aplicación.

## Arquitectura rápida
- Backend: Django 5 + Django REST Framework, Djoser + JWT, documentación con drf-spectacular, PostgreSQL, estáticos con WhiteNoise.
- Frontend: React 19 con Vite 7, MUI, React Router, Recharts y utilidades para consumo de la API.
- Infra: pensado para Railway/servicios similares (Procfile con gunicorn y migraciones antes de arrancar).

## Estructura de carpetas
- `backend/`: proyecto Django `migraine_app` con apps:
	- `usuarios`: autenticación y perfiles (médico, paciente, enfermera).
	- `evaluacion_diagnostico`: episodios de cefalea y autoevaluación MIDAS.
	- `tratamiento`: tratamientos, medicamentos y alertas/recordatorios.
	- `agendamiento_citas`: citas médicas y recordatorios asociados.
	- `analiticas`: vistas de análisis y patrones (en progreso).
- `frontend/`: SPA en React/Vite con módulos de funciones (`feature_Grupo1_EvaluacionMidas`, `feature_Grupo2_BitacoraAsistidaCefalea`, `feature_Grupo3_Recordatorios`, `feature_Grupo4_EstadisticasHistorial`, `feature_Grupo5_AgendamientoCitas`, `feature_Grupo6_AnalisisPatrones`, `feature_Grupo7_GeneracionSeguimientoTratamiento`).

## Requisitos previos
- Python 3.12+ (compatible con Django 5.2).
- Node.js 20+ y npm.
- PostgreSQL 14+.
- `git` y un shell compatible (instrucciones pensadas para Windows `cmd`).

## Backend (Django REST)

### Variables de entorno (.env en `backend/`)
```
SECRET_KEY=tu_clave_segura
DEBUG=True

# Opción 1: conexión directa a Postgres
POSTGRES_DB=migrania
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Opción 2: URL completa (p.ej. Railway)
# DATABASE_URL=postgresql://user:pass@host:port/dbname

# CORS/hosts
RAILWAY_PUBLIC_DOMAIN=
RAILWAY_STATIC_URL=
```

### Instalación y ejecución local
```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # opcional para acceder al admin
python manage.py runserver        # http://localhost:8000
```

### Documentación de la API
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- Redoc: `http://localhost:8000/api/schema/redoc/`
- Esquema OpenAPI JSON: `http://localhost:8000/api/schema/`

### Endpoints base
- Autenticación y registro: `api/auth/` (Djoser + JWT).
- Usuarios y perfiles: `api/` (app `usuarios`).
- Evaluación y diagnóstico: `api/` (app `evaluacion_diagnostico`).
- Tratamientos y recordatorios: `api/` (app `tratamiento`).
- Analíticas: `api/analiticas/`.

### Pruebas
```cmd
cd backend
python manage.py test
```

## Frontend (React + Vite)

### Variables de entorno (`frontend/.env`)
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Instalación y ejecución
```cmd
cd frontend
npm install
npm run dev       # http://localhost:5173 por defecto

# Otros scripts
npm run build     # build de producción en dist/
npm run preview   # sirve el build localmente
npm run lint      # chequeo ESLint
```

## Flujo local recomendado
1) Levanta PostgreSQL y crea la base de datos. 2) Configura `.env` del backend y ejecuta migraciones. 3) Arranca el backend en `:8000`. 4) Crea `.env` del frontend con la URL de la API. 5) Arranca el frontend en `:5173` y prueba el login/flujo completo.

## Despliegue
- `backend/Procfile` ejecuta migraciones, `collectstatic` y levanta `gunicorn` con `migraine_app.wsgi`. Adecuado para Railway/Heroku con la variable `PORT` provista por la plataforma.
