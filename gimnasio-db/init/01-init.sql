-- Crear la base de datos
CREATE DATABASE gimnasio_db;

-- Conectar a la base de datos
\c gimnasio_db;

-- Tabla CLIENTE
CREATE TABLE CLIENTE (
    Id SERIAL PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    NOMBRE VARCHAR(100) NOT NULL,
    APELLIDOS VARCHAR(100) NOT NULL,
    CORREO VARCHAR(150) NOT NULL UNIQUE,
    TELEFONO VARCHAR(20),
    FECHA_REGISTRO DATE NOT NULL,
    FECHA_MEMBRESIA DATE,
    Estado VARCHAR(20) CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1
);

-- Tabla MEMBRESIA
CREATE TABLE MEMBRESIA (
    Id SERIAL PRIMARY KEY,
    Nombre_Membresia VARCHAR(100) NOT NULL,
    tipo_membresia VARCHAR(50) NOT NULL,
    Estado VARCHAR(20) CHECK(Estado IN ('Activa', 'Inactiva')) DEFAULT 'Activa',
    Fecha_Creacion TIMESTAMP NOT NULL,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1
);

-- Tabla ADMINISTRADOR
CREATE TABLE ADMINISTRADOR (
    Id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Nombre_Usuario VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    estado VARCHAR(20) CHECK(estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1
);

-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    Id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    estado VARCHAR(20) CHECK(estado IN ('Activa', 'Inactiva')) DEFAULT 'Activa',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1
);

-- Tabla PRODUCTOS
CREATE TABLE PRODUCTOS (
    Id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Id_Categoria INTEGER NOT NULL,
    Fecha_vencimiento DATE,
    estado VARCHAR(20) CHECK(estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Categoria) REFERENCES CATEGORIA(Id)
);

-- Tabla INVENTARIO
CREATE TABLE INVENTARIO (
    Id SERIAL PRIMARY KEY,
    Id_Producto INTEGER NOT NULL,
    Nombre_Producto VARCHAR(100),
    Tipo_movimiento VARCHAR(20) CHECK(Tipo_movimiento IN ('Entrada', 'Salida')) NOT NULL,
    Motivo TEXT,
    Cantidad INTEGER NOT NULL,
    Stock_Anterior INTEGER NOT NULL,
    Stock_Actual INTEGER NOT NULL,
    Estado VARCHAR(20) CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Producto) REFERENCES PRODUCTOS(Id)
);

-- Tabla PRECIO_HISTORIAL
CREATE TABLE PRECIO_HISTORIAL (
    Id SERIAL PRIMARY KEY,
    Id_Producto INTEGER NOT NULL,
    Precio_anterior DECIMAL(10,2) NOT NULL,
    Precio_nuevo DECIMAL(10,2) NOT NULL,
    Fecha_Cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Estado VARCHAR(20) CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Producto) REFERENCES PRODUCTOS(Id)
);

-- Tabla PRECIO_MEMBRESIA
CREATE TABLE PRECIO_MEMBRESIA (
    Id SERIAL PRIMARY KEY,
    Id_Membresia INTEGER NOT NULL,
    Precio_Anterior DECIMAL(10,2),
    Precio_Actual DECIMAL(10,2) NOT NULL,
    Fecha_Inicio_Vigencia DATE NOT NULL,
    Estado VARCHAR(20) CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Membresia) REFERENCES MEMBRESIA(Id)
);

-- Tabla PAGO_MEMBRESIA
CREATE TABLE PAGO_MEMBRESIA (
    Id SERIAL PRIMARY KEY,
    Id_Cliente INTEGER NOT NULL,
    Id_Membresia INTEGER NOT NULL,
    Monto DECIMAL(10,2) NOT NULL,
    Metodo_Pago VARCHAR(50) NOT NULL,
    Fecha_Pago DATE NOT NULL,
    Estado VARCHAR(20) CHECK(Estado IN ('Pagado', 'Pendiente', 'Cancelado')) DEFAULT 'Pagado',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Cliente) REFERENCES CLIENTE(Id),
    FOREIGN KEY (Id_Membresia) REFERENCES MEMBRESIA(Id)
);

-- Tabla ASISTENCIA
CREATE TABLE ASISTENCIA (
    Id SERIAL PRIMARY KEY,
    Id_Cliente INTEGER NOT NULL,
    Nombre_Cliente VARCHAR(200) NOT NULL,
    Tipo_Membresia VARCHAR(50) NOT NULL,
    Fecha_Asistencia DATE DEFAULT CURRENT_DATE,
    Hora_Ingreso TIME DEFAULT CURRENT_TIME,
    Estado VARCHAR(20) CHECK(Estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario_Creacion VARCHAR(50),
    Usuario_Modificacion VARCHAR(50),
    row_version INTEGER DEFAULT 1,
    FOREIGN KEY (Id_Cliente) REFERENCES CLIENTE(Id)
);

-- Crear índices para mejorar rendimiento
CREATE INDEX idx_cliente_dni ON CLIENTE(DNI);
CREATE INDEX idx_cliente_correo ON CLIENTE(CORREO);
CREATE INDEX idx_asistencia_fecha ON ASISTENCIA(Fecha_Asistencia);
CREATE INDEX idx_pago_cliente ON PAGO_MEMBRESIA(Id_Cliente);
CREATE INDEX idx_inventario_producto ON INVENTARIO(Id_Producto);

-- Crear usuario de aplicación
CREATE USER gimnasio_app WITH PASSWORD 'cambiar_en_produccion';
GRANT ALL PRIVILEGES ON DATABASE gimnasio_db TO gimnasio_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gimnasio_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gimnasio_app;
