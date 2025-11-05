import sqlite3
from contextlib import contextmanager
from fastapi import APIRouter, Query
from typing import Optional
from services.reporte_service import ReporteService

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])
service = ReporteService()

# ==================== REPORTES DE PAGOS ====================


@router.get("/pagos/dia")
def reporte_pagos_dia(fecha: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD")):
    """
    Obtener reporte de pagos por día
    - Si no se envía fecha, se usa la fecha actual
    """
    return service.obtener_reporte_pagos_dia(fecha)


@router.get("/pagos/semana")
def reporte_pagos_semana(
    fecha_inicio: Optional[str] = Query(
        None, description="Fecha inicio en formato YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(
        None, description="Fecha fin en formato YYYY-MM-DD")
):
    """
    Obtener reporte de pagos por semana
    - Si no se envían fechas, se usa la semana actual (Lunes a Domingo)
    """
    return service.obtener_reporte_pagos_semana(fecha_inicio, fecha_fin)


@router.get("/pagos/mes")
def reporte_pagos_mes(
    mes: Optional[int] = Query(None, ge=1, le=12, description="Mes (1-12)"),
    anio: Optional[int] = Query(None, ge=2000, description="Año")
):
    """
    Obtener reporte de pagos por mes
    - Si no se envían parámetros, se usa el mes y año actual
    """
    return service.obtener_reporte_pagos_mes(mes, anio)


@router.get("/pagos/anio")
def reporte_pagos_anio(
    anio: Optional[int] = Query(None, ge=2000, description="Año")
):
    """
    Obtener reporte de pagos por año
    - Si no se envía año, se usa el año actual
    """
    return service.obtener_reporte_pagos_anio(anio)

# ==================== REPORTES DE CLIENTES ====================


@router.get("/clientes/general")
def reporte_clientes_general():
    """
    Obtener reporte general de clientes
    - Total de clientes
    - Clientes activos e inactivos
    - Membresías activas, vencidas y por vencer
    - Distribución por tipo de membresía
    """
    return service.obtener_reporte_clientes()


@router.get("/clientes/nuevos")
def reporte_clientes_nuevos(
    fecha_inicio: Optional[str] = Query(
        None, description="Fecha inicio en formato YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(
        None, description="Fecha fin en formato YYYY-MM-DD")
):
    """
    Obtener clientes nuevos en un período
    - Si no se envían fechas, se usan los últimos 30 días
    """
    return service.obtener_clientes_nuevos(fecha_inicio, fecha_fin)


@router.get("/clientes/membresia-vencida")
def reporte_clientes_membresia_vencida():
    """
    Obtener clientes con membresía vencida
    """
    return service.obtener_clientes_membresia_vencida()


@router.get("/clientes/membresia-por-vencer")
def reporte_clientes_membresia_por_vencer(
    dias: int = Query(7, ge=1, le=30, description="Días de anticipación")
):
    """
    Obtener clientes con membresía próxima a vencer
    - Por defecto: próximos 7 días
    """
    return service.obtener_clientes_membresia_por_vencer(dias)

# ==================== REPORTES DE ASISTENCIAS ====================


@router.get("/asistencias")
def reporte_asistencias(
    fecha_inicio: Optional[str] = Query(
        None, description="Fecha inicio en formato YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(
        None, description="Fecha fin en formato YYYY-MM-DD")
):
    """
    Obtener reporte de asistencias
    - Total de asistencias en el período
    - Asistencias por día
    - Clientes más frecuentes (top 10)
    - Si no se envían fechas, se usan los últimos 7 días
    """
    return service.obtener_reporte_asistencias(fecha_inicio, fecha_fin)  # ==================== app/database.py ====================


DATABASE_PATH = 'gimnasio.db'


@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
