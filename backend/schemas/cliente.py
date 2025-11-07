from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class ClienteCreate(BaseModel):
    dni: str = Field(..., min_length=8, max_length=12)
    nombre: str = Field(..., min_length=2)
    apellidos: str = Field(..., min_length=2)
    correo: EmailStr
    telefono: Optional[str] = None
    usuario_creacion: str = "admin"


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    estado: Optional[str] = None
    usuario_modificacion: str = "admin"


class ClienteResponse(BaseModel):
    id: int
    dni: str
    nombre: str
    apellidos: str
    correo: str
    telefono: Optional[str]
    fecha_registro: str
    fecha_membresia: Optional[str]
    estado: str

    class Config:
        from_attributes = True
        populate_by_name = True

    @field_validator('*', mode='before')
    @classmethod
    def convert_keys(cls, v, info):
        # Convertir nombres de columnas de mayúsculas a minúsculas
        if isinstance(v, dict):
            return {k.lower(): val for k, val in v.items()}
        return v
