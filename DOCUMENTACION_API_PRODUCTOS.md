# 📦 Documentación API de Productos - Frontend Guide

**Base URL:** `/api/productos`

Esta API maneja todo lo relacionado con productos, categorías, inventario, precios y estadísticas del gimnasio.

---

## 📑 Índice

1. [Categorías](#-categorías)
2. [Productos - CRUD](#-productos---crud)
3. [Inventario](#-inventario)
4. [Precios](#-precios)
5. [Estadísticas y Reportes](#-estadísticas-y-reportes)
6. [Modelos de Datos](#-modelos-de-datos)

---

## 🗂️ CATEGORÍAS

### 1. **Crear Categoría**
```http
POST /api/productos/categorias
```

**Propósito:** Crear una nueva categoría de productos (Ej: "Suplementos", "Bebidas", "Accesorios")

**Body (JSON):**
```json
{
  "nombre": "Suplementos",
  "descripcion": "Proteínas, aminoácidos, pre-entrenos",
  "slug": "suplementos",        // Opcional: se genera automáticamente del nombre
  "icono": "💊",                // Opcional: emoji o nombre de icono
  "orden": 1                    // Opcional: para ordenar en la UI
}
```

**Respuesta exitosa (201):**
```json
{
  "id": 1,
  "nombre": "Suplementos",
  "descripcion": "Proteínas, aminoácidos, pre-entrenos",
  "slug": "suplementos",
  "icono": "💊",
  "orden": 1,
  "estado": "Activa",
  "total_productos": 0,
  "fecha_creacion": "2025-01-15T10:30:00",
  "fecha_modificacion": null
}
```

**Casos de uso:**
- Formulario de creación de categoría
- Setup inicial del sistema
- Agregar nuevas líneas de productos

---

### 2. **Listar Categorías**
```http
GET /api/productos/categorias
```

**Propósito:** Obtener todas las categorías con sus productos

**Query Parameters:**
- `estado` (opcional): `Activa` | `Inactiva` - Filtrar por estado
- `incluir_conteo` (opcional, default: `true`): Incluir número de productos por categoría
- `buscar` (opcional): Texto para buscar en nombre o descripción

**Ejemplos:**
```http
GET /api/productos/categorias
GET /api/productos/categorias?estado=Activa
GET /api/productos/categorias?buscar=suplementos&incluir_conteo=true
```

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "nombre": "Suplementos",
    "slug": "suplementos",
    "icono": "💊",
    "orden": 1,
    "estado": "Activa",
    "total_productos": 25,
    "fecha_creacion": "2025-01-15T10:30:00"
  },
  {
    "id": 2,
    "nombre": "Bebidas",
    "slug": "bebidas",
    "icono": "🥤",
    "orden": 2,
    "estado": "Activa",
    "total_productos": 15,
    "fecha_creacion": "2025-01-15T10:31:00"
  }
]
```

**Casos de uso:**
- Selector de categorías en formulario de productos
- Menú de navegación de la tienda
- Dashboard de categorías
- Filtros de búsqueda

---

### 3. **Obtener Categoría por ID**
```http
GET /api/productos/categorias/{categoria_id}
```

**Propósito:** Obtener detalles de una categoría específica

**Ejemplo:**
```http
GET /api/productos/categorias/1
```

**Respuesta exitosa (200):** Similar al formato de listar categorías

**Casos de uso:**
- Ver detalles de categoría
- Editar categoría
- Ver productos de una categoría

---

### 4. **Obtener Categoría por Nombre**
```http
GET /api/productos/categorias/nombre/{nombre}
```

**Propósito:** Buscar categoría por nombre exacto (case-insensitive)

**Ejemplo:**
```http
GET /api/productos/categorias/nombre/Suplementos
GET /api/productos/categorias/nombre/suplementos  // También funciona
```

**Casos de uso:**
- Búsquedas por nombre
- Validación de nombres duplicados en frontend

---

### 5. **Actualizar Categoría**
```http
PATCH /api/productos/categorias/{categoria_id}
```

**Propósito:** Actualizar datos de una categoría (solo los campos enviados)

**Body (JSON) - Todos los campos son opcionales:**
```json
{
  "nombre": "Suplementos Nutricionales",
  "descripcion": "Nueva descripción",
  "icono": "💪",
  "orden": 5,
  "estado": "Inactiva"
}
```

**Casos de uso:**
- Formulario de edición de categoría
- Cambiar orden de visualización
- Activar/Desactivar categorías

---

### 6. **Eliminar Categoría**
```http
DELETE /api/productos/categorias/{categoria_id}
```

**Propósito:** Eliminar una categoría

**⚠️ IMPORTANTE:** No se puede eliminar si tiene productos asociados

**Respuesta exitosa (204):** Sin contenido

**Error (400):**
```json
{
  "detail": "No se puede eliminar una categoría que tiene productos asociados"
}
```

**Casos de uso:**
- Limpiar categorías sin uso
- Mantenimiento del catálogo

---

## 🛍️ PRODUCTOS - CRUD

### 7. **Crear Producto**
```http
POST /api/productos
```

**Propósito:** Crear un nuevo producto con toda su información

**Body (JSON):**
```json
{
  // Identificadores (REQUERIDOS)
  "sku": "PROT-WH-001",           // Código único del producto
  "nombre": "Proteína Whey 2kg Chocolate",
  "id_categoria": 1,

  // Identificadores opcionales
  "codigo_barras": "7501234567890",  // Para scanners
  "descripcion": "Proteína de suero concentrada sabor chocolate",

  // PRECIOS (REQUERIDOS: precio_costo y precio_venta)
  "precio_costo": 450.00,         // Lo que te costó comprarlo
  "precio_venta": 650.00,         // Precio al público
  "precio_mayorista": 600.00,     // Opcional: para ventas al mayoreo
  "precio_miembro": 600.00,       // Opcional: precio especial para miembros

  // INVENTARIO
  "stock_actual": 25,             // Stock inicial
  "stock_minimo": 5,              // Alerta cuando llegue a este número
  "stock_maximo": 100,            // Máximo permitido
  "permite_venta_sin_stock": false,  // true para servicios/productos digitales

  // MEDIDAS
  "unidad_medida": "Kg",          // "Unidad", "Kg", "Gramo", "Litro", etc.
  "peso": 2.0,                    // Peso en kg
  "volumen": null,                // Volumen en litros

  // IMPUESTOS
  "aplica_iva": true,
  "porcentaje_iva": 16.0,

  // MULTIMEDIA
  "imagen_url": "https://ejemplo.com/imagen.jpg",
  "imagenes_adicionales": [
    "https://ejemplo.com/img2.jpg",
    "https://ejemplo.com/img3.jpg"
  ],

  // INFORMACIÓN ADICIONAL
  "marca": "Optimum Nutrition",
  "fecha_vencimiento": "2026-12-31",  // Formato: YYYY-MM-DD
  "lote": "LOT-2025-001",

  // VISIBILIDAD
  "es_visible": true,             // Mostrar en tienda
  "es_destacado": true,           // Marcar como destacado
  "orden": 1,                     // Orden en listados

  // TAGS para búsqueda
  "tags": ["proteina", "whey", "chocolate", "suplemento"]
}
```

**Respuesta exitosa (201):** Producto completo con datos calculados (ver sección de respuestas)

**Validaciones automáticas:**
- ✅ `precio_venta >= precio_costo`
- ✅ `precio_miembro <= precio_venta`
- ✅ `stock_maximo >= stock_minimo`
- ✅ SKU único (no duplicados)
- ✅ Código de barras único (si se provee)
- ✅ Categoría debe existir
- ✅ Fecha de vencimiento debe ser futura

**Funcionalidades automáticas:**
- 🔄 Si hay stock inicial > 0, se registra automáticamente entrada en inventario
- 🔄 El SKU se convierte a mayúsculas automáticamente
- 🔄 Los tags se convierten a minúsculas

**Casos de uso:**
- Formulario de alta de productos
- Importación masiva de productos
- Setup inicial del inventario

---

### 8. **Listar Productos**
```http
GET /api/productos
```

**Propósito:** Listar productos con filtros avanzados y paginación

**Query Parameters (todos opcionales):**

**Filtros básicos:**
- `categoria_id` (int): Filtrar por ID de categoría
- `estado` (string): `Activo` | `Inactivo` | `Agotado` | `Descontinuado`

**Filtros de visibilidad:**
- `solo_visibles` (bool): Solo productos visibles en tienda
- `solo_destacados` (bool): Solo productos destacados
- `con_stock` (bool): Solo productos con stock disponible
- `stock_bajo` (bool): Solo productos con stock <= stock_minimo
- `proximos_vencer` (int): Productos que vencen en N días

**Búsqueda:**
- `buscar` (string): Buscar en nombre, SKU, descripción o código de barras
- `tags` (array): Filtrar por tags (se pueden enviar múltiples)
- `marca` (string): Filtrar por marca

**Rango de precios:**
- `precio_min` (decimal): Precio mínimo
- `precio_max` (decimal): Precio máximo

**Ordenamiento:**
- `ordenar_por`: `nombre` | `precio` | `stock` | `fecha` | `destacado` | `sku`
- `orden`: `asc` | `desc`

**Paginación:**
- `skip` (int, default: 0): Registros a saltar
- `limit` (int, default: 50, max: 500): Registros a retornar

**Ejemplos:**
```http
// Buscar proteínas en categoría Suplementos, solo visibles
GET /api/productos?buscar=proteina&categoria_id=1&solo_visibles=true

// Productos con stock bajo, ordenados por stock ascendente
GET /api/productos?stock_bajo=true&ordenar_por=stock&orden=asc

// Productos con múltiples tags y rango de precio
GET /api/productos?tags=suplemento&tags=proteina&precio_min=100&precio_max=500

// Productos destacados de una marca específica
GET /api/productos?solo_destacados=true&marca=Optimum%20Nutrition

// Productos que vencen en los próximos 30 días
GET /api/productos?proximos_vencer=30

// Paginación: segunda página de 20 productos
GET /api/productos?skip=20&limit=20
```

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "sku": "PROT-WH-001",
    "nombre": "Proteína Whey 2kg Chocolate",
    "nombre_categoria": "Suplementos",
    "precio_venta": 650.00,
    "precio_venta_con_iva": 754.00,    // Calculado automáticamente
    "precio_miembro": 600.00,
    "stock_actual": 25,
    "alerta_stock_bajo": false,
    "imagen_url": "https://ejemplo.com/imagen.jpg",
    "es_destacado": true,
    "estado": "Activo"
  }
]
```

**Casos de uso:**
- Catálogo de productos en la tienda
- Buscador de productos
- Dashboard de inventario
- Reportes filtrados
- Listados con paginación

---

### 9. **Obtener Producto por ID**
```http
GET /api/productos/{producto_id}
```

**Propósito:** Obtener información COMPLETA de un producto

**Ejemplo:**
```http
GET /api/productos/1
```

**Respuesta exitosa (200):**
```json
{
  // Identificación
  "id": 1,
  "sku": "PROT-WH-001",
  "codigo_barras": "7501234567890",
  "nombre": "Proteína Whey 2kg Chocolate",
  "descripcion": "Proteína de suero concentrada sabor chocolate",

  // Categoría
  "id_categoria": 1,
  "nombre_categoria": "Suplementos",

  // Precios originales
  "precio_costo": 450.00,
  "precio_venta": 650.00,
  "precio_mayorista": 600.00,
  "precio_miembro": 600.00,

  // Precios CALCULADOS automáticamente
  "precio_venta_con_iva": 754.00,      // precio_venta + IVA
  "monto_iva": 104.00,                 // IVA aplicado
  "margen_ganancia": 44.44,            // % de ganancia sobre costo

  // Inventario
  "stock_actual": 25,
  "stock_minimo": 5,
  "stock_maximo": 100,
  "permite_venta_sin_stock": false,
  "stock_disponible": true,            // CALCULADO: true si hay stock o permite venta sin stock
  "alerta_stock_bajo": false,          // CALCULADO: true si stock_actual <= stock_minimo
  "porcentaje_stock": 25.0,            // CALCULADO: % de stock respecto al máximo

  // Medidas
  "unidad_medida": "Kg",
  "peso": 2.0,
  "volumen": null,

  // Impuestos
  "aplica_iva": true,
  "porcentaje_iva": 16.0,

  // Multimedia
  "imagen_url": "https://ejemplo.com/imagen.jpg",
  "imagenes_adicionales": ["https://ejemplo.com/img2.jpg"],

  // Info adicional
  "marca": "Optimum Nutrition",
  "fecha_vencimiento": "2026-12-31",
  "dias_para_vencer": 365,             // CALCULADO: días desde hoy
  "alerta_por_vencer": false,          // CALCULADO: true si vence en <= 30 días
  "lote": "LOT-2025-001",

  // Visibilidad
  "es_visible": true,
  "es_destacado": true,
  "orden": 1,
  "tags": ["proteina", "whey", "chocolate", "suplemento"],

  // Valor del inventario CALCULADO
  "valor_inventario": 11250.00,        // stock_actual * precio_costo
  "valor_venta_inventario": 16250.00,  // stock_actual * precio_venta

  // Auditoría
  "estado": "Activo",
  "fecha_creacion": "2025-01-15T10:30:00",
  "fecha_modificacion": "2025-01-16T14:20:00"
}
```

**Casos de uso:**
- Vista de detalle del producto
- Formulario de edición (pre-llenado)
- Información en punto de venta
- Cálculos de inventario

---

### 10. **Obtener Producto por SKU**
```http
GET /api/productos/sku/{sku}
```

**Propósito:** Buscar producto por su código SKU

**Ejemplo:**
```http
GET /api/productos/sku/PROT-WH-001
```

**Casos de uso:**
- Búsqueda rápida por código
- Validación de SKU en formularios
- Importación de datos

---

### 11. **Obtener Producto por Código de Barras**
```http
GET /api/productos/codigo-barras/{codigo}
```

**Propósito:** Buscar producto escaneando código de barras

**Ejemplo:**
```http
GET /api/productos/codigo-barras/7501234567890
```

**Casos de uso:**
- **Punto de venta con scanner**
- Gestión de inventario con lector
- App móvil de inventario

---

### 12. **Obtener Producto por Nombre**
```http
GET /api/productos/nombre/{nombre}
```

**Propósito:** Buscar producto por nombre exacto (case-insensitive)

**Ejemplo:**
```http
GET /api/productos/nombre/Proteína Whey 2kg Chocolate
```

**Nota:** Para búsquedas parciales, usar `GET /api/productos?buscar=proteina`

---

### 13. **Actualizar Producto**
```http
PATCH /api/productos/{producto_id}
```

**Propósito:** Actualizar datos del producto (solo los campos enviados)

**Body (JSON) - Todos los campos son opcionales:**
```json
{
  "nombre": "Proteína Whey 2kg Chocolate Premium",
  "precio_venta": 680.00,
  "stock_minimo": 10,
  "es_destacado": false,
  "tags": ["proteina", "whey", "premium"]
}
```

**Funcionalidades automáticas:**
- 🔄 Los cambios de precio se registran en historial automáticamente
- 🔄 Se actualiza `fecha_modificacion`

**Casos de uso:**
- Formulario de edición de producto
- Actualización masiva de precios
- Cambiar visibilidad de productos

---

### 14. **Eliminar Producto**
```http
DELETE /api/productos/{producto_id}
```

**Propósito:** Eliminar un producto

**Query Parameters:**
- `eliminar_fisicamente` (bool, default: false)
  - `false`: Eliminación lógica (cambia estado a "Inactivo", conserva historial)
  - `true`: Eliminación física (borra de base de datos permanentemente)

**Ejemplos:**
```http
// Eliminación lógica (recomendado)
DELETE /api/productos/1?eliminar_fisicamente=false

// Eliminación física (solo si estás seguro)
DELETE /api/productos/1?eliminar_fisicamente=true
```

**Respuesta exitosa (204):** Sin contenido

**Casos de uso:**
- Desactivar productos descontinuados (lógica)
- Limpiar productos de prueba (física)

---

## 📦 INVENTARIO

### 15. **Registrar Entrada de Inventario**
```http
POST /api/productos/{producto_id}/inventario/entrada
```

**Propósito:** Registrar entrada de mercancía (compra, devolución, ajuste)

**Query Parameters:**
- `cantidad` (int, **requerido**): Cantidad a ingresar
- `costo_unitario` (decimal, opcional): Costo de compra
- `lote` (string, opcional): Número de lote
- `fecha_vencimiento` (date, opcional): Fecha de vencimiento
- `motivo` (string, opcional): Motivo de la entrada

**Ejemplo:**
```http
POST /api/productos/1/inventario/entrada?cantidad=50&costo_unitario=450&lote=LOT-2025-002&motivo=Compra%20a%20proveedor
```

**Respuesta exitosa (200):**
```json
{
  "id": 15,
  "id_producto": 1,
  "nombre_producto": "Proteína Whey 2kg Chocolate",
  "sku": "PROT-WH-001",
  "tipo_movimiento": "Entrada",
  "cantidad": 50,
  "stock_anterior": 25,
  "stock_nuevo": 75,               // Se actualiza automáticamente
  "costo_unitario": 450.00,
  "costo_total": 22500.00,         // Calculado: cantidad * costo_unitario
  "tipo_referencia": "Compra",
  "motivo": "Compra a proveedor",
  "lote": "LOT-2025-002",
  "fecha_creacion": "2025-01-16T09:30:00",
  "usuario_creacion": "admin"
}
```

**Casos de uso:**
- Recepción de mercancía
- Registro de compras
- Devoluciones de clientes
- Ajustes por conteo físico

---

### 16. **Registrar Salida de Inventario**
```http
POST /api/productos/{producto_id}/inventario/salida
```

**Propósito:** Registrar salida de mercancía (venta, uso interno)

**Query Parameters:**
- `cantidad` (int, **requerido**): Cantidad a sacar
- `motivo` (string, **requerido**): Motivo de la salida

**Ejemplo:**
```http
POST /api/productos/1/inventario/salida?cantidad=2&motivo=Venta%20al%20cliente
```

**⚠️ IMPORTANTE:** Valida que haya stock suficiente

**Error si no hay stock (400):**
```json
{
  "detail": "Stock insuficiente. Stock actual: 5, Cantidad solicitada: 10"
}
```

**Casos de uso:**
- Registrar ventas manuales
- Uso interno de productos
- Muestras gratis
- Devolución a proveedor

---

### 17. **Ajustar Inventario**
```http
POST /api/productos/{producto_id}/inventario/ajuste
```

**Propósito:** Ajustar stock a un valor específico (útil para conteos físicos)

**Query Parameters:**
- `stock_nuevo` (int, **requerido**): Nuevo valor de stock
- `motivo` (string, **requerido**, min 10 caracteres): Motivo del ajuste

**Ejemplo:**
```http
POST /api/productos/1/inventario/ajuste?stock_nuevo=80&motivo=Conteo%20físico%20mensual%20enero%202025
```

**Cómo funciona:**
- Si `stock_nuevo > stock_actual`: Registra ENTRADA por la diferencia
- Si `stock_nuevo < stock_actual`: Registra SALIDA por la diferencia

**Ejemplo:**
- Stock actual: 75
- Stock nuevo: 80
- Resultado: Entrada de 5 unidades

**Casos de uso:**
- Conteo físico de inventario
- Corrección de errores
- Auditorías
- Conciliación de inventario

---

### 18. **Registrar Merma**
```http
POST /api/productos/{producto_id}/inventario/merma
```

**Propósito:** Registrar pérdida de producto (vencido, dañado, robado)

**Query Parameters:**
- `cantidad` (int, **requerido**): Cantidad perdida
- `motivo` (string, **requerido**, min 10 caracteres): Motivo de la merma

**Ejemplo:**
```http
POST /api/productos/1/inventario/merma?cantidad=3&motivo=Producto%20vencido%20-%20lote%20LOT-2023-001
```

**Diferencia con Salida:**
- ✅ La merma se marca específicamente como pérdida
- ✅ No afecta estadísticas de ventas
- ✅ Útil para reportes de pérdidas

**Casos de uso:**
- Producto vencido
- Producto dañado
- Robo o extravío
- Control de calidad

---

### 19. **Ver Movimientos de Inventario**
```http
GET /api/productos/{producto_id}/inventario/movimientos
```

**Propósito:** Ver historial completo de movimientos de un producto

**Query Parameters (todos opcionales):**
- `tipo_movimiento`: `Entrada` | `Salida` | `Ajuste` | `Merma`
- `fecha_desde` (date): Desde fecha
- `fecha_hasta` (date): Hasta fecha
- `skip` (int, default: 0): Paginación
- `limit` (int, default: 100, max: 500): Registros por página

**Ejemplos:**
```http
// Todos los movimientos del producto
GET /api/productos/1/inventario/movimientos

// Solo entradas de los últimos 30 días
GET /api/productos/1/inventario/movimientos?tipo_movimiento=Entrada&fecha_desde=2025-01-01

// Movimientos con paginación
GET /api/productos/1/inventario/movimientos?skip=0&limit=50
```

**Respuesta exitosa (200):** Array de movimientos (ver formato en respuesta de entrada)

**Casos de uso:**
- Ver historial de movimientos
- Auditoría de inventario
- Análisis de rotación
- Rastreo de lotes

---

### 20. **Alertas de Stock Bajo**
```http
GET /api/productos/inventario/alertas
```

**Propósito:** Listar productos con stock bajo (stock_actual <= stock_minimo)

**Sin parámetros**

**Respuesta exitosa (200):** Array de productos (formato listado ligero)

**Casos de uso:**
- Dashboard de alertas
- Notificaciones push
- Reporte de compras necesarias
- Lista de pedido a proveedores

---

### 21. **Productos Próximos a Vencer**
```http
GET /api/productos/inventario/proximos-vencer
```

**Propósito:** Listar productos próximos a vencer

**Query Parameters:**
- `dias` (int, default: 30, min: 1, max: 365): Productos que vencen en N días

**Ejemplos:**
```http
// Productos que vencen en los próximos 30 días
GET /api/productos/inventario/proximos-vencer

// Productos que vencen en la próxima semana
GET /api/productos/inventario/proximos-vencer?dias=7
```

**Casos de uso:**
- Alertas de vencimiento
- Promociones por vencimiento cercano
- Control de calidad
- Gestión FIFO (First In, First Out)

---

### 22. **Productos Sin Stock**
```http
GET /api/productos/inventario/sin-stock
```

**Propósito:** Listar productos agotados (stock = 0 y no permiten venta sin stock)

**Casos de uso:**
- Reporte de productos a reponer
- Dashboard de inventario
- Lista de pedido urgente

---

## 💰 PRECIOS

### 23. **Actualizar Precios**
```http
PUT /api/productos/{producto_id}/precios
```

**Propósito:** Actualizar precios de un producto (se registra automáticamente en historial)

**Body (JSON):**
```json
{
  "precio_venta": 680.00,         // Opcional
  "precio_costo": 460.00,         // Opcional
  "precio_mayorista": 620.00,     // Opcional
  "precio_miembro": 620.00,       // Opcional
  "motivo": "Aumento de proveedor",  // REQUERIDO
  "usuario": "admin"              // Opcional
}
```

**Funcionalidades automáticas:**
- ✅ Valida que `precio_venta >= precio_costo`
- ✅ Registra cambio en historial automáticamente
- ✅ Calcula porcentaje de cambio

**Casos de uso:**
- Actualización de precios
- Ajustes por inflación
- Cambios de temporada
- Promociones

---

### 24. **Ver Historial de Precios**
```http
GET /api/productos/{producto_id}/historial-precios
```

**Propósito:** Ver historial completo de cambios de precios

**Query Parameters:**
- `tipo_precio` (opcional): `Venta` | `Costo` | `Mayorista` | `Miembro`
- `skip` (int, default: 0)
- `limit` (int, default: 50, max: 200)

**Ejemplos:**
```http
// Todo el historial
GET /api/productos/1/historial-precios

// Solo cambios de precio de venta
GET /api/productos/1/historial-precios?tipo_precio=Venta
```

**Respuesta exitosa (200):**
```json
[
  {
    "id": 5,
    "id_producto": 1,
    "tipo_precio": "Venta",
    "precio_anterior": 650.00,
    "precio_nuevo": 680.00,
    "porcentaje_cambio": 4.62,      // % de incremento/decremento
    "motivo": "Aumento de proveedor",
    "fecha_cambio": "2025-01-16T10:00:00",
    "usuario": "admin"
  }
]
```

**Casos de uso:**
- Auditoría de precios
- Análisis de variación de costos
- Reportes de cambios
- Trazabilidad de precios

---

### 25. **Calcular Precio Final**
```http
POST /api/productos/{producto_id}/calcular-precio
```

**Propósito:** Calcular precio final de un producto según cantidad y tipo de cliente

**Body (JSON):**
```json
{
  "cantidad": 2,              // Default: 1
  "es_miembro": true,         // Default: false
  "aplicar_mayorista": false  // Default: false
}
```

**Respuesta exitosa (200):**
```json
{
  "id_producto": 1,
  "nombre_producto": "Proteína Whey 2kg Chocolate",
  "cantidad": 2,
  "precio_unitario": 600.00,           // Precio base (según tipo de cliente)
  "precio_unitario_con_iva": 696.00,   // Precio + IVA
  "subtotal": 1200.00,                 // precio_unitario * cantidad
  "iva_total": 192.00,                 // IVA total
  "total": 1392.00,                    // Total a pagar
  "tipo_precio_aplicado": "Miembro",   // "Venta" | "Miembro" | "Mayorista"
  "ahorro": 100.00                     // Si aplica precio especial (vs precio regular)
}
```

**Lógica de precios:**
1. Si `aplicar_mayorista=true` y existe `precio_mayorista` → usa precio mayorista
2. Si `es_miembro=true` y existe `precio_miembro` → usa precio miembro
3. Sino → usa `precio_venta` (precio regular)

**Casos de uso:**
- **Calculadora de precios en carrito de compra**
- Cotizaciones
- Preview antes de checkout
- Mostrar ahorro para miembros

---

## 📊 ESTADÍSTICAS Y REPORTES

### 26. **Estadísticas Generales**
```http
GET /api/productos/estadisticas/resumen
```

**Propósito:** Dashboard general de productos e inventario

**Sin parámetros**

**Respuesta exitosa (200):**
```json
{
  "total_productos": 150,
  "productos_activos": 140,
  "productos_inactivos": 8,
  "productos_agotados": 2,
  "productos_con_stock_bajo": 12,
  "productos_por_vencer": 5,

  "valor_total_inventario": 125000.00,     // Valor a precio de costo
  "valor_total_venta": 180000.00,          // Valor a precio de venta
  "ganancia_potencial": 55000.00,          // Diferencia entre venta y costo

  "producto_mas_caro": {
    "id": 45,
    "nombre": "Bicicleta Spinning Pro",
    "precio_venta": 15000.00
  },

  "producto_mas_stock": {
    "id": 12,
    "nombre": "Barra Proteica",
    "stock_actual": 500
  },

  "categoria_con_mas_productos": {
    "id": 3,
    "nombre": "Snacks",
    "total_productos": 45
  }
}
```

**Casos de uso:**
- **Dashboard principal**
- KPIs de inventario
- Métricas para gerencia

---

### 27. **Estadísticas por Categoría**
```http
GET /api/productos/estadisticas/por-categoria
```

**Propósito:** Ver estadísticas agrupadas por categoría

**Sin parámetros**

**Respuesta exitosa (200):**
```json
[
  {
    "id_categoria": 1,
    "nombre_categoria": "Suplementos",
    "total_productos": 25,
    "valor_inventario": 45000.00,
    "valor_venta_inventario": 65000.00,
    "ganancia_potencial": 20000.00
  },
  {
    "id_categoria": 2,
    "nombre_categoria": "Bebidas",
    "total_productos": 15,
    "valor_inventario": 8000.00,
    "valor_venta_inventario": 12000.00,
    "ganancia_potencial": 4000.00
  }
]
```

**Casos de uso:**
- Análisis de categorías más rentables
- Reportes por línea de producto
- Decisiones de compra

---

### 28. **Reporte de Valor de Inventario**
```http
GET /api/productos/reportes/valor-inventario
```

**Propósito:** Reporte detallado del valor del inventario

**Query Parameters:**
- `categoria_id` (int, opcional): Filtrar por categoría

**Ejemplos:**
```http
// Todo el inventario
GET /api/productos/reportes/valor-inventario

// Solo categoría Suplementos
GET /api/productos/reportes/valor-inventario?categoria_id=1
```

**Respuesta exitosa (200):**
```json
{
  "total_productos": 150,
  "valor_total_costo": 125000.00,
  "valor_total_venta": 180000.00,
  "ganancia_potencial_total": 55000.00,

  "productos": [
    {
      "id": 1,
      "sku": "PROT-WH-001",
      "nombre": "Proteína Whey 2kg Chocolate",
      "stock_actual": 25,
      "precio_costo": 450.00,
      "precio_venta": 650.00,
      "valor_inventario_costo": 11250.00,     // stock * precio_costo
      "valor_inventario_venta": 16250.00,     // stock * precio_venta
      "ganancia_potencial": 5000.00
    }
  ]
}
```

**Casos de uso:**
- Reporte contable de inventario
- Valuación de activos
- Cierre mensual

---

### 29. **Productos por Margen de Ganancia**
```http
GET /api/productos/reportes/margen-ganancia
```

**Propósito:** Productos ordenados por margen de ganancia (mayor a menor)

**Sin parámetros**

**Respuesta exitosa (200):**
```json
[
  {
    "id": 15,
    "sku": "ACC-GUAN-001",
    "nombre": "Guantes de Entrenamiento",
    "precio_costo": 80.00,
    "precio_venta": 150.00,
    "margen_porcentaje": 87.50,      // % de ganancia sobre costo
    "ganancia_unitaria": 70.00       // Pesos de ganancia por unidad
  },
  {
    "id": 20,
    "sku": "SNCK-BAR-001",
    "nombre": "Barra Proteica",
    "precio_costo": 20.00,
    "precio_venta": 35.00,
    "margen_porcentaje": 75.00,
    "ganancia_unitaria": 15.00
  }
]
```

**Casos de uso:**
- Identificar productos más rentables
- Ajustar estrategia de precios
- Decidir qué productos promocionar
- Análisis de rentabilidad

---

## 📋 MODELOS DE DATOS

### Estados de Producto
```
"Activo"         - Producto disponible para venta
"Inactivo"       - Producto desactivado (eliminación lógica)
"Agotado"        - Sin stock
"Descontinuado"  - Ya no se venderá más
```

### Estados de Categoría
```
"Activa"    - Categoría habilitada
"Inactiva"  - Categoría deshabilitada
```

### Tipos de Movimiento de Inventario
```
"Entrada"  - Ingreso de mercancía (compra, devolución)
"Salida"   - Egreso de mercancía (venta, uso interno)
"Ajuste"   - Corrección de stock (conteo físico)
"Merma"    - Pérdida (vencido, dañado, robado)
```

### Tipos de Precio
```
"Venta"      - Precio público general
"Costo"      - Precio de compra
"Mayorista"  - Precio para ventas al mayoreo
"Miembro"    - Precio especial para miembros del gym
```

### Unidades de Medida
```
"Unidad"    - Piezas individuales
"Kg"        - Kilogramos
"Gramo"     - Gramos
"Litro"     - Litros
"Ml"        - Mililitros
"Caja"      - Cajas
"Paquete"   - Paquetes
```

---

## 🎯 Casos de Uso Recomendados

### Pantalla: Catálogo de Productos
```javascript
// 1. Listar categorías para el menú
GET /api/productos/categorias?estado=Activa

// 2. Listar productos visibles con paginación
GET /api/productos?solo_visibles=true&skip=0&limit=20

// 3. Filtrar por categoría seleccionada
GET /api/productos?categoria_id=1&solo_visibles=true

// 4. Buscar productos
GET /api/productos?buscar=proteina&solo_visibles=true
```

### Pantalla: Detalle de Producto
```javascript
// 1. Obtener producto completo
GET /api/productos/1

// 2. Calcular precio para el carrito
POST /api/productos/1/calcular-precio
Body: { "cantidad": 2, "es_miembro": true }
```

### Pantalla: Dashboard de Inventario
```javascript
// 1. Estadísticas generales
GET /api/productos/estadisticas/resumen

// 2. Alertas de stock bajo
GET /api/productos/inventario/alertas

// 3. Productos próximos a vencer
GET /api/productos/inventario/proximos-vencer?dias=30
```

### Pantalla: Gestión de Inventario
```javascript
// 1. Listar productos con filtros
GET /api/productos?ordenar_por=stock&orden=asc

// 2. Ver movimientos de un producto
GET /api/productos/1/inventario/movimientos

// 3. Registrar entrada
POST /api/productos/1/inventario/entrada?cantidad=50

// 4. Ajustar stock (conteo físico)
POST /api/productos/1/inventario/ajuste?stock_nuevo=75
```

### Pantalla: Punto de Venta
```javascript
// 1. Buscar producto por código de barras (scanner)
GET /api/productos/codigo-barras/7501234567890

// 2. Calcular total de la venta
POST /api/productos/1/calcular-precio
Body: { "cantidad": 2, "es_miembro": true }

// 3. Registrar salida (venta)
POST /api/productos/1/inventario/salida?cantidad=2&motivo=Venta
```

---

## ⚠️ Notas Importantes

### Paginación
- Límite máximo por request: 500 registros
- Default: 50 registros
- Usar `skip` y `limit` para paginación eficiente

### Fechas
- Formato: ISO 8601 (`YYYY-MM-DD` o `YYYY-MM-DDTHH:MM:SS`)
- Timezone: Se maneja en UTC

### Decimales (Precios)
- Precisión: 2 decimales
- Tipo: `Decimal` (se retorna como `float` en JSON)

### Búsqueda
- Case-insensitive (no importan mayúsculas/minúsculas)
- Búsqueda full-text en nombre, descripción, SKU

### Validaciones
- El backend valida automáticamente todos los constraints
- Errores retornan código 400 con mensaje descriptivo

### Performance
- Los listados usan versión "ligera" de productos
- Los detalles usan versión "completa" con todos los cálculos

---

## 🔒 Autenticación

**Nota:** Esta API no incluye autenticación aún. Se recomienda agregar:
- JWT tokens
- Roles de usuario (admin, vendedor, almacenista)
- Permisos por endpoint

---

## 📞 Soporte

Para dudas o problemas con la API, contactar al equipo de backend.

**Última actualización:** 2025-01-16
