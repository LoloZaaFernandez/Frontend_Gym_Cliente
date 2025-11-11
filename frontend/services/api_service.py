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
            elif response.status_code == 500:
                # Error del servidor - mostrar detalles si están disponibles
                try:
                    error_detail = response.json().get('detail', 'Error interno del servidor')
                    raise ValueError(f"Error del servidor: {error_detail}")
                except:
                    raise ValueError(f"Error interno del servidor (500). Verifica que el backend esté funcionando correctamente.")
            else:
                raise ValueError(f"Error en la API ({response.status_code}): {str(e)}")
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
        """Obtener asistencias del día actual (Perú UTC-5)

        IMPORTANTE: El backend guarda con fecha UTC, así que si son las 19:00-23:59 en Perú,
        la fecha UTC ya es el día siguiente. Por eso buscamos asistencias que fueron creadas
        en las últimas 24 horas y las filtramos por fecha de Perú.
        """
        from datetime import datetime, timezone, timedelta

        # Zona horaria de Perú (UTC-5)
        peru_tz = timezone(timedelta(hours=-5))
        ahora_peru = datetime.now(peru_tz)
        fecha_hoy_peru = ahora_peru.strftime("%Y-%m-%d")

        # Como el backend guarda en UTC, la fecha puede ser hoy o mañana en UTC
        # dependiendo de la hora en Perú
        ahora_utc = datetime.now(timezone.utc)
        fecha_hoy_utc = ahora_utc.strftime("%Y-%m-%d")
        fecha_manana_utc = (ahora_utc + timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"DEBUG API: Fecha HOY en Perú (UTC-5): {fecha_hoy_peru}")
        print(f"DEBUG API: Fecha en UTC: {fecha_hoy_utc}")
        print(f"DEBUG API: Hora actual Perú: {ahora_peru.strftime('%H:%M:%S')}")
        print(f"DEBUG API: Hora actual UTC: {ahora_utc.strftime('%H:%M:%S')}")

        # Obtener todas las asistencias de hoy (en todas las zonas horarias posibles)
        todas_asistencias = []

        # Buscar en fecha de hoy UTC
        asist_hoy = self.get_asistencias(fecha_inicio=fecha_hoy_utc, fecha_fin=fecha_hoy_utc)
        todas_asistencias.extend(asist_hoy)

        # Si la fecha UTC es diferente a la de Perú, también buscar en esa fecha
        if fecha_hoy_utc != fecha_hoy_peru:
            asist_ayer = self.get_asistencias(fecha_inicio=fecha_hoy_peru, fecha_fin=fecha_hoy_peru)
            todas_asistencias.extend(asist_ayer)

        # Si estamos después de las 19:00 en Perú (00:00 UTC del día siguiente)
        if ahora_peru.hour >= 19:
            asist_manana = self.get_asistencias(fecha_inicio=fecha_manana_utc, fecha_fin=fecha_manana_utc)
            todas_asistencias.extend(asist_manana)

        # Eliminar duplicados por ID
        asistencias_unicas = {}
        for asist in todas_asistencias:
            asist_id = asist.get('id')
            if asist_id and asist_id not in asistencias_unicas:
                asistencias_unicas[asist_id] = asist

        resultado = list(asistencias_unicas.values())
        print(f"DEBUG API: Se obtuvieron {len(resultado)} asistencias únicas del día de hoy")

        return resultado

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

    def get_metodo_pago_cliente(self, cliente_id: int) -> str:
        """Obtener el método de pago más reciente de un cliente"""
        try:
            pagos = self.get_pagos_membresia_cliente(cliente_id)
            if pagos and len(pagos) > 0:
                # Ordenar por fecha de pago (más reciente primero)
                pagos_ordenados = sorted(
                    pagos,
                    key=lambda x: x.get('fecha_pago', ''),
                    reverse=True
                )
                return pagos_ordenados[0].get('metodo_pago', 'No especificado')
            return 'Sin registro'
        except Exception as e:
            print(f"Error al obtener método de pago del cliente {cliente_id}: {e}")
            return 'Sin registro'

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

    def get_membresias_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        """Obtener membresías del cliente (información detallada)"""
        # Primero intentar obtener desde endpoint específico si existe
        url = f"{self.base_url}/api/membresias/cliente/{cliente_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener membresías del cliente desde endpoint específico: {e}")
            # Si falla, usar get_pagos_membresia_cliente como fallback
            pagos = self.get_pagos_membresia_cliente(cliente_id)
            if pagos:
                # Extraer información de la membresía del primer pago
                primer_pago = pagos[0]
                return [{
                    'nombre_membresia': primer_pago.get('nombre_membresia', 'Sin plan'),
                    'tipo_membresia': primer_pago.get('tipo_membresia', 'Mensual'),
                    'fecha_inicio': primer_pago.get('fecha_inicio'),
                    'fecha_fin': primer_pago.get('fecha_fin')
                }]
            return []

    # ==================== PRODUCTOS ====================

    def get_productos(self, categoria_id: Optional[int] = None, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener lista de productos con filtros opcionales"""
        url = f"{self.base_url}/api/productos"
        params = {}
        if categoria_id:
            params['categoria_id'] = categoria_id
        if estado:
            params['estado'] = estado

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    def get_producto_by_id(self, producto_id: int) -> Dict[str, Any]:
        """Obtener un producto por ID"""
        url = f"{self.base_url}/api/productos/{producto_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None

    def crear_producto(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo producto"""
        url = f"{self.base_url}/api/productos"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear producto: {str(e)}")

    def actualizar_producto(self, producto_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar un producto"""
        url = f"{self.base_url}/api/productos/{producto_id}"
        try:
            response = self.session.put(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al actualizar producto: {str(e)}")

    def eliminar_producto(self, producto_id: int) -> Dict[str, Any]:
        """Eliminar (desactivar) un producto"""
        url = f"{self.base_url}/api/productos/{producto_id}"
        try:
            response = self.session.delete(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al eliminar producto: {str(e)}")

    # Categorías de productos
    def get_categorias(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener lista de categorías de productos"""
        url = f"{self.base_url}/api/productos/categorias"
        params = {}
        if estado:
            params['estado'] = estado

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener categorías: {e}")
            return []

    def crear_categoria(self, nombre: str, descripcion: str = "") -> Dict[str, Any]:
        """Crear nueva categoría de producto"""
        url = f"{self.base_url}/api/productos/categorias"
        data = {"nombre": nombre, "descripcion": descripcion}
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear categoría: {str(e)}")

    # Inventario
    def get_stock_producto(self, producto_id: int) -> Dict[str, Any]:
        """Obtener stock actual de un producto"""
        url = f"{self.base_url}/api/productos/inventario/stock/{producto_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener stock: {e}")
            return {"stock_actual": 0}

    def registrar_movimiento_inventario(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registrar movimiento de inventario (Entrada/Salida)"""
        url = f"{self.base_url}/api/productos/inventario"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al registrar movimiento: {str(e)}")

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

    # Reportes de Pagos
    def get_reporte_pagos_dia(self, fecha: Optional[str] = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por día"""
        url = f"{self.base_url}/api/reportes/pagos/dia"
        params = {}
        if fecha:
            params['fecha'] = fecha
        try:
            print(f"DEBUG API: Llamando a {url} con params: {params}")
            response = self.session.get(url, params=params, timeout=self.timeout)
            print(f"DEBUG API: Status code: {response.status_code}")
            print(f"DEBUG API: Response text: {response.text[:500]}")  # Primeros 500 caracteres
            resultado = self._handle_response(response)
            print(f"DEBUG API: Resultado parseado: {resultado}")
            return resultado
        except Exception as e:
            print(f"ERROR API: Error al obtener reporte de pagos del día: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def get_reporte_pagos_semana(self, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por semana"""
        url = f"{self.base_url}/api/reportes/pagos/semana"
        params = {}
        if fecha_inicio:
            params['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            params['fecha_fin'] = fecha_fin
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de pagos de la semana: {e}")
            return {}

    def get_reporte_pagos_mes(self, mes: Optional[int] = None, anio: Optional[int] = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por mes"""
        url = f"{self.base_url}/api/reportes/pagos/mes"
        params = {}
        if mes:
            params['mes'] = mes
        if anio:
            params['anio'] = anio
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de pagos del mes: {e}")
            return {}

    def get_reporte_pagos_anio(self, anio: Optional[int] = None) -> Dict[str, Any]:
        """Obtener reporte de pagos por año"""
        url = f"{self.base_url}/api/reportes/pagos/anio"
        params = {}
        if anio:
            params['anio'] = anio
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de pagos del año: {e}")
            return {}

    # Reportes de Clientes
    def get_reporte_clientes_general(self) -> Dict[str, Any]:
        """Obtener reporte general de clientes"""
        url = f"{self.base_url}/api/reportes/clientes/general"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte general de clientes: {e}")
            return {}

    def get_reporte_clientes_nuevos(self, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None) -> Dict[str, Any]:
        """Obtener reporte de clientes nuevos"""
        url = f"{self.base_url}/api/reportes/clientes/nuevos"
        params = {}
        if fecha_inicio:
            params['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            params['fecha_fin'] = fecha_fin
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de clientes nuevos: {e}")
            return {}

    def get_reporte_clientes_membresia_vencida(self) -> Dict[str, Any]:
        """Obtener reporte de clientes con membresía vencida"""
        url = f"{self.base_url}/api/reportes/clientes/membresia-vencida"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de membresías vencidas: {e}")
            return {}

    def get_reporte_clientes_membresia_por_vencer(self, dias: int = 7) -> Dict[str, Any]:
        """Obtener reporte de clientes con membresía por vencer"""
        url = f"{self.base_url}/api/reportes/clientes/membresia-por-vencer"
        params = {'dias': dias}
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de membresías por vencer: {e}")
            return {}

    # Reportes de Asistencias
    def get_reporte_asistencias(self, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None) -> Dict[str, Any]:
        """Obtener reporte de asistencias"""
        url = f"{self.base_url}/api/reportes/asistencias"
        params = {}
        if fecha_inicio:
            params['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            params['fecha_fin'] = fecha_fin
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de asistencias: {e}")
            return {}

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
            return None  # Retorna None si no se encuentra el precio o hay error de conexión 

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
