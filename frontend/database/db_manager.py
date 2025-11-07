"""
Gestor de base de datos local
Este módulo maneja todas las operaciones de base de datos SQLite
En el futuro, puede ser reemplazado o complementado con llamadas al backend
"""

import sqlite3
from typing import Optional, List, Dict, Any
from config.settings import DB_NAME


class DatabaseManager:
    """Administrador de la base de datos local"""

    def __init__(self):
        self.db_name = DB_NAME
        self.crear_tablas_si_no_existen()
        self.insertar_datos_iniciales()

    def get_connection(self) -> sqlite3.Connection:
        """Obtener conexión a la base de datos"""
        return sqlite3.connect(self.db_name)

    def crear_tablas_si_no_existen(self):
        """Crear las tablas necesarias si no existen"""
        conn = self.get_connection()
        cursor = conn.cursor()

        script_sql = """
        -- Tabla CLIENTE
        CREATE TABLE IF NOT EXISTS CLIENTE (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            DNI TEXT NOT NULL UNIQUE,
            NOMBRE TEXT NOT NULL,
            APELLIDOS TEXT NOT NULL,
            CORREO TEXT NOT NULL UNIQUE,
            TELEFONO TEXT,
            FECHA_REGISTRO TEXT NOT NULL,
            FECHA_MEMBRESIA TEXT,
            Estado TEXT CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
            Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
            Usuario_Creacion TEXT,
            Usuario_Modificacion TEXT,
            row_version INTEGER DEFAULT 1
        );

        -- Tabla MEMBRESIA
        CREATE TABLE IF NOT EXISTS MEMBRESIA (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre_Membresia TEXT NOT NULL,
            tipo_membresia TEXT NOT NULL,
            Estado TEXT CHECK(Estado IN ('Activa', 'Inactiva')) DEFAULT 'Activa',
            Fecha_Creacion TEXT NOT NULL,
            Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
            Usuario_Creacion TEXT,
            Usuario_Modificacion TEXT,
            row_version INTEGER DEFAULT 1
        );

        -- Tabla ADMINISTRADOR
        CREATE TABLE IF NOT EXISTS ADMINISTRADOR (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Nombre_Usuario TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            estado TEXT CHECK(estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
            Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
            Usuario_Creacion TEXT,
            Usuario_Modificacion TEXT,
            row_version INTEGER DEFAULT 1
        );
        """

        cursor.executescript(script_sql)
        conn.commit()
        conn.close()

    def insertar_datos_iniciales(self):
        """Insertar datos iniciales de prueba"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Verificar si ya existen datos
        cursor.execute("SELECT COUNT(*) FROM ADMINISTRADOR")
        if cursor.fetchone()[0] == 0:
            # Insertar administrador por defecto
            cursor.execute("""
                INSERT INTO ADMINISTRADOR (Nombre, Apellido, Nombre_Usuario, Password)
                VALUES ('Admin', 'Sistema', 'admin', 'admin123')
            """)

            # Insertar algunos clientes de prueba
            cursor.execute("""
                INSERT INTO CLIENTE (DNI, NOMBRE, APELLIDOS, CORREO, TELEFONO, FECHA_REGISTRO)
                VALUES ('12345678', 'Juan', 'Pérez', 'juan@email.com', '123456789', date('now'))
            """)

            conn.commit()
        conn.close()

    # --- MÉTODOS PARA CLIENTES ---

    def get_cliente_por_dni(self, dni: str) -> Optional[Dict[str, Any]]:
        """Obtener cliente por DNI"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CLIENTE WHERE DNI = ? AND Estado = 'Activo'", (dni,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'dni': row[1],
                'nombre': row[2],
                'apellidos': row[3],
                'correo': row[4],
                'telefono': row[5],
                'fecha_registro': row[6],
                'fecha_membresia': row[7],
                'estado': row[8]
            }
        return None

    def get_todos_clientes(self) -> List[Dict[str, Any]]:
        """Obtener todos los clientes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CLIENTE ORDER BY NOMBRE")
        rows = cursor.fetchall()
        conn.close()

        clientes = []
        for row in rows:
            clientes.append({
                'id': row[0],
                'dni': row[1],
                'nombre': row[2],
                'apellidos': row[3],
                'correo': row[4],
                'telefono': row[5],
                'fecha_registro': row[6],
                'fecha_membresia': row[7],
                'estado': row[8],
                'activo': row[8] == 'Activo'
            })
        return clientes

    def create_cliente(self, dni: str, nombre: str, apellidos: str, correo: str, telefono: str = None):
        """Crear un nuevo cliente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO CLIENTE (DNI, NOMBRE, APELLIDOS, CORREO, TELEFONO, FECHA_REGISTRO)
                VALUES (?, ?, ?, ?, ?, date('now'))
            """, (dni, nombre, apellidos, correo, telefono))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al crear cliente: {e}")
            return False
        finally:
            conn.close()

    def update_cliente(self, cliente_id: int, nombre: str, apellidos: str, correo: str, telefono: str = None):
        """Actualizar un cliente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE CLIENTE
                SET NOMBRE = ?, APELLIDOS = ?, CORREO = ?, TELEFONO = ?, Fecha_Modificacion = CURRENT_TIMESTAMP
                WHERE Id = ?
            """, (nombre, apellidos, correo, telefono, cliente_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False
        finally:
            conn.close()

    def delete_cliente(self, cliente_id: int):
        """Eliminar un cliente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM CLIENTE WHERE Id = ?", (cliente_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False
        finally:
            conn.close()

    # --- MÉTODOS PARA ADMINISTRADORES ---

    def get_admin_por_credenciales(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Obtener administrador por credenciales"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ADMINISTRADOR WHERE Nombre_Usuario = ? AND Password = ?",
            (username, password)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'nombre': row[1],
                'apellido': row[2],
                'usuario': row[3],
                'estado': row[5]
            }
        return None
