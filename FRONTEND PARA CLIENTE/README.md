# BLESSED GYM - Frontend Cliente (Tablet)

Frontend para tablets del gimnasio, permite a los clientes registrarse y marcar asistencia de forma autónoma.

## 🎯 Funcionalidades

### ✅ Pantalla Inicial
- Dos opciones grandes y claras:
  - **Registrarse**: Para nuevos clientes
  - **Asistencia**: Para clientes ya registrados

### 👤 Flujo de Registro (Nuevos Clientes)

**Paso 1: Datos Personales**
- DNI (8 dígitos, verificación automática de no duplicados)
- Nombre y Apellidos
- Correo Electrónico
- Teléfono

**Paso 2: Selección de Membresía**
- Visualización de todas las membresías disponibles con:
  - Nombre de la membresía
  - Precio
  - Duración en días
- Selección de método de pago (Efectivo, Yape, Transferencia)

**Paso 3: Confirmación**
- Resumen completo de todos los datos ingresados
- Confirmación final antes de registrar

**Resultado:**
- Pantalla de éxito con información del registro
- Si el pago es con Yape: alerta de confirmación pendiente
- El personal del gimnasio recibe notificación del nuevo registro

### 🟦 Flujo de Asistencia (Clientes Registrados)

**Proceso:**
1. Cliente ingresa su DNI
2. Sistema verifica que el cliente existe y está activo
3. Sistema registra la asistencia automáticamente
4. Muestra confirmación con:
   - Nombre del cliente
   - Fecha y hora de asistencia
   - Fecha de vencimiento de membresía

**Alertas automáticas:**
- ⚠️ Si la membresía vence HOY
- ⚠️ Si la membresía vence MAÑANA
- ⚠️ Si la membresía vence en ≤5 días
- ❌ Si la membresía está vencida (no permite registrar asistencia)

## 📁 Estructura del Proyecto

```
FRONTEND PARA CLIENTE/
├── main.py                    # Punto de entrada de la aplicación
├── config/
│   ├── settings.py           # Configuración general (API URL, tamaños, etc.)
│   └── theme.py              # Sistema de diseño (colores, espaciados, fuentes)
├── services/
│   └── api_service.py        # Servicio de comunicación con backend API
├── components/
│   ├── buttons.py            # Botones reutilizables (optimizados para tablet)
│   ├── inputs.py             # Campos de texto reutilizables
│   └── cards.py              # Tarjetas y contenedores reutilizables
└── views/
    ├── pantalla_inicial.py   # Vista inicial (Registrarse/Asistencia)
    ├── registro_view.py      # Vista de registro de nuevos clientes
    └── asistencia_view.py    # Vista de registro de asistencias
```

## 🔧 Configuración

### Requisitos
- Python 3.8+
- Backend API ejecutándose en `http://localhost:8000`

### Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar URL del backend (si es diferente):
Editar `config/settings.py`:
```python
API_BASE_URL = "http://localhost:8000"  # Cambiar si es necesario
```

3. Ejecutar la aplicación:
```bash
python main.py
```

## 🌐 Endpoints Utilizados

| Función | Endpoint | Método |
|---------|----------|--------|
| Verificar si DNI ya existe | `/api/registro/verificar-dni/{dni}` | GET |
| Obtener opciones de membresía | `/api/registro/opciones` | GET |
| Registrar cliente completo | `/api/registro/cliente-con-validacion` | POST |
| Ver estado del cliente | `/api/clientes/dni/{dni}` | GET |
| Registrar asistencia | `/api/asistencias` | POST |

## 🎨 Diseño

### Colores Principales
- **Naranja (#F05D23)**: Color principal de BLESSED GYM
- **Verde (#00C853)**: Éxito, confirmaciones
- **Rojo (#EF5350)**: Errores, alertas críticas
- **Amarillo (#FF9100)**: Advertencias

### Tamaños Optimizados para Tablet
- Resolución base: 1024x768 (tablet horizontal)
- Botones grandes: 70px de altura
- Textos grandes y legibles
- Espaciados amplios para facilitar el toque

## 🔄 Flujo de Datos

### Registro de Cliente
```
Usuario ingresa datos → Verifica DNI disponible → Carga opciones de membresía →
Selecciona membresía y pago → Confirma → API registra cliente →
Muestra éxito + notifica al personal (si Yape)
```

### Registro de Asistencia
```
Usuario ingresa DNI → API verifica cliente activo → Verifica vencimiento de membresía →
API registra asistencia → Muestra confirmación + alerta (si membresía por vencer)
```

## 🚨 Validaciones

### Registro
- DNI: 8 dígitos numéricos, único
- Nombre: mínimo 2 caracteres
- Apellidos: mínimo 2 caracteres
- Correo: formato válido con @
- Teléfono: 9 dígitos
- Membresía: selección obligatoria
- Método de pago: selección obligatoria

### Asistencia
- DNI: 8 dígitos
- Cliente debe existir
- Cliente debe estar activo
- Membresía NO debe estar vencida

## 📱 Uso en Tablet

1. **Colocar en modo quiosco/fullscreen** para evitar que salgan de la app
2. **Conexión WiFi estable** a la red donde corre el backend
3. **Altura cómoda** para que los clientes puedan interactuar fácilmente
4. **Opcional**: Agregar teclado físico para facilitar entrada de datos

## 🔐 Seguridad

- El usuario del sistema es fijo: `tablet_gym`
- No hay autenticación en la tablet (es de acceso público)
- Todas las validaciones críticas se hacen en el backend
- Los datos sensibles no se almacenan localmente

## 🛠️ Mantenimiento

### Cambiar URL del Backend
Editar `config/settings.py`:
```python
API_BASE_URL = "http://nueva-ip:puerto"
```

### Ajustar Tamaño de Tablet
Editar `config/settings.py`:
```python
APP_WIDTH = 1024  # Ancho en píxeles
APP_HEIGHT = 768  # Alto en píxeles
```

### Cambiar Días de Alerta de Vencimiento
Por defecto es 5 días. Para cambiarlo, editar en `views/asistencia_view.py`:
```python
alerta_membresia = api_service.verificar_membresia_por_vencer(cliente, dias_alerta=5)
```

## 📞 Soporte

Para problemas o mejoras, contactar al equipo de desarrollo.

---

**BLESSED GYM** © 2025 - Frontend Cliente (Tablet)
