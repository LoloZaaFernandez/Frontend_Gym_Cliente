from dataclasses import dataclass
from typing import Optional


@dataclass
class Producto:
    id: Optional[int] = None
    nombre: str = ""
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None
    fecha_vencimiento: Optional[str] = None
    estado: str = "Activo"
    fecha_creacion: Optional[str] = None
    fecha_modificacion: Optional[str] = None
    usuario_creacion: Optional[str] = None
    usuario_modificacion: Optional[str] = None
    row_version: int = 1
