from typing import List, Optional, Dict, Any
from datetime import datetime
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario con keys en minúsculas"""
    if row is None:
        return None
    # Normalizar todas las keys a minúsculas
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
    def update(membresia_id: int, membresia_data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            # Construir la consulta dinámicamente basada en los campos proporcionados
            campos = []
            valores = []

            if 'nombre_membresia' in membresia_data and membresia_data['nombre_membresia'] is not None:
                campos.append("Nombre_Membresia = ?")
                valores.append(membresia_data['nombre_membresia'])

            if 'tipo_membresia' in membresia_data and membresia_data['tipo_membresia'] is not None:
                campos.append("tipo_membresia = ?")
                valores.append(membresia_data['tipo_membresia'])

            if 'estado' in membresia_data and membresia_data['estado'] is not None:
                campos.append("Estado = ?")
                valores.append(membresia_data['estado'])

            # Siempre actualizar fecha y usuario de modificación
            campos.append("Fecha_Modificacion = ?")
            valores.append(fecha_actual)

            campos.append("Usuario_Modificacion = ?")
            valores.append(membresia_data.get('usuario_modificacion', 'admin'))

            if not campos:
                return False

            # Agregar el ID al final de los valores
            valores.append(membresia_id)

            query = f"UPDATE MEMBRESIA SET {', '.join(campos)} WHERE Id = ?"
            cursor.execute(query, valores)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(membresia_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM MEMBRESIA WHERE Id = ?", (membresia_id,))
            conn.commit()
            return cursor.rowcount > 0

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