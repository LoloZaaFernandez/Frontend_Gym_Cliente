"""
Script para actualizar fechas de membresías y hacerlas válidas
"""

import sqlite3
from datetime import datetime, timedelta

DATABASE_PATH = 'gimnasio.db'


def actualizar_membresias():
    """Actualizar membresías de clientes para que estén activas"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("Actualizando fechas de membresías...")

    # Fecha actual
    fecha_actual = datetime.now()

    # Actualizar algunos clientes con membresías activas
    clientes_actualizar = [
        ('12345678', 30),  # 1 mes
        ('87654321', 90),  # 3 meses
        ('11223344', 180),  # 6 meses
        ('44332211', 365),  # 1 año
        ('72788702', 365),  # 1 año
    ]

    clientes_actualizados = 0

    for dni, dias in clientes_actualizar:
        fecha_vencimiento = (fecha_actual + timedelta(days=dias)).isoformat()

        try:
            cursor.execute("""
                UPDATE CLIENTE
                SET FECHA_MEMBRESIA = ?,
                    Usuario_Modificacion = 'system',
                    Fecha_Modificacion = CURRENT_TIMESTAMP
                WHERE DNI = ?
            """, (fecha_vencimiento, dni))

            if cursor.rowcount > 0:
                clientes_actualizados += 1
                print(f"Actualizado cliente DNI {dni} - Vence en {dias} días")
        except Exception as e:
            print(f"Error actualizando DNI {dni}: {e}")

    conn.commit()
    conn.close()

    print(f"\n{clientes_actualizados} clientes actualizados con membresías activas")
    print("\nClientes con membresías activas:")
    print("  - DNI 12345678 (30 días)")
    print("  - DNI 87654321 (90 días)")
    print("  - DNI 11223344 (180 días)")
    print("  - DNI 44332211 (365 días)")
    print("  - DNI 72788702 (365 días)")


if __name__ == "__main__":
    actualizar_membresias()
