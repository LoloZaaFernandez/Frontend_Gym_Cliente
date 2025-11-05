from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from services.cliente_service import ClienteService

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])
service = ClienteService()


@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: ClienteCreate):
    """Crear un nuevo cliente"""
    try:
        return service.crear_cliente(cliente.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[ClienteResponse])
def listar_clientes(estado: Optional[str] = None, skip: int = 0, limit: int = 100):
    """Listar todos los clientes con filtros opcionales"""
    return service.listar_clientes(estado, skip, limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int):
    """Obtener un cliente por ID"""
    try:
        return service.obtener_cliente(cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate):
    """Actualizar un cliente existente"""
    try:
        return service.actualizar_cliente(cliente_id, cliente.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int):
    """Eliminar (desactivar) un cliente"""
    try:
        service.eliminar_cliente(cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
