from pydantic import BaseModel
from typing import List, Optional


class ReportePagosDia(BaseModel):
    fecha: str
    total_pagos: int
    monto_total: float
    metodos_pago: dict


class ReportePagosSemana(BaseModel):
    fecha_inicio: str
    fecha_fin: str
    total_pagos: int
    monto_total: float
    pagos_por_dia: List[dict]


class ReportePagosMes(BaseModel):
    mes: str
    anio: int
    total_pagos: int
    monto_total: float
    pagos_por_semana: List[dict]


class ReportePagosAnio(BaseModel):
    anio: int
    total_pagos: int
    monto_total: float
    pagos_por_mes: List[dict]


class ReporteClientes(BaseModel):
    total_clientes: int
    clientes_activos: int
    clientes_inactivos: int
    membresias_activas: int
    membresias_vencidas: int
    membresias_por_vencer: int
    clientes_sin_membresia: int


class ReporteClientesPorMembresia(BaseModel):
    tipo_membresia: str
    cantidad: int
    porcentaje: float


class ReporteAsistencias(BaseModel):
    fecha_inicio: str
    fecha_fin: str
    total_asistencias: int
    asistencias_por_dia: List[dict]
    clientes_mas_frecuentes: List[dict]
