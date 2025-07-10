@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   CONFIGURANDO PROYECTO DJANGO
echo   Django + Supabase + Docker
echo ========================================
echo.

REM Verificar que Docker este instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado 
    echo Por favor, instala Docker Desktop primero.
    echo.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose no esta instalado.
    echo Por favor, instala Docker Compose primero.
    echo.
    pause
    exit /b 1
)

REM Crear .env si no existe
if not exist .env (
    echo [SETUP] Creando archivo .env desde template...
    copy .env.example .env >nul
    echo.
    echo [IMPORTANTE] Edita el archivo .env con las credenciales reales de Supabase
    echo              Contacta al administrador del proyecto para obtener las credenciales.
    echo.
    set /p response="Ya tienes las credenciales en .env? (y/n): "
    if /i not "%response%"=="y" (
        echo.
        echo Completa el archivo .env y ejecuta este script nuevamente.
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [BUILD] Construyendo contenedores...
docker-compose up --build -d

echo.
echo [WAIT] Esperando que el contenedor este listo...
timeout /t 5 /nobreak >nul

echo.
echo [MIGRATE] Aplicando migraciones...
docker exec django_app python manage.py migrate

echo.
echo ========================================
echo   SETUP COMPLETADO EXITOSAMENTE!
echo ========================================
echo.
echo Tu aplicacion esta corriendo en: http://localhost:8000
echo.
echo COMANDOS UTILES:
echo   docker-compose logs -f                          # Ver logs
echo   docker exec -it django_app bash                 # Terminal del contenedor  
echo   docker exec django_app python manage.py shell   # Shell de Django
echo.
echo Para detener: docker-compose down
echo.
pause