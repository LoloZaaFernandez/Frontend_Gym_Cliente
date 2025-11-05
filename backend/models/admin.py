from dataclasses import dataclass
from typing import Optional


@dataclass
class Administrador:
    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    nombre_usuario: str = ""
    password: str = ""
    estado: str = "Activo"
    fecha_creacion: Optional[str] = None
    fecha_modificacion: Optional[str] = None
    usuario_creacion: Optional[str] = None
    usuario_modificacion: Optional[str] = None
    row_version: int = 1
