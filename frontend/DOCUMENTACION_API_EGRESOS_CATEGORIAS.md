# 📚 Documentación API - Categorías de Egresos

## Endpoints de Categorías de Egresos

Esta documentación cubre los endpoints para la gestión completa (CRUD) de categorías de egresos.

---

## 📋 Tabla de Contenidos

1. [Listar Categorías](#1-listar-categorías)
2. [Crear Categoría](#2-crear-categoría)
3. [Obtener Categoría por ID](#3-obtener-categoría-por-id)
4. [Actualizar Categoría](#4-actualizar-categoría)
5. [Eliminar Categoría](#5-eliminar-categoría)
6. [Ejemplos de Integración](#ejemplos-de-integración)

---

## 1. Listar Categorías

Obtiene una lista de todas las categorías de egresos, con filtro opcional por estado.

### Request

```http
GET /api/egresos/categorias
```

### Query Parameters

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `estado` | string | No | Filtrar por estado: `Activa` o `Inactiva` |

### Response 200 OK

```json
[
  {
    "id": 1,
    "nombre": "Servicios Básicos",
    "descripcion": "Agua, luz, internet",
    "estado": "Activa",
    "fecha_creacion": "2025-01-15T10:30:00"
  },
  {
    "id": 2,
    "nombre": "Mantenimiento",
    "descripcion": "Reparaciones y mantenimiento del gimnasio",
    "estado": "Activa",
    "fecha_creacion": "2025-01-15T10:31:00"
  }
]
```

### Ejemplos

**JavaScript (Fetch):**
```javascript
// Obtener todas las categorías
const response = await fetch('http://localhost:8000/api/egresos/categorias')
const categorias = await response.json()

// Filtrar solo categorías activas
const response = await fetch('http://localhost:8000/api/egresos/categorias?estado=Activa')
const categoriasActivas = await response.json()
```

**JavaScript (Axios):**
```javascript
import axios from 'axios'

// Obtener todas las categorías
const { data } = await axios.get('/api/egresos/categorias')

// Filtrar solo categorías activas
const { data } = await axios.get('/api/egresos/categorias', {
  params: { estado: 'Activa' }
})
```

**TypeScript:**
```typescript
interface CategoriaEgreso {
  id: number
  nombre: string
  descripcion: string | null
  estado: 'Activa' | 'Inactiva'
  fecha_creacion: string
}

const getCategorias = async (estado?: 'Activa' | 'Inactiva'): Promise<CategoriaEgreso[]> => {
  const url = estado
    ? `/api/egresos/categorias?estado=${estado}`
    : '/api/egresos/categorias'

  const response = await fetch(url)
  return response.json()
}

// Uso
const categorias = await getCategorias()
const activas = await getCategorias('Activa')
```

---

## 2. Crear Categoría

Crea una nueva categoría de egreso.

### Request

```http
POST /api/egresos/categorias
Content-Type: application/json
```

### Body

```json
{
  "nombre": "Servicios Básicos",
  "descripcion": "Agua, luz, internet"
}
```

### Body Parameters

| Campo | Tipo | Requerido | Restricciones | Descripción |
|-------|------|-----------|---------------|-------------|
| `nombre` | string | ✅ Sí | Min: 3, Max: 100 | Nombre de la categoría |
| `descripcion` | string | No | - | Descripción opcional |

### Response 201 Created

```json
{
  "id": 3,
  "nombre": "Servicios Básicos",
  "descripcion": "Agua, luz, internet",
  "estado": "Activa",
  "fecha_creacion": "2025-01-15T10:35:00"
}
```

### Response 400 Bad Request

```json
{
  "detail": "El nombre debe tener al menos 3 caracteres"
}
```

### Response 500 Internal Server Error

```json
{
  "detail": "Error al crear categoría: [mensaje de error]"
}
```

### Ejemplos

**JavaScript (Fetch):**
```javascript
const crearCategoria = async (nombre, descripcion = null) => {
  const response = await fetch('http://localhost:8000/api/egresos/categorias', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      nombre,
      descripcion
    })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail)
  }

  return response.json()
}

// Uso
try {
  const nuevaCategoria = await crearCategoria('Servicios Básicos', 'Agua, luz, internet')
  console.log('Categoría creada:', nuevaCategoria)
} catch (error) {
  console.error('Error:', error.message)
}
```

**JavaScript (Axios):**
```javascript
import axios from 'axios'

const crearCategoria = async (nombre, descripcion = null) => {
  try {
    const { data } = await axios.post('/api/egresos/categorias', {
      nombre,
      descripcion
    })
    return data
  } catch (error) {
    throw new Error(error.response.data.detail)
  }
}
```

**React Hook:**
```javascript
import { useState } from 'react'
import axios from 'axios'

const useCrearCategoria = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const crear = async (nombre, descripcion) => {
    setLoading(true)
    setError(null)

    try {
      const { data } = await axios.post('/api/egresos/categorias', {
        nombre,
        descripcion
      })
      setLoading(false)
      return data
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear categoría')
      setLoading(false)
      throw err
    }
  }

  return { crear, loading, error }
}

// Uso en componente
function FormCrearCategoria() {
  const { crear, loading, error } = useCrearCategoria()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const categoria = await crear('Servicios Básicos', 'Agua, luz, internet')
      alert('Categoría creada exitosamente')
    } catch (err) {
      // Error ya manejado por el hook
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      <button disabled={loading}>
        {loading ? 'Creando...' : 'Crear'}
      </button>
    </form>
  )
}
```

---

## 3. Obtener Categoría por ID

Obtiene los detalles de una categoría específica.

### Request

```http
GET /api/egresos/categorias/{categoria_id}
```

### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `categoria_id` | integer | ID de la categoría (debe ser > 0) |

### Response 200 OK

```json
{
  "id": 1,
  "nombre": "Servicios Básicos",
  "descripcion": "Agua, luz, internet",
  "estado": "Activa",
  "fecha_creacion": "2025-01-15T10:30:00"
}
```

### Response 404 Not Found

```json
{
  "detail": "Categoría no encontrada"
}
```

### Ejemplos

**JavaScript (Fetch):**
```javascript
const obtenerCategoria = async (id) => {
  const response = await fetch(`http://localhost:8000/api/egresos/categorias/${id}`)

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Categoría no encontrada')
    }
    throw new Error('Error al obtener categoría')
  }

  return response.json()
}

// Uso
try {
  const categoria = await obtenerCategoria(1)
  console.log('Categoría:', categoria)
} catch (error) {
  console.error('Error:', error.message)
}
```

**JavaScript (Axios):**
```javascript
import axios from 'axios'

const obtenerCategoria = async (id) => {
  try {
    const { data } = await axios.get(`/api/egresos/categorias/${id}`)
    return data
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error('Categoría no encontrada')
    }
    throw new Error(error.response?.data?.detail || 'Error al obtener categoría')
  }
}
```

**React Hook con SWR:**
```javascript
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then(res => res.json())

const useCategoria = (id) => {
  const { data, error, mutate } = useSWR(
    id ? `/api/egresos/categorias/${id}` : null,
    fetcher
  )

  return {
    categoria: data,
    loading: !error && !data,
    error,
    mutate
  }
}

// Uso en componente
function DetalleCategoria({ id }) {
  const { categoria, loading, error } = useCategoria(id)

  if (loading) return <div>Cargando...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <h2>{categoria.nombre}</h2>
      <p>{categoria.descripcion}</p>
      <span>Estado: {categoria.estado}</span>
    </div>
  )
}
```

---

## 4. Actualizar Categoría

Actualiza una o más propiedades de una categoría existente (actualización parcial).

### Request

```http
PATCH /api/egresos/categorias/{categoria_id}
Content-Type: application/json
```

### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `categoria_id` | integer | ID de la categoría a actualizar |

### Body

**Puedes enviar solo los campos que quieres actualizar:**

```json
{
  "nombre": "Servicios Públicos",
  "descripcion": "Agua, luz, internet y teléfono",
  "estado": "Inactiva"
}
```

O solo un campo:

```json
{
  "nombre": "Servicios Públicos"
}
```

### Body Parameters

| Campo | Tipo | Requerido | Restricciones | Descripción |
|-------|------|-----------|---------------|-------------|
| `nombre` | string | No | Min: 3, Max: 100 | Nuevo nombre |
| `descripcion` | string | No | - | Nueva descripción |
| `estado` | string | No | `Activa` o `Inactiva` | Nuevo estado |

### Response 200 OK

```json
{
  "id": 1,
  "nombre": "Servicios Públicos",
  "descripcion": "Agua, luz, internet y teléfono",
  "estado": "Activa",
  "fecha_creacion": "2025-01-15T10:30:00"
}
```

### Response 404 Not Found

```json
{
  "detail": "Categoría no encontrada"
}
```

### Response 400 Bad Request

```json
{
  "detail": "No se pudo actualizar la categoría"
}
```

### Ejemplos

**JavaScript (Fetch):**
```javascript
const actualizarCategoria = async (id, datos) => {
  const response = await fetch(`http://localhost:8000/api/egresos/categorias/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datos)
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail)
  }

  return response.json()
}

// Uso: Actualizar solo el nombre
const categoriaActualizada = await actualizarCategoria(1, {
  nombre: 'Servicios Públicos'
})

// Uso: Actualizar múltiples campos
const categoriaActualizada = await actualizarCategoria(1, {
  nombre: 'Servicios Públicos',
  descripcion: 'Agua, luz, internet y teléfono',
  estado: 'Inactiva'
})
```

**JavaScript (Axios):**
```javascript
import axios from 'axios'

const actualizarCategoria = async (id, datos) => {
  try {
    const { data } = await axios.patch(`/api/egresos/categorias/${id}`, datos)
    return data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al actualizar')
  }
}

// Uso
const actualizada = await actualizarCategoria(1, { nombre: 'Nuevo Nombre' })
```

**React Hook:**
```javascript
import { useState } from 'react'
import axios from 'axios'

const useActualizarCategoria = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const actualizar = async (id, datos) => {
    setLoading(true)
    setError(null)

    try {
      const { data } = await axios.patch(`/api/egresos/categorias/${id}`, datos)
      setLoading(false)
      return data
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al actualizar')
      setLoading(false)
      throw err
    }
  }

  return { actualizar, loading, error }
}

// Uso en componente
function EditarCategoria({ categoriaId }) {
  const { actualizar, loading, error } = useActualizarCategoria()

  const handleActivarDesactivar = async (nuevoEstado) => {
    try {
      await actualizar(categoriaId, { estado: nuevoEstado })
      alert('Estado actualizado')
    } catch (err) {
      // Error ya manejado
    }
  }

  return (
    <div>
      {error && <div className="error">{error}</div>}
      <button
        onClick={() => handleActivarDesactivar('Inactiva')}
        disabled={loading}
      >
        Desactivar
      </button>
    </div>
  )
}
```

**Vue 3 Composition API:**
```javascript
import { ref } from 'vue'
import axios from 'axios'

export function useActualizarCategoria() {
  const loading = ref(false)
  const error = ref(null)

  const actualizar = async (id, datos) => {
    loading.value = true
    error.value = null

    try {
      const { data } = await axios.patch(`/api/egresos/categorias/${id}`, datos)
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al actualizar'
      throw err
    } finally {
      loading.value = false
    }
  }

  return { actualizar, loading, error }
}
```

---

## 5. Eliminar Categoría

Elimina permanentemente una categoría de egreso.

⚠️ **ADVERTENCIA**: Esta acción es irreversible. Asegúrate de que la categoría no tenga egresos asociados.

### Request

```http
DELETE /api/egresos/categorias/{categoria_id}
```

### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `categoria_id` | integer | ID de la categoría a eliminar |

### Response 204 No Content

Sin contenido en el cuerpo de la respuesta (eliminación exitosa).

### Response 404 Not Found

```json
{
  "detail": "Categoría no encontrada"
}
```

### Response 400 Bad Request

```json
{
  "detail": "No se pudo eliminar la categoría"
}
```

### Ejemplos

**JavaScript (Fetch):**
```javascript
const eliminarCategoria = async (id) => {
  const response = await fetch(`http://localhost:8000/api/egresos/categorias/${id}`, {
    method: 'DELETE'
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail)
  }

  // 204 No Content - no hay cuerpo de respuesta
  return true
}

