from pydantic import BaseModel, Field
from typing import Optional


class MembresiaCreate(BaseModel):
    nombre_membresia: str
    tipo_membresia: str = Field(...,
                                pattern="^(Dia|Mensual|Trimestral|Semestral|Anual)$")
    usuario_creacion: str = "admin"


class MembresiaUpdate(BaseModel):
    nombre_membresia: Optional[str] = None
    tipo_membresia: Optional[str] = Field(
        None, pattern="^(Dia|Mensual|Trimestral|Semestral|Anual)$")
    estado: Optional[str] = Field(
        None, pattern="^(Activa|Inactiva)$")
    usuario_modificacion: str = "admin"


class MembresiaResponse(BaseModel):
    id: int
    nombre_membresia: str
    tipo_membresia: str
    estado: str
    fecha_creacion: str

    class Config:
        from_attributes = True
        populate_by_name = True


class PrecioMembresiaCreate(BaseModel):
    id_membresia: int
    precio_actual: float = Field(..., gt=0)
    precio_anterior: Optional[float] = None
    usuario_creacion: str = "admin"


class PagoMembresiaCreate(BaseModel):
    id_cliente: int
    id_membresia: int
    monto: float = Field(..., gt=0)
    metodo_pago: str = Field(...,
                             pattern="^(Efectivo|Tarjeta|Transferencia|Yape|Plin)$")
    usuario_creacion: str = "admin"


class PagoMembresiaResponse(BaseModel):
    id: int
    id_cliente: int
    id_membresia: int
    monto: float
    metodo_pago: str
    fecha_pago: str
    estado: str

    class Config:
        from_attributes = True
        populate_by_name = True