import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('gimnasio.db')
    cursor = conn.cursor()
    
    # Script completo de tablas
    script_sql = """
    -- Tabla CLIENTE
CREATE TABLE CLIENTE (
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
CREATE TABLE MEMBRESIA (
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
CREATE TABLE ADMINISTRADOR (
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

-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Descripcion TEXT,
    estado TEXT CHECK(estado IN ('Activa', 'Inactiva')) DEFAULT 'Activa',
    Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion TEXT,
    Usuario_Modificacion TEXT,
    row_version INTEGER DEFAULT 1
);

-- Tabla PRODUCTOS
CREATE TABLE PRODUCTOS (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Descripcion TEXT,
    Id_Categoria INTEGER NOT NULL,
    Fecha_vencimiento TEXT,
    estado TEXT CHECK(estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion TEXT,
    Usuario_Modificacion TEXT,
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Categoria) REFERENCES CATEGORIA(Id)
);

-- Tabla INVENTARIO
CREATE TABLE INVENTARIO (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Producto INTEGER NOT NULL,
    Nombre_Producto TEXT,
    Tipo_movimiento TEXT CHECK(Tipo_movimiento IN ('Entrada', 'Salida')) NOT NULL,
    Motivo TEXT,
    Cantidad INTEGER NOT NULL,
    Stock_Anterior INTEGER NOT NULL,
    Stock_Actual INTEGER NOT NULL,
    Estado TEXT CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion TEXT,
    Usuario_Modificacion TEXT,
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Producto) REFERENCES PRODUCTOS(Id)
);

-- Tabla PRECIO_HISTORIAL
CREATE TABLE PRECIO_HISTORIAL (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Producto INTEGER NOT NULL,
    Precio_anterior REAL NOT NULL,
    Precio_nuevo REAL NOT NULL,
    Fecha_Cambio TEXT DEFAULT CURRENT_TIMESTAMP,
    Estado TEXT CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion TEXT,
    Usuario_Modificacion TEXT,
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Producto) REFERENCES PRODUCTOS(Id)
);

-- Tabla PRECIO_MEMBRESIA
CREATE TABLE PRECIO_MEMBRESIA (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Membresia INTEGER NOT NULL,
    Precio_Anterior REAL,
    Precio_Actual REAL NOT NULL,
    Fecha_Inicio_Vigencia TEXT NOT NULL,
    Estado TEXT CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion TEXT,
    Usuario_Modificacion TEXT,
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Membresia) REFERENCES MEMBRESIA(Id)
);

-- Tabla PAGO_MEMBRESIA
CREATE TABLE PAGO_MEMBRESIA (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Cliente INTEGER NOT NULL,
    Id_Membresia INTEGER NOT NULL,
    Monto REAL NOT NULL,
    Metodo_Pago TEXT NOT NULL,
    Fecha_Pago TEXT NOT NULL,
    Estado TEXT CHECK(Estado IN ('Pagado', 'Pendiente', 'Cancelado')) DEFAULT 'Pagado',
    Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion TEXT,
    Usuario_Modificacion TEXT,
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Cliente) REFERENCES CLIENTE(Id),
    FOREIGN KEY (Id_Membresia) REFERENCES MEMBRESIA(Id)
);
-- Tabla ASISTENCIA
CREATE TABLE ASISTENCIA (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Cliente INTEGER NOT NULL,
    Nombre_Cliente TEXT NOT NULL,
    Tipo_Membresia TEXT NOT NULL,
    Fecha_Asistencia TEXT DEFAULT CURRENT_DATE,
    Hora_Ingreso TEXT DEFAULT CURRENT_TIME,
    Estado TEXT CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion TEXT,
    Usuario_Modificacion TEXT,
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Cliente) REFERENCES CLIENTE(Id)
);
        """
    
    # Ejecutar script completo
    cursor.executescript(script_sql)
    conn.commit()
    conn.close()
    print("Base de datos creada")

# Ejecutar la función
crear_base_datos()
