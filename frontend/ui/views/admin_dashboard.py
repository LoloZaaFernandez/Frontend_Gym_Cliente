"""
Vista de dashboard para administradores
"""

import flet as ft
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG
from ui.components.common import create_header, create_nav_button


def show_admin_dashboard(page: ft.Page, auth_service, on_logout, on_section_click):
    """
    Mostrar dashboard del administrador

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_logout: Callback para cerrar sesión
        on_section_click: Callback para navegar a secciones (recibe nombre de sección)
    """
    page.clean()

    current_user = auth_service.get_current_user()

    header = create_header(
        "BLESSED GYM",
        f"Bienvenido, {current_user['nombre']}",
        on_logout
    )

    nav_buttons = ft.Row(
        controls=[
            create_nav_button("Dashboard", ft.Icons.DASHBOARD, lambda _: show_admin_dashboard(page, auth_service, on_logout, on_section_click)),
            create_nav_button("Clientes", ft.Icons.PEOPLE, lambda _: on_section_click("Clientes")),
            create_nav_button("Asistencia", ft.Icons.DIRECTIONS_RUN, lambda _: on_section_click("Asistencia")),
            create_nav_button("POS", ft.Icons.SHOPPING_CART, lambda _: on_section_click("POS")),
            create_nav_button("Reportes", ft.Icons.ANALYTICS, lambda _: on_section_click("Reportes")),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER
    )

    content = ft.Container(
        content=ft.Column([
            ft.Text("Dashboard Principal", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Text("Bienvenido al sistema de gestión de Blessed Gym", color=TEXT_SECONDARY),
            ft.Container(height=20),
            ft.Text("Estadísticas y resumen del sistema aparecerán aquí...", color=TEXT_SECONDARY),
        ]),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=20,
        border=ft.border.all(1, "#333333")
    )

    page.add(header, nav_buttons, content)
    page.update()
