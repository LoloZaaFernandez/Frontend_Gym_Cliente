from typing import List, Optional, Dict, Any
from repositories.cliente_repository import ClienteRepository
import sqlite3


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def crear_cliente(self, cliente_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            cliente_id = self.repository.create(cliente_data)
            return self.repository.find_by_id(cliente_id)
        except sqlite3.IntegrityError:
            raise ValueError("DNI o correo ya registrado")

    def obtener_cliente(self, cliente_id: int) -> Dict[str, Any]:
        cliente = self.repository.find_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")
        return cliente

    def listar_clientes(self, estado: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return self.repository.find_all(estado, skip, limit)

    def actualizar_cliente(self, cliente_id: int, cliente_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.repository.find_by_id(cliente_id):
            raise ValueError("Cliente no encontrado")

        self.repository.update(cliente_id, cliente_data)
        return self.repository.find_by_id(cliente_id)

    def eliminar_cliente(self, cliente_id: int) -> bool:
        if not self.repository.delete(cliente_id):
            raise ValueError("Cliente no encontrado")
        return True

    # Métodos que usan DNI
    def obtener_cliente_por_dni(self, dni: str) -> Dict[str, Any]:
        cliente = self.repository.find_by_dni(dni)
        if not cliente:
            raise ValueError("Cliente no encontrado")
        return cliente

    def actualizar_cliente_por_dni(self, dni: str, cliente_data: Dict[str, Any]) -> Dict[str, Any]:
        cliente = self.repository.find_by_dni(dni)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        self.repository.update(cliente['id'], cliente_data)
        return self.repository.find_by_dni(dni)

    def eliminar_cliente_por_dni(self, dni: str) -> bool:
        cliente = self.repository.find_by_dni(dni)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        if not self.repository.delete(cliente['id']):
            raise ValueError("Error al eliminar el cliente")
        return True
