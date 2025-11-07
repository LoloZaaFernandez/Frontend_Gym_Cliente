from dataclasses import dataclass
from typing import Optional


@dataclass
class Membresia:
    id: Optional[int] = None
    nombre_membresia: str = ""
    tipo_membresia: str = ""
    estado: str = "Activa"
    fecha_creacion: Optional[str] = None
    fecha_modificacion: Optional[str] = None
    usuario_creacion: Optional[str] = None
    usuario_modificacion: Optional[str] = None
    row_version: int = 1