// Uso con confirmación
const handleEliminar = async (id) => {
  if (!confirm('¿Estás seguro de eliminar esta categoría?')) {
    return
  }

  try {
    await eliminarCategoria(id)
    alert('Categoría eliminada exitosamente')
    // Recargar lista de categorías
  } catch (error) {
    alert(`Error: ${error.message}`)
  }
}
```

**JavaScript (Axios):**
```javascript
import axios from 'axios'

const eliminarCategoria = async (id) => {
  try {
    await axios.delete(`/api/egresos/categorias/${id}`)
    return true
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al eliminar')
  }
}
```

**React Hook:**
```javascript
import { useState } from 'react'
import axios from 'axios'

const useEliminarCategoria = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const eliminar = async (id) => {
    setLoading(true)
    setError(null)

    try {
      await axios.delete(`/api/egresos/categorias/${id}`)
      setLoading(false)
      return true
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al eliminar')
      setLoading(false)
      throw err
    }
  }

  return { eliminar, loading, error }
}

// Uso en componente
function ListaCategorias({ categorias, onCategoriaEliminada }) {
  const { eliminar, loading, error } = useEliminarCategoria()

  const handleEliminar = async (id) => {
    if (!window.confirm('¿Eliminar esta categoría?')) return

    try {
      await eliminar(id)
      onCategoriaEliminada(id)
      alert('Categoría eliminada')
    } catch (err) {
      // Error ya manejado
    }
  }

  return (
    <div>
      {error && <div className="error">{error}</div>}
      {categorias.map(cat => (
        <div key={cat.id}>
          <span>{cat.nombre}</span>
          <button
            onClick={() => handleEliminar(cat.id)}
            disabled={loading}
          >
            Eliminar
          </button>
        </div>
      ))}
    </div>
  )
}
```

---

## Ejemplos de Integración

### Servicio Completo de Categorías (JavaScript/TypeScript)

```typescript
// services/categoriaEgresoService.ts
import axios from 'axios'

