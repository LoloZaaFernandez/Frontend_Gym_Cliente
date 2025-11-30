"""
Servicio API para Frontend Cliente (Tablet)
Maneja todas las comunicaciones con el backend para registro y asistencias
"""

from typing import Optional, Dict, Any, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta


class APIService:
    """Servicio para comunicación con el backend API"""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Inicializar el servicio API con reconexión automática

        Args:
            base_url: URL base del backend
            timeout: Tiempo de espera para las peticiones (segundos)
        """
        self.base_url = base_url
        self.timeout = timeout
        self._create_session()

    def _create_session(self):
        """Crear o recrear la sesión HTTP con retry automático"""
        self.session = requests.Session()

        # Configurar retry automático
        retry_strategy = Retry(
            total=3,  # 3 intentos
            backoff_factor=1,  # Espera 1s, 2s, 4s entre reintentos
            status_forcelist=[500, 502, 503, 504],  # Reintentar en estos errores
            allowed_methods=["GET", "POST", "PUT", "DELETE"]  # Métodos para reintentar
        )

        # Configurar adapter HTTP con retry
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )

        # Montar el adapter para http y https
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Headers comunes
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Connection': 'keep-alive'  # Mantener conexión viva
        })

    def _handle_response(self, response: requests.Response) -> Any:
        """Manejar la respuesta de la API"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            # Error de conexión - intentar recrear la sesión
            print(f"ERROR: Pérdida de conexión con el backend. Recreando sesión...")
            self._create_session()
            raise ValueError("No se pudo conectar con el backend. Verifica que esté corriendo.")
        except requests.exceptions.Timeout as e:
            # Timeout - probablemente red lenta o backend ocupado
            print(f"ERROR: Timeout al conectar con el backend")
            raise ValueError("El backend tardó demasiado en responder. Intenta de nuevo.")
        except requests.exceptions.HTTPError as e:
            # Intentar obtener detalles del error del backend
            error_detail = None
            try:
                error_data = response.json()
                error_detail = error_data.get('detail') or error_data.get('error') or error_data.get('message')
                # Imprimir el error completo para debugging
                print(f"ERROR del backend - Status {response.status_code}:")
                print(f"Detalles: {error_data}")
            except:
                # Si no se puede parsear el JSON, intentar obtener el texto
                error_detail = response.text[:200] if response.text else None
                print(f"ERROR del backend - Status {response.status_code}:")
                print(f"Respuesta: {response.text[:500]}")

            if response.status_code == 404:
                raise ValueError("Recurso no encontrado")
            elif response.status_code == 400:
                raise ValueError(f"Error: {error_detail or 'Error en la solicitud'}")
            elif response.status_code == 500:
                raise ValueError(f"Error interno del servidor: {error_detail or 'Revisa los logs del backend'}")
            else:
                raise ValueError(f"Error HTTP {response.status_code}: {error_detail or str(e)}")
        except ValueError:
            # Re-lanzar los ValueError que ya creamos
            raise
        except Exception as e:
            raise ValueError(f"Error en la comunicación con el servidor: {str(e)}")

    # ==================== VERIFICACIÓN Y REGISTRO ====================

    def verificar_dni(self, dni: str) -> Dict[str, Any]:
        """
        Verificar si un DNI está disponible para registro

        Endpoint: GET /api/registro/verificar-dni/{dni}

        Args:
            dni: Número de DNI a verificar

        Returns:
            {
                "dni": "12345678",
                "disponible": true/false,
                "mensaje": "DNI disponible" o "DNI ya registrado"
            }
        """
        url = f"{self.base_url}/api/registro/verificar-dni/{dni}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al verificar DNI: {e}")
            raise

    def get_opciones_registro(self) -> Dict[str, Any]:
        """
        Obtener opciones de membresías y métodos de pago disponibles

        Endpoint: GET /api/registro/opciones

        Returns:
            {
                "membresias": [
                    {"id": 1, "nombre": "Básica", "precio": 100.0, "duracion_dias": 30},
                    ...
                ],
                "metodos_pago": ["Efectivo", "Yape", "Transferencia"]
            }
        """
        url = f"{self.base_url}/api/registro/opciones"
        print(f"API GET: {url}")
        try:
            response = self.session.get(url, timeout=self.timeout)
            print(f"Status Code: {response.status_code}")
            resultado = self._handle_response(response)
            print(f"Respuesta del backend: {resultado}")
            return resultado
        except Exception as e:
            print(f"ERROR - Error al obtener opciones de registro: {e}")
            import traceback
            traceback.print_exc()
            raise

    def registrar_cliente_con_validacion(
        self,
        dni: str,
        nombre: str,
        apellidos: str,
        correo: str,
        telefono: str,
        id_membresia: int,
        metodo_pago: str,
        usuario_creacion: str = "tablet_gym"
    ) -> Dict[str, Any]:
        """
        Crear registro pendiente de confirmación

        Endpoint: POST /api/registro/cliente-con-validacion

        Este endpoint crea un registro PENDIENTE que debe ser confirmado por el administrador.

        Args:
            dni: Número de DNI
            nombre: Nombre del cliente
            apellidos: Apellidos del cliente
            correo: Correo electrónico
            telefono: Número de teléfono
            id_membresia: ID de la membresía seleccionada
            metodo_pago: Método de pago ("Efectivo", "Yape")
            usuario_creacion: Usuario que registra (default: "tablet_gym")

        Returns:
            {
                "registro_creado": true,
                "id_registro_pendiente": 5,
                "mensaje": "Registro pendiente creado. Esperando confirmación...",
                "resumen": {
                    "nombre_completo": "Juan Pérez García",
                    "dni": "12345678",
                    "metodo_pago": "Efectivo",
                    "monto": 150.00,
                    "tipo_membresia": "Mensual",
                    "nombre_membresia": "Membresía Mensual"
                }
            }
        """
        url = f"{self.base_url}/api/registro/cliente-con-validacion"
        data = {
            "confirmar_registro": "preparar",
            "dni": dni,
            "nombre": nombre,
            "apellidos": apellidos,
            "correo": correo,
            "telefono": telefono,
            "id_membresia": id_membresia,
            "metodo_pago": metodo_pago,
            "usuario_creacion": usuario_creacion
        }

        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al registrar cliente: {e}")
            raise

    def renovar_membresia_cliente(
        self,
        dni: str,
        id_membresia: int,
        metodo_pago: str,
        usuario_creacion: str = "tablet_gym"
    ) -> Dict[str, Any]:
        """
        Renovar membresía de un cliente existente

        Endpoint: POST /api/registro/renovar-membresia

        Este endpoint crea un registro PENDIENTE de renovación que debe ser confirmado por el administrador.

        Args:
            dni: Número de DNI del cliente
            id_membresia: ID de la nueva membresía
            metodo_pago: Método de pago ("Efectivo", "Yape")
            usuario_creacion: Usuario que registra (default: "tablet_gym")

        Returns:
            {
                "renovacion_creada": true,
                "id_registro_pendiente": 6,
                "mensaje": "Renovación pendiente creada. Esperando confirmación...",
                "resumen": {
                    "nombre_completo": "Juan Pérez García",
                    "dni": "12345678",
                    "metodo_pago": "Efectivo",
                    "monto": 150.00,
                    "tipo_membresia": "Mensual",
                    "nombre_membresia": "Membresía Mensual"
                }
            }
        """
        url = f"{self.base_url}/api/registro/renovar-membresia"
        data = {
            "dni": dni,
            "id_membresia": id_membresia,
            "metodo_pago": metodo_pago,
            "usuario_creacion": usuario_creacion
        }

        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al renovar membresía: {e}")
            raise

    # ==================== CLIENTES ====================

    def get_cliente_por_dni(self, dni: str) -> Optional[Dict[str, Any]]:
        """
        Obtener información de un cliente por DNI

        Endpoint: GET /api/clientes/dni/{dni}

        Args:
            dni: Número de DNI del cliente

        Returns:
            Cliente con toda su información incluyendo:
            - datos personales
            - fecha_membresia (fecha de vencimiento)
            - estado
            - tipo_membresia
        """
        url = f"{self.base_url}/api/clientes/dni/{dni}"
        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al obtener cliente por DNI: {e}")
            return None

    # ==================== ASISTENCIAS ====================

    def registrar_asistencia(
        self,
        dni: str,
        usuario_creacion: str = "tablet_gym"
    ) -> Dict[str, Any]:
        """
        Registrar asistencia de un cliente

        Endpoint: POST /api/asistencias

        Args:
            dni: Número de DNI del cliente
            usuario_creacion: Usuario que registra (default: "tablet_gym")

        Returns:
            {
                "id": 123,
                "cliente_id": 45,
                "dni": "12345678",
                "nombre_completo": "Juan Pérez",
                "fecha_asistencia": "2025-01-14T10:30:00",
                "mensaje": "Asistencia registrada correctamente"
            }
        """
        url = f"{self.base_url}/api/asistencias"
        data = {
            "dni": dni,
            "usuario_creacion": usuario_creacion
        }

        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(f"Error al registrar asistencia: {e}")
            raise

    # ==================== UTILIDADES ====================

    def verificar_membresia_por_vencer(self, cliente: Dict[str, Any], dias_alerta: int = 5) -> Optional[Dict[str, str]]:
        """
        Verificar si la membresía de un cliente está por vencer

        Args:
            cliente: Diccionario con información del cliente (debe incluir 'fecha_membresia')
            dias_alerta: Días antes del vencimiento para alertar (default: 5)

        Returns:
            None si no hay alerta, o dict con:
            {
                "tipo": "vencida" o "por_vencer",
                "dias_restantes": -3 o 2,
                "mensaje": "Tu membresía venció hace 3 días" o "Tu membresía vence en 2 días"
            }
        """
        if not cliente or 'fecha_membresia' not in cliente:
            return None

        try:
            # La fecha_membresia viene del backend en formato ISO string
            fecha_membresia_str = cliente['fecha_membresia']

            # Convertir a datetime (puede venir con o sin timezone)
            if 'T' in fecha_membresia_str:
                # Formato con hora: "2025-01-20T00:00:00"
                fecha_membresia = datetime.fromisoformat(fecha_membresia_str.replace('Z', '+00:00'))
            else:
                # Formato solo fecha: "2025-01-20"
                fecha_membresia = datetime.strptime(fecha_membresia_str, '%Y-%m-%d')

            # Obtener fecha actual (sin hora para comparación de días)
            fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            fecha_membresia = fecha_membresia.replace(hour=0, minute=0, second=0, microsecond=0)

            # Calcular días restantes
            dias_restantes = (fecha_membresia - fecha_actual).days

            # Membresía vencida
            if dias_restantes < 0:
                return {
                    "tipo": "vencida",
                    "dias_restantes": dias_restantes,
                    "mensaje": f"ALERTA: Tu membresia vencio hace {abs(dias_restantes)} dias. Renuevala pronto!"
                }

            # Membresía por vencer
            elif dias_restantes <= dias_alerta:
                if dias_restantes == 0:
                    mensaje = "ALERTA: Tu membresia vence HOY. No olvides renovarla!"
                elif dias_restantes == 1:
                    mensaje = "ALERTA: Tu membresia vence MAÑANA. No olvides renovarla!"
                else:
                    mensaje = f"ALERTA: Tu membresia vence en {dias_restantes} dias. No olvides renovarla!"

                return {
                    "tipo": "por_vencer",
                    "dias_restantes": dias_restantes,
                    "mensaje": mensaje
                }

            # Membresía activa sin alerta
            return None

        except Exception as e:
            print(f"Error al verificar vencimiento de membresía: {e}")
            return None

    def health_check(self) -> bool:
        """
        Verificar si el backend está disponible

        Returns:
            True si el backend responde, False en caso contrario
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
