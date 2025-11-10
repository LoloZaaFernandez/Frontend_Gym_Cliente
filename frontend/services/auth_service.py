"""
Servicio de autenticación
Maneja el login de usuarios (administradores y clientes)
Conectado con el Backend API
"""

from typing import Optional, Dict, Any
import requests
from config.settings import API_BASE_URL, API_TIMEOUT


class AuthService:
    """Servicio de autenticación de usuarios"""

    def __init__(self):
        self.current_user: Optional[Dict[str, Any]] = None
        self.current_role: Optional[str] = None
        self.use_api = True  # Flag para usar API o fallback local

    def _check_backend(self) -> bool:
        """Verificar si el backend está disponible"""
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def login_admin(self, username: str, password: str) -> bool:
        """
        Autenticar administrador

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            True si el login es exitoso, False en caso contrario
        """
        if self.use_api and self._check_backend():
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/auth/login-admin",
                    json={"username": username, "password": password},
                    timeout=API_TIMEOUT
                )

                if response.status_code == 200:
                    data = response.json()
                    self.current_user = data['user']
                    self.current_role = data['role']
                    return True
                return False
            except Exception as e:
                print(f"Error al autenticar con API: {e}")
                return self._login_admin_local(username, password)
        else:
            return self._login_admin_local(username, password)

    def _login_admin_local(self, username: str, password: str) -> bool:
        """Fallback: autenticación local (actualmente deshabilitado, requiere API)"""
        # La base de datos local fue removida, ahora solo se usa la API
        print("Advertencia: Autenticación local no disponible. Se requiere conexión con el backend.")
        return False

    def login_cliente(self, dni: str) -> bool:
        """
        Autenticar cliente por DNI

        Args:
            dni: Documento de identidad del cliente

        Returns:
            True si el login es exitoso, False en caso contrario
        """
        if self.use_api and self._check_backend():
            try:
                response = requests.get(
                    f"{API_BASE_URL}/api/clientes",
                    params={"estado": "Activo"},
                    timeout=API_TIMEOUT
                )

                if response.status_code == 200:
                    clientes = response.json()
                    for cliente in clientes:
                        if cliente['dni'] == dni:
                            self.current_user = cliente
                            self.current_role = 'cliente'
                            return True
                return False
            except Exception as e:
                print(f"Error al autenticar cliente con API: {e}")
                return self._login_cliente_local(dni)
        else:
            return self._login_cliente_local(dni)

    def _login_cliente_local(self, dni: str) -> bool:
        """Fallback: autenticación local de cliente (actualmente deshabilitado, requiere API)"""
        # La base de datos local fue removida, ahora solo se usa la API
        print("Advertencia: Autenticación local no disponible. Se requiere conexión con el backend.")
        return False

    def logout(self):
        """Cerrar sesión actual"""
        self.current_user = None
        self.current_role = None

    def is_authenticated(self) -> bool:
        """Verificar si hay un usuario autenticado"""
        return self.current_user is not None

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Obtener el usuario actual"""
        return self.current_user

    def get_current_role(self) -> Optional[str]:
        """Obtener el rol del usuario actual"""
        return self.current_role
