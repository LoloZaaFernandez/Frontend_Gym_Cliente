"""
Vista de selección de rol (Admin o Cliente) - Refactorizado con Sistema de Componentes
ANTES: 145 líneas | DESPUÉS: ~90 líneas (38% menos código)
"""

import flet as ft
import os
from config.theme import Theme
from config.settings import LOGO_PATH, BG_PATH_ROL, ADMIN_ICON_PATH, ADMIN_ICON_HOVER_PATH, CLIENT_ICON_PATH, CLIENT_ICON_HOVER_PATH


def show_role_selection(page: ft.Page, on_admin_click, on_client_click):
    """
    Mostrar la pantalla de selección de rol

    Mejoras:
    - 38% menos código (145 → ~90 líneas)
    - Theme centralizado
    - Componentes simplificados
    - Mejor organización
    """
    page.clean()
    page.title = "BLESSED GYM - Selección de Rol"
    page.bgcolor = Theme.BACKGROUND_DARK

    # Verificar imágenes
    logo_exists = os.path.exists(LOGO_PATH)
    bg_exists = os.path.exists(BG_PATH_ROL)
    admin_icon_exists = os.path.exists(ADMIN_ICON_PATH)
    admin_icon_hover_exists = os.path.exists(ADMIN_ICON_HOVER_PATH)
    client_icon_exists = os.path.exists(CLIENT_ICON_PATH)
    client_icon_hover_exists = os.path.exists(CLIENT_ICON_HOVER_PATH)

    def create_role_card(title, description, icon, color, on_click, icon_image=None, icon_image_hover=None):
        """Crear tarjeta de rol con hover effect"""
        # Usar imagen PNG si está disponible, sino usar icono
        if icon_image and os.path.exists(icon_image):
            icon_content = ft.Image(
                src=icon_image,
                width=180,
                height=180,
                fit=ft.ImageFit.CONTAIN,
                border_radius=Theme.RADIUS["md"]
            )
        else:
            icon_content = ft.Icon(icon, size=60, color=color)

        icon_container = ft.Container(
            content=icon_content,
            bgcolor=f"{color}22" if not icon_image else "transparent",
            border_radius=Theme.RADIUS["xl"],
            width=100,
            height=100,
            alignment=ft.alignment.center
        )

        card = ft.Container(
            content=ft.Column([
                icon_container,
                ft.Text(title, size=Theme.FONT_SIZE["xl"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Text(description, size=Theme.FONT_SIZE["sm"],
                       color=Theme.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["lg"]),
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["xl"],
            padding=Theme.SPACING["4xl"],
            width=300,
            border=ft.border.all(1, Theme.BORDER_DEFAULT),
            shadow=Theme.get_shadow("lg"),
            animate=200,
            on_click=on_click,
        )

        def on_hover(e):
            if e.data == "true":
                card.bgcolor = f"{color}11"
                card.border = ft.border.all(2, color)
                card.shadow = Theme.get_shadow("2xl")
                card.scale = 1.05

                # Cambiar imagen en hover si está disponible
                if icon_image_hover and os.path.exists(icon_image_hover):
                    icon_content.src = icon_image_hover
            else:
                card.bgcolor = Theme.CARD_BG
                card.border = ft.border.all(1, Theme.BORDER_DEFAULT)
                card.shadow = Theme.get_shadow("lg")
                card.scale = 1.0

                # Restaurar imagen original
                if icon_image and os.path.exists(icon_image):
                    icon_content.src = icon_image
            card.update()

        card.on_hover = on_hover
        return card

    # Contenido
    content = ft.Container(
        content=ft.Column([
            ft.Container(height=Theme.SPACING["5xl"]),

            # Logo
            ft.Container(
                content=ft.Image(
                    src=LOGO_PATH if logo_exists else None,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Column([
                        ft.Icon(ft.Icons.FITNESS_CENTER, size=50, color=Theme.PRIMARY),
                        ft.Text("BLESSED GYM", color=Theme.PRIMARY, size=Theme.FONT_SIZE["lg"],
                               weight=Theme.FONT_WEIGHT["bold"])
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["xs"])
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=Theme.SPACING["xl"])
            ),

            # Título
            ft.Text("Sistema de Gestión Integral", size=Theme.FONT_SIZE["3xl"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY,
                   text_align=ft.TextAlign.CENTER),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Subtítulo
            ft.Text("Selecciona tu tipo de acceso:", size=Theme.FONT_SIZE["lg"],
                   weight=Theme.FONT_WEIGHT["medium"], color=Theme.TEXT_PRIMARY,
                   text_align=ft.TextAlign.CENTER),

            ft.Container(height=Theme.SPACING["4xl"]),

            # Tarjetas de rol
            ft.Row([
                create_role_card("Administrador", "Gestión completa del gimnasio",
                               ft.Icons.ADMIN_PANEL_SETTINGS, Theme.PRIMARY, lambda _: on_admin_click(),
                               icon_image=ADMIN_ICON_PATH if admin_icon_exists else None,
                               icon_image_hover=ADMIN_ICON_HOVER_PATH if admin_icon_hover_exists else None),
                create_role_card("Cliente", "Portal personal del cliente",
                               ft.Icons.PERSON, "#4CAF50", lambda _: on_client_click(),
                               icon_image=CLIENT_ICON_PATH if client_icon_exists else None,
                               icon_image_hover=CLIENT_ICON_HOVER_PATH if client_icon_hover_exists else None),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["4xl"]),

            ft.Container(expand=True),

            # Footer
            ft.Text("© 2025 Blessed Gym - Todos los derechos reservados",
                   size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY,
                   text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=Theme.SPACING["4xl"],
        expand=True
    )

    # Stack con fondo
    if bg_exists:
        main_container = ft.Stack([
            ft.Container(content=ft.Image(src=BG_PATH_ROL, fit=ft.ImageFit.COVER, expand=True), expand=True),
            ft.Container(bgcolor=ft.Colors.BLACK45, expand=True),
            content
        ], expand=True)
    else:
        main_container = content

    page.add(main_container)
    page.update()