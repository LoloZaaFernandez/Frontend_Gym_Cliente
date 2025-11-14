# 📊 ANÁLISIS DE ENDPOINTS - Frontend vs Backend

**Fecha:** 2025-11-13
**Autor:** Análisis automático

---

## 🎯 RESUMEN EJECUTIVO

### ✅ Endpoints Implementados en Frontend
- **Total métodos en api_service.py:** 82 métodos
- **Cobertura estimada:** ~75%

### ❌ Endpoints NO Implementados (Faltantes)

---

## 🛍️ SISTEMA DE VENTAS DE PRODUCTOS

### ✅ IMPLEMENTADOS
| Endpoint | Método API | Ubicación |
|----------|-----------|-----------|
| `POST /api/ventas` | `crear_venta()` | ✅ Línea 781 |
| `GET /api/ventas` | `get_ventas()` | ✅ Línea 829 |
| `GET /api/ventas/{id}` | `get_venta_por_id()` | ✅ Línea 878 |
| `GET /api/ventas/folio/{folio}` | `get_venta_por_folio()` | ✅ Línea 888 |
| `POST /api/ventas/{id}/cancelar` | `cancelar_venta()` | ✅ Línea 898 |
| `GET /api/ventas/reportes/metodos-pago` | `get_reporte_ventas_metodos_pago()` | ✅ Línea 911 |
| `GET /api/ventas/reportes/diario` | `get_reporte_ventas_diario()` | ✅ Línea 934 |
| `GET /api/ventas/reportes/semanal` | `get_reporte_ventas_semanal()` | ✅ Línea 948 |
| `GET /api/ventas/reportes/mensual` | `get_reporte_ventas_mensual()` | ✅ Línea 962 |
| `GET /api/ventas/reportes/anual` | `get_reporte_ventas_anual()` | ✅ Línea 978 |

**Cobertura Ventas: 10/10 = 100% ✅**

---

## 💸 SISTEMA DE EGRESOS

### ❌ NO IMPLEMENTADOS (0/17 endpoints)

| Endpoint Backend | Método Faltante | Prioridad | Dónde Usar |
|------------------|-----------------|-----------|------------|
| `GET /api/egresos/categorias` | `get_categorias_egresos()` | 🔴 ALTA | Selector en formulario de egresos |
| `POST /api/egresos` | `crear_egreso()` | 🔴 ALTA | Formulario de registro de gastos |
| `GET /api/egresos` | `get_egresos()` | 🔴 ALTA | Listado de egresos con filtros |
| `GET /api/egresos/{id}` | `get_egreso_por_id()` | 🟡 MEDIA | Ver detalle de egreso |
| `PATCH /api/egresos/{id}` | `actualizar_egreso()` | 🟡 MEDIA | Editar egreso |
| `DELETE /api/egresos/{id}` | `eliminar_egreso()` | 🟡 MEDIA | Eliminar egreso |
| `GET /api/egresos/reportes/por-categoria` | `get_reporte_egresos_por_categoria()` | 🔴 ALTA | Dashboard de egresos |

### 📝 Implementación Recomendada para Egresos:

