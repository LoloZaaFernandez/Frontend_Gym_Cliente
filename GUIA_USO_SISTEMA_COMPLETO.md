# GUÍA RÁPIDA - SISTEMA BLESSED GYM COMPLETO

## 🚀 INICIO RÁPIDO

### **Paso 1: Preparar Base de Datos**

```bash
# Ir al directorio backend
cd backend

# Ejecutar migración (agregar campo Id_Membresia)
python migrate_add_membresia_to_cliente.py

# Insertar membresías iniciales con precios
python seed_membresias.py
```

**Resultado:**
- ✅ Campo `Id_Membresia` agregado a tabla CLIENTE
- ✅ 5 membresías creadas (Diaria, Mensual, Trimestral, Semestral, Anual)
- ✅ Precios asignados a cada membresía

---

### **Paso 2: Iniciar Backend**

```bash
cd backend
python -m uvicorn main:app --reload
```

**Verificar:**
- Backend corre en: http://localhost:8000
- Documentación API: http://localhost:8000/api/docs

---

### **Paso 3: Iniciar Frontend**

```bash
cd frontend
flet run main.py
```

---

## 👨‍💼 USO DEL SISTEMA - ADMINISTRADOR

### **Login**
- Usuario: `admin`
- Contraseña: `admin123`

### **1. GESTIÓN DE MEMBRESÍAS**

**Navegar:** Dashboard → Membresías

#### **Crear Nueva Membresía**
1. Click en "Nueva Membresía"
2. Llenar formulario:
   - Nombre: "Membresía VIP"
   - Tipo: Seleccionar tipo (Mensual, Trimestral, etc.)
   - Precio: 200.00
3. Click "Crear"
4. ✅ Membresía creada con precio asignado

#### **Modificar Precio de Membresía**
1. Seleccionar membresía
2. Click en icono 💰 "Gestionar Precios"
3. Ingresar nuevo precio
4. Click "Actualizar Precio"
5. ✅ Precio actualizado (se mantiene historial)

#### **Editar Membresía**
1. Seleccionar membresía
2. Click en icono ✏️ "Editar"
3. Modificar nombre
4. Click "Guardar"
5. ✅ Cambios guardados

#### **Activar/Desactivar Membresía**
1. Seleccionar membresía
2. Click en icono de toggle (🔄)
3. Confirmar cambio
4. ✅ Estado actualizado

**Nota:** Las membresías inactivas NO aparecen para los clientes.

---

### **2. REGISTRO DE ASISTENCIAS**

**Navegar:** Dashboard → Asistencia

#### **Registrar Asistencia**
1. Ingresar DNI del cliente en el campo de búsqueda
2. Click "Buscar Cliente" o presionar Enter
3. El sistema verifica:
   - ✅ Cliente existe
   - ✅ Cliente activo
   - ✅ Tiene membresía asignada
   - ✅ Membresía no vencida
4. Si todo OK: Click "Registrar Asistencia"
5. ✅ Asistencia registrada

**Estados posibles:**
- 🟢 **Membresía Activa** → Puede registrar
- 🟡 **Sin Membresía** → NO puede registrar
- 🔴 **Membresía Vencida** → NO puede registrar
- ⚫ **Cliente Inactivo** → NO puede registrar

#### **Ver Estadísticas**
- **Asistencias Hoy**: Total de asistencias del día
- **Clientes Activos Mes**: Clientes únicos que asistieron
- **Promedio Diario**: Promedio de asistencias por día

---

### **3. GESTIÓN DE CLIENTES**

**Navegar:** Dashboard → Clientes

#### **Crear Cliente**
1. Click "Nuevo Cliente"
2. Llenar formulario:
   - DNI (único)
   - Nombre
   - Apellidos
   - Correo (único)
   - Teléfono
3. Click "Guardar"
4. ✅ Cliente creado (Estado: Inactivo)

**Nota:** El cliente se activa automáticamente al comprar una membresía.

---

## 👤 USO DEL SISTEMA - CLIENTE

### **Login**
- Ingresar con DNI del cliente

### **1. COMPRAR MEMBRESÍA**

**Navegar:** Dashboard → Membresías

1. Ver membresías disponibles con precios reales
2. Leer beneficios de cada plan
3. Click "Adquirir Plan" en la membresía deseada
4. Confirmar compra en diálogo
5. ✅ Membresía asignada automáticamente
6. Ver "Membresía Activa" con días restantes

**Lo que sucede en el backend:**
```
1. Registra pago en PAGO_MEMBRESIA
2. Calcula fecha_vencimiento según tipo:
   - Diaria: +1 día
   - Mensual: +30 días
   - Trimestral: +90 días
   - Semestral: +180 días
   - Anual: +365 días
3. Actualiza CLIENTE:
   - Id_Membresia = ID de la membresía comprada
   - FECHA_MEMBRESIA = fecha de vencimiento
   - Estado = 'Activo'
```

