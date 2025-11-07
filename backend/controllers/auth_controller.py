from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas.auth import LoginRequest, LoginResponse, AdminCreate, AdminUpdate, AdminResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])
service = AuthService()


@router.post("/login-admin", response_model=LoginResponse)
def login_admin(credentials: LoginRequest):
    """Login de administrador"""
    try:
        result = service.login_admin(credentials.username, credentials.password)
        if result:
            return LoginResponse(
                success=True, user=result, role="admin", message="Login exitoso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login-client", response_model=LoginResponse)
def login_client(dni: str):
    """Login de cliente por DNI"""
    try:
        result = service.login_cliente(dni)
        if result:
            return LoginResponse(
                success=True, user=result, role="cliente", message="Login exitoso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cliente no encontrado o inactivo",
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# CRUD de Administradores


@router.post("/admin", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def crear_admin(admin: AdminCreate):
    """Crear un nuevo administrador"""
    try:
        return service.crear_admin(admin.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/admin", response_model=List[AdminResponse])
def listar_admins(estado: Optional[str] = None):
    """Listar todos los administradores"""
    return service.listar_admins(estado)


@router.get("/admin/{admin_id}", response_model=AdminResponse)
def obtener_admin(admin_id: int):
    """Obtener un administrador por ID"""
    try:
        return service.obtener_admin(admin_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/admin/{admin_id}", response_model=AdminResponse)
def actualizar_admin(admin_id: int, admin: AdminUpdate):
    """Actualizar un administrador (incluye cambio de estado)"""
    try:
        return service.actualizar_admin(admin_id, admin.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/admin/{admin_id}", status_code=status.HTTP_200_OK)
def eliminar_admin(admin_id: int):
    """Eliminar un administrador"""
    try:
        return service.eliminar_admin(admin_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