```python
# En services/api_service.py

# ==================== EGRESOS ====================

def get_categorias_egresos(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
    """Obtener categorías de egresos"""
    url = f"{self.base_url}/api/egresos/categorias"
    params = {}
    if estado:
        params['estado'] = estado

    try:
        response = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        print(f"Error al obtener categorías de egresos: {e}")
        return []

def crear_egreso(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crear nuevo egreso

    Args:
        data: {
            "id_categoria": 1,
            "concepto": "Pago de luz",
            "descripcion": "Consumo de enero",
            "monto": 1500.00,
            "metodo_pago": "Transferencia",
            "fecha_egreso": "2025-01-15",
            "proveedor": "CFE",
            "numero_factura": "FAC-001",
            "estado": "Pagado",
            "es_recurrente": true,
            "frecuencia": "Mensual",
            "notas": "...",
            "usuario_creacion": "admin"
        }
    """
    url = f"{self.base_url}/api/egresos"
    try:
        response = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        raise ValueError(f"Error al crear egreso: {str(e)}")

def get_egresos(self,
                fecha_desde: Optional[str] = None,
                fecha_hasta: Optional[str] = None,
                id_categoria: Optional[int] = None,
                estado: Optional[str] = None,
                skip: int = 0,
                limit: int = 50) -> List[Dict[str, Any]]:
    """Obtener lista de egresos con filtros"""
    url = f"{self.base_url}/api/egresos"
    params = {}
    if fecha_desde:
        params['fecha_desde'] = fecha_desde
    if fecha_hasta:
        params['fecha_hasta'] = fecha_hasta
    if id_categoria:
        params['id_categoria'] = id_categoria
    if estado:
        params['estado'] = estado
    if skip:
        params['skip'] = skip
    if limit:
        params['limit'] = limit

    try:
        response = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        print(f"Error al obtener egresos: {e}")
        return []

def get_egreso_por_id(self, egreso_id: int) -> Optional[Dict[str, Any]]:
    """Obtener egreso por ID"""
    url = f"{self.base_url}/api/egresos/{egreso_id}"
    try:
        response = self.session.get(url, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        print(f"Error al obtener egreso: {e}")
        return None

def actualizar_egreso(self, egreso_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """Actualizar egreso (PATCH - campos opcionales)"""
    url = f"{self.base_url}/api/egresos/{egreso_id}"
    try:
        response = self.session.patch(url, json=data, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        raise ValueError(f"Error al actualizar egreso: {str(e)}")

def eliminar_egreso(self, egreso_id: int) -> bool:
    """Eliminar egreso"""
    url = f"{self.base_url}/api/egresos/{egreso_id}"
    try:
        response = self.session.delete(url, timeout=self.timeout)
        self._handle_response(response)
        return True
    except Exception as e:
        raise ValueError(f"Error al eliminar egreso: {str(e)}")

def get_reporte_egresos_por_categoria(self,
                                       fecha_desde: Optional[str] = None,
                                       fecha_hasta: Optional[str] = None) -> Dict[str, Any]:
    """Obtener reporte de egresos agrupado por categoría"""
    url = f"{self.base_url}/api/egresos/reportes/por-categoria"
    params = {}
    if fecha_desde:
        params['fecha_desde'] = fecha_desde
    if fecha_hasta:
        params['fecha_hasta'] = fecha_hasta

    try:
        response = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        print(f"Error al obtener reporte de egresos: {e}")
        return {
            "total_egresos": 0,
            "total_monto": 0,
            "egresos_por_categoria": []
        }
```

### 🎨 Vista Recomendada: `egresos_view.py`

**Ubicación:** `ui/views/admin/egresos_view.py`

**Características:**
- Formulario para crear egresos
- Listado con filtros por:
  - Rango de fechas
  - Categoría
  - Estado (Pagado/Pendiente/Cancelado)
- Tabla con columnas:
  - Folio
  - Fecha
  - Categoría
  - Concepto
  - Monto
  - Estado
  - Acciones (Editar/Eliminar)
- Dashboard con gráficos:
  - Total de egresos del mes
  - Egresos por categoría (pie chart)
  - Tendencia mensual (line chart)

---

## 📊 REPORTES FINANCIEROS FINALES

### ❌ NO IMPLEMENTADOS (0/3 endpoints)

| Endpoint Backend | Método Faltante | Prioridad | Dónde Usar |
|------------------|-----------------|-----------|------------|
| `GET /api/egresos/reportes/financiero-diario` | `get_reporte_financiero_diario()` | 🔴 ALTA | Dashboard principal |
| `GET /api/egresos/reportes/financiero-mensual` | `get_reporte_financiero_mensual()` | 🔴 ALTA | Reportes mensuales |
| `GET /api/egresos/reportes/financiero-anual` | `get_reporte_financiero_anual()` | 🟡 MEDIA | Reportes anuales |

### 📝 Implementación Recomendada:

```python
# En services/api_service.py

# ==================== REPORTES FINANCIEROS ====================

def get_reporte_financiero_diario(self, fecha: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtener reporte financiero completo del día

    Incluye:
    - Ingresos por membresías
    - Ingresos por ventas de productos
    - Ganancia de productos
    - Egresos del día
    - Ganancia neta final
    """
    url = f"{self.base_url}/api/egresos/reportes/financiero-diario"
    params = {}
    if fecha:
        params['fecha'] = fecha

    try:
        response = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        print(f"Error al obtener reporte financiero diario: {e}")
        return {
            "fecha": fecha or "",
            "ingresos_membresias": 0,
            "ingresos_productos": 0,
            "ganancia_productos": 0,
            "total_ingresos": 0,
            "total_egresos": 0,
            "ganancia_neta": 0,
            "margen_neto": 0
        }

def get_reporte_financiero_mensual(self,
                                     mes: Optional[int] = None,
                                     anio: Optional[int] = None) -> Dict[str, Any]:
    """Obtener reporte financiero mensual completo"""
    url = f"{self.base_url}/api/egresos/reportes/financiero-mensual"
    params = {}
    if mes:
        params['mes'] = mes
    if anio:
        params['anio'] = anio

    try:
        response = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        print(f"Error al obtener reporte financiero mensual: {e}")
        return {}

def get_reporte_financiero_anual(self, anio: Optional[int] = None) -> Dict[str, Any]:
    """Obtener reporte financiero anual completo"""
    url = f"{self.base_url}/api/egresos/reportes/financiero-anual"
    params = {}
    if anio:
        params['anio'] = anio

    try:
        response = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        print(f"Error al obtener reporte financiero anual: {e}")
        return {}
```

