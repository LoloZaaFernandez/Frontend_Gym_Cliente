"""
Vista simple para mostrar mensajes de secciones en desarrollo
"""

import flet as ft
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG


def show_simple_message(page: ft.Page, section: str, on_back):
    """
    Mostrar mensaje simple para secciones en desarrollo

    Args:
        page: Página de Flet
        section: Nombre de la sección
        on_back: Callback para volver atrás
    """
    page.clean()

    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=PRIMARY_COLOR,
                on_click=lambda _: on_back()
            ),
            ft.Text(f"{section} - BLESSED GYM", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
        ]),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    content = ft.Container(
        content=ft.Column([
            ft.Text(f"Sección: {section}", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Text("Esta funcionalidad está en desarrollo...", color=TEXT_SECONDARY),
            ft.Container(height=20),
            ft.Text("Próximamente disponible", size=16, color=TEXT_SECONDARY),
        ]),
        padding=40,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=20,
        alignment=ft.alignment.center,
        border=ft.border.all(1, "#333333")
    )

    page.add(header, content)
    page.update()
