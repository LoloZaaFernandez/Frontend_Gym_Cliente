"""
Servicio de WebSocket para recibir notificaciones en tiempo real
"""

import threading
import json
import time
from typing import Callable, Optional
try:
    from websocket import WebSocketApp
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("⚠️ websocket-client no está instalado. Ejecuta: pip install websocket-client")

from config.settings import API_BASE_URL


class WebSocketService:
    """Servicio para manejar conexiones WebSocket con el backend"""

    def __init__(self, on_message_callback: Optional[Callable] = None):
        """
        Inicializar el servicio de WebSocket

        Args:
            on_message_callback: Función a llamar cuando se recibe un mensaje
        """
        if not WEBSOCKET_AVAILABLE:
            print("❌ WebSocket no disponible - websocket-client no instalado")
            self.url = None
            self.on_message_callback = None
            self.ws = None
            self.thread = None
            self.is_running = False
            return

        # Convertir URL HTTP a WebSocket
        ws_url = API_BASE_URL.replace("http://", "ws://").replace("https://", "wss://")
        self.url = f"{ws_url}/ws/notificaciones"
        self.on_message_callback = on_message_callback
        self.ws: Optional[WebSocketApp] = None
        self.thread: Optional[threading.Thread] = None
        self.is_running = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

    def _on_message(self, ws, message):
        """Callback cuando se recibe un mensaje"""
        try:
            data = json.loads(message)
            print(f"📩 WebSocket - Mensaje recibido: {data.get('tipo', 'desconocido')}")

            if self.on_message_callback:
                self.on_message_callback(data)
        except Exception as e:
            print(f"❌ Error al procesar mensaje WebSocket: {e}")

    def _on_error(self, ws, error):
        """Callback cuando hay un error"""
        print(f"❌ WebSocket - Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """Callback cuando se cierra la conexión"""
        print(f"🔌 WebSocket - Conexión cerrada: {close_msg} (código: {close_status_code})")
        self.is_running = False

        # Intentar reconectar si no fue un cierre intencional
        if self.reconnect_attempts < self.max_reconnect_attempts and close_status_code != 1000:
            self.reconnect_attempts += 1
            print(f"🔄 Intentando reconectar ({self.reconnect_attempts}/{self.max_reconnect_attempts})...")
            time.sleep(2)
            self.connect()

    def _on_open(self, ws):
        """Callback cuando se abre la conexión"""
        print(f"✅ WebSocket - Conectado a {self.url}")
        self.is_running = True
        self.reconnect_attempts = 0  # Reset intentos al conectar exitosamente

        # Enviar ping inicial para mantener viva la conexión
        try:
            ws.send(json.dumps({"tipo": "ping"}))
        except Exception as e:
            print(f"⚠️ Error enviando ping inicial: {e}")

    def connect(self):
        """Conectar al WebSocket en un hilo separado"""
        if not WEBSOCKET_AVAILABLE:
            print("❌ No se puede conectar - websocket-client no está instalado")
            return

        if self.is_running:
            print("⚠️ WebSocket ya está conectado")
            return

        try:
            print(f"🔄 WebSocket - Iniciando conexión a {self.url}...")

            self.ws = WebSocketApp(
                self.url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )

            # Ejecutar en un hilo separado para no bloquear la UI
            self.thread = threading.Thread(target=self._run_forever_with_ping, daemon=True)
            self.thread.start()

        except Exception as e:
            print(f"❌ Error al conectar WebSocket: {e}")
            self.is_running = False

    def _run_forever_with_ping(self):
        """Ejecutar WebSocket con ping periódico para mantener la conexión"""
        try:
            self.ws.run_forever(ping_interval=30, ping_timeout=10)
        except Exception as e:
            print(f"❌ Error en run_forever: {e}")
            self.is_running = False

    def disconnect(self):
        """Desconectar del WebSocket"""
        if self.ws:
            self.ws.close()
            self.is_running = False
            print("🔌 WebSocket - Desconectado")

    def send_message(self, message: dict):
        """Enviar un mensaje al WebSocket"""
        if self.ws and self.is_running:
            try:
                self.ws.send(json.dumps(message))
            except Exception as e:
                print(f"❌ Error al enviar mensaje WebSocket: {e}")
        else:
            print("⚠️ WebSocket no está conectado")
