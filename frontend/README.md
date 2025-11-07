
# BLESSED GYM - Sistema de Gestión Integral (Frontend)

Sistema de gestión integral para gimnasio desarrollado con Flet (Python).

## Estructura del Proyecto

```
frontend/
│
├── config/                      # Configuración global
│   ├── __init__.py
│   └── settings.py             # Colores, rutas, configuración de app
│
├── database/                    # Gestión de base de datos
│   ├── __init__.py
│   └── db_manager.py           # Manager de SQLite (temporal, para backend futuro)
│
├── services/                    # Servicios de negocio
│   ├── __init__.py
│   └── auth_service.py         # Servicio de autenticación
│
├── ui/                          # Interfaz de usuario
│   ├── __init__.py
│   │
│   ├── components/              # Componentes reutilizables
│   │   ├── __init__.py
│   │   └── common.py           # Botones, cards, headers, etc.
│   │
│   └── views/                   # Vistas de la aplicación
│       ├── __init__.py
│       ├── role_selection.py   # Selección Admin/Cliente
│       ├── admin_login.py      # Login de administrador
│       ├── client_login.py     # Login de cliente
│       ├── admin_dashboard.py  # Dashboard administrador
│       ├── client_dashboard.py # Dashboard cliente
│       └── simple_message.py   # Mensajes de secciones en desarrollo
│
├── main.py                      # Punto de entrada de la aplicación
└── README.md                    # Este archivo
```

## Características

### Módulos Principales

#### 1. **Config** (`config/settings.py`)
- Configuración centralizada de colores
- Rutas de recursos (imágenes, logos)
- Configuración de la aplicación (dimensiones, títulos)
- URL del backend API (para integración futura)

#### 2. **Database** (`database/db_manager.py`)
- Gestión de base de datos SQLite local
- CRUD de clientes y administradores
- Preparado para ser reemplazado/complementado con llamadas al backend

#### 3. **Services** (`services/auth_service.py`)
- Autenticación de usuarios (admin/cliente)
- Gestión de sesión
- Lógica de negocio separada de la UI

#### 4. **UI Components** (`ui/components/common.py`)
- Componentes reutilizables (botones, cards, headers, campos de texto)
- Estilos consistentes en toda la aplicación

#### 5. **UI Views** (`ui/views/`)
- Vistas separadas por funcionalidad
- Cada vista es independiente y recibe callbacks para navegación
- Fácil de mantener y extender

## Ventajas de la Refactorización

1. **Separación de Responsabilidades**: Cada módulo tiene una función específica
2. **Reutilización de Código**: Componentes y estilos centralizados
3. **Fácil Mantenimiento**: Código organizado y documentado
4. **Escalabilidad**: Fácil añadir nuevas vistas o servicios
5. **Preparado para Backend**: Estructura lista para integrar API REST
6. **Testing**: Cada módulo puede testearse independientemente

## Cómo Ejecutar

```bash
# Instalar dependencias
pip install flet

# Ejecutar la aplicación
python main.py
```

## Integración Futura con Backend

### Paso 1: Crear Servicio API
Crear `services/api_service.py`:
```python
import requests
from config.settings import API_BASE_URL, API_TIMEOUT

class APIService:
    def __init__(self):
        self.base_url = API_BASE_URL

    def login_admin(self, username, password):
        response = requests.post(
            f"{self.base_url}/auth/admin/login",
            json={"username": username, "password": password},
            timeout=API_TIMEOUT
        )
        return response.json()
```

### Paso 2: Modificar AuthService
En `services/auth_service.py`, reemplazar llamadas a `DatabaseManager` con llamadas a `APIService`.

### Paso 3: Actualizar Configuración
En `config/settings.py`, actualizar `API_BASE_URL` con la URL real del backend.

## Credenciales por Defecto

- **Admin**:
  - Usuario: `admin`
  - Contraseña: `admin123`

- **Cliente de prueba**:
  - DNI: `12345678`

## Próximos Pasos

- [ ] Integrar con backend FastAPI
- [ ] Implementar gestión de clientes completa
- [ ] Añadir sistema de asistencias
- [ ] Implementar módulo POS
- [ ] Crear reportes y analíticas
- [ ] Añadir gestión de membresías

## Notas Técnicas

- **Base de datos**: SQLite (temporal, para desarrollo sin backend)
- **Framework UI**: Flet (Flutter para Python)
- **Arquitectura**: Patrón de servicios + vistas separadas
- **Estado**: Manejado por servicios (AuthService)
