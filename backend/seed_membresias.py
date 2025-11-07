"""
Script para insertar membresías iniciales en la base de datos con sus precios
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def seed_membresias():
    # Buscar la base de datos
    db_paths = [
        Path(__file__).parent.parent / "gimnasio.db",
        Path(__file__).parent / "gimnasio.db",
        Path("gimnasio.db")
    ]

    db_path = None
    for path in db_paths:
        if path.exists():
            db_path = path
            break

    if not db_path:
        print("No se encontro la base de datos gimnasio.db")
        return

    print(f"Usando base de datos: {db_path}")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        fecha_actual = datetime.now().isoformat()

        # Membresías a insertar
        membresias = [
            ("Membresía Diaria", "Dia"),
            ("Membresía Mensual", "Mensual"),
            ("Membresía Trimestral", "Trimestral"),
            ("Membresía Semestral", "Semestral"),
            ("Membresía Anual", "Anual"),
        ]

        # Precios correspondientes
        precios = {
            "Dia": 15.00,
            "Mensual": 150.00,
            "Trimestral": 400.00,
            "Semestral": 750.00,
            "Anual": 1500.00
        }

        print("\nInsertando membresias...")

        for nombre, tipo in membresias:
            # Verificar si ya existe
            cursor.execute("SELECT Id FROM MEMBRESIA WHERE tipo_membresia = ?", (tipo,))
            existing = cursor.fetchone()

            if existing:
                membresia_id = existing[0]
                print(f"  - {nombre} ya existe (ID: {membresia_id})")
            else:
                # Insertar membresía
                cursor.execute("""
                    INSERT INTO MEMBRESIA (Nombre_Membresia, tipo_membresia, Estado, Fecha_Creacion, Usuario_Creacion)
                    VALUES (?, ?, 'Activa', ?, 'sistema')
                """, (nombre, tipo, fecha_actual))
                membresia_id = cursor.lastrowid
                print(f"  + {nombre} creada (ID: {membresia_id})")

            # Verificar si ya tiene precio
            cursor.execute("SELECT Id FROM PRECIO_MEMBRESIA WHERE Id_Membresia = ? AND Estado = 'Activo'", (membresia_id,))
            precio_existente = cursor.fetchone()

            if precio_existente:
                print(f"    Precio ya existe para {nombre}")
            else:
                # Insertar precio
                precio = precios[tipo]
                cursor.execute("""
                    INSERT INTO PRECIO_MEMBRESIA (Id_Membresia, Precio_Actual, Fecha_Inicio_Vigencia, Estado, Fecha_Creacion, Usuario_Creacion)
                    VALUES (?, ?, ?, 'Activo', ?, 'sistema')
                """, (membresia_id, precio, fecha_actual, fecha_actual))
                print(f"    Precio S/. {precio:.2f} asignado")

        conn.commit()

        # Mostrar resumen
        cursor.execute("""
            SELECT m.Id, m.Nombre_Membresia, m.tipo_membresia, m.Estado, p.Precio_Actual
            FROM MEMBRESIA m
            LEFT JOIN PRECIO_MEMBRESIA p ON m.Id = p.Id_Membresia AND p.Estado = 'Activo'
            ORDER BY
                CASE m.tipo_membresia
                    WHEN 'Dia' THEN 1
                    WHEN 'Mensual' THEN 2
                    WHEN 'Trimestral' THEN 3
                    WHEN 'Semestral' THEN 4
                    WHEN 'Anual' THEN 5
                END
        """)

        print("\n" + "="*70)
        print("MEMBRESIAS EN LA BASE DE DATOS:")
        print("="*70)
        print(f"{'ID':<5} {'Nombre':<25} {'Tipo':<15} {'Estado':<10} {'Precio':<10}")
        print("-"*70)

        for row in cursor.fetchall():
            id_mem, nombre, tipo, estado, precio = row
            precio_str = f"S/. {precio:.2f}" if precio else "Sin precio"
            print(f"{id_mem:<5} {nombre:<25} {tipo:<15} {estado:<10} {precio_str:<10}")

        print("="*70)
        print("\nDatos iniciales insertados correctamente")

    except Exception as e:
        print(f"Error durante la insercion: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("="*70)
    print("INSERCION DE DATOS INICIALES - Sistema BLESSED GYM")
    print("Membresias y Precios")
    print("="*70)
    print()
    seed_membresias()
