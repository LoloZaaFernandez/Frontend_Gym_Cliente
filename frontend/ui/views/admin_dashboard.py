"""
Vista de dashboard para administradores con estadísticas mejoradas
"""

import flet as ft
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from ui.components.common import create_header, create_nav_button, create_info_card
from datetime import datetime


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
    page.title = "BLESSED GYM - Dashboard Administrador"

    current_user = auth_service.get_current_user()

    # Estadísticas simuladas (integrar con DB real)
    stats = {
        "clientes_total": 150,
        "clientes_activos": 142,
        "asistencias_hoy": 45,
        "ingresos_hoy": 850.00
    }

    header = create_header(
        "BLESSED GYM",
        f"Bienvenido, {current_user['nombre']}",
        on_logout
    )

    # Botones de navegación mejorados
    nav_buttons = ft.Row(
        controls=[
            create_nav_button("Dashboard", ft.Icons.DASHBOARD, lambda _: show_admin_dashboard(page, auth_service, on_logout, on_section_click)),
            create_nav_button("Clientes", ft.Icons.PEOPLE, lambda _: on_section_click("Clientes")),
            create_nav_button("Asistencia", ft.Icons.DIRECTIONS_RUN, lambda _: on_section_click("Asistencia")),
            create_nav_button("POS", ft.Icons.SHOPPING_CART, lambda _: on_section_click("POS")),
            create_nav_button("Reportes", ft.Icons.ANALYTICS, lambda _: on_section_click("Reportes")),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True
    )

    # Tarjetas de estadísticas
    stats_row = ft.Row([
        create_info_card(
            "Total Clientes",
            str(stats["clientes_total"]),
            ft.Icons.PEOPLE,
            PRIMARY_COLOR
        ),
        create_info_card(
            "Clientes Activos",
            str(stats["clientes_activos"]),
            ft.Icons.PERSON_ADD,
            "#4CAF50"
        ),
        create_info_card(
            "Asistencias Hoy",
            str(stats["asistencias_hoy"]),
            ft.Icons.FITNESS_CENTER,
            "#2196F3"
        ),
        create_info_card(
            "Ingresos Hoy",
            f"S/. {stats['ingresos_hoy']:.0f}",
            ft.Icons.ATTACH_MONEY,
            "#FF6F00"
        ),
    ], spacing=15, scroll=ft.ScrollMode.AUTO, wrap=True)

    stats_container = ft.Container(
        content=ft.Column([
            ft.Text(
                "Resumen del Día",
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

    # Actividad reciente
    actividades = [
        {"texto": "Nuevo cliente registrado: Juan Pérez", "icono": ft.Icons.PERSON_ADD, "hora": "10:30"},
        {"texto": "Venta realizada: Membresía Mensual", "icono": ft.Icons.POINT_OF_SALE, "hora": "11:15"},
        {"texto": "Asistencia registrada: María García", "icono": ft.Icons.FITNESS_CENTER, "hora": "12:00"},
    ]

    actividad_list = ft.Column(spacing=8)
    for act in actividades:
        actividad_list.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(act['icono'], size=20, color=PRIMARY_COLOR),
                    ft.Text(act['texto'], size=13, color=TEXT_PRIMARY, expand=True),
                    ft.Text(act['hora'], size=12, color=TEXT_SECONDARY),
                ], spacing=10),
                bgcolor=f"{CARD_BG}",
                border_radius=8,
                padding=12,
                border=ft.border.all(1, "#333333")
            )
        )

    actividad_container = ft.Container(
        content=ft.Column([
            ft.Text(
                "Actividad Reciente",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            actividad_list,
        ], spacing=10),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=True
    )

    # Contenido principal
    content = ft.Column([
        header,
        ft.Container(
            content=nav_buttons,
            margin=10
        ),
        stats_container,
        actividad_container
    ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    page.add(
        ft.Container(
            content=content,
            bgcolor=BACKGROUND_DARK,
            expand=True
        )
    )
    page.update()
