from fastapi import APIRouter, HTTPException, status
from schemas.auth import LoginRequest, LoginResponse
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
                success=True,
                user=result,
                role="admin",
                message="Login exitoso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
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
                success=True,
                user=result,
                role="cliente",
                message="Login exitoso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cliente no encontrado o inactivo"
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
