"""
Vista de Configuración de API
Permite configurar la IP y puerto del servidor API
"""
import flet as ft
import sys
import os
import re

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme
from config.settings import BACKGROUND_IMAGE
from components.buttons import create_large_button, create_back_button
from components.inputs import create_text_input
from components.cards import create_alert_card
from utils.config_manager import get_config_manager
from services.api_service import APIService


def show_configuracion_view(page: ft.Page, on_back, on_config_saved=None):
    """
    Mostrar vista de configuración de API

    Args:
        page: Instancia de la página de Flet
        on_back: Función para volver a la pantalla anterior
        on_config_saved: Callback opcional cuando se guarda la configuración
    """
    page.clean()
    page.bgcolor = Theme.BACKGROUND_DARK

    # Obtener dimensiones de la página
    page_width = page.window.width or page.width or Theme.BASE_WIDTH
    page_height = page.window.height or page.height or Theme.BASE_HEIGHT

    # Obtener gestor de configuración
    config_manager = get_config_manager()

    # Cargar valores actuales
    current_host = config_manager.config.get("api_host", "localhost")
    current_port = config_manager.config.get("api_port", 8000)
    current_timeout = config_manager.config.get("api_timeout", 30)

    # Controles
    mensaje_container = ft.Container()

    # Inputs con valores actuales
    host_input = create_text_input(
        label="IP o Hostname del Servidor",
        hint_text="Ej: 192.168.1.100 o localhost",
        icon=ft.Icons.COMPUTER_ROUNDED,
        value=current_host,
        page_width=page_width,
        page_height=page_height
    )

    port_input = create_text_input(
        label="Puerto",
        hint_text="Ej: 8000",
        icon=ft.Icons.NUMBERS_ROUNDED,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=5,
        value=str(current_port),
        page_width=page_width,
        page_height=page_height
    )

    timeout_input = create_text_input(
        label="Timeout (segundos)",
        hint_text="Ej: 30",
        icon=ft.Icons.TIMER_ROUNDED,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=3,
        value=str(current_timeout),
        page_width=page_width,
        page_height=page_height
    )

    # Estado de conexión
    conexion_status = ft.Container()

    def mostrar_mensaje(mensaje: str, tipo: str = "info"):
        """Mostrar mensaje de feedback"""
        mensaje_container.content = create_alert_card(mensaje, tipo, page_width=page_width)
        mensaje_container.update()

    def limpiar_mensaje():
        """Limpiar mensaje"""
        mensaje_container.content = None
        mensaje_container.update()

    def validar_ip(ip: str) -> bool:
        """Validar formato de IP"""
        # Permitir localhost
        if ip.lower() in ["localhost", "127.0.0.1"]:
            return True

        # Validar formato IP (simple)
        patron = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(patron, ip):
            # Verificar que cada octeto esté en rango 0-255
            octetos = ip.split('.')
            return all(0 <= int(octeto) <= 255 for octeto in octetos)

        # Permitir hostnames (letras, números, guiones, puntos)
        patron_hostname = r'^[a-zA-Z0-9][a-zA-Z0-9\-\.]*[a-zA-Z0-9]$'
        return bool(re.match(patron_hostname, ip))

    def validar_puerto(puerto_str: str) -> tuple:
        """
        Validar puerto

        Returns:
            (bool, int): (es_valido, puerto_int)
        """
        try:
            puerto = int(puerto_str)
            if 1 <= puerto <= 65535:
                return True, puerto
            return False, 0
        except ValueError:
            return False, 0

    def validar_timeout(timeout_str: str) -> tuple:
        """
        Validar timeout

        Returns:
            (bool, int): (es_valido, timeout_int)
        """
        try:
            timeout = int(timeout_str)
            if 5 <= timeout <= 300:  # Entre 5 y 300 segundos
                return True, timeout
            return False, 0
        except ValueError:
            return False, 0

    def probar_conexion(e):
        """Probar conexión con el servidor"""
        limpiar_mensaje()

        # Validar inputs
        if not host_input.value:
            mostrar_mensaje("Debes ingresar una IP o hostname", "error")
            return

        if not validar_ip(host_input.value):
            mostrar_mensaje("IP o hostname inválido", "error")
            return

        puerto_valido, puerto = validar_puerto(port_input.value or "0")
        if not puerto_valido:
            mostrar_mensaje("Puerto debe estar entre 1 y 65535", "error")
            return

        timeout_valido, timeout = validar_timeout(timeout_input.value or "0")
        if not timeout_valido:
            mostrar_mensaje("Timeout debe estar entre 5 y 300 segundos", "error")
            return

        # Construir URL de prueba
        test_url = f"http://{host_input.value}:{puerto}"

        # Mostrar estado de prueba
        conexion_status.content = ft.Row([
            ft.ProgressRing(width=24, height=24, stroke_width=3, color=Theme.PRIMARY),
            ft.Text(
                f"Probando conexión a {test_url}...",
                size=Theme.FONT_SIZE["md"],
                color=Theme.TEXT_SECONDARY
            )
        ], spacing=Theme.SPACING["sm"])
        conexion_status.update()

        # Intentar conexión
        try:
            api_service = APIService(base_url=test_url, timeout=timeout)
            if api_service.health_check():
                # Conexión exitosa
                conexion_status.content = ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=Theme.SUCCESS, size=28),
                    ft.Text(
                        "✓ Conexión exitosa",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.SUCCESS
                    )
                ], spacing=Theme.SPACING["sm"])
                mostrar_mensaje(
                    f"Conexión exitosa con el servidor en {test_url}",
                    "success"
                )
            else:
                # Conexión fallida
                conexion_status.content = ft.Row([
                    ft.Icon(ft.Icons.ERROR_ROUNDED, color=Theme.ERROR, size=28),
                    ft.Text(
                        "✗ No se pudo conectar",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.ERROR
                    )
                ], spacing=Theme.SPACING["sm"])
                mostrar_mensaje(
                    f"No se pudo conectar con el servidor en {test_url}",
                    "error"
                )
        except Exception as e:
            conexion_status.content = ft.Row([
                ft.Icon(ft.Icons.ERROR_ROUNDED, color=Theme.ERROR, size=28),
                ft.Text(
                    "✗ Error de conexión",
                    size=Theme.FONT_SIZE["lg"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.ERROR
                )
            ], spacing=Theme.SPACING["sm"])
            mostrar_mensaje(
                f"Error al conectar: {str(e)}",
                "error"
            )

        conexion_status.update()

    def guardar_configuracion(e):
        """Guardar configuración"""
        limpiar_mensaje()

        # Validar inputs
        if not host_input.value:
            mostrar_mensaje("Debes ingresar una IP o hostname", "error")
            return

        if not validar_ip(host_input.value):
            mostrar_mensaje("IP o hostname inválido", "error")
            return

        puerto_valido, puerto = validar_puerto(port_input.value or "0")
        if not puerto_valido:
            mostrar_mensaje("Puerto debe estar entre 1 y 65535", "error")
            return

        timeout_valido, timeout = validar_timeout(timeout_input.value or "0")
        if not timeout_valido:
            mostrar_mensaje("Timeout debe estar entre 5 y 300 segundos", "error")
            return

        # Guardar configuración
        if config_manager.set_api_config(host_input.value, puerto, timeout):
            mostrar_mensaje(
                f"✓ Configuración guardada exitosamente\n\nNueva URL: {config_manager.get_api_base_url()}",
                "success"
            )

            # Llamar callback si existe
            if on_config_saved:
                on_config_saved()

            # Mostrar confirmación visual
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Configuración guardada. Reinicia la aplicación para aplicar cambios.",
                    color=ft.Colors.WHITE
                ),
                bgcolor=Theme.SUCCESS,
                duration=4000
            )
            page.snack_bar.open = True
            page.update()
        else:
            mostrar_mensaje("Error al guardar la configuración", "error")

    def resetear_configuracion(e):
        """Resetear a valores por defecto"""
        if config_manager.reset_to_default():
            host_input.value = config_manager.config["api_host"]
            port_input.value = str(config_manager.config["api_port"])
            timeout_input.value = str(config_manager.config["api_timeout"])
            host_input.update()
            port_input.update()
            timeout_input.update()
            mostrar_mensaje("Configuración restablecida a valores por defecto", "info")
            conexion_status.content = None
            conexion_status.update()

    # ==================== CONTENIDO PRINCIPAL ====================

    # Header
    header = ft.Container(
        content=ft.Column([
            # Ícono de configuración
            ft.Container(
                content=ft.Icon(
                    ft.Icons.SETTINGS_ROUNDED,
                    size=Theme.ICON_SIZE["2xl"],
                    color=Theme.PRIMARY
                ),
                width=120,
                height=120,
                bgcolor="rgba(159, 255, 51, 0.1)",
                border_radius=60,
                border=ft.border.all(3, Theme.PRIMARY),
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=25,
                    color="rgba(159, 255, 51, 0.3)",
                    offset=ft.Offset(0, 0),
                ),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            ft.Text(
                "Configuración de API",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["extrabold"],
                color=Theme.PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Container(height=Theme.SPACING["sm"]),

            ft.Text(
                "Configura la conexión con el servidor API",
                size=Theme.FONT_SIZE["lg"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
                weight=Theme.FONT_WEIGHT["medium"],
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        margin=ft.margin.only(bottom=Theme.SPACING["2xl"]),
    )

    # Card de configuración
    card_config = ft.Container(
        content=ft.Column([
            # Título
            ft.Row([
                ft.Icon(ft.Icons.DNS_ROUNDED, color=Theme.PRIMARY, size=28),
                ft.Text(
                    "Datos del Servidor",
                    size=Theme.FONT_SIZE["2xl"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_PRIMARY
                )
            ], spacing=Theme.SPACING["sm"]),

            ft.Container(height=Theme.SPACING["xl"]),

            # Inputs
            host_input,
            ft.Container(height=Theme.SPACING["lg"]),
            port_input,
            ft.Container(height=Theme.SPACING["lg"]),
            timeout_input,

            ft.Container(height=Theme.SPACING["2xl"]),

            # Estado de conexión
            conexion_status,

            ft.Container(height=Theme.SPACING["lg"]),

            # Mensajes
            mensaje_container,

            ft.Container(height=Theme.SPACING["2xl"]),

            # Botones de acción
            ft.Row([
                create_large_button(
                    "Probar Conexión",
                    probar_conexion,
                    icon=ft.Icons.WIFI_FIND_ROUNDED,
                    bgcolor=Theme.INFO,
                    page_width=page_width,
                    page_height=page_height
                ),
                create_large_button(
                    "Guardar",
                    guardar_configuracion,
                    icon=ft.Icons.SAVE_ROUNDED,
                    bgcolor=Theme.SUCCESS,
                    page_width=page_width,
                    page_height=page_height
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["xl"], wrap=True),

            ft.Container(height=Theme.SPACING["lg"]),

            # Botón resetear
            ft.Row([
                ft.TextButton(
                    "Restablecer valores por defecto",
                    icon=ft.Icons.RESTORE_ROUNDED,
                    on_click=resetear_configuracion,
                    style=ft.ButtonStyle(
                        color=Theme.WARNING,
                    )
                )
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Container(height=Theme.SPACING["xl"]),

            # Info actual
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Configuración Actual",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                    ft.Container(height=Theme.SPACING["sm"]),
                    ft.Text(
                        f"URL: {config_manager.get_api_base_url()}",
                        size=Theme.FONT_SIZE["md"],
                        color=Theme.TEXT_SECONDARY
                    ),
                    ft.Text(
                        f"Timeout: {config_manager.get_api_timeout()}s",
                        size=Theme.FONT_SIZE["md"],
                        color=Theme.TEXT_SECONDARY
                    ),
                ], spacing=Theme.SPACING["xs"]),
                padding=Theme.SPACING["lg"],
                bgcolor=Theme.CARD_BG_DARK,
                border_radius=Theme.RADIUS["md"],
                border=ft.border.all(1, Theme.BORDER_DARK),
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Botón volver
            create_back_button(
                lambda e: on_back(),
                "Volver",
                page_width=page_width,
                page_height=page_height
            )

        ], spacing=0),
        width=700,
        padding=Theme.SPACING["3xl"],
        bgcolor=Theme.CARD_BG,
        border_radius=Theme.RADIUS["2xl"],
        border=ft.border.all(1, Theme.BORDER_LIGHT),
        shadow=Theme.get_shadow("xl"),
    )

    # Contenido principal
    contenido_principal = ft.Column([
        header,
        card_config,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Layout con background
    background_existe = os.path.exists(BACKGROUND_IMAGE)

    if background_existe:
        main_container = ft.Stack([
            ft.Image(
                src=BACKGROUND_IMAGE,
                fit=ft.ImageFit.COVER,
                width=float('inf'),
                height=float('inf'),
            ),
            ft.Container(
                bgcolor=Theme.OVERLAY_DARK,
                expand=True,
            ),
            ft.Container(
                content=ft.Column(
                    [contenido_principal],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["4xl"],
                expand=True,
                alignment=ft.alignment.center
            ),
        ], expand=True)
    else:
        main_container = ft.Container(
            content=ft.Column(
                [contenido_principal],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=Theme.SPACING["4xl"],
            bgcolor=Theme.BACKGROUND_DARK,
            expand=True,
            alignment=ft.alignment.center
        )

    # Limpiar y mostrar
    page.controls.clear()
    page.add(main_container)
    page.update()

    # Enfocar el campo host automáticamente
    host_input.focus()
