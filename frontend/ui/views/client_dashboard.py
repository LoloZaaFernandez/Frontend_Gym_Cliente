"""
Vista de dashboard para clientes con información personalizada
"""

import flet as ft
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from ui.components.common import create_nav_button, create_info_card
from datetime import datetime


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
    page.title = "BLESSED GYM - Dashboard Cliente"

    client_data = auth_service.get_current_user()

    # Datos simulados (integrar con DB real)
    stats_cliente = {
        "asistencias_mes": 18,
        "racha_dias": 5,
        "dias_restantes_membresia": 25,
        "ultima_asistencia": "05/11/2025"
    }

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=PRIMARY_COLOR),
                        bgcolor=f"{PRIMARY_COLOR}22",
                        border_radius=25,
                        padding=5
                    ),
                    ft.Column([
                        ft.Text("BLESSED GYM", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                        ft.Text(f"{client_data['nombre']} {client_data['apellidos']}",
                               color=TEXT_PRIMARY, size=16, weight=ft.FontWeight.W_500),
                        ft.Text(f"DNI: {client_data['dni']}", color=TEXT_SECONDARY, size=12),
                    ], spacing=2),
                ], spacing=15),
                ft.ElevatedButton(
                    "Cerrar Sesión",
                    icon=ft.Icons.LOGOUT,
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        bgcolor=ft.Colors.TRANSPARENT,
                        side=ft.border.all(1, PRIMARY_COLOR)
                    ),
                    on_click=on_logout,
                    height=40
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
            create_nav_button("Dashboard", ft.Icons.DASHBOARD, lambda _: show_client_dashboard(page, auth_service, on_logout, on_section_click)),
            create_nav_button("Mi Perfil", ft.Icons.PERSON, lambda _: on_section_click("Mi Perfil")),
            create_nav_button("Membresías", ft.Icons.CARD_MEMBERSHIP, lambda _: on_section_click("Membresías")),
            create_nav_button("Asistencias", ft.Icons.DIRECTIONS_RUN, lambda _: on_section_click("Asistencias")),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True
    )

    # Tarjetas de estadísticas personales
    stats_row = ft.Row([
        create_info_card(
            "Asistencias del Mes",
            str(stats_cliente["asistencias_mes"]),
            ft.Icons.FITNESS_CENTER,
            PRIMARY_COLOR
        ),
        create_info_card(
            "Racha Actual",
            f"{stats_cliente['racha_dias']} días",
            ft.Icons.LOCAL_FIRE_DEPARTMENT,
            "#FF6F00"
        ),
        create_info_card(
            "Días Restantes",
            str(stats_cliente["dias_restantes_membresia"]),
            ft.Icons.CALENDAR_MONTH,
            "#4CAF50"
        ),
    ], spacing=15, scroll=ft.ScrollMode.AUTO, wrap=True)

    stats_container = ft.Container(
        content=ft.Column([
            ft.Text(
                "Mi Progreso",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            stats_row,
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Información de membresía
    membresia_card = ft.Container(
        content=ft.Column([
            ft.Text(
                "Mi Membresía",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=40, color=PRIMARY_COLOR),
                    bgcolor=f"{PRIMARY_COLOR}22",
                    border_radius=10,
                    padding=12
                ),
                ft.Column([
                    ft.Text(
                        "Membresía Mensual",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY
                    ),
                    ft.Text(
                        "Vence: 30/11/2025",
                        size=13,
                        color=TEXT_SECONDARY
                    ),
                    ft.Container(
                        content=ft.Text(
                            "ACTIVA",
                            size=11,
                            color=TEXT_PRIMARY,
                            weight=ft.FontWeight.BOLD
                        ),
                        bgcolor=PRIMARY_COLOR,
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        border_radius=6,
                        margin=ft.margin.only(top=5)
                    ),
                ], spacing=5, expand=True),
                ft.ElevatedButton(
                    "Renovar",
                    icon=ft.Icons.AUTORENEW,
                    bgcolor=PRIMARY_COLOR,
                    color=ft.Colors.BLACK,
                    on_click=lambda _: on_section_click("Membresías")
                ),
            ], spacing=15),
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    def crear_info_row(label, value, icon):
        """Crear fila de información"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=18, color=PRIMARY_COLOR),
                ft.Text(f"{label}:", size=13, color=TEXT_SECONDARY, width=120),
                ft.Text(value, size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
            ], spacing=10),
            padding=8,
            bgcolor=f"{CARD_BG}",
            border_radius=6,
            border=ft.border.all(1, "#333333")
        )

    # Información personal
    info_card = ft.Container(
        content=ft.Column([
            ft.Text("Información Personal", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Divider(height=1, color="#333333"),
            crear_info_row("Correo", client_data['correo'], ft.Icons.EMAIL),
            crear_info_row("Teléfono", client_data.get('telefono') or "No registrado", ft.Icons.PHONE),
            crear_info_row("Última Asistencia", stats_cliente['ultima_asistencia'], ft.Icons.ACCESS_TIME),
        ], spacing=10),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=True
    )

    # Layout principal
    content = ft.Column([
        header,
        ft.Container(content=nav_buttons, margin=10),
        stats_container,
        membresia_card,
        info_card
    ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    page.add(
        ft.Container(
            content=content,
            bgcolor=BACKGROUND_DARK,
            expand=True
        )
    )
    page.update()
