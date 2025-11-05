"""
Servicio de autenticación
Maneja el login de usuarios (administradores y clientes)
En el futuro, este servicio puede hacer llamadas al backend API
"""

from typing import Optional, Dict, Any
from database.db_manager import DatabaseManager


class AuthService:
    """Servicio de autenticación de usuarios"""

    def __init__(self):
        self.db = DatabaseManager()
        self.current_user: Optional[Dict[str, Any]] = None
        self.current_role: Optional[str] = None

    def login_admin(self, username: str, password: str) -> bool:
        """
        Autenticar administrador

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            True si el login es exitoso, False en caso contrario
        """
        user = self.db.get_admin_por_credenciales(username, password)

        if user:
            self.current_user = user
            self.current_role = 'admin'
            return True
        return False

    def login_cliente(self, dni: str) -> bool:
        """
        Autenticar cliente por DNI

        Args:
            dni: Documento de identidad del cliente

        Returns:
            True si el login es exitoso, False en caso contrario
        """
        user = self.db.get_cliente_por_dni(dni)

        if user:
            self.current_user = user
            self.current_role = 'cliente'
            return True
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
