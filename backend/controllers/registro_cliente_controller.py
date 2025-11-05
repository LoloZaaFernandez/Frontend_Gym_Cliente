# ==================== app/controllers/registro_cliente_controller.py ====================
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from schemas.registro_cliente import RegistroClienteCompleto, RegistroClienteResponse
from services.registro_cliente_service import RegistroClienteService

router = APIRouter(prefix="/api/registro", tags=["Registro de Clientes"])
service = RegistroClienteService()


@router.post("/cliente-completo", response_model=RegistroClienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_cliente_completo(registro: RegistroClienteCompleto):
    """
    Registrar un cliente completo con su membresía en un solo proceso

    Este endpoint permite:
    - Registrar los datos personales del cliente
    - Seleccionar y pagar una membresía
    - Activar automáticamente la membresía del cliente
    - Establecer la fecha de vencimiento

    Todo en una sola transacción.
    """
    try:
        resultado = service.registrar_cliente_completo(registro.dict())
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en el registro: {str(e)}")


@router.get("/opciones")
def obtener_opciones_registro():
    """
    Obtener opciones disponibles para el registro

    Retorna:
    - Lista de membresías activas con sus precios
    - Métodos de pago disponibles
    """
    try:
        return service.obtener_opciones_registro()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener opciones: {str(e)}")


@router.get("/verificar-dni/{dni}")
def verificar_dni_disponible(dni: str):
    """
    Verificar si un DNI está disponible para registro

    Útil para verificar antes de enviar el formulario completo
    """
    try:
        from repositories.cliente_repository import ClienteRepository
        cliente_repo = ClienteRepository()

        cliente_existente = cliente_repo.find_by_dni(dni)

        return {
            'dni': dni,
            'disponible': cliente_existente is None,
            'mensaje': 'DNI disponible' if cliente_existente is None else 'DNI ya registrado'
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al verificar DNI: {str(e)}")
