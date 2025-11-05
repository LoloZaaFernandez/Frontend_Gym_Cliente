from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas.asistencia import AsistenciaCreate, AsistenciaResponse
from services.asistencia_service import AsistenciaService

router = APIRouter(prefix="/api/asistencias", tags=["Asistencias"])
service = AsistenciaService()


@router.post("", response_model=AsistenciaResponse, status_code=status.HTTP_201_CREATED)
def registrar_asistencia(asistencia: AsistenciaCreate):
    """Registrar asistencia de un cliente"""
    try:
        return service.registrar_asistencia(asistencia.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[AsistenciaResponse])
def listar_asistencias(fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None,
                       cliente_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    """Listar asistencias con filtros opcionales"""
    return service.listar_asistencias(fecha_inicio, fecha_fin, cliente_id, skip, limit)


@router.get("/cliente/{cliente_id}", response_model=List[AsistenciaResponse])
def listar_asistencias_cliente(cliente_id: int, skip: int = 0, limit: int = 50):
    """Listar asistencias de un cliente específico"""
    return service.listar_asistencias(None, None, cliente_id, skip, limit)


@router.get("/estadisticas/hoy")
def obtener_estadisticas_hoy():
    """Obtener estadísticas de asistencias del día actual"""
    try:
        return service.obtener_estadisticas_dia()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas/mes")
def obtener_estadisticas_mes():
    """Obtener estadísticas de asistencias del mes actual"""
    try:
        return service.obtener_estadisticas_mes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cliente/{cliente_id}/estadisticas")
def obtener_estadisticas_cliente(cliente_id: int):
    """Obtener estadísticas de asistencias de un cliente"""
    try:
        return service.obtener_estadisticas_cliente(cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
