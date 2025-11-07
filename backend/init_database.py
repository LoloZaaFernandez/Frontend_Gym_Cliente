"""
Script para inicializar la base de datos con datos de prueba
"""

import sqlite3
from datetime import datetime

DATABASE_PATH = 'gimnasio.db'


def init_database():
    """Inicializar base de datos con estructura y datos de prueba"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("Inicializando base de datos...")

    # Crear tabla ADMINISTRADOR si no existe
    cursor.execute("""
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
        )
    """)

    # Crear tabla CLIENTE si no existe
    cursor.execute("""
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
        )
    """)

    # Crear tabla MEMBRESIA si no existe
    cursor.execute("""
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
        )
    """)

    # Crear tabla ASISTENCIA si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ASISTENCIA (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Id_Cliente INTEGER NOT NULL,
            Fecha_Asistencia TEXT NOT NULL,
            Hora_Ingreso TEXT NOT NULL,
            Estado TEXT DEFAULT 'Activo',
            Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            Usuario_Creacion TEXT,
            FOREIGN KEY (Id_Cliente) REFERENCES CLIENTE(Id)
        )
    """)

    # Crear tabla PRODUCTO si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PRODUCTO (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Descripcion TEXT,
            Precio REAL NOT NULL,
            Stock INTEGER DEFAULT 0,
            Tipo TEXT,
            Estado TEXT DEFAULT 'Activo',
            Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            Usuario_Creacion TEXT
        )
    """)

    print("Tablas creadas/verificadas")

    # Insertar administrador por defecto
    try:
        cursor.execute("""
            INSERT INTO ADMINISTRADOR (Nombre, Apellido, Nombre_Usuario, Password, Usuario_Creacion)
            VALUES ('Admin', 'Sistema', 'admin', 'admin123', 'system')
        """)
        print("Administrador 'admin' creado")
    except sqlite3.IntegrityError:
        print("Administrador 'admin' ya existe")

    # Insertar clientes de prueba
    clientes_prueba = [
        ('12345678', 'Juan', 'Pérez García', 'juan.perez@email.com', '987654321'),
        ('87654321', 'María', 'García López', 'maria.garcia@email.com', '987654322'),
        ('11223344', 'Carlos', 'López Martínez', 'carlos.lopez@email.com', '987654323'),
        ('44332211', 'Ana', 'Martínez Rodríguez', 'ana.martinez@email.com', '987654324'),
        ('55667788', 'Luis', 'Rodríguez Sánchez', 'luis.rodriguez@email.com', '987654325'),
    ]

    fecha_actual = datetime.now().isoformat()
    clientes_insertados = 0

    for dni, nombre, apellidos, correo, telefono in clientes_prueba:
        try:
            cursor.execute("""
                INSERT INTO CLIENTE (DNI, NOMBRE, APELLIDOS, CORREO, TELEFONO, FECHA_REGISTRO, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, ?, 'system')
            """, (dni, nombre, apellidos, correo, telefono, fecha_actual))
            clientes_insertados += 1
        except sqlite3.IntegrityError:
            pass  # Cliente ya existe

    if clientes_insertados > 0:
        print(f"{clientes_insertados} clientes de prueba creados")
    else:
        print("Clientes de prueba ya existen")

    # Insertar productos de prueba
    productos_prueba = [
        ('Membresía Mensual', 'Acceso completo por 30 días', 150.00, 100, 'membresia'),
        ('Membresía Trimestral', 'Acceso completo por 90 días', 400.00, 100, 'membresia'),
        ('Membresía Anual', 'Acceso completo por 365 días', 1500.00, 100, 'membresia'),
        ('Proteína Whey 1kg', 'Proteína de suero de leche', 80.00, 50, 'suplemento'),
        ('Creatina 300g', 'Creatina monohidrato', 45.00, 30, 'suplemento'),
        ('Shaker', 'Vaso mezclador deportivo', 15.00, 100, 'accesorio'),
        ('Toalla Deportiva', 'Toalla de microfibra', 25.00, 75, 'accesorio'),
        ('Guantes de Gym', 'Guantes para entrenamiento', 35.00, 50, 'accesorio'),
    ]

    productos_insertados = 0
    for nombre, descripcion, precio, stock, tipo in productos_prueba:
        cursor.execute("""
            SELECT COUNT(*) FROM PRODUCTO WHERE Nombre = ?
        """, (nombre,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO PRODUCTO (Nombre, Descripcion, Precio, Stock, Tipo, Usuario_Creacion)
                VALUES (?, ?, ?, ?, ?, 'system')
            """, (nombre, descripcion, precio, stock, tipo))
            productos_insertados += 1

    if productos_insertados > 0:
        print(f"{productos_insertados} productos de prueba creados")
    else:
        print("Productos de prueba ya existen")

    conn.commit()
    conn.close()

    print("\nBase de datos inicializada correctamente!")
    print("\nCredenciales de prueba:")
    print("   Admin: admin / admin123")
    print("   Cliente: DNI 12345678")


if __name__ == "__main__":
    init_database()
