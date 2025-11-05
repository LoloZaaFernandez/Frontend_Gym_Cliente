from typing import List, Optional, Dict, Any
from datetime import datetime
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario con keys en minúsculas"""
    if row is None:
        return None
    return {k.lower(): row[k] for k in row.keys()}


class MembresiaRepository:
    @staticmethod
    def create(membresia_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO MEMBRESIA (Nombre_Membresia, tipo_membresia, Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?)
            """, (membresia_data['nombre_membresia'], membresia_data['tipo_membresia'],
                  fecha_actual, membresia_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def find_by_id(membresia_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM MEMBRESIA WHERE Id = ?", (membresia_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def find_all(estado: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM MEMBRESIA WHERE 1=1"
            params = []

            if estado:
                query += " AND Estado = ?"
                params.append(estado)

            cursor.execute(query, params)
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def create_precio(precio_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO PRECIO_MEMBRESIA (Id_Membresia, Precio_Anterior, Precio_Actual, 
                                             Fecha_Inicio_Vigencia, Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (precio_data['id_membresia'], precio_data.get('precio_anterior'),
                  precio_data['precio_actual'], fecha_actual, fecha_actual,
                  precio_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_precio_vigente(membresia_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM PRECIO_MEMBRESIA 
                WHERE Id_Membresia = ? AND Estado = 'Activo'
                ORDER BY Fecha_Inicio_Vigencia DESC LIMIT 1
            """, (membresia_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def create_pago(pago_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO PAGO_MEMBRESIA (Id_Cliente, Id_Membresia, Monto, Metodo_Pago, 
                                           Fecha_Pago, Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (pago_data['id_cliente'], pago_data['id_membresia'], pago_data['monto'],
                  pago_data['metodo_pago'], fecha_actual, fecha_actual,
                  pago_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def find_pago_by_id(pago_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM PAGO_MEMBRESIA WHERE Id = ?", (pago_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def find_pagos_by_cliente(cliente_id: int) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM PAGO_MEMBRESIA 
                WHERE Id_Cliente = ? 
                ORDER BY Fecha_Pago DESC
            """, (cliente_id,))
            return [dict_from_row(row) for row in cursor.fetchall()]
