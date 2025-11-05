from typing import List, Optional, Dict, Any
from datetime import datetime
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario con keys en minúsculas"""
    if row is None:
        return None
    return {k.lower(): row[k] for k in row.keys()}


class AsistenciaRepository:
    @staticmethod
    def create(asistencia_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now()
            cursor.execute("""
                INSERT INTO ASISTENCIA (Id_Cliente, Nombre_Cliente, Tipo_Membresia, 
                                       Fecha_Asistencia, Hora_Ingreso, Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (asistencia_data['id_cliente'], asistencia_data['nombre_cliente'],
                  asistencia_data['tipo_membresia'], fecha_actual.date(
            ).isoformat(),
                fecha_actual.time().isoformat(), fecha_actual.isoformat(),
                asistencia_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def find_by_id(asistencia_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM ASISTENCIA WHERE Id = ?", (asistencia_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def find_all(fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None,
                 cliente_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM ASISTENCIA WHERE 1=1"
            params = []

            if fecha_inicio:
                query += " AND Fecha_Asistencia >= ?"
                params.append(fecha_inicio)
            if fecha_fin:
                query += " AND Fecha_Asistencia <= ?"
                params.append(fecha_fin)
            if cliente_id:
                query += " AND Id_Cliente = ?"
                params.append(cliente_id)

            query += " ORDER BY Fecha_Asistencia DESC, Hora_Ingreso DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            cursor.execute(query, params)
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_cliente_info_by_dni(dni: str) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.Id, c.NOMBRE, c.APELLIDOS, c.FECHA_MEMBRESIA, c.Estado,
                       m.tipo_membresia
                FROM CLIENTE c
                LEFT JOIN PAGO_MEMBRESIA pm ON c.Id = pm.Id_Cliente
                LEFT JOIN MEMBRESIA m ON pm.Id_Membresia = m.Id
                WHERE c.DNI = ?
                ORDER BY pm.Fecha_Pago DESC LIMIT 1
            """, (dni,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def get_cliente_info(cliente_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.Id, c.NOMBRE, c.APELLIDOS, c.FECHA_MEMBRESIA, c.Estado,
                       m.tipo_membresia
                FROM CLIENTE c
                LEFT JOIN PAGO_MEMBRESIA pm ON c.Id = pm.Id_Cliente
                LEFT JOIN MEMBRESIA m ON pm.Id_Membresia = m.Id
                WHERE c.Id = ?
                ORDER BY pm.Fecha_Pago DESC LIMIT 1
            """, (cliente_id,))
            row = cursor.fetchone()
            return dict_from_row(row)
