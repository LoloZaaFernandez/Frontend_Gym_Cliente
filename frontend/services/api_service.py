"""
Servicio para comunicación con el Backend API
Maneja todas las peticiones HTTP al servidor FastAPI
"""

import requests
from typing import Optional, Dict, Any, List
from config.settings import API_BASE_URL, API_TIMEOUT


class APIService:
    """Servicio centralizado para comunicación con la API"""

    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Manejar respuesta de la API"""
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return {"success": True}
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError("Recurso no encontrado")
            elif response.status_code == 400:
                error_detail = response.json().get('detail', 'Error de validación')
                raise ValueError(error_detail)
            else:
                raise ValueError(f"Error en la API: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error de conexión: {str(e)}")

    # ==================== CLIENTES ====================

    def get_clientes(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener lista de clientes"""
        url = f"{self.base_url}/api/clientes"
        params = {}
        if estado:
            params['estado'] = estado

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []

    def get_cliente_por_id(self, cliente_id: int) -> Optional[Dict[str, Any]]:
        """Obtener cliente por ID"""
        url = f"{self.base_url}/api/clientes/{cliente_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
            return None

    def get_cliente_por_dni(self, dni: str) -> Optional[Dict[str, Any]]:
        """Obtener cliente por DNI (buscar en la lista)"""
        clientes = self.get_clientes(estado="Activo")
        for cliente in clientes:
            if cliente['dni'] == dni:
                return cliente
        return None

    def get_cliente_by_dni(self, dni: str) -> Optional[Dict[str, Any]]:
        """Alias de get_cliente_por_dni para compatibilidad"""
        return self.get_cliente_por_dni(dni)

    def crear_cliente(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo cliente"""
        url = f"{self.base_url}/api/clientes"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear cliente: {str(e)}")

    def actualizar_cliente(self, cliente_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar cliente existente"""
        url = f"{self.base_url}/api/clientes/{cliente_id}"
        try:
            response = self.session.put(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al actualizar cliente: {str(e)}")

    def eliminar_cliente(self, cliente_id: int) -> bool:
        """Eliminar (desactivar) cliente"""
        url = f"{self.base_url}/api/clientes/{cliente_id}"
        try:
            response = self.session.delete(url, timeout=self.timeout)
            self._handle_response(response)
            return True
        except Exception as e:
            raise ValueError(f"Error al eliminar cliente: {str(e)}")

    # Alias para compatibilidad
    def create_cliente(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Alias de crear_cliente"""
        return self.crear_cliente(data)

    def update_cliente(self, cliente_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Alias de actualizar_cliente"""
        return self.actualizar_cliente(cliente_id, data)

    def delete_cliente(self, cliente_id: int) -> bool:
        """Alias de eliminar_cliente"""
        return self.eliminar_cliente(cliente_id)

    # ==================== ASISTENCIAS ====================

    def registrar_asistencia(self, dni: str) -> Dict[str, Any]:
        """Registrar asistencia de un cliente por DNI"""
        url = f"{self.base_url}/api/asistencias"
        data = {"dni": dni, "usuario_creacion": "admin"}
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al registrar asistencia: {str(e)}")

    def get_asistencias(self, fecha_inicio: Optional[str] = None,
                       fecha_fin: Optional[str] = None,
                       cliente_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtener lista de asistencias con filtros"""
        url = f"{self.base_url}/api/asistencias"
        params = {}
        if fecha_inicio:
            params['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            params['fecha_fin'] = fecha_fin
        if cliente_id:
            params['cliente_id'] = cliente_id

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener asistencias: {e}")
            return []

    def get_asistencias_hoy(self) -> List[Dict[str, Any]]:
        """Obtener asistencias del día actual"""
        from datetime import datetime
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return self.get_asistencias(fecha_inicio=fecha_hoy, fecha_fin=fecha_hoy)

    def get_asistencias_mes(self) -> List[Dict[str, Any]]:
        """Obtener asistencias del mes actual"""
        from datetime import datetime
        hoy = datetime.now()
        fecha_inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        fecha_fin = hoy.strftime("%Y-%m-%d")
        return self.get_asistencias(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    def get_asistencias_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        """Obtener asistencias de un cliente específico"""
        url = f"{self.base_url}/api/asistencias/cliente/{cliente_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener asistencias del cliente: {e}")
            return []

    def get_estadisticas_asistencias_hoy(self) -> Dict[str, Any]:
        """Obtener estadísticas de asistencias del día"""
        url = f"{self.base_url}/api/asistencias/estadisticas/hoy"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener estadísticas del día: {e}")
            return {"fecha": "", "total_asistencias": 0, "asistencias": []}

    def get_estadisticas_asistencias_mes(self) -> Dict[str, Any]:
        """Obtener estadísticas de asistencias del mes"""
        url = f"{self.base_url}/api/asistencias/estadisticas/mes"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener estadísticas del mes: {e}")
            return {"mes": "", "total_asistencias": 0, "clientes_activos": 0, "promedio_diario": 0}

    def get_estadisticas_cliente(self, cliente_id: int) -> Dict[str, Any]:
        """Obtener estadísticas de asistencias de un cliente"""
        url = f"{self.base_url}/api/asistencias/cliente/{cliente_id}/estadisticas"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener estadísticas del cliente: {e}")
            return {
                "cliente_id": cliente_id,
                "total_asistencias": 0,
                "ultima_asistencia": None,
                "asistencias_mes_actual": 0,
                "asistencias_recientes": []
            }

    # ==================== MEMBRESÍAS ====================

    def get_membresias(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener lista de membresías"""
        url = f"{self.base_url}/api/membresias"
        params = {}
        if estado:
            params['estado'] = estado 

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener membresías: {e}")
            return []

    def comprar_membresia(self, cliente_id: int, membresia_id: int, monto: float,
                         metodo_pago: str = "Efectivo") -> Dict[str, Any]:
        """Registrar compra de membresía"""
        url = f"{self.base_url}/api/membresias/pagos"
        data = {
            "id_cliente": cliente_id,
            "id_membresia": membresia_id,
            "monto": monto,
            "metodo_pago": metodo_pago,
            "usuario_creacion": "sistema"
        }
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al comprar membresía: {str(e)}")

    def get_pagos_membresia_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        """Obtener historial de pagos de membresías de un cliente"""
        url = f"{self.base_url}/api/membresias/pagos/cliente/{cliente_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener pagos del cliente: {e}")
            return []

    # ==================== PRODUCTOS ====================

    def get_productos(self, tipo: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener lista de productos"""
        url = f"{self.base_url}/api/productos"
        params = {}
        if tipo:
            params['tipo'] = tipo

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    def crear_producto(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo producto"""
        url = f"{self.base_url}/api/productos"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear producto: {str(e)}")

    # ==================== VENTAS (POS) ====================

    def crear_venta(self, items: List[Dict[str, Any]], cliente_id: Optional[int] = None) -> Dict[str, Any]:
        """Crear una venta (desde POS)"""
        url = f"{self.base_url}/api/ventas"
        data = {
            "cliente_id": cliente_id,
            "items": items
        }
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear venta: {str(e)}")

    # ==================== REPORTES ====================

    def get_reportes_generales(self) -> Dict[str, Any]:
        """Obtener reportes generales del gimnasio"""
        url = f"{self.base_url}/api/reportes/general"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reportes: {e}")
            return {
                "total_clientes": 0,
                "clientes_activos": 0,
                "asistencias_hoy": 0,
                "asistencias_mes": 0,
                "ingresos_hoy": 0.0,
                "ingresos_mes": 0.0
            }

    def get_ventas_recientes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener ventas recientes"""
        url = f"{self.base_url}/api/reportes/ventas-recientes"
        params = {"limit": limit}
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener ventas recientes: {e}")
            return []

    def get_productos_top(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtener productos más vendidos"""
        url = f"{self.base_url}/api/reportes/productos-top"
        params = {"limit": limit}
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener productos top: {e}")
            return []

    def get_precio_membresia(self, membresia_id: int) -> Dict[str, Any]:
        """Obtener precio vigente de una membresía"""
        url = f"{self.base_url}/api/membresias/precios/{membresia_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener precio de membresía: {e}")
            return None  # 

    def crear_membresia(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nueva membresía"""
        url = f"{self.base_url}/api/membresias"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear membresía: {str(e)}")

    def actualizar_membresia(self, membresia_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar membresía existente"""
        url = f"{self.base_url}/api/membresias/{membresia_id}"
        try:
            response = self.session.put(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al actualizar membresía: {str(e)}")

    def crear_precio_membresia(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear o actualizar precio de membresía"""
        url = f"{self.base_url}/api/membresias/precios"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear precio: {str(e)}")

    # ==================== UTILIDADES ====================

    def health_check(self) -> bool:
        """Verificar si el backend está disponible"""
        url = f"{self.base_url}/health"
        try:
            response = self.session.get(url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def close(self):
        """Cerrar la sesión"""
        self.session.close()
