from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas.producto import (CategoriaCreate, ProductoCreate, ProductoUpdate,
                              ProductoResponse, InventarioCreate, InventarioResponse)
from services.producto_service import ProductoService

router = APIRouter(prefix="/api/productos", tags=["Productos"])
service = ProductoService()


@router.post("/categorias", status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaCreate):
    """Crear una nueva categoría de producto"""
    return service.crear_categoria(categoria.dict())


@router.get("/categorias")
def listar_categorias(estado: Optional[str] = None):
    """Listar todas las categorías"""
    return service.listar_categorias(estado)


@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    try:
        return service.crear_producto(producto.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ProductoResponse])
def listar_productos(categoria_id: Optional[int] = None, estado: Optional[str] = None,
                     skip: int = 0, limit: int = 100):
    """Listar todos los productos con filtros opcionales"""
    return service.listar_productos(categoria_id, estado, skip, limit)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int):
    """Obtener un producto por ID"""
    try:
        return service.obtener_producto(producto_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoUpdate):
    """Actualizar un producto existente"""
    try:
        return service.actualizar_producto(producto_id, producto.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/inventario", response_model=InventarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimiento_inventario(movimiento: InventarioCreate):
    """Registrar movimiento de inventario (Entrada/Salida)"""
    try:
        return service.registrar_movimiento_inventario(movimiento.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/inventario/movimientos", response_model=List[InventarioResponse])
def listar_movimientos_inventario(producto_id: Optional[int] = None,
                                  tipo_movimiento: Optional[str] = None,
                                  skip: int = 0, limit: int = 100):
    """Listar movimientos de inventario con filtros opcionales"""
    return service.listar_movimientos_inventario(producto_id, tipo_movimiento, skip, limit)


@router.get("/inventario/stock/{producto_id}")
def obtener_stock_producto(producto_id: int):
    """Obtener stock actual de un producto"""
    try:
        return service.obtener_stock_producto(producto_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
