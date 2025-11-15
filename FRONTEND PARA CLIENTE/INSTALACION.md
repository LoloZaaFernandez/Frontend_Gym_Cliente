# BLESSED GYM - Frontend Cliente - Guía de Instalación

## 📋 Requisitos Previos

- **Python 3.8 o superior**
- **Backend API ejecutándose** en `http://localhost:8000`
- **Conexión a internet** para descargar dependencias

## 🚀 Instalación Rápida

### 1. Instalar Dependencias

```bash
cd "C:\FRONTEND V4\FRONTEND PARA CLIENTE"
pip install -r requirements.txt
```

Esto instalará:
- `flet==0.24.1` - Framework de UI
- `requests==2.31.0` - Cliente HTTP para API
- `websocket-client==1.6.4` - Cliente WebSocket para notificaciones
- `python-dateutil==2.8.2` - Utilidades de fecha

### 2. Configurar Backend

Editar `config/settings.py` si tu backend está en otra URL:

```python
API_BASE_URL = "http://localhost:8000"  # Cambiar si es necesario
```

### 3. Ejecutar la Aplicación

```bash
python main.py
```

O usando flet:

```bash
flet run
```

## 🔧 Configuración Avanzada

### WebSocket para Notificaciones

El sistema envía notificaciones en tiempo real al admin cuando:
- Se registra un nuevo cliente
- El pago es con **Yape** (notificación prioritaria)

**URL WebSocket:** `ws://localhost:8000/ws/notificaciones`

Si el WebSocket no está disponible:
- La aplicación funcionará normalmente
- Se mostrará advertencia en consola
- NO se enviarán notificaciones al admin

### Configurar Tamaño de Pantalla

Editar `config/settings.py`:

```python
APP_WIDTH = 1024  # Ancho en píxeles
APP_HEIGHT = 768  # Alto en píxeles
```

Tamaños comunes de tablets:
- iPad (horizontal): 1024x768
- iPad Pro (horizontal): 1366x1024
- Android Tablet (horizontal): 1280x800

## 🧪 Verificación de Instalación

Ejecuta estos comandos para verificar:

```bash
# Verificar Python
python --version
# Debe mostrar: Python 3.8.x o superior

# Verificar dependencias
pip list | grep flet
pip list | grep requests
pip list | grep websocket-client

# Verificar backend (desde otra terminal)
curl http://localhost:8000/health
# Debe responder: {"status": "ok"}
```

## 🐛 Solución de Problemas

### Error: "Module 'flet' not found"
```bash
pip install flet==0.24.1
```

### Error: "No se puede conectar con el backend"
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Prueba: `curl http://localhost:8000/health`
- Revisa `config/settings.py` para verificar la URL

### Error: "WebSocket no disponible"
```bash
pip install websocket-client==1.6.4
```
Nota: Las notificaciones funcionarán sin WebSocket, solo no se enviarán al admin.

### Error: "Container Control must be added to the page first"
Este error se corrigió automáticamente. Si persiste:
- Cierra completamente la aplicación
- Ejecuta de nuevo: `python main.py`

## 📦 Estructura de Archivos

```
FRONTEND PARA CLIENTE/
├── main.py                      # Punto de entrada
├── requirements.txt             # Dependencias
├── INSTALACION.md              # Esta guía
├── config/
│   ├── settings.py             # Configuración (API URL, tamaños)
│   └── theme.py                # Tema visual
├── services/
│   ├── api_service.py          # Cliente API REST
│   └── websocket_service.py    # Cliente WebSocket
├── components/
│   ├── buttons.py              # Botones
│   ├── inputs.py               # Campos de texto
│   └── cards.py                # Tarjetas
└── views/
    ├── pantalla_inicial.py     # Vista inicial
    ├── registro_view.py        # Vista de registro
    └── asistencia_view.py      # Vista de asistencia
```

## 🚀 Ejecutar en Producción

### Modo Fullscreen (Kiosco)

Para tablets en modo quiosco, ejecuta:

```bash
python main.py --fullscreen
```

O edita `main.py` y agrega:

```python
page.window.full_screen = True
```

### Auto-inicio en Windows

Crear un acceso directo en:
`C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\`

Contenido del acceso directo:
```
Target: C:\Users\...\python.exe "C:\FRONTEND V4\FRONTEND PARA CLIENTE\main.py"
Start in: C:\FRONTEND V4\FRONTEND PARA CLIENTE
```

## 📞 Soporte

Para problemas técnicos:
1. Revisa los logs en la consola
2. Verifica la conexión con el backend
3. Consulta este documento

---

**BLESSED GYM** © 2025 - Frontend Cliente (Tablet)