### 🎨 Mejora Recomendada: Dashboard Principal

**Ubicación:** `ui/views/admin/admin_dashboard.py`

**Agregar sección:**
```python
def load_reporte_financiero_hoy():
    """Cargar reporte financiero del día"""
    try:
        from ui.utils.datetime_utils import get_now_local

        fecha_hoy = get_now_local().strftime('%Y-%m-%d')
        reporte = api.get_reporte_financiero_diario(fecha=fecha_hoy)

        return {
            "ingresos_membresias": reporte.get('ingresos_membresias', 0),
            "ingresos_productos": reporte.get('ingresos_productos', 0),
            "total_ingresos": reporte.get('total_ingresos', 0),
            "total_egresos": reporte.get('total_egresos', 0),
            "ganancia_neta": reporte.get('ganancia_neta', 0),
            "margen_neto": reporte.get('margen_neto', 0)
        }
    except Exception as e:
        print(f"Error al cargar reporte financiero: {e}")
        return None
```

**Visualización:**
- Card grande mostrando GANANCIA NETA del día
- Gráfico de barras: Ingresos vs Egresos
- Indicador de margen neto (%)
- Comparativa con días anteriores

---

## 👤 REGISTRO DE CLIENTE CON VALIDACIÓN

### ❌ NO IMPLEMENTADO (0/1 endpoint)

| Endpoint Backend | Método Faltante | Prioridad | Dónde Usar |
|------------------|-----------------|-----------|------------|
| `POST /api/registro/cliente-con-validacion` | `registrar_cliente_con_validacion()` | 🟡 MEDIA | Formulario de registro mejorado |

### 📝 Implementación Recomendada:

```python
# En services/api_service.py

def registrar_cliente_con_validacion(self,
                                      confirmar: bool,
                                      dni: str,
                                      nombre: str,
                                      apellidos: str,
                                      correo: str,
                                      telefono: str,
                                      id_membresia: int,
                                      metodo_pago: str,
                                      usuario_creacion: str = "admin") -> Dict[str, Any]:
    """
    Registrar cliente con confirmación previa

    Args:
        confirmar: True para confirmar, False para cancelar
        dni: DNI del cliente
        nombre: Nombre
        apellidos: Apellidos
        correo: Email
        telefono: Teléfono
        id_membresia: ID de membresía
        metodo_pago: "Efectivo" o "Yape"
        usuario_creacion: Usuario que registra

    Returns:
        {
            "registrado": bool,
            "mensaje": str,
            "resumen": {...},
            "cliente": {...} or null,
            "pago_membresia": {...} or null
        }
    """
    url = f"{self.base_url}/api/registro/cliente-con-validacion"
    data = {
        "confirmar_registro": "si" if confirmar else "no",
        "dni": dni,
        "nombre": nombre,
        "apellidos": apellidos,
        "correo": correo,
        "telefono": telefono,
        "id_membresia": id_membresia,
        "metodo_pago": metodo_pago,
        "usuario_creacion": usuario_creacion
    }

    try:
        response = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(response)
    except Exception as e:
        raise ValueError(f"Error al registrar cliente: {str(e)}")
```

### 🎨 Flujo de UI Recomendado:

1. Usuario llena formulario de registro
2. Presiona "Registrar"
3. **Diálogo de confirmación:**
   ```
   ¿Confirmar registro?

   Nombre: Juan Pérez García
   DNI: 12345678
   Membresía: Mensual
   Método de pago: Efectivo

   [Cancelar] [Confirmar]
   ```
4. Si confirma → `confirmar=True` → Se registra
5. Si cancela → `confirmar=False` → Se aborta