---

### **2. VER HISTORIAL DE ASISTENCIAS**

**Navegar:** Dashboard → Asistencias

- Ver total de asistencias
- Ver asistencias del mes actual
- Ver fecha de última asistencia
- Ver historial reciente con fechas y horas

---

### **3. VER MI PERFIL**

**Navegar:** Dashboard → Mi Perfil

- Ver información personal
- Ver estado de membresía
- Ver días restantes
- Actualizar datos personales

---

## 🔄 FLUJOS COMPLETOS

### **FLUJO 1: Nuevo Cliente Compra Membresía**

```
1. Admin crea cliente (DNI: 12345678)
   └─> Estado: Inactivo
   └─> Sin membresía

2. Cliente hace login con DNI: 12345678

3. Cliente va a "Membresías"
   └─> Ve 5 membresías disponibles con precios

4. Cliente compra "Membresía Mensual" (S/. 80.00)
   └─> Sistema registra pago
   └─> Sistema asigna membresía
   └─> Cliente.Estado = 'Activo'
   └─> Cliente.Id_Membresia = 2
   └─> Cliente.FECHA_MEMBRESIA = HOY + 30 días

5. Cliente ve "Membresía Activa" con 30 días restantes

6. Cliente va al gimnasio

7. Admin registra asistencia con DNI: 12345678
   └─> ✅ Sistema verifica membresía activa
   └─> ✅ Asistencia registrada
```

---

### **FLUJO 2: Admin Actualiza Precio**

```
1. Admin va a "Membresías"

2. Admin selecciona "Membresía Mensual"

3. Admin click "Gestionar Precios"

4. Admin cambia precio de S/. 80.00 a S/. 100.00

5. Sistema:
   └─> Desactiva precio anterior (Estado='Inactivo')
   └─> Crea nuevo precio (Estado='Activo')
   └─> Mantiene historial

6. Cliente ve nuevo precio S/. 100.00 al comprar
```

---

### **FLUJO 3: Renovación de Membresía**

```
1. Cliente tiene membresía que vence mañana

2. Cliente va a "Membresías"
   └─> Ve estado "Membresía Activa - 1 día restante"

3. Cliente compra misma membresía o diferente

4. Sistema:
   └─> Registra nuevo pago
   └─> Actualiza Id_Membresia (si cambió)
   └─> Actualiza FECHA_MEMBRESIA = HOY + días del nuevo plan

5. ✅ Membresía renovada
```

---

## 📊 CONSULTAS SQL ÚTILES

### **Ver clientes con membresías activas**
```sql
SELECT
    c.DNI,
    c.NOMBRE,
    c.APELLIDOS,
    m.Nombre_Membresia,
    c.FECHA_MEMBRESIA,
    c.Estado
FROM CLIENTE c
LEFT JOIN MEMBRESIA m ON c.Id_Membresia = m.Id
WHERE c.Estado = 'Activo'
  AND c.FECHA_MEMBRESIA > date('now');
```

### **Ver historial de pagos de un cliente**
```sql
SELECT
    p.Id,
    p.Fecha_Pago,
    m.Nombre_Membresia,
    p.Monto,
    p.Metodo_Pago
FROM PAGO_MEMBRESIA p
JOIN MEMBRESIA m ON p.Id_Membresia = m.Id
WHERE p.Id_Cliente = 1
ORDER BY p.Fecha_Pago DESC;
```

### **Ver precios actuales de membresías**
```sql
SELECT
    m.Id,
    m.Nombre_Membresia,
    m.tipo_membresia,
    p.Precio_Actual,
    m.Estado
FROM MEMBRESIA m
LEFT JOIN PRECIO_MEMBRESIA p ON m.Id = p.Id_Membresia AND p.Estado = 'Activo'
ORDER BY
    CASE m.tipo_membresia
        WHEN 'Dia' THEN 1
        WHEN 'Mensual' THEN 2
        WHEN 'Trimestral' THEN 3
        WHEN 'Semestral' THEN 4
        WHEN 'Anual' THEN 5
    END;
```

