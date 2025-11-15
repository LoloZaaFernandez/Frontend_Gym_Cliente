"""
Componentes de Botones Reutilizables
Botones optimizados para tablets con tamaños más grandes
"""
import flet as ft
import sys
import os

# Agregar path del config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme


def create_large_button(
    text: str,
    on_click,
    icon=None,
    bgcolor=None,
    color=None,
    width=None,
    height=None,
    disabled=False
):
    """
    Crear botón grande para tablet (principal)

    Args:
        text: Texto del botón
        on_click: Función al hacer clic
        icon: Ícono opcional
        bgcolor: Color de fondo (default: PRIMARY)
        color: Color de texto (default: WHITE)
        width: Ancho personalizado
        height: Alto personalizado (default: 70px)
        disabled: Si está deshabilitado

    Returns:
        ft.ElevatedButton configurado para tablet
    """
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width or Theme.DIMENSIONS["button_width_lg"],
        height=height or Theme.DIMENSIONS["button_height_lg"],
        disabled=disabled,
        style=ft.ButtonStyle(
            bgcolor=bgcolor or Theme.PRIMARY,
            color=color or ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["lg"]),
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["3xl"],
                vertical=Theme.SPACING["xl"]
            ),
            text_style=ft.TextStyle(
                size=Theme.FONT_SIZE["2xl"],
                weight=Theme.FONT_WEIGHT["bold"]
            )
        )
    )


def create_outlined_button(
    text: str,
    on_click,
    icon=None,
    color=None,
    width=None,
    height=None,
    disabled=False
):
    """
    Crear botón con borde (secundario)

    Args:
        text: Texto del botón
        on_click: Función al hacer clic
        icon: Ícono opcional
        color: Color del borde y texto (default: PRIMARY)
        width: Ancho personalizado
        height: Alto personalizado
        disabled: Si está deshabilitado

    Returns:
        ft.ElevatedButton con estilo outlined
    """
    btn_color = color or Theme.PRIMARY

    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width or Theme.DIMENSIONS["button_width_lg"],
        height=height or Theme.DIMENSIONS["button_height_lg"],
        disabled=disabled,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.TRANSPARENT,
            color=btn_color,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["lg"]),
            side=ft.border.all(2, btn_color),
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["3xl"],
                vertical=Theme.SPACING["xl"]
            ),
            text_style=ft.TextStyle(
                size=Theme.FONT_SIZE["2xl"],
                weight=Theme.FONT_WEIGHT["bold"]
            )
        )
    )


def create_success_button(
    text: str,
    on_click,
    icon=None,
    width=None,
    height=None,
    disabled=False
):
    """Crear botón de éxito (verde)"""
    return create_large_button(
        text=text,
        on_click=on_click,
        icon=icon,
        bgcolor=Theme.SUCCESS,
        color=ft.Colors.WHITE,
        width=width,
        height=height,
        disabled=disabled
    )


def create_danger_button(
    text: str,
    on_click,
    icon=None,
    width=None,
    height=None,
    disabled=False
):
    """Crear botón de peligro (rojo)"""
    return create_large_button(
        text=text,
        on_click=on_click,
        icon=icon,
        bgcolor=Theme.ERROR,
        color=ft.Colors.WHITE,
        width=width,
        height=height,
        disabled=disabled
    )


def create_back_button(on_click, text="Volver"):
    """
    Crear botón de retroceso estándar

    Args:
        on_click: Función al hacer clic
        text: Texto del botón (default: "Volver")

    Returns:
        Botón con ícono de flecha
    """
    return create_outlined_button(
        text=text,
        on_click=on_click,
        icon=ft.Icons.ARROW_BACK,
        color=Theme.TEXT_SECONDARY,
        width=180
    )
