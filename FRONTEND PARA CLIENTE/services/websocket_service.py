"""
Servicio WebSocket para notificaciones en tiempo real
Notifica al admin cuando hay nuevos registros (especialmente con Yape)
"""

import json
import threading
from typing import Optional, Dict, Any

try:
    import websocket
    WEBSOCKET_AVAILABLE = True
    print("✅ Módulo websocket-client importado correctamente")
except ImportError as e:
    WEBSOCKET_AVAILABLE = False
    print("⚠️ Módulo 'websocket-client' no disponible. Instalar con: pip install websocket-client")
    print(f"   Error de import: {e}")


class WebSocketService:
    """Servicio para enviar notificaciones WebSocket al admin"""

    def __init__(self, ws_url: str = "ws://localhost:8000/ws/notificaciones"):
        """
        Inicializar servicio WebSocket

        Args:
            ws_url: URL del WebSocket del backend
        """
        self.ws_url = ws_url
        self.ws = None
        self.connected = False

    def conectar(self):
        """Conectar al WebSocket del backend"""
        if not WEBSOCKET_AVAILABLE:
            print("⚠️ WebSocket no disponible - notificaciones deshabilitadas")
            return False

        try:
            print(f"🔌 Conectando a WebSocket: {self.ws_url}")
            self.ws = websocket.create_connection(self.ws_url, timeout=5)
            self.connected = True
            print("✅ WebSocket conectado")
            return True
        except Exception as e:
            print(f"❌ Error al conectar WebSocket: {e}")
            self.connected = False
            return False

    def enviar_notificacion_registro(
        self,
        cliente: Dict[str, Any],
        membresia: Dict[str, Any],
        metodo_pago: str,
        pago: Optional[Dict[str, Any]] = None
    ):
        """
        Enviar notificación de nuevo registro al admin

        Args:
            cliente: Datos del cliente registrado
            membresia: Datos de la membresía seleccionada
            metodo_pago: Método de pago usado
            pago: Información del pago (opcional)
        """
        if not WEBSOCKET_AVAILABLE:
            print("⚠️ WebSocket no disponible - notificación no enviada")
            return

        # Si no está conectado, intentar conectar
        if not self.connected:
            if not self.conectar():
                print("⚠️ No se pudo conectar al WebSocket - notificación no enviada")
                return

        try:
            # Construir mensaje de notificación
            # TODOS los pagos (Yape y Efectivo) requieren confirmación del admin
            notificacion = {
                "evento": "nuevo_registro",
                "tipo": "registro_cliente",
                "prioridad": "alta",  # Siempre alta porque TODOS requieren confirmación
                "datos": {
                    "cliente": {
                        "dni": cliente.get("dni", ""),
                        "nombre_completo": f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}",
                        "correo": cliente.get("correo", ""),
                        "telefono": cliente.get("telefono", "")
                    },
                    "membresia": {
                        "nombre": membresia.get("nombre", ""),
                        "precio": membresia.get("precio", 0),
                        "duracion_dias": membresia.get("duracion_dias", 0)
                    },
                    "pago": {
                        "metodo": metodo_pago,
                        "monto": pago.get("monto", 0) if pago else membresia.get("precio", 0),
                        "estado": pago.get("estado", "Pendiente") if pago else "Pendiente",
                        "requiere_confirmacion": True  # SIEMPRE requiere confirmación
                    }
                },
                "mensaje": self._generar_mensaje_notificacion(cliente, metodo_pago)
            }

            # Enviar notificación
            print(f"📤 Enviando notificación WebSocket: {notificacion}")
            self.ws.send(json.dumps(notificacion))
            print("✅ Notificación enviada al admin")

        except Exception as e:
            print(f"❌ Error al enviar notificación WebSocket: {e}")
            self.connected = False

    def _generar_mensaje_notificacion(self, cliente: Dict[str, Any], metodo_pago: str) -> str:
        """Generar mensaje de notificación"""
        nombre = f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}"
        dni = cliente.get('dni', '')

        # TODOS los pagos requieren confirmación del admin
        return f"⚠️ NUEVO REGISTRO - {nombre} (DNI: {dni}) - Pago: {metodo_pago.upper()} - CONFIRMAR"

    def desconectar(self):
        """Desconectar del WebSocket"""
        if self.ws and self.connected:
            try:
                self.ws.close()
                print("🔌 WebSocket desconectado")
            except:
                pass
            finally:
                self.connected = False

    def __del__(self):
        """Destructor - cerrar conexión"""
        self.desconectar()


# Función auxiliar para enviar notificación en segundo plano (no bloquear UI)
def enviar_notificacion_async(
    cliente: Dict[str, Any],
    membresia: Dict[str, Any],
    metodo_pago: str,
    pago: Optional[Dict[str, Any]] = None,
    ws_url: str = "ws://localhost:8000/ws/notificaciones"
):
    """
    Enviar notificación en segundo plano (thread separado)

    Args:
        cliente: Datos del cliente
        membresia: Datos de la membresía
        metodo_pago: Método de pago
        pago: Información del pago (opcional)
        ws_url: URL del WebSocket
    """
    def _enviar():
        ws_service = WebSocketService(ws_url)
        ws_service.enviar_notificacion_registro(cliente, membresia, metodo_pago, pago)
        ws_service.desconectar()

    # Ejecutar en thread separado para no bloquear la UI
    thread = threading.Thread(target=_enviar, daemon=True)
    thread.start()