### **Ver asistencias de hoy**
```sql
SELECT
    a.Nombre_Cliente,
    a.Hora_Ingreso,
    a.Tipo_Membresia
FROM ASISTENCIA a
WHERE a.Fecha_Asistencia = date('now')
ORDER BY a.Hora_Ingreso DESC;
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **Problema: Cliente no puede comprar membresía**

**Verificar:**
1. ✅ Cliente existe en la BD
2. ✅ Membresía está en estado "Activa"
3. ✅ Precio está configurado para la membresía
4. ✅ Backend está corriendo
5. ✅ Frontend puede conectar al backend

**Consulta:**
```sql
SELECT * FROM MEMBRESIA WHERE tipo_membresia = 'Mensual';
SELECT * FROM PRECIO_MEMBRESIA WHERE Id_Membresia = 2 AND Estado = 'Activo';
```

---

### **Problema: No se puede registrar asistencia**

**Verificar:**
1. ✅ Cliente tiene membresía (Id_Membresia no es NULL)
2. ✅ FECHA_MEMBRESIA > HOY (no vencida)
3. ✅ Cliente.Estado = 'Activo'

**Consulta:**
```sql
SELECT
    DNI,
    NOMBRE,
    Estado,
    Id_Membresia,
    FECHA_MEMBRESIA,
    date('now') as Hoy,
    CASE
        WHEN FECHA_MEMBRESIA > date('now') THEN 'Vigente'
        ELSE 'Vencida'
    END as Estado_Membresia
FROM CLIENTE
WHERE DNI = '12345678';
```

---

### **Problema: Precios no se actualizan en frontend**

**Solución:**
1. Verificar que el backend esté corriendo
2. Click "Actualizar" en la vista de membresías
3. Verificar en la BD:
```sql
SELECT * FROM PRECIO_MEMBRESIA
WHERE Id_Membresia = 2
ORDER BY Fecha_Creacion DESC;
```

---

### **Problema: CRUD de Admin no funciona**

**Verificar:**
1. ✅ Backend corriendo en puerto 8000
2. ✅ API_BASE_URL correcto en `frontend/config/settings.py`
3. ✅ Revisar consola del backend para ver errores
4. ✅ Revisar terminal del frontend para ver excepciones

---

## 📋 CHECKLIST DE VERIFICACIÓN

### **Backend:**
- [ ] Base de datos tiene campo `Id_Membresia` en CLIENTE
- [ ] Membresías iniciales insertadas
- [ ] Precios asignados a membresías
- [ ] Backend corriendo en puerto 8000
- [ ] API docs accesible: http://localhost:8000/api/docs

### **Frontend:**
- [ ] Frontend corriendo sin errores
- [ ] Puede hacer login como admin
- [ ] Puede hacer login como cliente
- [ ] Vista de membresías muestra precios
- [ ] CRUD de admin funciona

### **Flujos:**
- [ ] Admin puede crear membresía con precio
- [ ] Admin puede modificar precio
- [ ] Cliente puede comprar membresía
- [ ] Cliente aparece con "Membresía Activa"
- [ ] Admin puede registrar asistencia del cliente

---

## 🎯 ENDPOINTS API PRINCIPALES

```
POST   /api/membresias              - Crear membresía
GET    /api/membresias              - Listar membresías
PUT    /api/membresias/{id}         - Actualizar membresía
POST   /api/membresias/precios      - Crear/actualizar precio
GET    /api/membresias/precios/{id} - Obtener precio vigente
POST   /api/membresias/pagos        - Comprar membresía
GET    /api/membresias/pagos/cliente/{id} - Historial pagos

POST   /api/asistencias             - Registrar asistencia
GET    /api/asistencias             - Listar asistencias
GET    /api/asistencias/estadisticas/hoy - Stats del día
GET    /api/asistencias/estadisticas/mes - Stats del mes
GET    /api/asistencias/cliente/{id}/estadisticas - Stats cliente

GET    /api/clientes                - Listar clientes
POST   /api/clientes                - Crear cliente
PUT    /api/clientes/{id}           - Actualizar cliente
GET    /api/clientes/{id}           - Obtener cliente
```

---

## ✅ SISTEMA FUNCIONANDO

**El sistema está 100% operativo cuando:**

1. ✅ Admin puede crear y modificar membresías
2. ✅ Admin puede actualizar precios
3. ✅ Cliente ve precios reales desde la BD
4. ✅ Cliente puede comprar membresías
5. ✅ Cliente queda con membresía asignada (Id_Membresia)
6. ✅ Cliente tiene fecha de vencimiento calculada
7. ✅ Cliente puede registrar asistencias
8. ✅ Sistema valida membresías vencidas
9. ✅ Historial de precios se mantiene
10. ✅ Todas las operaciones se registran con usuario y fecha

---

**Fecha:** 05 de Noviembre, 2025
**Sistema:** BLESSED GYM - Sistema de Gestión Integral
**Estado:** ✅ PRODUCCIÓN - COMPLETAMENTE FUNCIONAL
**Versión:** 2.0 - Con CRUD completo y flujos validados
