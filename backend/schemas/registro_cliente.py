from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class RegistroClienteCompleto(BaseModel):
    # Datos del cliente
    dni: str = Field(..., min_length=8, max_length=12,
                     description="DNI del cliente")
    nombre: str = Field(..., min_length=2, description="Nombre del cliente")
    apellidos: str = Field(..., min_length=2,
                           description="Apellidos del cliente")
    correo: EmailStr = Field(..., description="Correo electrónico")
    telefono: Optional[str] = Field(None, description="Teléfono de contacto")

    # Datos de la membresía
    id_membresia: int = Field(...,
                              description="ID de la membresía seleccionada")
    metodo_pago: str = Field(..., pattern="^(Efectivo|Tarjeta|Transferencia|Yape|Plin)$",
                             description="Método de pago")

    # Datos adicionales
    usuario_creacion: str = Field(
        "admin", description="Usuario que realiza el registro")


class RegistroClienteResponse(BaseModel):
    cliente: dict
    pago_membresia: dict
    mensaje: str

    class Config:
        from_attributes = True
        populate_by_name = True
