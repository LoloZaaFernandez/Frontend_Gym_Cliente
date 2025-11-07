from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario con keys en minúsculas"""
    if row is None:
        return None
    return {k.lower(): row[k] for k in row.keys()}


class ReporteRepository:

    # ==================== REPORTES DE PAGOS ====================

    @staticmethod
    def get_pagos_por_dia(fecha: str) -> List[Dict[str, Any]]:
        """Obtener todos los pagos de un día específico"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pm.*, c.NOMBRE, c.APELLIDOS, m.Nombre_Membresia, m.tipo_membresia
                FROM PAGO_MEMBRESIA pm
                JOIN CLIENTE c ON pm.Id_Cliente = c.Id
                JOIN MEMBRESIA m ON pm.Id_Membresia = m.Id
                WHERE DATE(pm.Fecha_Pago) = DATE(?)
                ORDER BY pm.Fecha_Pago DESC
            """, (fecha,))
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_estadisticas_pagos_dia(fecha: str) -> Dict[str, Any]:
        """Obtener estadísticas de pagos por día"""
        with get_db() as conn:
            cursor = conn.cursor()

            # Total y monto
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_pagos,
                    COALESCE(SUM(Monto), 0) as monto_total
                FROM PAGO_MEMBRESIA
                WHERE DATE(Fecha_Pago) = DATE(?)
            """, (fecha,))
            row = cursor.fetchone()

            # Métodos de pago
            cursor.execute("""
                SELECT Metodo_Pago, COUNT(*) as cantidad, SUM(Monto) as monto
                FROM PAGO_MEMBRESIA
                WHERE DATE(Fecha_Pago) = DATE(?)
                GROUP BY Metodo_Pago
            """, (fecha,))
            metodos = {row[0]: {'cantidad': row[1], 'monto': row[2]}
                       for row in cursor.fetchall()}

            return {
                'total_pagos': row[0],
                'monto_total': row[1],
                'metodos_pago': metodos
            }

    @staticmethod
    def get_pagos_por_semana(fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """Obtener pagos de una semana"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    DATE(Fecha_Pago) as fecha,
                    COUNT(*) as total_pagos,
                    SUM(Monto) as monto_total
                FROM PAGO_MEMBRESIA
                WHERE DATE(Fecha_Pago) BETWEEN DATE(?) AND DATE(?)
                GROUP BY DATE(Fecha_Pago)
                ORDER BY fecha
            """, (fecha_inicio, fecha_fin))
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_estadisticas_pagos_semana(fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
        """Obtener estadísticas de pagos por semana"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_pagos,
                    COALESCE(SUM(Monto), 0) as monto_total
                FROM PAGO_MEMBRESIA
                WHERE DATE(Fecha_Pago) BETWEEN DATE(?) AND DATE(?)
            """, (fecha_inicio, fecha_fin))
            row = cursor.fetchone()

            return {
                'total_pagos': row[0],
                'monto_total': row[1]
            }

    @staticmethod
    def get_pagos_por_mes(mes: int, anio: int) -> List[Dict[str, Any]]:
        """Obtener pagos de un mes específico agrupados por semana"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    strftime('%W', Fecha_Pago) as semana,
                    COUNT(*) as total_pagos,
                    SUM(Monto) as monto_total,
                    MIN(DATE(Fecha_Pago)) as fecha_inicio,
                    MAX(DATE(Fecha_Pago)) as fecha_fin
                FROM PAGO_MEMBRESIA
                WHERE strftime('%m', Fecha_Pago) = ? 
                  AND strftime('%Y', Fecha_Pago) = ?
                GROUP BY semana
                ORDER BY semana
            """, (f'{mes:02d}', str(anio)))
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_estadisticas_pagos_mes(mes: int, anio: int) -> Dict[str, Any]:
        """Obtener estadísticas de pagos por mes"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_pagos,
                    COALESCE(SUM(Monto), 0) as monto_total
                FROM PAGO_MEMBRESIA
                WHERE strftime('%m', Fecha_Pago) = ? 
                  AND strftime('%Y', Fecha_Pago) = ?
            """, (f'{mes:02d}', str(anio)))
            row = cursor.fetchone()

            return {
                'total_pagos': row[0],
                'monto_total': row[1]
            }

    @staticmethod
    def get_pagos_por_anio(anio: int) -> List[Dict[str, Any]]:
        """Obtener pagos de un año agrupados por mes"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    strftime('%m', Fecha_Pago) as mes,
                    COUNT(*) as total_pagos,
                    SUM(Monto) as monto_total
                FROM PAGO_MEMBRESIA
                WHERE strftime('%Y', Fecha_Pago) = ?
                GROUP BY mes
                ORDER BY mes
            """, (str(anio),))
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_estadisticas_pagos_anio(anio: int) -> Dict[str, Any]:
        """Obtener estadísticas de pagos por año"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_pagos,
                    COALESCE(SUM(Monto), 0) as monto_total
                FROM PAGO_MEMBRESIA
                WHERE strftime('%Y', Fecha_Pago) = ?
            """, (str(anio),))
            row = cursor.fetchone()

            return {
                'total_pagos': row[0],
                'monto_total': row[1]
            }

    # ==================== REPORTES DE CLIENTES ====================

    @staticmethod
    def get_estadisticas_clientes() -> Dict[str, Any]:
        """Obtener estadísticas generales de clientes"""
        with get_db() as conn:
            cursor = conn.cursor()

            # Total de clientes
            cursor.execute("SELECT COUNT(*) FROM CLIENTE")
            total_clientes = cursor.fetchone()[0]

            # Clientes activos
            cursor.execute(
                "SELECT COUNT(*) FROM CLIENTE WHERE Estado = 'Activo'")
            clientes_activos = cursor.fetchone()[0]

            # Clientes inactivos
            cursor.execute(
                "SELECT COUNT(*) FROM CLIENTE WHERE Estado = 'Inactivo'")
            clientes_inactivos = cursor.fetchone()[0]

            # Membresías activas (vigentes)
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM CLIENTE 
                WHERE FECHA_MEMBRESIA IS NOT NULL 
                  AND FECHA_MEMBRESIA >= ?
                  AND Estado = 'Activo'
            """, (fecha_actual,))
            membresias_activas = cursor.fetchone()[0]

            # Membresías vencidas
            cursor.execute("""
                SELECT COUNT(*) 
                FROM CLIENTE 
                WHERE FECHA_MEMBRESIA IS NOT NULL 
                  AND FECHA_MEMBRESIA < ?
                  AND Estado = 'Activo'
            """, (fecha_actual,))
            membresias_vencidas = cursor.fetchone()[0]

            # Membresías por vencer (próximos 7 días)
            fecha_limite = (datetime.now() + timedelta(days=7)).isoformat()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM CLIENTE 
                WHERE FECHA_MEMBRESIA IS NOT NULL 
                  AND FECHA_MEMBRESIA BETWEEN ? AND ?
                  AND Estado = 'Activo'
            """, (fecha_actual, fecha_limite))
            membresias_por_vencer = cursor.fetchone()[0]

            # Clientes sin membresía
            cursor.execute("""
                SELECT COUNT(*) 
                FROM CLIENTE 
                WHERE FECHA_MEMBRESIA IS NULL 
                  AND Estado = 'Activo'
            """)
            clientes_sin_membresia = cursor.fetchone()[0]

            return {
                'total_clientes': total_clientes,
                'clientes_activos': clientes_activos,
                'clientes_inactivos': clientes_inactivos,
                'membresias_activas': membresias_activas,
                'membresias_vencidas': membresias_vencidas,
                'membresias_por_vencer': membresias_por_vencer,
                'clientes_sin_membresia': clientes_sin_membresia
            }

    @staticmethod
    def get_clientes_por_tipo_membresia() -> List[Dict[str, Any]]:
        """Obtener distribución de clientes por tipo de membresía"""
        with get_db() as conn:
            cursor = conn.cursor()

            # Total de clientes con membresía activa
            cursor.execute("""
                SELECT COUNT(*) 
                FROM CLIENTE c
                WHERE c.FECHA_MEMBRESIA IS NOT NULL 
                  AND c.FECHA_MEMBRESIA >= ?
                  AND c.Estado = 'Activo'
            """, (datetime.now().isoformat(),))
            total = cursor.fetchone()[0]

            # Clientes por tipo de membresía
            cursor.execute("""
                SELECT 
                    m.tipo_membresia,
                    COUNT(*) as cantidad
                FROM CLIENTE c
                JOIN PAGO_MEMBRESIA pm ON c.Id = pm.Id_Cliente
                JOIN MEMBRESIA m ON pm.Id_Membresia = m.Id
                WHERE c.FECHA_MEMBRESIA IS NOT NULL 
                  AND c.FECHA_MEMBRESIA >= ?
                  AND c.Estado = 'Activo'
                  AND pm.Id = (
                      SELECT Id 
                      FROM PAGO_MEMBRESIA 
                      WHERE Id_Cliente = c.Id 
                      ORDER BY Fecha_Pago DESC 
                      LIMIT 1
                  )
                GROUP BY m.tipo_membresia
                ORDER BY cantidad DESC
            """, (datetime.now().isoformat(),))

            resultado = []
            for row in cursor.fetchall():
                tipo_membresia, cantidad = row
                porcentaje = (cantidad / total * 100) if total > 0 else 0
                resultado.append({
                    'tipo_membresia': tipo_membresia,
                    'cantidad': cantidad,
                    'porcentaje': round(porcentaje, 2)
                })

            return resultado

    @staticmethod
    def get_clientes_nuevos(fecha_inicio: str, fecha_fin: str) -> List[Dict[str, Any]]:
        """Obtener clientes nuevos en un rango de fechas"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM CLIENTE
                WHERE DATE(FECHA_REGISTRO) BETWEEN DATE(?) AND DATE(?)
                ORDER BY FECHA_REGISTRO DESC
            """, (fecha_inicio, fecha_fin))
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_clientes_membresia_vencida() -> List[Dict[str, Any]]:
        """Obtener clientes con membresía vencida"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, m.tipo_membresia
                FROM CLIENTE c
                LEFT JOIN PAGO_MEMBRESIA pm ON c.Id = pm.Id_Cliente
                LEFT JOIN MEMBRESIA m ON pm.Id_Membresia = m.Id
                WHERE c.FECHA_MEMBRESIA IS NOT NULL 
                  AND c.FECHA_MEMBRESIA < ?
                  AND c.Estado = 'Activo'
                  AND pm.Id = (
                      SELECT Id 
                      FROM PAGO_MEMBRESIA 
                      WHERE Id_Cliente = c.Id 
                      ORDER BY Fecha_Pago DESC 
                      LIMIT 1
                  )
                ORDER BY c.FECHA_MEMBRESIA DESC
            """, (datetime.now().isoformat(),))
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_clientes_membresia_por_vencer(dias: int = 7) -> List[Dict[str, Any]]:
        """Obtener clientes con membresía próxima a vencer"""
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            fecha_limite = (datetime.now() + timedelta(days=dias)).isoformat()

            cursor.execute("""
                SELECT c.*, m.tipo_membresia
                FROM CLIENTE c
                LEFT JOIN PAGO_MEMBRESIA pm ON c.Id = pm.Id_Cliente
                LEFT JOIN MEMBRESIA m ON pm.Id_Membresia = m.Id
                WHERE c.FECHA_MEMBRESIA BETWEEN ? AND ?
                  AND c.Estado = 'Activo'
                  AND pm.Id = (
                      SELECT Id 
                      FROM PAGO_MEMBRESIA 
                      WHERE Id_Cliente = c.Id 
                      ORDER BY Fecha_Pago DESC 
                      LIMIT 1
                  )
                ORDER BY c.FECHA_MEMBRESIA ASC
            """, (fecha_actual, fecha_limite))
            return [dict_from_row(row) for row in cursor.fetchall()]

    # ==================== REPORTES DE ASISTENCIAS ====================

    @staticmethod
    def get_estadisticas_asistencias(fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
        """Obtener estadísticas de asistencias en un rango de fechas"""
        with get_db() as conn:
            cursor = conn.cursor()

            # Total de asistencias
            cursor.execute("""
                SELECT COUNT(*) 
                FROM ASISTENCIA
                WHERE Fecha_Asistencia BETWEEN DATE(?) AND DATE(?)
            """, (fecha_inicio, fecha_fin))
            total_asistencias = cursor.fetchone()[0]

            # Asistencias por día
            cursor.execute("""
                SELECT 
                    Fecha_Asistencia as fecha,
                    COUNT(*) as total
                FROM ASISTENCIA
                WHERE Fecha_Asistencia BETWEEN DATE(?) AND DATE(?)
                GROUP BY Fecha_Asistencia
                ORDER BY Fecha_Asistencia
            """, (fecha_inicio, fecha_fin))
            asistencias_por_dia = [dict_from_row(
                row) for row in cursor.fetchall()]

            # Clientes más frecuentes
            cursor.execute("""
                SELECT 
                    Nombre_Cliente,
                    COUNT(*) as total_asistencias,
                    Tipo_Membresia
                FROM ASISTENCIA
                WHERE Fecha_Asistencia BETWEEN DATE(?) AND DATE(?)
                GROUP BY Id_Cliente
                ORDER BY total_asistencias DESC
                LIMIT 10
            """, (fecha_inicio, fecha_fin))
            clientes_frecuentes = [dict_from_row(
                row) for row in cursor.fetchall()]

            return {
                'total_asistencias': total_asistencias,
                'asistencias_por_dia': asistencias_por_dia,
                'clientes_mas_frecuentes': clientes_frecuentes
            }
