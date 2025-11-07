@echo off
echo ========================================
echo   BLESSED GYM - Inicio Completo
echo   Backend + Frontend
echo ========================================
echo.

echo Iniciando Backend en nueva ventana...
start "BLESSED GYM - Backend" cmd /k "%~dp0iniciar_backend.bat"

echo Esperando que el backend se inicie...
timeout /t 5 /nobreak >nul

echo Iniciando Frontend en nueva ventana...
start "BLESSED GYM - Frontend" cmd /k "%~dp0iniciar_frontend.bat"

echo.
echo ========================================
echo   Aplicacion iniciada!
echo
echo   Backend:  http://localhost:8000
echo   Frontend: Ventana de aplicacion
echo ========================================
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul
