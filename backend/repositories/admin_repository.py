from typing import Optional, List, Dict, Any
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario"""
    if row is None:
        return None
    return {k.lower(): row[k] for k in row.keys()}


class AdminRepository:
    """Repositorio para gestión de administradores"""

    @staticmethod
    def get_por_credenciales(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Obtener administrador por credenciales"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM ADMINISTRADOR
                WHERE Nombre_Usuario = ? AND Password = ? AND estado = 'Activo'
            """, (username, password))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def get_por_id(admin_id: int) -> Optional[Dict[str, Any]]:
        """Obtener administrador por ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ADMINISTRADOR WHERE Id = ?", (admin_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def listar() -> List[Dict[str, Any]]:
        """Listar todos los administradores"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ADMINISTRADOR ORDER BY Nombre")
            return [dict_from_row(row) for row in cursor.fetchall()]
