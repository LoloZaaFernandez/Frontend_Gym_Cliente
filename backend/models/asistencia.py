from dataclasses import dataclass
from typing import Optional


@dataclass
class Asistencia:
    id: Optional[int] = None
    id_cliente: Optional[int] = None
    nombre_cliente: str = ""
    tipo_membresia: str = ""
    fecha_asistencia: Optional[str] = None
    hora_ingreso: Optional[str] = None
    estado: str = "Activo"
    fecha_creacion: Optional[str] = None
    fecha_modificacion: Optional[str] = None
    usuario_creacion: Optional[str] = None
    usuario_modificacion: Optional[str] = None
    row_version: int = 1
