import sqlite3
from contextlib import contextmanager

DATABASE_PATH = 'gimnasio.db'


@contextmanager
def get_db():
    """Context manager para obtener conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_connection():
    """Obtener conexión directa a la base de datos"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
