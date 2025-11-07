from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from repositories.membresia_repository import MembresiaRepository
from repositories.cliente_repository import ClienteRepository


class MembresiaService:
    def __init__(self):
        self.repository = MembresiaRepository()
        self.cliente_repository = ClienteRepository()

    def crear_membresia(self, membresia_data: Dict[str, Any]) -> Dict[str, Any]:
        membresia_id = self.repository.create(membresia_data)
        return self.repository.find_by_id(membresia_id)

    def listar_membresias(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.repository.find_all(estado)

    def actualizar_membresia(self, membresia_id: int, membresia_data: Dict[str, Any]) -> Dict[str, Any]:
        # Verificar que la membresía existe
        membresia = self.repository.find_by_id(membresia_id)
        if not membresia:
            raise ValueError("Membresía no encontrada")

        # Actualizar la membresía
        success = self.repository.update(membresia_id, membresia_data)
        if not success:
            raise ValueError("Error al actualizar la membresía")

        # Retornar la membresía actualizada
        return self.repository.find_by_id(membresia_id)

    def eliminar_membresia(self, membresia_id: int) -> Dict[str, str]:
        # Verificar que la membresía existe
        membresia = self.repository.find_by_id(membresia_id)
        if not membresia:
            raise ValueError("Membresía no encontrada")

        # Eliminar la membresía
        success = self.repository.delete(membresia_id)
        if not success:
            raise ValueError("Error al eliminar la membresía")

        return {"message": "Membresía eliminada exitosamente"}

    def crear_precio_membresia(self, precio_data: Dict[str, Any]) -> Dict[str, Any]:
        precio_id = self.repository.create_precio(precio_data)
        return {"message": "Precio creado exitosamente", "id": precio_id}

    def obtener_precio_vigente(self, membresia_id: int) -> Dict[str, Any]:
        precio = self.repository.get_precio_vigente(membresia_id)
        if not precio:
            raise ValueError("Precio no encontrado")
        return precio

    def registrar_pago_membresia(self, pago_data: Dict[str, Any]) -> Dict[str, Any]:
        # Verificar cliente
        cliente = self.cliente_repository.find_by_id(pago_data['id_cliente'])
        if not cliente:
            raise ValueError("Cliente no encontrado")

        # Verificar membresía
        membresia = self.repository.find_by_id(pago_data['id_membresia'])
        if not membresia:
            raise ValueError("Membresía no encontrada")

        # Calcular fecha de vencimiento
        tipo_membresia = membresia['tipo_membresia']
        dias_duracion = {
            "Dia": 1,
            "Mensual": 30,
            "Trimestral": 90,
            "Semestral": 180,
            "Anual": 365
        }

        fecha_actual = datetime.now()
        fecha_vencimiento = fecha_actual + \
            timedelta(days=dias_duracion.get(tipo_membresia, 30))

        # Registrar pago
        pago_id = self.repository.create_pago(pago_data)

        # Actualizar fecha de membresía del cliente
        self.cliente_repository.update(pago_data['id_cliente'], {
            'fecha_membresia': fecha_vencimiento.isoformat()
        })

        return self.repository.find_pago_by_id(pago_id)

    def listar_pagos_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        return self.repository.find_pagos_by_cliente(cliente_id)

    def listar_pagos_cliente_por_dni(self, dni: str) -> List[Dict[str, Any]]:
        """Listar pagos de un cliente por DNI"""
        cliente = self.cliente_repository.find_by_dni(dni)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        return self.repository.find_pagos_by_cliente(cliente['id'])