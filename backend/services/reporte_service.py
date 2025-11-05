from typing import Dict, Any, List
from datetime import datetime, timedelta
from repositories.reporte_repository import ReporteRepository


class ReporteService:
    def __init__(self):
        self.repository = ReporteRepository()

    # ==================== REPORTES DE PAGOS ====================

    def obtener_reporte_pagos_dia(self, fecha: str = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por día"""
        if not fecha:
            fecha = datetime.now().date().isoformat()

        estadisticas = self.repository.get_estadisticas_pagos_dia(fecha)
        pagos = self.repository.get_pagos_por_dia(fecha)

        return {
            'fecha': fecha,
            **estadisticas,
            'detalle_pagos': pagos
        }

    def obtener_reporte_pagos_semana(self, fecha_inicio: str = None, fecha_fin: str = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por semana"""
        if not fecha_inicio:
            # Semana actual (Lunes a Domingo)
            hoy = datetime.now().date()
            dias_desde_lunes = hoy.weekday()
            fecha_inicio = (hoy - timedelta(days=dias_desde_lunes)).isoformat()
            fecha_fin = (hoy + timedelta(days=6-dias_desde_lunes)).isoformat()
        elif not fecha_fin:
            fecha_fin = (datetime.fromisoformat(fecha_inicio) +
                         timedelta(days=6)).date().isoformat()

        estadisticas = self.repository.get_estadisticas_pagos_semana(
            fecha_inicio, fecha_fin)
        pagos_por_dia = self.repository.get_pagos_por_semana(
            fecha_inicio, fecha_fin)

        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            **estadisticas,
            'pagos_por_dia': pagos_por_dia
        }

    def obtener_reporte_pagos_mes(self, mes: int = None, anio: int = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por mes"""
        if not mes or not anio:
            hoy = datetime.now()
            mes = hoy.month
            anio = hoy.year

        estadisticas = self.repository.get_estadisticas_pagos_mes(mes, anio)
        pagos_por_semana = self.repository.get_pagos_por_mes(mes, anio)

        meses_nombres = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        return {
            'mes': meses_nombres[mes-1],
            'mes_numero': mes,
            'anio': anio,
            **estadisticas,
            'pagos_por_semana': pagos_por_semana
        }

    def obtener_reporte_pagos_anio(self, anio: int = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por año"""
        if not anio:
            anio = datetime.now().year

        estadisticas = self.repository.get_estadisticas_pagos_anio(anio)
        pagos_por_mes = self.repository.get_pagos_por_anio(anio)

        meses_nombres = {
            "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
            "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
            "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
        }

        # Agregar nombres de meses
        for pago in pagos_por_mes:
            pago['nombre_mes'] = meses_nombres.get(pago['mes'], pago['mes'])

        return {
            'anio': anio,
            **estadisticas,
            'pagos_por_mes': pagos_por_mes
        }

    # ==================== REPORTES DE CLIENTES ====================

    def obtener_reporte_clientes(self) -> Dict[str, Any]:
        """Obtener reporte general de clientes"""
        estadisticas = self.repository.get_estadisticas_clientes()
        por_tipo = self.repository.get_clientes_por_tipo_membresia()

        return {
            **estadisticas,
            'distribucion_membresias': por_tipo
        }

    def obtener_clientes_nuevos(self, fecha_inicio: str = None, fecha_fin: str = None) -> Dict[str, Any]:
        """Obtener clientes nuevos en un período"""
        if not fecha_inicio:
            # Últimos 30 días
            fecha_fin = datetime.now().date().isoformat()
            fecha_inicio = (datetime.now().date() -
                            timedelta(days=30)).isoformat()
        elif not fecha_fin:
            fecha_fin = datetime.now().date().isoformat()

        clientes = self.repository.get_clientes_nuevos(fecha_inicio, fecha_fin)

        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total': len(clientes),
            'clientes': clientes
        }

    def obtener_clientes_membresia_vencida(self) -> Dict[str, Any]:
        """Obtener clientes con membresía vencida"""
        clientes = self.repository.get_clientes_membresia_vencida()

        return {
            'total': len(clientes),
            'clientes': clientes
        }

    def obtener_clientes_membresia_por_vencer(self, dias: int = 7) -> Dict[str, Any]:
        """Obtener clientes con membresía próxima a vencer"""
        clientes = self.repository.get_clientes_membresia_por_vencer(dias)

        return {
            'dias_anticipacion': dias,
            'total': len(clientes),
            'clientes': clientes
        }

    # ==================== REPORTES DE ASISTENCIAS ====================

    def obtener_reporte_asistencias(self, fecha_inicio: str = None, fecha_fin: str = None) -> Dict[str, Any]:
        """Obtener reporte de asistencias"""
        if not fecha_inicio:
            # Últimos 7 días
            fecha_fin = datetime.now().date().isoformat()
            fecha_inicio = (datetime.now().date() -
                            timedelta(days=7)).isoformat()
        elif not fecha_fin:
            fecha_fin = datetime.now().date().isoformat()

        estadisticas = self.repository.get_estadisticas_asistencias(
            fecha_inicio, fecha_fin)

        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            **estadisticas
        }
