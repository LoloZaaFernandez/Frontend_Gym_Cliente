"""
Vista de Autenticación para Configuración
Requiere contraseña antes de acceder a la configuración de API
"""
import flet as ft
import sys
import os

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme
from config.settings import BACKGROUND_IMAGE
from components.buttons import create_large_button, create_back_button
from components.inputs import create_text_input
from components.cards import create_alert_card

# Contraseña de administrador
ADMIN_PASSWORD = "Adminjrojas123$"


def show_auth_config_view(page: ft.Page, on_back, on_auth_success):
    """
    Mostrar vista de autenticación para configuración

    Args:
        page: Instancia de la página de Flet
        on_back: Función para volver a la pantalla anterior
        on_auth_success: Callback cuando la autenticación es exitosa
    """
    page.clean()
    page.bgcolor = Theme.BACKGROUND_DARK

    # Obtener dimensiones de la página
    page_width = page.window.width or page.width or Theme.BASE_WIDTH
    page_height = page.window.height or page.height or Theme.BASE_HEIGHT

    # Controles
    mensaje_container = ft.Container()
    intentos_fallidos = {"count": 0}  # Contador de intentos fallidos

    # Input de contraseña
    password_input = create_text_input(
        label="Contraseña de Administrador",
        hint_text="Ingresa la contraseña",
        icon=ft.Icons.LOCK_ROUNDED,
        password=True,
        page_width=page_width,
        page_height=page_height
    )

    def mostrar_mensaje(mensaje: str, tipo: str = "error"):
        """Mostrar mensaje de feedback"""
        mensaje_container.content = create_alert_card(mensaje, tipo, page_width=page_width)
        mensaje_container.update()

    def limpiar_mensaje():
        """Limpiar mensaje"""
        mensaje_container.content = None
        mensaje_container.update()

    def verificar_password(e):
        """Verificar contraseña ingresada"""
        limpiar_mensaje()

        if not password_input.value:
            mostrar_mensaje("Por favor, ingresa la contraseña", "error")
            return

        if password_input.value == ADMIN_PASSWORD:
            # Contraseña correcta
            mostrar_mensaje("✓ Contraseña correcta. Accediendo...", "success")
            page.update()

            # Pequeña pausa para que el usuario vea el mensaje de éxito
            import time
            time.sleep(0.5)

            # Llamar callback de éxito
            on_auth_success()
        else:
            # Contraseña incorrecta
            intentos_fallidos["count"] += 1

            if intentos_fallidos["count"] >= 3:
                mostrar_mensaje(
                    f"✗ Contraseña incorrecta ({intentos_fallidos['count']} intentos fallidos)\n\n"
                    "Por seguridad, contacta al administrador del sistema.",
                    "error"
                )
            else:
                mostrar_mensaje(
                    f"✗ Contraseña incorrecta. Intento {intentos_fallidos['count']} de 3",
                    "error"
                )

            # Limpiar campo de contraseña
            password_input.value = ""
            password_input.update()
            password_input.focus()

    def on_password_submit(e):
        """Manejar submit del campo de contraseña (Enter)"""
        verificar_password(e)

    # Configurar eventos
    password_input.on_submit = on_password_submit

    # ==================== CONTENIDO PRINCIPAL ====================

    # Header
    header = ft.Container(
        content=ft.Column([
            # Ícono de candado con efecto glow
            ft.Container(
                content=ft.Icon(
                    ft.Icons.SHIELD_ROUNDED,
                    size=Theme.ICON_SIZE["2xl"],
                    color=Theme.WARNING
                ),
                width=120,
                height=120,
                bgcolor="rgba(255, 152, 0, 0.1)",
                border_radius=60,
                border=ft.border.all(3, Theme.WARNING),
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=25,
                    color="rgba(255, 152, 0, 0.3)",
                    offset=ft.Offset(0, 0),
                ),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            ft.Text(
                "Acceso Restringido",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["extrabold"],
                color=Theme.WARNING,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Container(height=Theme.SPACING["sm"]),

            ft.Text(
                "Se requiere contraseña de administrador",
                size=Theme.FONT_SIZE["lg"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
                weight=Theme.FONT_WEIGHT["medium"],
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        margin=ft.margin.only(bottom=Theme.SPACING["2xl"]),
    )

    # Card de autenticación
    card_auth = ft.Container(
        content=ft.Column([
            # Alerta de seguridad
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, color=Theme.INFO, size=24),
                    ft.Text(
                        "Solo personal autorizado",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    )
                ], spacing=Theme.SPACING["sm"]),
                padding=Theme.SPACING["lg"],
                bgcolor=Theme.CARD_BG_DARK,
                border_radius=Theme.RADIUS["md"],
                border=ft.border.all(1, Theme.INFO),
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Input de contraseña
            password_input,

            ft.Container(height=Theme.SPACING["sm"]),

            # Info adicional
            ft.Row([
                ft.Icon(ft.Icons.SECURITY_ROUNDED, color=Theme.TEXT_SECONDARY, size=16),
                ft.Text(
                    "La contraseña es sensible a mayúsculas y minúsculas",
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_SECONDARY,
                    italic=True
                )
            ], spacing=Theme.SPACING["xs"]),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Mensajes
            mensaje_container,

            ft.Container(height=Theme.SPACING["2xl"]),

            # Botones
            ft.Row([
                create_back_button(
                    lambda e: on_back(),
                    "Cancelar",
                    page_width=page_width,
                    page_height=page_height
                ),
                create_large_button(
                    "Acceder",
                    verificar_password,
                    icon=ft.Icons.LOGIN_ROUNDED,
                    bgcolor=Theme.WARNING,
                    page_width=page_width,
                    page_height=page_height
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),

            ft.Container(height=Theme.SPACING["xl"]),

            # Advertencia de seguridad
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.WARNING_ROUNDED, color=Theme.ERROR, size=20),
                        ft.Text(
                            "Advertencia de Seguridad",
                            size=Theme.FONT_SIZE["md"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=Theme.ERROR
                        )
                    ], spacing=Theme.SPACING["xs"]),
                    ft.Container(height=Theme.SPACING["xs"]),
                    ft.Text(
                        "Cambiar la configuración incorrectamente puede impedir\n"
                        "el funcionamiento de la aplicación. Solo personal\n"
                        "técnico autorizado debe acceder a esta sección.",
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=Theme.SPACING["lg"],
                bgcolor="rgba(239, 83, 80, 0.1)",
                border_radius=Theme.RADIUS["md"],
                border=ft.border.all(1, Theme.ERROR),
            ),

        ], spacing=0),
        width=650,
        padding=Theme.SPACING["3xl"],
        bgcolor=Theme.CARD_BG,
        border_radius=Theme.RADIUS["2xl"],
        border=ft.border.all(1, Theme.BORDER_LIGHT),
        shadow=Theme.get_shadow("xl"),
    )

    # Contenido principal
    contenido_principal = ft.Column([
        header,
        card_auth,
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

    # Enfocar el campo de contraseña automáticamente
    password_input.focus()
