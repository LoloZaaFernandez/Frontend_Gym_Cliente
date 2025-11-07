"""
Script de migración para agregar el campo Id_Membresia a la tabla CLIENTE
Esto permite rastrear qué membresía tiene asignada cada cliente
"""

import sqlite3
from pathlib import Path

def migrate():
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
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(CLIENTE)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'Id_Membresia' in columns:
            print("La columna Id_Membresia ya existe en la tabla CLIENTE")
        else:
            print("Agregando columna Id_Membresia a tabla CLIENTE...")
            cursor.execute("""
                ALTER TABLE CLIENTE
                ADD COLUMN Id_Membresia INTEGER
            """)
            conn.commit()
            print("Columna Id_Membresia agregada exitosamente")

        # Verificar estructura final
        cursor.execute("PRAGMA table_info(CLIENTE)")
        print("\nEstructura actual de la tabla CLIENTE:")
        for row in cursor.fetchall():
            print(f"   {row[1]} ({row[2]})")

        print("\nMigracion completada con exito")

    except Exception as e:
        print(f"Error durante la migracion: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRACIÓN DE BASE DE DATOS - Sistema BLESSED GYM")
    print("Agregando campo Id_Membresia a tabla CLIENTE")
    print("=" * 60)
    print()
    migrate()
