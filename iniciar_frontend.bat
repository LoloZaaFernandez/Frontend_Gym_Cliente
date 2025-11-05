@echo off
echo ========================================
echo   BLESSED GYM - Iniciar Frontend
echo ========================================
echo.

cd /d "%~dp0frontend"

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
pip show flet >nul 2>&1
if errorlevel 1 (
    echo       Instalando dependencias...
    pip install -r requirements.txt
) else (
    echo       Dependencias OK
)

echo.
echo [3/3] Iniciando aplicacion Flet...
echo.
echo ========================================
echo   BLESSED GYM Frontend
echo
echo   Credenciales de prueba:
echo   Admin: admin / admin123
echo   Cliente: DNI 12345678
echo ========================================
echo.

python main.py
