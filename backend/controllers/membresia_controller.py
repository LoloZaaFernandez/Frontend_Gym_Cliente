from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas.membresia import (MembresiaCreate, MembresiaResponse,
                               PrecioMembresiaCreate, PagoMembresiaCreate, PagoMembresiaResponse)
from services.membresia_service import MembresiaService

router = APIRouter(prefix="/api/membresias", tags=["Membresías"])
service = MembresiaService()


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_membresia(membresia: MembresiaCreate):
    """Crear una nueva membresía"""
    return service.crear_membresia(membresia.dict())


@router.get("", response_model=List[MembresiaResponse])
def listar_membresias(estado: Optional[str] = None):
    """Listar todas las membresías"""
    return service.listar_membresias(estado)


@router.post("/precios", status_code=status.HTTP_201_CREATED)
def crear_precio_membresia(precio: PrecioMembresiaCreate):
    """Crear o actualizar precio de membresía"""
    return service.crear_precio_membresia(precio.dict())


@router.get("/precios/{membresia_id}")
def obtener_precio_vigente(membresia_id: int):
    """Obtener precio vigente de una membresía"""
    try:
        return service.obtener_precio_vigente(membresia_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/pagos", response_model=PagoMembresiaResponse, status_code=status.HTTP_201_CREATED)
def registrar_pago_membresia(pago: PagoMembresiaCreate):
    """Registrar un pago de membresía"""
    try:
        return service.registrar_pago_membresia(pago.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/pagos/cliente/{cliente_id}", response_model=List[PagoMembresiaResponse])
def listar_pagos_cliente(cliente_id: int):
    """Listar pagos de un cliente"""
    return service.listar_pagos_cliente(cliente_id)
