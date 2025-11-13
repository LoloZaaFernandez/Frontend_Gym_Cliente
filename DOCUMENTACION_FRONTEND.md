# 📘 Documentación API - Guía para Frontend

**Base URL:** `http://localhost:8000`

Esta documentación cubre todos los endpoints nuevos agregados al sistema del gimnasio.

---

## 📑 Índice

1. [Sistema de Ventas de Productos](#-sistema-de-ventas-de-productos)
2. [Sistema de Egresos](#-sistema-de-egresos)
3. [Reportes Financieros Finales](#-reportes-financieros-finales)
4. [Registro de Cliente con Validación](#-registro-de-cliente-con-validación)

---

## 🛍️ Sistema de Ventas de Productos

### 1. Crear Venta

**Endpoint:** `POST /api/ventas`

**Descripción:** Registra una nueva venta de productos. Valida stock, calcula totales automáticamente y registra salida de inventario.

**Request Body:**
```json
{
  "id_cliente": 1,
  "tipo_cliente": "Miembro",
  "metodo_pago": "Efectivo",
  "descuento": 0,
  "notas": "Venta de productos varios",
  "productos": [
    {
      "id_producto": 1,
      "cantidad": 2
    },
    {
      "id_producto": 3,
      "cantidad": 1
    }
  ],
  "usuario_creacion": "admin"
}
```

**Parámetros:**
| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id_cliente` | integer | No | ID del cliente (opcional para venta pública) |
| `tipo_cliente` | string | Sí | "Publico", "Miembro", "Mayorista" |
| `metodo_pago` | string | Sí | Método de pago |
| `descuento` | float | No | Descuento aplicado (default: 0) |
| `notas` | string | No | Notas adicionales |
| `productos` | array | Sí | Lista de productos a vender (mínimo 1) |
| `usuario_creacion` | string | No | Usuario que registra (default: "system") |

**Response (201 Created):**
```json
{
  "id": 1,
  "folio": "VEN-20250113-0001",
  "id_cliente": 1,
  "nombre_cliente": "Juan Pérez García",
  "tipo_cliente": "Miembro",
  "subtotal": 1300.00,
  "iva": 208.00,
  "descuento": 0,
  "total": 1508.00,
  "metodo_pago": "Efectivo",
  "estado": "Completada",
  "notas": "Venta de productos varios",
  "fecha_venta": "2025-01-13T10:30:00",
  "usuario_creacion": "admin",
  "ganancia": 600.00,
  "total_productos": 2,
  "detalles": [
    {
      "id": 1,
      "id_producto": 1,
      "sku": "PROT-WH-001",
      "nombre_producto": "Proteína Whey 2kg Chocolate",
      "cantidad": 2,
      "precio_unitario": 600.00,
      "precio_costo": 450.00,
      "subtotal": 1200.00,
      "iva": 192.00,
      "total": 1392.00,
      "ganancia_producto": 300.00
    }
  ]
}
```

**Errores Comunes:**
- `400`: Stock insuficiente, producto no encontrado
- `404`: Producto no existe
- `500`: Error del servidor

---

### 2. Listar Ventas

**Endpoint:** `GET /api/ventas`

**Descripción:** Lista todas las ventas con filtros opcionales.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha_desde` | date | No | Fecha inicial (YYYY-MM-DD) |
| `fecha_hasta` | date | No | Fecha final (YYYY-MM-DD) |
| `estado` | string | No | "Completada", "Cancelada", "Pendiente" |
| `id_cliente` | integer | No | Filtrar por cliente |
| `tipo_cliente` | string | No | "Publico", "Miembro", "Mayorista" |
| `skip` | integer | No | Paginación: registros a saltar (default: 0) |
| `limit` | integer | No | Paginación: registros por página (default: 50, max: 500) |

**Ejemplo:**
```
GET /api/ventas?fecha_desde=2025-01-01&fecha_hasta=2025-01-31&tipo_cliente=Miembro
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "folio": "VEN-20250113-0001",
    "nombre_cliente": "Juan Pérez García",
    "tipo_cliente": "Miembro",
    "total": 1508.00,
    "metodo_pago": "Efectivo",
    "estado": "Completada",
    "fecha_venta": "2025-01-13T10:30:00",
    "ganancia": 600.00
  }
]
```

---

### 3. Obtener Venta por ID

**Endpoint:** `GET /api/ventas/{venta_id}`

**Ejemplo:** `GET /api/ventas/1`

**Response:** Igual que la respuesta de crear venta (incluye detalles).

---

### 4. Buscar Venta por Folio

**Endpoint:** `GET /api/ventas/folio/{folio}`

**Ejemplo:** `GET /api/ventas/folio/VEN-20250113-0001`

**Response:** Igual que obtener por ID.

---

### 5. Cancelar Venta

**Endpoint:** `POST /api/ventas/{venta_id}/cancelar`

**Descripción:** Cancela una venta y revierte el inventario automáticamente.

**Request Body:**
```json
{
  "motivo": "Cliente solicitó devolución por producto defectuoso",
  "usuario": "admin"
}
```

**Response (200 OK):** Venta actualizada con estado "Cancelada".

---

### 6. Reporte de Ventas por Método de Pago

**Endpoint:** `GET /api/ventas/reportes/metodos-pago`

**Descripción:** Muestra ventas agrupadas por método de pago (Efectivo, Yape, Otros).

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha_desde` | date | No | Fecha inicial (YYYY-MM-DD) |
| `fecha_hasta` | date | No | Fecha final (YYYY-MM-DD) |

**Ejemplo:**
```
GET /api/ventas/reportes/metodos-pago?fecha_desde=2025-01-01&fecha_hasta=2025-01-31
```

**Response (200 OK):**
```json
{
  "fecha_desde": "2025-01-01",
  "fecha_hasta": "2025-01-31",
  "total_general": 15000.00,
  "total_ventas": 45,
  "metodos_pago": {
    "Efectivo": {
      "cantidad": 20,
      "total": 8000.00,
      "porcentaje": 53.33
    },
    "Yape": {
      "cantidad": 15,
      "total": 5000.00,
      "porcentaje": 33.33
    },
    "Tarjeta": {
      "cantidad": 10,
      "total": 2000.00,
      "porcentaje": 13.33
    }
  },
  "efectivo": {
    "cantidad": 20,
    "total": 8000.00,
    "porcentaje": 53.33
  },
  "yape": {
    "cantidad": 15,
    "total": 5000.00,
    "porcentaje": 33.33
  },
  "otros": {
    "cantidad": 10,
    "total": 2000.00,
    "porcentaje": 13.33
  }
}
```

---

### 7. Reporte Diario de Ventas

**Endpoint:** `GET /api/ventas/reportes/diario`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha` | date | No | Fecha del reporte (default: hoy) |

**Ejemplo:** `GET /api/ventas/reportes/diario?fecha=2025-01-13`

**Response (200 OK):**
```json
{
  "fecha": "2025-01-13",
  "total_ventas": 25,
  "total_productos_vendidos": 150,
  "subtotal": 12000.00,
  "iva": 1920.00,
  "descuentos": 200.00,
  "total": 13720.00,
  "ganancia": 5000.00,
  "margen_promedio": 41.67,
  "ticket_promedio": 548.80,
  "ventas_por_metodo_pago": {
    "Efectivo": {
      "cantidad": 15,
      "total": 8000.00
    },
    "Yape": {
      "cantidad": 10,
      "total": 5720.00
    }
  },
  "ventas_por_tipo_cliente": {
    "Miembro": {
      "cantidad": 18,
      "total": 10000.00
    },
    "Publico": {
      "cantidad": 7,
      "total": 3720.00
    }
  },
  "productos_mas_vendidos": [
    {
      "nombre_producto": "Proteína Whey 2kg Chocolate",
      "sku": "PROT-WH-001",
      "cantidad_vendida": 50,
      "total_vendido": 6000.00,
      "ganancia": 2500.00
    }
  ]
}
```

---

### 8. Reporte Semanal de Ventas

**Endpoint:** `GET /api/ventas/reportes/semanal`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha` | date | No | Fecha dentro de la semana (default: hoy) |

**Response:** Similar al diario + ventas por día.

---

### 9. Reporte Mensual de Ventas

**Endpoint:** `GET /api/ventas/reportes/mensual`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `mes` | integer | No | Mes (1-12, default: mes actual) |
| `anio` | integer | No | Año (default: año actual) |

**Ejemplo:** `GET /api/ventas/reportes/mensual?mes=1&anio=2025`

**Response:** Similar al diario + ventas por día/semana + categorías más vendidas.

---

### 10. Reporte Anual de Ventas

**Endpoint:** `GET /api/ventas/reportes/anual`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `anio` | integer | No | Año (default: año actual) |

**Response:** Similar al mensual + mejor/peor mes del año.

---

## 💸 Sistema de Egresos

### 11. Listar Categorías de Egresos

**Endpoint:** `GET /api/egresos/categorias`

**Descripción:** Lista las categorías de gastos disponibles.

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `estado` | string | No | "Activa", "Inactiva" |

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Servicios",
    "descripcion": "Agua, luz, internet, teléfono",
    "estado": "Activa",
    "fecha_creacion": "2025-01-01T00:00:00"
  },
  {
    "id": 2,
    "nombre": "Sueldos",
    "descripcion": "Pago de nómina y salarios",
    "estado": "Activa",
    "fecha_creacion": "2025-01-01T00:00:00"
  }
]
```

**Categorías Predefinidas:**
1. Servicios
2. Mantenimiento
3. Sueldos
4. Alquiler
5. Compras
6. Marketing
7. Impuestos
8. Otros

---

### 12. Crear Egreso

**Endpoint:** `POST /api/egresos`

**Descripción:** Registra un nuevo gasto/egreso. Genera folio automáticamente.

**Request Body:**
```json
{
  "id_categoria": 1,
  "concepto": "Pago de luz",
  "descripcion": "Consumo de enero 2025",
  "monto": 1500.00,
  "metodo_pago": "Transferencia",
  "fecha_egreso": "2025-01-15",
  "proveedor": "CFE",
  "numero_factura": "FAC-2025-001",
  "estado": "Pagado",
  "es_recurrente": true,
  "frecuencia": "Mensual",
  "notas": "Pago puntual",
  "usuario_creacion": "admin"
}
```

**Parámetros:**
| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id_categoria` | integer | Sí | ID de categoría de egreso |
| `concepto` | string | Sí | Concepto del gasto (min 3 chars) |
| `descripcion` | string | No | Descripción detallada |
| `monto` | float | Sí | Monto del egreso (> 0) |
| `metodo_pago` | string | Sí | Método de pago |
| `fecha_egreso` | date | Sí | Fecha del egreso (YYYY-MM-DD) |
| `proveedor` | string | No | Nombre del proveedor |
| `numero_factura` | string | No | Número de factura |
| `estado` | string | No | "Pagado", "Pendiente", "Cancelado" (default: "Pagado") |
| `es_recurrente` | boolean | No | ¿Es un gasto recurrente? (default: false) |
| `frecuencia` | string | No | "Mensual", "Semanal", "Quincenal", "Anual" |
| `notas` | string | No | Notas adicionales |
| `usuario_creacion` | string | No | Usuario que registra |

**Response (201 Created):**
```json
{
  "id": 1,
  "folio": "EGR-20250115-0001",
  "id_categoria": 1,
  "nombre_categoria": "Servicios",
  "concepto": "Pago de luz",
  "descripcion": "Consumo de enero 2025",
  "monto": 1500.00,
  "metodo_pago": "Transferencia",
  "fecha_egreso": "2025-01-15",
  "proveedor": "CFE",
  "numero_factura": "FAC-2025-001",
  "estado": "Pagado",
  "es_recurrente": true,
  "frecuencia": "Mensual",
  "notas": "Pago puntual",
  "fecha_creacion": "2025-01-15T10:30:00",
  "usuario_creacion": "admin"
}
```

---

### 13. Listar Egresos

**Endpoint:** `GET /api/egresos`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha_desde` | date | No | Fecha inicial (YYYY-MM-DD) |
| `fecha_hasta` | date | No | Fecha final (YYYY-MM-DD) |
| `id_categoria` | integer | No | Filtrar por categoría |
| `estado` | string | No | "Pagado", "Pendiente", "Cancelado" |
| `skip` | integer | No | Paginación: registros a saltar (default: 0) |
| `limit` | integer | No | Paginación: registros por página (default: 50, max: 500) |

**Ejemplo:**
```
GET /api/egresos?fecha_desde=2025-01-01&fecha_hasta=2025-01-31&id_categoria=1
```

**Response (200 OK):** Array de egresos.

---

### 14. Obtener Egreso por ID

**Endpoint:** `GET /api/egresos/{egreso_id}`

**Ejemplo:** `GET /api/egresos/1`

**Response:** Igual que la respuesta de crear egreso.

---

### 15. Actualizar Egreso

**Endpoint:** `PATCH /api/egresos/{egreso_id}`

**Request Body:** Cualquier campo del egreso (todos opcionales).

**Ejemplo:**
```json
{
  "estado": "Pagado",
  "notas": "Pago realizado"
}
```

---

### 16. Eliminar Egreso

**Endpoint:** `DELETE /api/egresos/{egreso_id}`

**Response:** `204 No Content` (sin contenido si es exitoso)

---

### 17. Reporte de Egresos por Categoría

**Endpoint:** `GET /api/egresos/reportes/por-categoria`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha_desde` | date | No | Fecha inicial (YYYY-MM-DD) |
| `fecha_hasta` | date | No | Fecha final (YYYY-MM-DD) |

**Response (200 OK):**
```json
{
  "fecha_desde": "2025-01-01",
  "fecha_hasta": "2025-01-31",
  "total_egresos": 45,
  "total_monto": 25000.00,
  "egresos_por_categoria": [
    {
      "categoria": "Sueldos",
      "cantidad": 15,
      "total": 12000.00
    },
    {
      "categoria": "Servicios",
      "cantidad": 20,
      "total": 8000.00
    },
    {
      "categoria": "Alquiler",
      "cantidad": 10,
      "total": 5000.00
    }
  ]
}
```

---

## 📊 Reportes Financieros Finales

### 18. Reporte Financiero Diario

**Endpoint:** `GET /api/egresos/reportes/financiero-diario`

**Descripción:** Reporte financiero completo del día que integra:
- Ingresos por membresías
- Ingresos por ventas de productos
- Ganancia de productos
- Egresos del día
- **Ganancia neta final**

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fecha` | date | No | Fecha del reporte (default: hoy) |

**Ejemplo:** `GET /api/egresos/reportes/financiero-diario?fecha=2025-01-15`

**Response (200 OK):**
```json
{
  "fecha": "2025-01-15",
  "ingresos_membresias": 15000.00,
  "ingresos_productos": 8000.00,
  "ganancia_productos": 3000.00,
  "total_ingresos": 23000.00,
  "total_egresos": 5000.00,
  "ganancia_neta": 13000.00,
  "margen_neto": 56.52,
  "detalle_ingresos": {
    "Membresias": {
      "cantidad": 10,
      "total": 15000.00
    },
    "Productos": {
      "cantidad": 25,
      "total": 8000.00
    }
  },
  "detalle_egresos": {
    "Servicios": {
      "cantidad": 2,
      "total": 2500.00
    },
    "Sueldos": {
      "cantidad": 1,
      "total": 2500.00
    }
  }
}
```

**Cálculo de Ganancia Neta:**
```
Ganancia Neta = Ingresos Membresías + Ganancia Productos - Egresos
Ganancia Neta = $15,000 + $3,000 - $5,000 = $13,000
```

---

### 19. Reporte Financiero Mensual

**Endpoint:** `GET /api/egresos/reportes/financiero-mensual`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `mes` | integer | No | Mes (1-12, default: mes actual) |
| `anio` | integer | No | Año (default: año actual) |

**Ejemplo:** `GET /api/egresos/reportes/financiero-mensual?mes=1&anio=2025`

**Response (200 OK):**
```json
{
  "mes": 1,
  "anio": 2025,
  "nombre_mes": "Enero",
  "ingresos_membresias": 450000.00,
  "ingresos_productos": 240000.00,
  "ganancia_productos": 90000.00,
  "total_ingresos": 690000.00,
  "total_egresos": 150000.00,
  "ganancia_neta": 390000.00,
  "margen_neto": 56.52,
  "ingresos_por_dia": [
    {
      "fecha": "2025-01-01",
      "ingresos_membresias": 15000.00,
      "ingresos_productos": 8000.00,
      "total": 23000.00
    }
  ],
  "egresos_por_dia": [
    {
      "fecha": "2025-01-15",
      "cantidad": 3,
      "total": 5000.00
    }
  ],
  "egresos_por_categoria": [
    {
      "categoria": "Sueldos",
      "cantidad": 30,
      "total": 90000.00
    },
    {
      "categoria": "Alquiler",
      "cantidad": 1,
      "total": 30000.00
    },
    {
      "categoria": "Servicios",
      "cantidad": 15,
      "total": 20000.00
    }
  ]
}
```

---

### 20. Reporte Financiero Anual

**Endpoint:** `GET /api/egresos/reportes/financiero-anual`

**Query Parameters:**
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `anio` | integer | No | Año (default: año actual) |

**Ejemplo:** `GET /api/egresos/reportes/financiero-anual?anio=2025`

**Response (200 OK):**
```json
{
  "anio": 2025,
  "ingresos_membresias": 5400000.00,
  "ingresos_productos": 2880000.00,
  "ganancia_productos": 1080000.00,
  "total_ingresos": 8280000.00,
  "total_egresos": 1800000.00,
  "ganancia_neta": 4680000.00,
  "margen_neto": 56.52,
  "ingresos_por_mes": [
    {
      "mes": 1,
      "ingresos_membresias": 450000.00,
      "ingresos_productos": 240000.00,
      "ganancia_productos": 90000.00,
      "total_ingresos": 690000.00
    }
  ],
  "egresos_por_mes": [
    {
      "mes": 1,
      "cantidad": 45,
      "total": 150000.00
    }
  ],
  "egresos_por_categoria": [
    {
      "categoria": "Sueldos",
      "cantidad": 360,
      "total": 1080000.00
    }
  ],
  "mejor_mes": {
    "mes": 3,
    "total_ingresos": 750000.00
  },
  "peor_mes": {
    "mes": 8,
    "total_ingresos": 580000.00
  }
}
```

---

## 👤 Registro de Cliente con Validación

### 21. Registrar Cliente con Validación

**Endpoint:** `POST /api/registro/cliente-con-validacion`

**Descripción:** Registra un cliente con confirmación previa. Permite al usuario confirmar o cancelar el registro antes de procesarlo.

**Request Body:**
```json
{
  "confirmar_registro": "si",
  "dni": "12345678",
  "nombre": "Juan",
  "apellidos": "Pérez García",
  "correo": "juan.perez@email.com",
  "telefono": "987654321",
  "id_membresia": 1,
  "metodo_pago": "Efectivo",
  "usuario_creacion": "admin"
}
```

**Parámetros:**
| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `confirmar_registro` | string | Sí | "si" o "no" (case insensitive) |
| `dni` | string | Sí | DNI del cliente (8-12 chars) |
| `nombre` | string | Sí | Nombre del cliente |
| `apellidos` | string | Sí | Apellidos del cliente |
| `correo` | email | Sí | Correo electrónico |
| `telefono` | string | No | Teléfono de contacto |
| `id_membresia` | integer | Sí | ID de la membresía |
| `metodo_pago` | string | Sí | "Efectivo" o "Yape" |
| `usuario_creacion` | string | No | Usuario que registra |

**Response cuando confirma "SI" (200 OK):**
```json
{
  "registrado": true,
  "mensaje": "Cliente registrado exitosamente",
  "resumen": {
    "nombre_completo": "Juan Pérez García",
    "dni": "12345678",
    "metodo_pago": "Efectivo"
  },
  "cliente": {
    "id": 15,
    "dni": "12345678",
    "nombre": "Juan",
    "apellidos": "Pérez García",
    "correo": "juan.perez@email.com",
    "telefono": "987654321",
    "fecha_registro": "2025-01-13T10:30:00",
    "fecha_membresia": "2025-02-12T10:30:00",
    "estado": "Activo"
  },
  "pago_membresia": {
    "id": 45,
    "id_cliente": 15,
    "id_membresia": 1,
    "monto": 150.00,
    "metodo_pago": "Efectivo",
    "fecha_pago": "2025-01-13T10:30:00",
    "estado": "Pagado"
  }
}
```

**Response cuando confirma "NO" (200 OK):**
```json
{
  "registrado": false,
  "mensaje": "Inténtalo de nuevo",
  "resumen": {
    "nombre_completo": "Juan Pérez García",
    "dni": "12345678",
    "metodo_pago": "Efectivo"
  },
  "cliente": null,
  "pago_membresia": null
}
```

**Comportamiento:**
- **Si `confirmar_registro` = "si"**: Procesa el registro completo y retorna los datos del cliente
- **Si `confirmar_registro` = "no"**: NO procesa nada, solo muestra el resumen y "Inténtalo de nuevo"
- **Siempre muestra el resumen** con nombre completo, DNI y método de pago

---

## 🎨 Ejemplos de Uso en Frontend

### Ejemplo 1: Crear una Venta

```javascript
async function crearVenta() {
  const ventaData = {
    id_cliente: 1,
    tipo_cliente: "Miembro",
    metodo_pago: "Efectivo",
    descuento: 0,
    productos: [
      { id_producto: 1, cantidad: 2 },
      { id_producto: 3, cantidad: 1 }
    ],
    usuario_creacion: "admin"
  };

  try {
    const response = await fetch('http://localhost:8000/api/ventas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(ventaData)
    });

    if (response.ok) {
      const venta = await response.json();
      console.log('Venta creada:', venta.folio);
      console.log('Total:', venta.total);
      console.log('Ganancia:', venta.ganancia);
    } else {
      const error = await response.json();
      console.error('Error:', error.detail);
    }
  } catch (error) {
    console.error('Error de red:', error);
  }
}
```

---

### Ejemplo 2: Obtener Reporte Financiero del Día

```javascript
async function obtenerReporteFinancieroDiario() {
  const fecha = '2025-01-15';

  try {
    const response = await fetch(
      `http://localhost:8000/api/egresos/reportes/financiero-diario?fecha=${fecha}`
    );

    const reporte = await response.json();

    console.log('Ingresos totales:', reporte.total_ingresos);
    console.log('Egresos totales:', reporte.total_egresos);
    console.log('Ganancia neta:', reporte.ganancia_neta);
    console.log('Margen neto:', reporte.margen_neto + '%');

    // Mostrar desglose
    console.log('Ingresos por membresías:', reporte.ingresos_membresias);
    console.log('Ganancia de productos:', reporte.ganancia_productos);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

### Ejemplo 3: Registrar Cliente con Validación

```javascript
async function registrarClienteConValidacion(confirmar) {
  const clienteData = {
    confirmar_registro: confirmar ? "si" : "no",
    dni: "12345678",
    nombre: "Juan",
    apellidos: "Pérez García",
    correo: "juan@email.com",
    telefono: "987654321",
    id_membresia: 1,
    metodo_pago: "Efectivo"
  };

  try {
    const response = await fetch(
      'http://localhost:8000/api/registro/cliente-con-validacion',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(clienteData)
      }
    );

    const resultado = await response.json();

    // Siempre mostrar resumen
    console.log('Nombre:', resultado.resumen.nombre_completo);
    console.log('DNI:', resultado.resumen.dni);
    console.log('Método de pago:', resultado.resumen.metodo_pago);

    if (resultado.registrado) {
      console.log('✅ Cliente registrado exitosamente');
      console.log('ID Cliente:', resultado.cliente.id);
      console.log('Monto pagado:', resultado.pago_membresia.monto);
    } else {
      console.log('❌', resultado.mensaje); // "Inténtalo de nuevo"
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Uso
registrarClienteConValidacion(true);  // Confirma el registro
registrarClienteConValidacion(false); // No registra
```

---

### Ejemplo 4: Listar Ventas con Filtros

```javascript
async function listarVentas() {
  const params = new URLSearchParams({
    fecha_desde: '2025-01-01',
    fecha_hasta: '2025-01-31',
    tipo_cliente: 'Miembro',
    skip: 0,
    limit: 20
  });

  try {
    const response = await fetch(
      `http://localhost:8000/api/ventas?${params}`
    );

    const ventas = await response.json();

    ventas.forEach(venta => {
      console.log(`Folio: ${venta.folio}`);
      console.log(`Cliente: ${venta.nombre_cliente}`);
      console.log(`Total: $${venta.total}`);
      console.log(`Ganancia: $${venta.ganancia}`);
      console.log('---');
    });
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

### Ejemplo 5: Crear un Egreso

```javascript
async function crearEgreso() {
  const egresoData = {
    id_categoria: 1, // Servicios
    concepto: "Pago de luz",
    descripcion: "Consumo de enero 2025",
    monto: 1500.00,
    metodo_pago: "Transferencia",
    fecha_egreso: "2025-01-15",
    proveedor: "CFE",
    estado: "Pagado",
    es_recurrente: true,
    frecuencia: "Mensual"
  };

  try {
    const response = await fetch('http://localhost:8000/api/egresos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(egresoData)
    });

    const egreso = await response.json();
    console.log('Egreso registrado:', egreso.folio);
    console.log('Monto:', egreso.monto);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

## ⚠️ Manejo de Errores

### Códigos de Estado HTTP

| Código | Significado | Cuándo ocurre |
|--------|-------------|---------------|
| `200` | OK | Operación exitosa |
| `201` | Created | Recurso creado exitosamente |
| `204` | No Content | Eliminación exitosa |
| `400` | Bad Request | Datos inválidos o validación fallida |
| `404` | Not Found | Recurso no encontrado |
| `500` | Server Error | Error interno del servidor |

### Formato de Error

```json
{
  "detail": "Mensaje descriptivo del error"
}
```

### Ejemplo de Manejo de Errores

```javascript
try {
  const response = await fetch('http://localhost:8000/api/ventas', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ventaData)
  });

  if (!response.ok) {
    const error = await response.json();

    switch (response.status) {
      case 400:
        console.error('Datos inválidos:', error.detail);
        break;
      case 404:
        console.error('No encontrado:', error.detail);
        break;
      case 500:
        console.error('Error del servidor:', error.detail);
        break;
      default:
        console.error('Error:', error.detail);
    }
    return;
  }

  const resultado = await response.json();
  console.log('Éxito:', resultado);
} catch (error) {
  console.error('Error de red:', error);
}
```

---

## 📝 Notas Importantes

### Formatos de Fecha
- Usar formato ISO: `YYYY-MM-DD` para fechas
- Ejemplo: `"2025-01-15"`

### Tipos de Cliente
- `"Publico"`: Cliente general
- `"Miembro"`: Miembro del gimnasio (aplica precio especial)
- `"Mayorista"`: Compra al mayoreo (aplica precio mayorista)

### Estados de Venta
- `"Completada"`: Venta finalizada
- `"Cancelada"`: Venta cancelada (inventario revertido)
- `"Pendiente"`: Venta en proceso

### Estados de Egreso
- `"Pagado"`: Egreso ya pagado
- `"Pendiente"`: Egreso pendiente de pago
- `"Cancelado"`: Egreso cancelado

### Paginación
- Usar `skip` y `limit` para paginar resultados
- Límite máximo: 500 registros por página

---

## 🔗 Recursos Adicionales

- **Documentación Interactiva (Swagger):** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

---

## 📞 Soporte

Para dudas o problemas con la API, contactar al equipo de backend.

**Última actualización:** 2025-01-13