const BASE_URL = '/api/egresos/categorias'

export interface CategoriaEgreso {
  id: number
  nombre: string
  descripcion: string | null
  estado: 'Activa' | 'Inactiva'
  fecha_creacion: string
}

export interface CrearCategoriaDTO {
  nombre: string
  descripcion?: string
}

export interface ActualizarCategoriaDTO {
  nombre?: string
  descripcion?: string
  estado?: 'Activa' | 'Inactiva'
}

class CategoriaEgresoService {
  async listar(estado?: 'Activa' | 'Inactiva'): Promise<CategoriaEgreso[]> {
    const { data } = await axios.get(BASE_URL, {
      params: estado ? { estado } : {}
    })
    return data
  }

  async crear(categoria: CrearCategoriaDTO): Promise<CategoriaEgreso> {
    const { data } = await axios.post(BASE_URL, categoria)
    return data
  }

  async obtenerPorId(id: number): Promise<CategoriaEgreso> {
    const { data } = await axios.get(`${BASE_URL}/${id}`)
    return data
  }

  async actualizar(id: number, categoria: ActualizarCategoriaDTO): Promise<CategoriaEgreso> {
    const { data } = await axios.patch(`${BASE_URL}/${id}`, categoria)
    return data
  }

  async eliminar(id: number): Promise<void> {
    await axios.delete(`${BASE_URL}/${id}`)
  }
}