---

## 📦 PRODUCTOS - ENDPOINTS AVANZADOS

### ⚠️ PARCIALMENTE IMPLEMENTADOS

Todos los endpoints de productos CRUD están implementados ✅, pero algunos **avanzados** no se usan en las vistas actuales:

| Funcionalidad | Implementado | Usado en UI | Recomendación |
|---------------|--------------|-------------|---------------|
| Búsqueda por código de barras | ✅ | ❌ | Agregar scanner en POS |
| Búsqueda por SKU | ✅ | ❌ | Agregar campo de búsqueda rápida |
| Productos próximos a vencer | ✅ | ❌ | Agregar alerta en dashboard |
| Historial de precios | ✅ | ❌ | Agregar en vista de detalle |
| Cálculo de precio | ✅ | ❌ | Usar en cotizaciones |
| Productos por margen | ✅ | ❌ | Agregar reporte de rentabilidad |

### 🎨 Mejoras Recomendadas en `productos_view.py`:

**1. Agregar búsqueda por código de barras:**
```python
def buscar_por_codigo_barras(codigo: str):
    """Buscar producto escaneando código de barras"""
    producto = api.get_producto_por_codigo_barras(codigo)
    if producto:
        mostrar_detalle_producto(producto)
    else:
        mostrar_error(page, "Producto no encontrado")
```

**2. Mostrar alertas de vencimiento:**
```python
def cargar_alertas():
    """Cargar productos próximos a vencer"""
    productos = api.get_productos_proximos_vencer(dias=30)

    if productos:
        # Mostrar badge o alerta
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=Theme.WARNING),
                ft.Text(f"{len(productos)} producto(s) próximos a vencer")
            ])
        )
```

---

## 📈 PRIORIDADES DE IMPLEMENTACIÓN

### 🔴 PRIORIDAD ALTA (Implementar primero)

1. **Sistema de Egresos Completo**
   - `get_categorias_egresos()`
   - `crear_egreso()`
   - `get_egresos()`
   - `get_reporte_egresos_por_categoria()`
   - **Vista:** `egresos_view.py`

2. **Reportes Financieros**
   - `get_reporte_financiero_diario()`
   - `get_reporte_financiero_mensual()`
   - **Integrar en:** Dashboard principal

### 🟡 PRIORIDAD MEDIA (Mejorar experiencia)

3. **Registro con Validación**
   - `registrar_cliente_con_validacion()`
   - **Mejorar:** Formulario de clientes

4. **Búsqueda Avanzada de Productos**
   - Usar `get_producto_por_codigo_barras()` en POS
   - Agregar scanner/input de código de barras

### 🟢 PRIORIDAD BAJA (Futuras mejoras)

5. **Alertas de Productos**
   - Dashboard con `get_productos_proximos_vencer()`
   - Notificaciones de stock bajo

6. **Reportes Anuales**
   - `get_reporte_financiero_anual()`
   - Vista dedicada de reportes anuales

---

## 📝 RESUMEN DE ACCIONES

### ✅ LO QUE YA TIENES FUNCIONANDO
- ✅ Sistema completo de Ventas de Productos
- ✅ Sistema completo de Clientes
- ✅ Sistema completo de Asistencias
- ✅ Sistema completo de Membresías
- ✅ Sistema completo de Productos (CRUD + Inventario)
- ✅ Todos los reportes de ventas

### ❌ LO QUE FALTA IMPLEMENTAR

1. **Sistema de Egresos** (20 métodos aprox.)
2. **Reportes Financieros Integrados** (3 métodos)
3. **Registro con Validación** (1 método)

### 📊 ESTADÍSTICAS

- **Endpoints implementados:** ~82 métodos
- **Endpoints faltantes:** ~24 métodos
- **Cobertura actual:** ~77%
- **Cobertura objetivo:** 100%

---

## 🚀 PLAN DE ACCIÓN RECOMENDADO

### Semana 1: Sistema de Egresos
1. Agregar métodos al `api_service.py`
2. Crear `egresos_view.py`
3. Agregar sección "Egresos" al menú admin

### Semana 2: Reportes Financieros
1. Agregar métodos de reportes financieros
2. Integrar en dashboard principal
3. Crear vista de reportes mensuales

### Semana 3: Mejoras y Optimizaciones
1. Implementar registro con validación
2. Agregar búsqueda por código de barras
3. Agregar alertas de productos

---

**FIN DEL ANÁLISIS**
