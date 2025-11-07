# Como Iniciar BLESSED GYM

## Inicio Rapido

### Opcion 1: Un Solo Click (Recomendado)

Hacer doble clic en:
```
iniciar_completo.bat
```

Esto iniciara automaticamente:
- Backend (API en http://localhost:8000)
- Frontend (Aplicacion de escritorio)

---

## Opcion 2: Inicio Manual

### Paso 1: Iniciar Backend

**Terminal 1:**
```bash
cd backend
python main.py
```

Deberas ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Paso 2: Iniciar Frontend

**Terminal 2:**
```bash
cd frontend
python main.py
```

La aplicacion se abrira automaticamente.

---

## Credenciales de Acceso

### Para Administradores
- **Usuario:** `admin`
- **Password:** `admin123`

### Para Clientes
- **DNI:** `12345678`

Otros DNIs validos:
- `29480466` (Membresia Anual activa)
- `72788702` (Membresia activa hasta 2026)

---

## Verificar que Todo Funciona

### 1. Verificar Backend

Abrir en navegador:
```
http://localhost:8000/health
```

Deberia mostrar:
```json
{"status":"healthy"}
```

### 2. Verificar Documentacion API

Abrir en navegador:
```
http://localhost:8000/api/docs
```

Veras la documentacion interactiva de todos los endpoints.

### 3. Ejecutar Pruebas de Integracion

```bash
python test_integration.py
```

Deberia mostrar:
```
Total de pruebas: 9
Exitosas: 9
Porcentaje de exito: 100.0%
```

---

## Solucionar Problemas

### Backend no inicia

1. Verificar que estas en la carpeta backend:
   ```bash
   cd backend
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicializar base de datos:
   ```bash
   python init_database.py
   ```

4. Iniciar nuevamente:
   ```bash
   python main.py
   ```

### Frontend no conecta al backend

1. Verificar que el backend este corriendo:
   ```
   http://localhost:8000/health
   ```

2. Si el backend no responde, el frontend usara la base de datos local automaticamente.

### Error "Port already in use"

Si el puerto 8000 ya esta en uso:

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [numero_del_proceso] /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Base de datos bloqueada

1. Cerrar todas las instancias de la aplicacion
2. Reiniciar el backend
3. Reiniciar el frontend

---

## Estructura de Carpetas

```
C:\Sistema_Blessed\
├── backend/              # API REST
├── frontend/             # Aplicacion de escritorio
├── gimnasio.db          # Base de datos
├── iniciar_completo.bat # Inicio automatico
├── test_integration.py  # Pruebas
└── COMO_INICIAR.md     # Este archivo
```

---

## Funcionalidades Principales

### Como Administrador puedes:
- Gestionar clientes (crear, editar, eliminar)
- Registrar asistencias
- Ver estadisticas y reportes
- Gestionar productos y ventas
- Ver dashboard con metricas

### Como Cliente puedes:
- Ver tu perfil y membresia
- Ver tu historial de asistencias
- Consultar planes disponibles
- Ver informacion de contacto

---

## Documentacion Adicional

- **Integracion Completa:** `INTEGRACION_EXITOSA.md`
- **Guia Tecnica:** `INTEGRACION_FRONTEND_BACKEND.md`
- **README General:** `README_INTEGRACION.md`
- **API Docs:** http://localhost:8000/api/docs

---

## Soporte

Si encuentras algun problema:

1. Verificar los logs del backend y frontend
2. Revisar `INTEGRACION_EXITOSA.md` para errores comunes
3. Ejecutar `test_integration.py` para diagnostico

---

**Sistema listo para usar!**

Desarrollado con FastAPI + Flet