export default new CategoriaEgresoService()
```

### Hook Completo de React

```javascript
// hooks/useCategorias.js
import { useState, useEffect } from 'react'
import categoriaService from '../services/categoriaEgresoService'

export const useCategorias = (estado = null) => {
  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const cargar = async () => {
    try {
      setLoading(true)
      const data = await categoriaService.listar(estado)
      setCategorias(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    cargar()
  }, [estado])

  const crear = async (categoria) => {
    const nueva = await categoriaService.crear(categoria)
    setCategorias([...categorias, nueva])
    return nueva
  }

  const actualizar = async (id, datos) => {
    const actualizada = await categoriaService.actualizar(id, datos)
    setCategorias(categorias.map(c => c.id === id ? actualizada : c))
    return actualizada
  }

  const eliminar = async (id) => {
    await categoriaService.eliminar(id)
    setCategorias(categorias.filter(c => c.id !== id))
  }

  return {
    categorias,
    loading,
    error,
    crear,
    actualizar,
    eliminar,
    recargar: cargar
  }
}
```

### Composable de Vue 3

```javascript
// composables/useCategorias.js
import { ref, onMounted } from 'vue'
import categoriaService from '../services/categoriaEgresoService'

export function useCategorias(estado = null) {
  const categorias = ref([])
  const loading = ref(true)
  const error = ref(null)

  const cargar = async () => {
    try {
      loading.value = true
      categorias.value = await categoriaService.listar(estado)
      error.value = null
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const crear = async (categoria) => {
    const nueva = await categoriaService.crear(categoria)
    categorias.value.push(nueva)
    return nueva
  }

  const actualizar = async (id, datos) => {
    const actualizada = await categoriaService.actualizar(id, datos)
    const index = categorias.value.findIndex(c => c.id === id)
    if (index !== -1) {
      categorias.value[index] = actualizada
    }
    return actualizada
  }

  const eliminar = async (id) => {
    await categoriaService.eliminar(id)
    categorias.value = categorias.value.filter(c => c.id !== id)
  }

  onMounted(() => {
    cargar()
  })

  return {
    categorias,
    loading,
    error,
    crear,
    actualizar,
    eliminar,
    recargar: cargar
  }
}
```

### Ejemplo de Componente React Completo

```javascript
// components/CategoriasManager.jsx
import React, { useState } from 'react'
import { useCategorias } from '../hooks/useCategorias'

export default function CategoriasManager() {
  const { categorias, loading, error, crear, actualizar, eliminar } = useCategorias()
  const [editando, setEditando] = useState(null)
  const [formulario, setFormulario] = useState({ nombre: '', descripcion: '' })

  const handleCrear = async (e) => {
    e.preventDefault()
    try {
      await crear(formulario)
      setFormulario({ nombre: '', descripcion: '' })
      alert('Categoría creada')
    } catch (err) {
      alert('Error al crear: ' + err.message)
    }
  }

  const handleActualizar = async (id) => {
    try {
      await actualizar(id, formulario)
      setEditando(null)
      setFormulario({ nombre: '', descripcion: '' })
      alert('Categoría actualizada')
    } catch (err) {
      alert('Error al actualizar: ' + err.message)
    }
  }

  const handleEliminar = async (id) => {
    if (!window.confirm('¿Eliminar?')) return
    try {
      await eliminar(id)
      alert('Categoría eliminada')
    } catch (err) {
      alert('Error al eliminar: ' + err.message)
    }
  }

  if (loading) return <div>Cargando...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <h2>Categorías de Egresos</h2>

      {/* Formulario */}
      <form onSubmit={handleCrear}>
        <input
          type="text"
          placeholder="Nombre"
          value={formulario.nombre}
          onChange={e => setFormulario({ ...formulario, nombre: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Descripción"
          value={formulario.descripcion}
          onChange={e => setFormulario({ ...formulario, descripcion: e.target.value })}
        />
        <button type="submit">Crear</button>
      </form>

      {/* Lista */}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {categorias.map(cat => (
            <tr key={cat.id}>
              <td>{cat.id}</td>
              <td>{cat.nombre}</td>
              <td>{cat.descripcion}</td>
              <td>{cat.estado}</td>
              <td>
                <button onClick={() => {
                  setEditando(cat.id)
                  setFormulario({ nombre: cat.nombre, descripcion: cat.descripcion })
                }}>
                  Editar
                </button>
                <button onClick={() => handleEliminar(cat.id)}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

---

## 📊 Resumen de Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/egresos/categorias` | Listar categorías | - |
| POST | `/api/egresos/categorias` | Crear categoría | - |
| GET | `/api/egresos/categorias/{id}` | Obtener por ID | - |
| PATCH | `/api/egresos/categorias/{id}` | Actualizar | - |
| DELETE | `/api/egresos/categorias/{id}` | Eliminar | - |

---

## 🔧 Configuración Base URL

```javascript
// config/api.js
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

// Configurar axios globalmente
import axios from 'axios'
axios.defaults.baseURL = API_BASE_URL
```

---

## 🎯 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa (GET, PATCH) |
| 201 | Created - Recurso creado exitosamente (POST) |
| 204 | No Content - Eliminación exitosa (DELETE) |
| 400 | Bad Request - Datos inválidos |
| 404 | Not Found - Categoría no encontrada |
| 500 | Internal Server Error - Error del servidor |

---

**Última actualización:** 2025-11-15
**Versión API:** 1.0.0
