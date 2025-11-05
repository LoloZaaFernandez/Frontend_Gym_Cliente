from typing import Optional, Dict, Any
from repositories.admin_repository import AdminRepository
from repositories.cliente_repository import ClienteRepository


class AuthService:
    """Servicio de autenticación"""

    def login_admin(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autenticar administrador"""
        admin = AdminRepository.get_por_credenciales(username, password)
        if admin:
            return {
                'id': admin.get('id'),
                'nombre': admin.get('nombre'),
                'apellido': admin.get('apellido'),
                'usuario': admin.get('nombre_usuario'),
                'estado': admin.get('estado')
            }
        return None

    def login_cliente(self, dni: str) -> Optional[Dict[str, Any]]:
        """Autenticar cliente por DNI"""
        cliente = ClienteRepository.find_by_dni(dni)
        if cliente and cliente.get('estado') == 'Activo':
            return {
                'id': cliente.get('id'),
                'dni': cliente.get('dni'),
                'nombre': cliente.get('nombre'),
                'apellidos': cliente.get('apellidos'),
                'correo': cliente.get('correo'),
                'telefono': cliente.get('telefono'),
                'fecha_registro': cliente.get('fecha_registro'),
                'estado': cliente.get('estado')
            }
        return None
