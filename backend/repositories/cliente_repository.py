from typing import List, Optional, Dict, Any
from datetime import datetime
import sqlite3
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario con keys en minúsculas"""
    if row is None:
        return None
    return {k.lower(): row[k] for k in row.keys()}


class ClienteRepository:
    @staticmethod
    def create(cliente_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO CLIENTE (DNI, NOMBRE, APELLIDOS, CORREO, TELEFONO, 
                                   FECHA_REGISTRO, Usuario_Creacion, Fecha_Creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (cliente_data['dni'], cliente_data['nombre'], cliente_data['apellidos'],
                  cliente_data['correo'], cliente_data.get('telefono'),
                  fecha_actual, cliente_data.get('usuario_creacion', 'admin'), fecha_actual))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def find_by_id(cliente_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLIENTE WHERE Id = ?", (cliente_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def find_by_dni(dni: str) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLIENTE WHERE DNI = ?", (dni,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def find_all(estado: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM CLIENTE WHERE 1=1"
            params = []

            if estado:
                query += " AND Estado = ?"
                params.append(estado)

            query += " ORDER BY Id DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            cursor.execute(query, params)
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def update(cliente_id: int, cliente_data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if 'nombre' in cliente_data and cliente_data['nombre']:
                updates.append("NOMBRE = ?")
                params.append(cliente_data['nombre'])
            if 'apellidos' in cliente_data and cliente_data['apellidos']:
                updates.append("APELLIDOS = ?")
                params.append(cliente_data['apellidos'])
            if 'correo' in cliente_data and cliente_data['correo']:
                updates.append("CORREO = ?")
                params.append(cliente_data['correo'])
            if 'telefono' in cliente_data:
                updates.append("TELEFONO = ?")
                params.append(cliente_data['telefono'])
            if 'estado' in cliente_data:
                updates.append("Estado = ?")
                params.append(cliente_data['estado'])
            if 'fecha_membresia' in cliente_data:
                updates.append("FECHA_MEMBRESIA = ?")
                params.append(cliente_data['fecha_membresia'])
            if 'id_membresia' in cliente_data:
                updates.append("Id_Membresia = ?")
                params.append(cliente_data['id_membresia'])

            updates.append("Fecha_Modificacion = ?")
            params.append(datetime.now().isoformat())
            updates.append("Usuario_Modificacion = ?")
            params.append(cliente_data.get('usuario_modificacion', 'admin'))
            updates.append("row_version = row_version + 1")

            params.append(cliente_id)

            query = f"UPDATE CLIENTE SET {', '.join(updates)} WHERE Id = ?"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(cliente_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE CLIENTE SET Estado = 'Inactivo' WHERE Id = ?", (cliente_id,))
            conn.commit()
            return cursor.rowcount > 0
