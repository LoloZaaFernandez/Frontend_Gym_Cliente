"""
Componentes de UI comunes y reutilizables
"""

import flet as ft
from config.settings import (
    PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG,
    TEXT_PRIMARY, BACKGROUND_DARK
)


def create_role_card(title: str, description: str, icon, color: str, on_click):
    """
    Crear tarjeta de selección de rol

    Args:
        title: Título de la tarjeta
        description: Descripción del rol
        icon: Ícono de Flet
        color: Color de acento
        on_click: Función a ejecutar al hacer clic

    Returns:
        Container con la tarjeta de rol
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=40, color=color),
                ft.Text(
                    title,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    description,
                    size=14,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    text="Acceder",
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLACK,
                        bgcolor=color,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    on_click=on_click
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=CARD_BG,
        border_radius=12,
        width=300,
        height=280,
        padding=30,
        border=ft.border.all(1, "#333333"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK45,
            offset=ft.Offset(0, 4)
        )
    )


def create_nav_button(text: str, icon, on_click, color: str = PRIMARY_COLOR):
    """
    Crear botón de navegación para el dashboard

    Args:
        text: Texto del botón
        icon: Ícono de Flet
        on_click: Función a ejecutar al hacer clic
        color: Color del ícono

    Returns:
        Container con el botón de navegación
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=30, color=color),
                ft.Text(text, size=12, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        ),
        width=120,
        height=100,
        padding=15,
        bgcolor=CARD_BG,
        border_radius=12,
        on_click=on_click,
        border=ft.border.all(1, "#333333"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2)
        )
    )


def create_header(title: str, subtitle: str, on_logout):
    """
    Crear header común para dashboards

    Args:
        title: Título principal
        subtitle: Subtítulo o nombre de usuario
        on_logout: Función para cerrar sesión

    Returns:
        Container con el header
    """
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column([
                    ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    ft.Text(subtitle, color=TEXT_SECONDARY),
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


def create_text_field(label: str, password: bool = False, width: int = 320):
    """
    Crear campo de texto estilizado

    Args:
        label: Etiqueta del campo
        password: Si es campo de contraseña
        width: Ancho del campo

    Returns:
        TextField configurado
    """
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,
        border_radius=8,
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        height=50,
        text_size=14,
        content_padding=15,
        width=width,
        bgcolor=CARD_BG,
        border_width=1,
        color=TEXT_PRIMARY,
        label_style=ft.TextStyle(color=TEXT_SECONDARY)
    )


def create_primary_button(text: str, on_click, width: int = 320):
    """
    Crear botón primario estilizado

    Args:
        text: Texto del botón
        on_click: Función a ejecutar al hacer clic
        width: Ancho del botón

    Returns:
        ElevatedButton configurado
    """
    return ft.ElevatedButton(
        text=text,
        width=width,
        height=45,
        bgcolor=PRIMARY_COLOR,
        color=ft.Colors.BLACK,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=on_click
    )
