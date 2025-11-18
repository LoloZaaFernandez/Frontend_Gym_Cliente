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
            elif response.status_code == 422:
                # Error de validación - mostrar detalles completos
                try:
                    error_data = response.json()
                    print(f"DEBUG API: Error 422 completo: {error_data}")

                    # FastAPI devuelve errores de validación en este formato
                    if 'detail' in error_data:
                        if isinstance(error_data['detail'], list):
                            # Lista de errores de validación
                            errores = []
                            for err in error_data['detail']:
                                campo = " -> ".join(str(x) for x in err.get('loc', []))
                                mensaje = err.get('msg', 'Error de validación')
                                tipo = err.get('type', '')
                                errores.append(f"{campo}: {mensaje} ({tipo})")
                            raise ValueError(f"Errores de validación:\n" + "\n".join(errores))
                        else:
                            # Detalle simple
                            raise ValueError(f"Error de validación: {error_data['detail']}")
                    else:
                        raise ValueError(f"Error de validación (422): {error_data}")
                except ValueError:
                    raise
                except Exception:
                    raise ValueError(f"Error de validación en el servidor (422). Verifica los datos enviados.")
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

    def validar_cliente_registro(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos de cliente antes del registro - NO registra"""
        url = f"{self.base_url}/api/registro/cliente-con-validacion"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error en validación: {str(e)}")

    def registrar_cliente_completo(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registrar cliente con membresía y pago (después de confirmación)"""
        url = f"{self.base_url}/api/registro/cliente-completo"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al registrar cliente: {str(e)}")

    def get_registros_pendientes(self) -> List[Dict[str, Any]]:
        """Obtener lista de registros pendientes de confirmación"""
        url = f"{self.base_url}/api/registro/registros-pendientes"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener registros pendientes: {e}")
            return []

    def confirmar_registro_pendiente(self, id_registro: int) -> Dict[str, Any]:
        """Confirmar un registro pendiente y crear el cliente"""
        url = f"{self.base_url}/api/registro/confirmar-registro/{id_registro}"
        try:
            response = self.session.post(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al confirmar registro: {str(e)}")

    def rechazar_registro_pendiente(self, id_registro: int, motivo: str = "Pago no verificado") -> Dict[str, Any]:
        """Rechazar un registro pendiente"""
        url = f"{self.base_url}/api/registro/rechazar-registro/{id_registro}"
        params = {"motivo": motivo}
        try:
            response = self.session.post(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al rechazar registro: {str(e)}")

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
        """Obtener asistencias del día actual (zona horaria local del sistema)

        IMPORTANTE: El backend ahora guarda usando zona horaria LOCAL del sistema,
        por lo que solo necesitamos buscar por la fecha de hoy en zona local.
        """
        from datetime import datetime

        # Fecha de hoy en zona horaria local del sistema
        fecha_hoy_local = datetime.now().strftime("%Y-%m-%d")

        # Buscar asistencias solo de hoy (el backend ya usa zona local)
        asistencias = self.get_asistencias(fecha_inicio=fecha_hoy_local, fecha_fin=fecha_hoy_local)

        return asistencias

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
            response = self.session.patch(url, json=data, timeout=self.timeout)
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

    def actualizar_categoria(self, categoria_id: int, nombre: str, descripcion: str = "") -> Dict[str, Any]:
        """Actualizar categoría existente"""
        url = f"{self.base_url}/api/productos/categorias/{categoria_id}"
        data = {"nombre": nombre, "descripcion": descripcion}
        try:
            response = self.session.patch(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al actualizar categoría: {str(e)}")

    def eliminar_categoria(self, categoria_id: int) -> Dict[str, Any]:
        """Eliminar categoría de producto"""
        url = f"{self.base_url}/api/productos/categorias/{categoria_id}"
        try:
            response = self.session.delete(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al eliminar categoría: {str(e)}")

    def get_categoria_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Buscar categoría por nombre"""
        try:
            categorias = self.get_categorias()
            for cat in categorias:
                if cat.get('nombre', '').lower() == nombre.lower():
                    return cat
            return None
        except Exception as e:
            print(f"Error al buscar categoría por nombre: {e}")
            return None

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

    # ==================== PRODUCTOS - BÚSQUEDAS ESPECIALES ====================

    def get_producto_por_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        """Obtener producto por SKU - GET /api/productos/sku/{sku}"""
        url = f"{self.base_url}/api/productos/sku/{sku}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener producto por SKU: {e}")
            return None

    def get_producto_por_codigo_barras(self, codigo: str) -> Optional[Dict[str, Any]]:
        """Obtener producto por código de barras - GET /api/productos/codigo-barras/{codigo}"""
        url = f"{self.base_url}/api/productos/codigo-barras/{codigo}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener producto por código de barras: {e}")
            return None

    def get_producto_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Obtener producto por nombre exacto - GET /api/productos/nombre/{nombre}"""
        url = f"{self.base_url}/api/productos/nombre/{nombre}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener producto por nombre: {e}")
            return None

    # ==================== INVENTARIO AVANZADO ====================

    def registrar_entrada_inventario(self, producto_id: int, cantidad: int,
                                     costo_unitario: Optional[float] = None,
                                     lote: Optional[str] = None,
                                     fecha_vencimiento: Optional[str] = None,
                                     motivo: Optional[str] = None) -> Dict[str, Any]:
        """Registrar entrada de inventario - POST /api/productos/{producto_id}/inventario/entrada"""
        url = f"{self.base_url}/api/productos/{producto_id}/inventario/entrada"
        params = {"cantidad": cantidad}
        if costo_unitario is not None:
            params["costo_unitario"] = costo_unitario
        if lote:
            params["lote"] = lote
        if fecha_vencimiento:
            params["fecha_vencimiento"] = fecha_vencimiento
        if motivo:
            params["motivo"] = motivo

        try:
            response = self.session.post(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al registrar entrada: {str(e)}")

    def registrar_salida_inventario(self, producto_id: int, cantidad: int, motivo: str) -> Dict[str, Any]:
        """Registrar salida de inventario - POST /api/productos/{producto_id}/inventario/salida"""
        url = f"{self.base_url}/api/productos/{producto_id}/inventario/salida"
        params = {"cantidad": cantidad, "motivo": motivo}

        try:
            response = self.session.post(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al registrar salida: {str(e)}")

    def ajustar_inventario(self, producto_id: int, stock_nuevo: int, motivo: str) -> Dict[str, Any]:
        """Ajustar inventario a un valor específico - POST /api/productos/{producto_id}/inventario/ajuste"""
        url = f"{self.base_url}/api/productos/{producto_id}/inventario/ajuste"
        params = {"stock_nuevo": stock_nuevo, "motivo": motivo}

        try:
            print(f"DEBUG: Enviando ajuste con params={params}")
            response = self.session.post(url, params=params, timeout=self.timeout)
            print(f"DEBUG: Response status={response.status_code}")
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al ajustar inventario: {str(e)}")

    def registrar_merma(self, producto_id: int, cantidad: int, motivo: str) -> Dict[str, Any]:
        """Registrar merma (producto perdido/dañado/vencido) - POST /api/productos/{producto_id}/inventario/merma"""
        url = f"{self.base_url}/api/productos/{producto_id}/inventario/merma"
        params = {"cantidad": cantidad, "motivo": motivo}

        try:
            print(f"DEBUG: Enviando merma con params={params}")
            response = self.session.post(url, params=params, timeout=self.timeout)
            print(f"DEBUG: Response status={response.status_code}")
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al registrar merma: {str(e)}")

    def get_movimientos_inventario(self, producto_id: int,
                                   tipo_movimiento: Optional[str] = None,
                                   fecha_desde: Optional[str] = None,
                                   fecha_hasta: Optional[str] = None,
                                   skip: int = 0,
                                   limit: int = 100) -> List[Dict[str, Any]]:
        """Ver movimientos de inventario - GET /api/productos/{producto_id}/inventario/movimientos"""
        url = f"{self.base_url}/api/productos/{producto_id}/inventario/movimientos"
        params = {"skip": skip, "limit": limit}
        if tipo_movimiento:
            params["tipo_movimiento"] = tipo_movimiento
        if fecha_desde:
            params["fecha_desde"] = fecha_desde
        if fecha_hasta:
            params["fecha_hasta"] = fecha_hasta

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener movimientos: {e}")
            return []

    # ==================== ALERTAS Y REPORTES ====================

    def get_productos_stock_bajo(self) -> List[Dict[str, Any]]:
        """Productos con stock bajo - GET /api/productos/inventario/alertas"""
        url = f"{self.base_url}/api/productos/inventario/alertas"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener productos con stock bajo: {e}")
            return []

    def get_productos_proximos_vencer(self, dias: int = 30) -> List[Dict[str, Any]]:
        """Productos próximos a vencer - GET /api/productos/inventario/proximos-vencer"""
        url = f"{self.base_url}/api/productos/inventario/proximos-vencer"
        params = {"dias": dias}
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener productos próximos a vencer: {e}")
            return []

    def get_productos_sin_stock(self) -> List[Dict[str, Any]]:
        """Productos sin stock - GET /api/productos/inventario/sin-stock"""
        url = f"{self.base_url}/api/productos/inventario/sin-stock"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener productos sin stock: {e}")
            return []

    # ==================== ESTADÍSTICAS ====================

    def get_estadisticas_productos(self) -> Dict[str, Any]:
        """Estadísticas generales de productos - GET /api/productos/estadisticas/resumen"""
        url = f"{self.base_url}/api/productos/estadisticas/resumen"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                "total_productos": 0,
                "productos_activos": 0,
                "productos_con_stock_bajo": 0,
                "valor_total_inventario": 0,
                "valor_total_venta": 0
            }

    def get_estadisticas_por_categoria(self) -> List[Dict[str, Any]]:
        """Estadísticas por categoría - GET /api/productos/estadisticas/por-categoria"""
        url = f"{self.base_url}/api/productos/estadisticas/por-categoria"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener estadísticas por categoría: {e}")
            return []

    def get_reporte_valor_inventario(self, categoria_id: Optional[int] = None) -> Dict[str, Any]:
        """Reporte de valor de inventario - GET /api/productos/reportes/valor-inventario"""
        url = f"{self.base_url}/api/productos/reportes/valor-inventario"
        params = {}
        if categoria_id:
            params["categoria_id"] = categoria_id

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de valor: {e}")
            return {"total_productos": 0, "valor_total_costo": 0, "productos": []}

    def get_productos_por_margen(self) -> List[Dict[str, Any]]:
        """Productos ordenados por margen de ganancia - GET /api/productos/reportes/margen-ganancia"""
        url = f"{self.base_url}/api/productos/reportes/margen-ganancia"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener productos por margen: {e}")
            return []

    # ==================== PRECIOS ====================

    def actualizar_precios(self, producto_id: int,
                          precio_venta: Optional[float] = None,
                          precio_costo: Optional[float] = None,
                          precio_mayorista: Optional[float] = None,
                          precio_miembro: Optional[float] = None,
                          motivo: str = "Actualización de precios",
                          usuario: Optional[str] = None) -> Dict[str, Any]:
        """Actualizar precios de un producto - PUT /api/productos/{producto_id}/precios"""
        url = f"{self.base_url}/api/productos/{producto_id}/precios"
        data = {"motivo": motivo}

        if precio_venta is not None:
            data["precio_venta"] = precio_venta
        if precio_costo is not None:
            data["precio_costo"] = precio_costo
        if precio_mayorista is not None:
            data["precio_mayorista"] = precio_mayorista
        if precio_miembro is not None:
            data["precio_miembro"] = precio_miembro
        if usuario:
            data["usuario"] = usuario

        try:
            response = self.session.put(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al actualizar precios: {str(e)}")

    def get_historial_precios(self, producto_id: int,
                             tipo_precio: Optional[str] = None,
                             skip: int = 0,
                             limit: int = 50) -> List[Dict[str, Any]]:
        """Ver historial de cambios de precios - GET /api/productos/{producto_id}/historial-precios"""
        url = f"{self.base_url}/api/productos/{producto_id}/historial-precios"
        params = {"skip": skip, "limit": limit}
        if tipo_precio:
            params["tipo_precio"] = tipo_precio

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener historial de precios: {e}")
            return []

    def calcular_precio_producto(self, producto_id: int,
                                 cantidad: int = 1,
                                 es_miembro: bool = False,
                                 aplicar_mayorista: bool = False) -> Dict[str, Any]:
        """Calcular precio final de un producto - POST /api/productos/{producto_id}/calcular-precio"""
        url = f"{self.base_url}/api/productos/{producto_id}/calcular-precio"
        data = {
            "cantidad": cantidad,
            "es_miembro": es_miembro,
            "aplicar_mayorista": aplicar_mayorista
        }

        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al calcular precio: {str(e)}")

    # ==================== VENTAS (POS) ====================

    def crear_venta(self, items: List[Dict[str, Any]],
                    cliente_id: Optional[int] = None,
                    tipo_cliente: str = "Publico",
                    metodo_pago: str = "Efectivo",
                    descuento: float = 0,
                    notas: str = "",
                    usuario_creacion: str = "sistema") -> Dict[str, Any]:
        """
        Crear una venta (desde POS)

        Args:
            items: Lista de productos con id_producto y cantidad
            cliente_id: ID del cliente (opcional)
            tipo_cliente: "Publico", "Miembro", "Mayorista"
            metodo_pago: Método de pago
            descuento: Descuento aplicado
            notas: Notas adicionales
            usuario_creacion: Usuario que registra
        """
        url = f"{self.base_url}/api/ventas"

        # Transformar items al formato que espera el backend
        productos = [
            {
                "id_producto": item.get('id_producto', item.get('producto_id', item.get('id'))),
                "cantidad": item['cantidad']
                # NO enviar precio_unitario - el backend lo calcula automáticamente
            }
            for item in items
        ]

        # Estructura correcta según documentación del backend
        data = {
            "id_cliente": cliente_id,           # Backend espera "id_cliente" no "cliente_id"
            "tipo_cliente": tipo_cliente,       # Requerido por el backend
            "metodo_pago": metodo_pago,
            "descuento": descuento,
            "notas": notas,
            "productos": productos,             # Backend espera "productos" no "items"
            "usuario_creacion": usuario_creacion
        }

        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear venta: {str(e)}")

    def get_ventas(self, fecha_desde: Optional[str] = None,
                   fecha_hasta: Optional[str] = None,
                   estado: Optional[str] = None,
                   id_cliente: Optional[int] = None,
                   tipo_cliente: Optional[str] = None,
                   metodo_pago: Optional[str] = None,
                   skip: int = 0,
                   limit: int = 50) -> List[Dict[str, Any]]:
        """
        Obtener ventas con filtros

        Args:
            fecha_desde: Fecha inicial (YYYY-MM-DD)
            fecha_hasta: Fecha final (YYYY-MM-DD)
            estado: "Completada", "Cancelada", "Pendiente"
            id_cliente: Filtrar por ID de cliente
            tipo_cliente: "Publico", "Miembro", "Mayorista"
            metodo_pago: Filtrar por método de pago
            skip: Registros a saltar (paginación)
            limit: Registros por página (default: 50, max: 500)
        """
        url = f"{self.base_url}/api/ventas"
        params = {}

        # Backend espera "fecha_desde" y "fecha_hasta"
        if fecha_desde:
            params['fecha_desde'] = fecha_desde
        if fecha_hasta:
            params['fecha_hasta'] = fecha_hasta
        if estado:
            params['estado'] = estado
        if id_cliente:
            params['id_cliente'] = id_cliente
        if tipo_cliente:
            params['tipo_cliente'] = tipo_cliente
        if metodo_pago:
            params['metodo_pago'] = metodo_pago
        if skip:
            params['skip'] = skip
        if limit:
            params['limit'] = limit

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener ventas: {e}")
            return []

    def get_venta_por_id(self, venta_id: int) -> Optional[Dict[str, Any]]:
        """Obtener una venta específica por ID (incluye detalles completos)"""
        url = f"{self.base_url}/api/ventas/{venta_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener venta: {e}")
            return None

    def get_venta_por_folio(self, folio: str) -> Optional[Dict[str, Any]]:
        """Buscar venta por folio (ej: VEN-20250113-0001)"""
        url = f"{self.base_url}/api/ventas/folio/{folio}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al buscar venta por folio: {e}")
            return None

    def cancelar_venta(self, venta_id: int, motivo: str, usuario: str = "admin") -> Dict[str, Any]:
        """Cancelar una venta (revierte inventario automáticamente)"""
        url = f"{self.base_url}/api/ventas/{venta_id}/cancelar"
        data = {
            "motivo": motivo,
            "usuario": usuario
        }
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al cancelar venta: {str(e)}")

    def get_reporte_ventas_metodos_pago(self, fecha_desde: Optional[str] = None,
                                         fecha_hasta: Optional[str] = None) -> Dict[str, Any]:
        """Obtener reporte de ventas agrupado por método de pago"""
        url = f"{self.base_url}/api/ventas/reportes/metodos-pago"
        params = {}
        if fecha_desde:
            params['fecha_desde'] = fecha_desde
        if fecha_hasta:
            params['fecha_hasta'] = fecha_hasta

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte por métodos de pago: {e}")
            return {
                "total_general": 0,
                "total_ventas": 0,
                "efectivo": {"cantidad": 0, "total": 0},
                "yape": {"cantidad": 0, "total": 0},
                "otros": {"cantidad": 0, "total": 0}
            }

    def get_estadisticas_ventas_hoy(self) -> Dict[str, Any]:
        """Obtener estadísticas rápidas del día actual"""
        url = f"{self.base_url}/api/ventas/estadisticas/hoy"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener estadísticas de hoy: {e}")
            return {
                "total_ventas": 0,
                "total": 0,
                "ganancia": 0,
                "ticket_promedio": 0
            }

    def get_estadisticas_ventas_mes(self) -> Dict[str, Any]:
        """Obtener estadísticas rápidas del mes actual"""
        url = f"{self.base_url}/api/ventas/estadisticas/mes"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener estadísticas del mes: {e}")
            return {
                "mes": "N/A",
                "total_ventas": 0,
                "total": 0,
                "ganancia": 0,
                "ticket_promedio": 0
            }

    def get_reporte_ventas_diario(self, fecha: Optional[str] = None) -> Dict[str, Any]:
        """Obtener reporte diario de ventas"""
        url = f"{self.base_url}/api/ventas/reportes/diario"
        params = {}
        if fecha:
            params['fecha'] = fecha

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte diario: {e}")
            return {}

    def get_reporte_ventas_semanal(self, fecha: Optional[str] = None) -> Dict[str, Any]:
        """Obtener reporte semanal de ventas"""
        url = f"{self.base_url}/api/ventas/reportes/semanal"
        params = {}
        if fecha:
            params['fecha'] = fecha

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte semanal: {e}")
            return {}

    def get_reporte_ventas_mensual(self, mes: Optional[int] = None, anio: Optional[int] = None) -> Dict[str, Any]:
        """Obtener reporte mensual de ventas"""
        url = f"{self.base_url}/api/ventas/reportes/mensual"
        params = {}
        if mes:
            params['mes'] = mes
        if anio:
            params['anio'] = anio

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte mensual: {e}")
            return {}

    def get_reporte_ventas_anual(self, anio: Optional[int] = None) -> Dict[str, Any]:
        """Obtener reporte anual de ventas"""
        url = f"{self.base_url}/api/ventas/reportes/anual"
        params = {}
        if anio:
            params['anio'] = anio

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte anual: {e}")
            return {}

    # DEPRECATED: Mantener por compatibilidad
    def get_reporte_ventas(self, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None) -> Dict[str, Any]:
        """
        DEPRECATED: Usar get_reporte_ventas_metodos_pago en su lugar
        Obtener reporte de ventas con totales por método de pago
        """
        # Redirigir al nuevo método con nombres correctos
        return self.get_reporte_ventas_metodos_pago(fecha_desde=fecha_inicio, fecha_hasta=fecha_fin)

    # ==================== EGRESOS ====================

    def get_categorias_egresos(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtener categorías de egresos

        Args:
            estado: "Activa" o "Inactiva" (opcional)

        Returns:
            Lista de categorías: [{"id": 1, "nombre": "Servicios", "descripcion": "...", ...}]
        """
        url = f"{self.base_url}/api/egresos/categorias"
        params = {}
        if estado:
            params['estado'] = estado

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener categorías de egresos: {e}")
            return []

    def crear_categoria_egreso(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear nueva categoría de egreso

        Args:
            data: {
                "nombre": "Nueva Categoría",       # Requerido (min 3 chars)
                "descripcion": "Descripción...",   # Opcional
                "estado": "Activa"                 # Opcional (default: "Activa")
            }

        Returns:
            Categoría creada
        """
        url = f"{self.base_url}/api/egresos/categorias"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al crear categoría de egreso: {e}")
            raise

    def get_categoria_egreso_por_id(self, categoria_id: int) -> Optional[Dict[str, Any]]:
        """Obtener categoría de egreso específica por ID"""
        url = f"{self.base_url}/api/egresos/categorias/{categoria_id}"
        print(f"🌐 API GET: {url}")
        try:
            response = self.session.get(url, timeout=self.timeout)
            print(f"📥 Status Code: {response.status_code}")
            result = self._handle_response(response)
            print(f"📥 Resultado: {result}")
            return result
        except Exception as e:
            print(f"❌ Error al obtener categoría de egreso: {e}")
            import traceback
            traceback.print_exc()
            return None

    def actualizar_categoria_egreso(self, categoria_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar categoría de egreso

        Args:
            categoria_id: ID de la categoría
            data: Campos a actualizar (nombre, descripcion, estado)

        Returns:
            Categoría actualizada
        """
        url = f"{self.base_url}/api/egresos/categorias/{categoria_id}"
        print(f"🌐 API PATCH: {url}")
        print(f"📤 Datos: {data}")
        try:
            response = self.session.patch(url, json=data, timeout=self.timeout)
            print(f"📥 Status Code: {response.status_code}")
            result = self._handle_response(response)
            print(f"📥 Resultado: {result}")
            return result
        except Exception as e:
            print(f"❌ Error al actualizar categoría de egreso: {e}")
            import traceback
            traceback.print_exc()
            raise

    def eliminar_categoria_egreso(self, categoria_id: int) -> bool:
        """Eliminar categoría de egreso (solo si no tiene egresos asociados)"""
        url = f"{self.base_url}/api/egresos/categorias/{categoria_id}"
        print(f"🌐 API DELETE: {url}")
        try:
            response = self.session.delete(url, timeout=self.timeout)
            print(f"📥 Status Code: {response.status_code}")
            print(f"📥 Response text: {response.text}")
            success = response.status_code in [200, 204]
            print(f"📥 Resultado: {success}")
            return success
        except Exception as e:
            print(f"❌ Error al eliminar categoría de egreso: {e}")
            import traceback
            traceback.print_exc()
            return False

    def crear_egreso(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear nuevo egreso

        Args:
            data: {
                "id_categoria": 1,              # Requerido
                "concepto": "Pago de luz",      # Requerido (min 3 chars)
                "descripcion": "Consumo enero", # Opcional
                "monto": 1500.00,               # Requerido (> 0)
                "metodo_pago": "Transferencia", # Requerido
                "fecha_egreso": "2025-01-15",   # Requerido (YYYY-MM-DD)
                "proveedor": "CFE",             # Opcional
                "numero_factura": "FAC-001",    # Opcional
                "estado": "Pagado",             # Opcional (default: "Pagado")
                "es_recurrente": true,          # Opcional (default: false)
                "frecuencia": "Mensual",        # Opcional
                "notas": "...",                 # Opcional
                "usuario_creacion": "admin"     # Opcional
            }

        Returns:
            Egreso creado con folio generado automáticamente
        """
        url = f"{self.base_url}/api/egresos"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al crear egreso: {str(e)}")

    def get_egresos(self,
                    fecha_desde: Optional[str] = None,
                    fecha_hasta: Optional[str] = None,
                    id_categoria: Optional[int] = None,
                    estado: Optional[str] = None,
                    skip: int = 0,
                    limit: int = 50) -> List[Dict[str, Any]]:
        """
        Obtener lista de egresos con filtros

        Args:
            fecha_desde: Fecha inicial (YYYY-MM-DD)
            fecha_hasta: Fecha final (YYYY-MM-DD)
            id_categoria: Filtrar por categoría
            estado: "Pagado", "Pendiente", "Cancelado"
            skip: Registros a saltar (paginación)
            limit: Registros por página (default: 50, max: 500)

        Returns:
            Lista de egresos
        """
        url = f"{self.base_url}/api/egresos"
        params = {}
        if fecha_desde:
            params['fecha_desde'] = fecha_desde
        if fecha_hasta:
            params['fecha_hasta'] = fecha_hasta
        if id_categoria:
            params['id_categoria'] = id_categoria
        if estado:
            params['estado'] = estado
        if skip:
            params['skip'] = skip
        if limit:
            params['limit'] = limit

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener egresos: {e}")
            return []

    def get_egreso_por_id(self, egreso_id: int) -> Optional[Dict[str, Any]]:
        """Obtener egreso específico por ID"""
        url = f"{self.base_url}/api/egresos/{egreso_id}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener egreso: {e}")
            return None

    def actualizar_egreso(self, egreso_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar egreso (PATCH - todos los campos son opcionales)

        Args:
            egreso_id: ID del egreso
            data: Campos a actualizar (cualquiera de los del create)
        """
        url = f"{self.base_url}/api/egresos/{egreso_id}"
        try:
            response = self.session.patch(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            raise ValueError(f"Error al actualizar egreso: {str(e)}")

    def eliminar_egreso(self, egreso_id: int) -> bool:
        """Eliminar egreso"""
        url = f"{self.base_url}/api/egresos/{egreso_id}"
        try:
            response = self.session.delete(url, timeout=self.timeout)
            self._handle_response(response)
            return True
        except Exception as e:
            raise ValueError(f"Error al eliminar egreso: {str(e)}")

    def get_egreso_por_folio(self, folio: str) -> Optional[Dict[str, Any]]:
        """
        Obtener egreso específico por folio

        Args:
            folio: Folio del egreso (ej: "EGR-20250113-0001")

        Returns:
            Egreso completo o None si no existe
        """
        url = f"{self.base_url}/api/egresos/folio/{folio}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener egreso por folio: {e}")
            return None

    def get_reporte_egresos_por_categoria(self,
                                           fecha_desde: Optional[str] = None,
                                           fecha_hasta: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener reporte de egresos agrupado por categoría

        Returns:
            {
                "fecha_desde": "2025-01-01",
                "fecha_hasta": "2025-01-31",
                "total_egresos": 45,
                "total_monto": 25000.00,
                "egresos_por_categoria": [
                    {"categoria": "Sueldos", "cantidad": 15, "total": 12000.00},
                    ...
                ]
            }
        """
        url = f"{self.base_url}/api/egresos/reportes/por-categoria"
        params = {}
        if fecha_desde:
            params['fecha_desde'] = fecha_desde
        if fecha_hasta:
            params['fecha_hasta'] = fecha_hasta

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte de egresos: {e}")
            return {
                "total_egresos": 0,
                "total_monto": 0,
                "egresos_por_categoria": []
            }

    # ==================== REPORTES FINANCIEROS ====================

    def get_reporte_financiero_diario(self, fecha: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener reporte financiero completo del día

        Incluye:
        - Ingresos por membresías
        - Ingresos por ventas de productos
        - Ganancia de productos
        - Egresos del día
        - Ganancia neta final (lo más importante)

        Args:
            fecha: Fecha del reporte (YYYY-MM-DD), default: hoy

        Returns:
            {
                "fecha": "2025-01-15",
                "ingresos_membresias": 15000.00,
                "ingresos_productos": 8000.00,
                "ganancia_productos": 3000.00,
                "total_ingresos": 23000.00,
                "total_egresos": 5000.00,
                "ganancia_neta": 13000.00,      # ← Lo más importante
                "margen_neto": 56.52,
                "detalle_ingresos": {...},
                "detalle_egresos": {...}
            }
        """
        url = f"{self.base_url}/api/egresos/reportes/financiero-diario"
        params = {}
        if fecha:
            params['fecha'] = fecha

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte financiero diario: {e}")
            return {
                "fecha": fecha or "",
                "ingresos_membresias": 0,
                "ingresos_productos": 0,
                "ganancia_productos": 0,
                "total_ingresos": 0,
                "total_egresos": 0,
                "ganancia_neta": 0,
                "margen_neto": 0
            }

    def get_reporte_financiero_mensual(self,
                                         mes: Optional[int] = None,
                                         anio: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtener reporte financiero mensual completo

        Args:
            mes: Mes (1-12), default: mes actual
            anio: Año, default: año actual

        Returns:
            Similar al diario + ingresos por día, egresos por día, mejor día del mes
        """
        url = f"{self.base_url}/api/egresos/reportes/financiero-mensual"
        params = {}
        if mes:
            params['mes'] = mes
        if anio:
            params['anio'] = anio

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte financiero mensual: {e}")
            return {}

    def get_reporte_financiero_anual(self, anio: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtener reporte financiero anual completo

        Args:
            anio: Año, default: año actual

        Returns:
            Similar al mensual + ingresos por mes, mejor/peor mes del año
        """
        url = f"{self.base_url}/api/egresos/reportes/financiero-anual"
        params = {}
        if anio:
            params['anio'] = anio

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener reporte financiero anual: {e}")
            return {}

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
