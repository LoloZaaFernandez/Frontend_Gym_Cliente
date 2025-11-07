from pydantic import BaseModel, Field
from typing import Optional


class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    usuario_creacion: str = "admin"


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = Field(None, pattern="^(Activo|Inactivo)$")
    usuario_modificacion: str = "admin"


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    id_categoria: int
    fecha_vencimiento: Optional[str] = None
    usuario_creacion: str = "admin"


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None
    fecha_vencimiento: Optional[str] = None
    estado: Optional[str] = None
    usuario_modificacion: str = "admin"


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    id_categoria: int
    fecha_vencimiento: Optional[str]
    estado: str

    class Config:
        from_attributes = True
        populate_by_name = True


class InventarioCreate(BaseModel):
    id_producto: int
    tipo_movimiento: str = Field(..., pattern="^(Entrada|Salida)$")
    motivo: Optional[str] = None
    cantidad: int = Field(..., gt=0)
    usuario_creacion: str = "admin"


class InventarioResponse(BaseModel):
    id: int
    id_producto: int
    nombre_producto: str
    tipo_movimiento: str
    cantidad: int
    stock_anterior: int
    stock_actual: int
    fecha_creacion: str

    class Config:
        from_attributes = True
        populate_by_name = True
