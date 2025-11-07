from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    user: dict
    role: str
    message: str = ""


class AdminCreate(BaseModel):
    nombre: str
    apellido: str
    nombre_usuario: str
    password: str
    usuario_creacion: str = "admin"


class AdminUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    nombre_usuario: Optional[str] = None
    password: Optional[str] = None
    estado: Optional[str] = Field(None, pattern="^(Activo|Inactivo)$")
    usuario_modificacion: str = "admin"


class AdminResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    nombre_usuario: str
    estado: str
    fecha_creacion: str

    class Config:
        from_attributes = True
        populate_by_name = True
