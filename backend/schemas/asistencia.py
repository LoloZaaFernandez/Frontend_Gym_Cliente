from pydantic import BaseModel, Field
from typing import Optional


class AsistenciaCreate(BaseModel):
    dni: str = Field(..., min_length=8, max_length=12,
                     description="DNI del cliente")
    usuario_creacion: str = "admin"


class AsistenciaResponse(BaseModel):
    id: int
    id_cliente: int
    nombre_cliente: str
    tipo_membresia: str
    fecha_asistencia: str
    hora_ingreso: str
    estado: str

    class Config:
        from_attributes = True
        populate_by_name = True
