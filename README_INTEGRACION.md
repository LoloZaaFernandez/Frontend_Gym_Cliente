# 🏋️ BLESSED GYM - Sistema de Gestión Integral

## Sistema Full-Stack Completo

**Frontend:** Flet (Python UI Framework)
**Backend:** FastAPI (Python REST API)
**Base de Datos:** SQLite/MySQL

---

## 🚀 Inicio Rápido

### Opción 1: Inicio Automático (Recomendado)

```bash
# Hacer doble clic en:
iniciar_completo.bat
```

Esto iniciará automáticamente:
- ✅ Backend en `http://localhost:8000`
- ✅ Frontend (aplicación de escritorio)

### Opción 2: Inicio Manual

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python main.py
```

---

## 📋 Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

---

## 🔧 Instalación Inicial

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Frontend

```bash
cd frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📁 Estructura del Proyecto

```
C:\Sistema_Blessed\
│
├── backend/                      # Backend FastAPI
│   ├── controllers/             # Endpoints de la API
│   ├── services/                # Lógica de negocio
│   ├── repositories/            # Acceso a datos
│   ├── models/                  # Modelos de datos
│   ├── schemas/                 # Validación con Pydantic
│   ├── main.py                  # Punto de entrada
│   └── requirements.txt         # Dependencias
│
├── frontend/                     # Frontend Flet
│   ├── ui/
│   │   ├── views/               # Vistas de la aplicación
│   │   └── components/          # Componentes reutilizables
│   ├── services/
│   │   ├── api_service.py       # Cliente API REST
│   │   └── auth_service.py      # Autenticación
│   ├── config/                  # Configuración
│   ├── database/                # DB local (fallback)
│   ├── main.py                  # Punto de entrada
│   └── requirements.txt         # Dependencias
│
├── gimnasio-db/                  # Base de datos
│   └── data/                    # Datos persistentes
│
├── iniciar_backend.bat           # Script inicio backend
├── iniciar_frontend.bat          # Script inicio frontend
├── iniciar_completo.bat          # Script inicio completo
│
└── INTEGRACION_FRONTEND_BACKEND.md   # Documentación técnica
```

---

## 🎯 Funcionalidades Implementadas

### 🔐 Autenticación
- ✅ Login de Administrador (usuario/contraseña)
- ✅ Login de Cliente (DNI)
- ✅ Gestión de sesiones
- ✅ Sistema de fallback local

### 👥 Gestión de Clientes
- ✅ Crear nuevos clientes
- ✅ Editar información de clientes
- ✅ Eliminar clientes
- ✅ Listar todos los clientes
- ✅ Búsqueda por DNI
- ✅ Estados (Activo/Inactivo)

### 📊 Control de Asistencia
- ✅ Registrar asistencia por DNI
- ✅ Historial de asistencias
- ✅ Estadísticas del día
- ✅ Estadísticas del mes
- ✅ Validación de clientes activos

### 💳 Punto de Venta (POS)
- ✅ Catálogo de productos
- ✅ Carrito de compras
- ✅ Cálculo de totales
- ⏳ Procesamiento de ventas (en integración)

### 📈 Reportes y Estadísticas
- ✅ Dashboard de estadísticas
- ✅ Ventas recientes
- ✅ Productos más vendidos
- ⏳ Exportación a Excel/PDF (pendiente)

### 👤 Portal del Cliente
- ✅ Perfil personal
- ✅ Información de membresía
- ✅ Historial de asistencias
- ✅ Planes de membresía disponibles

---

## 🌐 Endpoints de la API

Documentación completa en: **http://localhost:8000/api/docs**

### Autenticación
- `POST /api/auth/login-admin` - Login administrador
- `GET /api/auth/login-client` - Login cliente

### Clientes
- `GET /api/clientes` - Listar clientes
- `POST /api/clientes` - Crear cliente
- `PUT /api/clientes/{id}` - Actualizar cliente
- `DELETE /api/clientes/{id}` - Eliminar cliente

### Asistencias
- `POST /api/asistencias` - Registrar asistencia
- `GET /api/asistencias` - Listar asistencias

### Otros
- `GET /health` - Health check
- `GET /api/docs` - Documentación Swagger

---

## 🎨 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI

### Frontend
- **Flet** - Framework UI multiplataforma
- **Requests** - Cliente HTTP
- **Python-dateutil** - Manejo de fechas

### Base de Datos
- **SQLite** - Desarrollo/Local
- **MySQL** - Producción (opcional)

---

## 🔐 Credenciales de Prueba

### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`

### Cliente
- **DNI:** `12345678`
- **Nombre:** Juan Pérez

---

## 🛠️ Configuración

### Frontend - API URL

Archivo: `frontend/config/settings.py`

```python
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30
```

### Backend - Base de Datos

Archivo: `backend/database.py`

```python
DB_NAME = 'gimnasio.db'  # SQLite local
# Para MySQL:
# DATABASE_URL = "mysql://user:pass@localhost/gimnasio"
```

---

## 🐛 Solución de Problemas

### El backend no inicia

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### El frontend no se conecta

1. Verificar que el backend esté corriendo
2. Probar: http://localhost:8000/health
3. Revisar `frontend/config/settings.py`

### Error "ModuleNotFoundError"

```bash
# En el directorio correspondiente:
pip install -r requirements.txt
```

### Base de datos bloqueada

- Cerrar todas las instancias de la aplicación
- En producción, usar PostgreSQL/MySQL

---

## 📊 Características Técnicas

### Arquitectura
- **Patrón:** REST API + Cliente
- **Separación:** Frontend/Backend independientes
- **Comunicación:** HTTP JSON
- **Fallback:** Base de datos local si API no disponible

### Seguridad
- Validación de datos con Pydantic
- CORS configurado
- Sanitización de inputs
- ⏳ JWT Tokens (próximamente)

### Performance
- Consultas optimizadas
- Caché en memoria
- Conexiones pooling
- ⏳ Redis cache (próximamente)

---

## 🚀 Próximos Pasos

### Corto Plazo
- [ ] Integrar POS completo con ventas
- [ ] Implementar reportes avanzados
- [ ] Agregar sistema de notificaciones
- [ ] Implementar JWT para autenticación

### Mediano Plazo
- [ ] Migrar a PostgreSQL
- [ ] Implementar WebSockets
- [ ] Sistema de backup automático
- [ ] Panel de administración web

### Largo Plazo
- [ ] Dockerizar aplicación
- [ ] Despliegue en la nube
- [ ] App móvil (iOS/Android)
- [ ] Integración con sistemas de pago

---

## 📚 Documentación Adicional

- **Integración Técnica:** `INTEGRACION_FRONTEND_BACKEND.md`
- **Frontend:** `frontend/README.md`
- **Mejoras UI/UX:** `frontend/MEJORAS_IMPLEMENTADAS.md`
- **API Docs:** http://localhost:8000/api/docs

---

## 👥 Soporte

Para reportar bugs o solicitar funcionalidades, crear un issue en el repositorio.

---

## 📄 Licencia

Proyecto privado - BLESSED GYM © 2025

---

**¡Sistema completo y funcional! 🎉**

*Desarrollado con ❤️ usando FastAPI + Flet*
