from typing import List, Optional, Dict, Any
from datetime import datetime
from database import get_db


def dict_from_row(row) -> Dict[str, Any]:
    """Convertir Row de sqlite3 a diccionario con keys en minúsculas"""
    if row is None:
        return None
    # Normalizar todas las keys a minúsculas
    return {k.lower(): row[k] for k in row.keys()}


class ProductoRepository:
    @staticmethod
    def create_categoria(categoria_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO CATEGORIA (Nombre, Descripcion, Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?)
            """, (categoria_data['nombre'], categoria_data.get('descripcion'),
                  fecha_actual, categoria_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def find_categorias(estado: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM CATEGORIA WHERE 1=1"
            params = []

            if estado:
                query += " AND Estado = ?"
                params.append(estado)

            cursor.execute(query, params)
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def find_categoria_by_id(categoria_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CATEGORIA WHERE Id = ?", (categoria_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def update_categoria(categoria_id: int, categoria_data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            campos = []
            valores = []

            if 'nombre' in categoria_data and categoria_data['nombre'] is not None:
                campos.append("Nombre = ?")
                valores.append(categoria_data['nombre'])

            if 'descripcion' in categoria_data:
                campos.append("Descripcion = ?")
                valores.append(categoria_data['descripcion'])

            if 'estado' in categoria_data and categoria_data['estado'] is not None:
                campos.append("Estado = ?")
                valores.append(categoria_data['estado'])

            # Siempre actualizar fecha y usuario de modificación
            campos.append("Fecha_Modificacion = ?")
            valores.append(fecha_actual)

            campos.append("Usuario_Modificacion = ?")
            valores.append(categoria_data.get('usuario_modificacion', 'admin'))

            if not campos:
                return False

            valores.append(categoria_id)

            query = f"UPDATE CATEGORIA SET {', '.join(campos)} WHERE Id = ?"
            cursor.execute(query, valores)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_categoria(categoria_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CATEGORIA WHERE Id = ?", (categoria_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def create(producto_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO PRODUCTOS (Nombre, Descripcion, Id_Categoria, Fecha_vencimiento, 
                                      Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto_data['nombre'], producto_data.get('descripcion'),
                  producto_data['id_categoria'], producto_data.get(
                      'fecha_vencimiento'),
                  fecha_actual, producto_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def find_by_id(producto_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM PRODUCTOS WHERE Id = ?", (producto_id,))
            row = cursor.fetchone()
            return dict_from_row(row)

    @staticmethod
    def find_all(categoria_id: Optional[int] = None, estado: Optional[str] = None,
                 skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM PRODUCTOS WHERE 1=1"
            params = []

            if categoria_id:
                query += " AND Id_Categoria = ?"
                params.append(categoria_id)
            if estado:
                query += " AND Estado = ?"
                params.append(estado)

            query += " ORDER BY Id DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            cursor.execute(query, params)
            return [dict_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def update(producto_id: int, producto_data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if 'nombre' in producto_data and producto_data['nombre']:
                updates.append("Nombre = ?")
                params.append(producto_data['nombre'])
            if 'descripcion' in producto_data:
                updates.append("Descripcion = ?")
                params.append(producto_data['descripcion'])
            if 'id_categoria' in producto_data:
                updates.append("Id_Categoria = ?")
                params.append(producto_data['id_categoria'])
            if 'fecha_vencimiento' in producto_data:
                updates.append("Fecha_vencimiento = ?")
                params.append(producto_data['fecha_vencimiento'])
            if 'estado' in producto_data:
                updates.append("Estado = ?")
                params.append(producto_data['estado'])

            updates.append("Fecha_Modificacion = ?")
            params.append(datetime.now().isoformat())
            updates.append("Usuario_Modificacion = ?")
            params.append(producto_data.get('usuario_modificacion', 'admin'))

            params.append(producto_id)

            query = f"UPDATE PRODUCTOS SET {', '.join(updates)} WHERE Id = ?"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(producto_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PRODUCTOS WHERE Id = ?", (producto_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def create_movimiento_inventario(movimiento_data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO INVENTARIO (Id_Producto, Nombre_Producto, Tipo_movimiento, Motivo,
                                       Cantidad, Stock_Anterior, Stock_Actual, Fecha_Creacion, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (movimiento_data['id_producto'], movimiento_data['nombre_producto'],
                  movimiento_data['tipo_movimiento'], movimiento_data.get(
                      'motivo'),
                  movimiento_data['cantidad'], movimiento_data['stock_anterior'],
                  movimiento_data['stock_actual'], fecha_actual,
                  movimiento_data.get('usuario_creacion', 'admin')))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_stock_actual(producto_id: int) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Stock_Actual FROM INVENTARIO 
                WHERE Id_Producto = ? 
                ORDER BY Id DESC LIMIT 1
            """, (producto_id,))
            row = cursor.fetchone()
            return row[0] if row else 0

    @staticmethod
    def find_movimientos_inventario(producto_id: Optional[int] = None,
                                    tipo_movimiento: Optional[str] = None,
                                    skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM INVENTARIO WHERE 1=1"
            params = []

            if producto_id:
                query += " AND Id_Producto = ?"
                params.append(producto_id)
            if tipo_movimiento:
                query += " AND Tipo_movimiento = ?"
                params.append(tipo_movimiento)

            query += " ORDER BY Fecha_Creacion DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            cursor.execute(query, params)
            return [dict_from_row(row) for row in cursor.fetchall()]