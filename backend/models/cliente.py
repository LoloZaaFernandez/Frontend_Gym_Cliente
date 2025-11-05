from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    id: Optional[int] = None
    dni: str = ""
    nombre: str = ""
    apellidos: str = ""
    correo: str = ""
    telefono: Optional[str] = None
    fecha_registro: Optional[str] = None
    fecha_membresia: Optional[str] = None
    estado: str = "Activo"
    fecha_creacion: Optional[str] = None
    fecha_modificacion: Optional[str] = None
    usuario_creacion: Optional[str] = None
    usuario_modificacion: Optional[str] = None
    row_version: int = 1
