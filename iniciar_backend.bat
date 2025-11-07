@echo off
echo ========================================
echo   BLESSED GYM - Iniciar Backend API
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/3] Verificando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    echo       Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo       [!] No se encontro entorno virtual
    echo       Usando Python global
)

echo.
echo [2/3] Verificando dependencias...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo       Instalando dependencias...
    pip install -r requirements.txt
) else (
    echo       Dependencias OK
)

echo.
echo [3/3] Iniciando servidor FastAPI...
echo.
echo ========================================
echo   Backend corriendo en:
echo   http://localhost:8000
echo
echo   Documentacion:
echo   http://localhost:8000/api/docs
echo ========================================
echo.

python main.py
