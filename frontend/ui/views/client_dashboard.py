"""
Vista de dashboard para clientes
"""

import flet as ft
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY
from ui.components.common import create_header, create_nav_button


def show_client_dashboard(page: ft.Page, auth_service, on_logout, on_section_click):
    """
    Mostrar dashboard del cliente

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_logout: Callback para cerrar sesión
        on_section_click: Callback para navegar a secciones
    """
    page.clean()

    client_data = auth_service.get_current_user()

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column([
                    ft.Text("BLESSED GYM", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    ft.Text(f"Bienvenido, {client_data['nombre']} {client_data['apellidos']}",
                           color=TEXT_SECONDARY),
                    ft.Text(f"DNI: {client_data['dni']}", color=TEXT_SECONDARY, size=12),
                ]),
                ft.ElevatedButton(
                    "Cerrar Sesión",
                    icon=ft.Icons.LOGOUT,
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        bgcolor=ft.Colors.TRANSPARENT,
                        side=ft.border.all(1, PRIMARY_COLOR)
                    ),
                    on_click=on_logout
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    nav_buttons = ft.Row(
        controls=[
            create_nav_button("Mi Perfil", ft.Icons.PERSON, lambda _: on_section_click("Mi Perfil")),
            create_nav_button("Membresías", ft.Icons.CARD_MEMBERSHIP, lambda _: on_section_click("Membresías")),
            create_nav_button("Asistencias", ft.Icons.DIRECTIONS_RUN, lambda _: on_section_click("Asistencias")),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Información rápida del cliente
    info_card = ft.Container(
        content=ft.Column([
            ft.Text("Mi Información", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Divider(height=1, color="#333333"),
            ft.Row([ft.Text("Correo:", width=100, color=TEXT_SECONDARY), ft.Text(client_data['correo'], color=TEXT_PRIMARY)]),
            ft.Row([ft.Text("Teléfono:", width=100, color=TEXT_SECONDARY), ft.Text(client_data['telefono'] or "No registrado", color=TEXT_PRIMARY)]),
            ft.Row([ft.Text("Estado:", width=100, color=TEXT_SECONDARY),
                   ft.Text("Activo", color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD)]),
        ]),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=20,
        border=ft.border.all(1, "#333333")
    )

    page.add(header, nav_buttons, info_card)
    page.update()
