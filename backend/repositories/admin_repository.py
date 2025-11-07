from typing import Optional, List, Dict, Any
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario con keys en minúsculas"""
    if row is None:
        return None
    # Normalizar todas las keys a minúsculas
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
    @staticmethod
    def verificar_usuario_existe(nombre_usuario: str, excluir_id: int = None) -> bool:
        """Verificar si un nombre de usuario ya existe"""
        with get_db() as conn:
            cursor = conn.cursor()
            if excluir_id:
                cursor.execute("""
                    SELECT COUNT(*) FROM ADMINISTRADOR 
                    WHERE Nombre_Usuario = ? AND Id != ?
                """, (nombre_usuario, excluir_id))
            else:
                cursor.execute("""
                    SELECT COUNT(*) FROM ADMINISTRADOR 
                    WHERE Nombre_Usuario = ?
                """, (nombre_usuario,))
            return cursor.fetchone()[0] > 0

    @staticmethod
    def create(admin_data: Dict[str, Any]) -> int:
        """Crear un nuevo administrador"""
        from datetime import datetime
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO ADMINISTRADOR (Nombre, Apellido, Nombre_Usuario, Password,
                                          Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (admin_data['nombre'], admin_data['apellido'], 
                  admin_data['nombre_usuario'], admin_data['password'],
                fecha_actual, admin_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update(admin_id: int, admin_data: Dict[str, Any]) -> bool:
        """Actualizar un administrador"""
        from datetime import datetime
        with get_db() as conn:
            cursor = conn.cursor()
            updates = []
            params = []
        
            if 'nombre' in admin_data and admin_data['nombre']:
                updates.append("Nombre = ?")
                params.append(admin_data['nombre'])
            if 'apellido' in admin_data and admin_data['apellido']:
                updates.append("Apellido = ?")
                params.append(admin_data['apellido'])
            if 'nombre_usuario' in admin_data and admin_data['nombre_usuario']:
                updates.append("Nombre_Usuario = ?")
                params.append(admin_data['nombre_usuario'])
            if 'password' in admin_data and admin_data['password']:
                updates.append("Password = ?")
                params.append(admin_data['password'])
            if 'estado' in admin_data:
                updates.append("estado = ?")
                params.append(admin_data['estado'])
        
            updates.append("Fecha_Modificacion = ?")
            params.append(datetime.now().isoformat())
            updates.append("Usuario_Modificacion = ?")
            params.append(admin_data.get('usuario_modificacion', 'admin'))
        
            params.append(admin_id)
        
            query = f"UPDATE ADMINISTRADOR SET {', '.join(updates)} WHERE Id = ?"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(admin_id: int) -> bool:
        """Eliminar (desactivar) un administrador"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE ADMINISTRADOR SET estado = 'Inactivo' 
                WHERE Id = ?
            """, (admin_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def listar(estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """Listar todos los administradores con filtro opcional"""
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM ADMINISTRADOR WHERE 1=1"
            params = []
        
            if estado:
                query += " AND estado = ?"
                params.append(estado)
        
            query += " ORDER BY Nombre"
            cursor.execute(query, params)
            return [dict_from_row(row) for row in cursor.fetchall()]
