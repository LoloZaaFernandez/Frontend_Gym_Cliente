from typing import Optional, Dict, Any, List
from repositories.admin_repository import AdminRepository
from repositories.cliente_repository import ClienteRepository


class AuthService:
    """Servicio de autenticación y gestión de administradores"""

    def __init__(self):
        self.admin_repository = AdminRepository()

    def login_admin(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autenticar administrador"""
        admin = AdminRepository.get_por_credenciales(username, password)
        if admin:
            return {
                "id": admin.get("id"),
                "nombre": admin.get("nombre"),
                "apellido": admin.get("apellido"),
                "usuario": admin.get("nombre_usuario"),
                "estado": admin.get("estado"),
            }
        return None

    def login_cliente(self, dni: str) -> Optional[Dict[str, Any]]:
        """Autenticar cliente por DNI"""
        cliente = ClienteRepository.find_by_dni(dni)
        if cliente and cliente.get("estado") == "Activo":
            return {
                "id": cliente.get("id"),
                "dni": cliente.get("dni"),
                "nombre": cliente.get("nombre"),
                "apellidos": cliente.get("apellidos"),
                "correo": cliente.get("correo"),
                "telefono": cliente.get("telefono"),
                "fecha_registro": cliente.get("fecha_registro"),
                "estado": cliente.get("estado"),
            }
        return None

    def crear_admin(self, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo administrador"""
        # Verificar que el nombre de usuario no exista
        if AdminRepository.verificar_usuario_existe(admin_data["nombre_usuario"]):
            raise ValueError("El nombre de usuario ya existe")

        admin_id = AdminRepository.create(admin_data)
        return AdminRepository.get_por_id(admin_id)

    def listar_admins(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """Listar todos los administradores"""
        return AdminRepository.listar(estado)

    def obtener_admin(self, admin_id: int) -> Dict[str, Any]:
        """Obtener un administrador por ID"""
        admin = AdminRepository.get_por_id(admin_id)
        if not admin:
            raise ValueError("Administrador no encontrado")
        return admin

    def actualizar_admin(self, admin_id: int, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar un administrador"""
        # Verificar que el administrador existe
        admin = AdminRepository.get_por_id(admin_id)
        if not admin:
            raise ValueError("Administrador no encontrado")

        # Si se está cambiando el nombre de usuario, verificar que no exista
        if "nombre_usuario" in admin_data and admin_data["nombre_usuario"] is not None:
            if AdminRepository.verificar_usuario_existe(
                admin_data["nombre_usuario"], admin_id
            ):
                raise ValueError("El nombre de usuario ya existe")

        # Actualizar el administrador
        success = AdminRepository.update(admin_id, admin_data)
        if not success:
            raise ValueError("Error al actualizar el administrador")

        # Retornar el administrador actualizado
        return AdminRepository.get_por_id(admin_id)

    def eliminar_admin(self, admin_id: int) -> Dict[str, str]:
        """Eliminar un administrador"""
        # Verificar que el administrador existe
        admin = AdminRepository.get_por_id(admin_id)
        if not admin:
            raise ValueError("Administrador no encontrado")

        # Eliminar el administrador
        success = AdminRepository.delete(admin_id)
        if not success:
            raise ValueError("Error al eliminar el administrador")

        return {"message": "Administrador eliminado exitosamente"}
