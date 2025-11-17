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
    disabled=False,
    page_width=None,
    page_height=None
):
    """
    Crear botón grande para tablet (principal) - RESPONSIVE

    Args:
        text: Texto del botón
        on_click: Función al hacer clic
        icon: Ícono opcional
        bgcolor: Color de fondo (default: PRIMARY)
        color: Color de texto (default: WHITE)
        width: Ancho personalizado (sobreescribe cálculo responsive)
        height: Alto personalizado (sobreescribe cálculo responsive)
        disabled: Si está deshabilitado
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        ft.ElevatedButton configurado para tablet
    """
    # Calcular dimensiones responsive si se proporciona page_width/page_height
    if page_width and page_height and not width:
        width = Theme.get_responsive_width(page_width, "button", "lg")
    if page_height and not height:
        height = Theme.get_responsive_height(page_height, Theme.DIMENSIONS["button_height_lg"])

    # Calcular espaciado responsive
    h_padding = Theme.SPACING["3xl"]
    v_padding = Theme.SPACING["xl"]
    font_size = Theme.FONT_SIZE["2xl"]

    if page_width:
        h_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["3xl"])
        v_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["xl"])
        font_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["2xl"])

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
                horizontal=h_padding,
                vertical=v_padding
            ),
            text_style=ft.TextStyle(
                size=font_size,
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
    disabled=False,
    page_width=None,
    page_height=None
):
    """
    Crear botón con borde (secundario) - RESPONSIVE

    Args:
        text: Texto del botón
        on_click: Función al hacer clic
        icon: Ícono opcional
        color: Color del borde y texto (default: PRIMARY)
        width: Ancho personalizado (sobreescribe cálculo responsive)
        height: Alto personalizado (sobreescribe cálculo responsive)
        disabled: Si está deshabilitado
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        ft.ElevatedButton con estilo outlined
    """
    btn_color = color or Theme.PRIMARY

    # Calcular dimensiones responsive si se proporciona page_width/page_height
    if page_width and page_height and not width:
        width = Theme.get_responsive_width(page_width, "button", "lg")
    if page_height and not height:
        height = Theme.get_responsive_height(page_height, Theme.DIMENSIONS["button_height_lg"])

    # Calcular espaciado responsive
    h_padding = Theme.SPACING["3xl"]
    v_padding = Theme.SPACING["xl"]
    font_size = Theme.FONT_SIZE["2xl"]

    if page_width:
        h_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["3xl"])
        v_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["xl"])
        font_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["2xl"])

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
                horizontal=h_padding,
                vertical=v_padding
            ),
            text_style=ft.TextStyle(
                size=font_size,
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
    disabled=False,
    page_width=None,
    page_height=None
):
    """Crear botón de éxito (verde) - RESPONSIVE"""
    return create_large_button(
        text=text,
        on_click=on_click,
        icon=icon,
        bgcolor=Theme.SUCCESS,
        color=ft.Colors.WHITE,
        width=width,
        height=height,
        disabled=disabled,
        page_width=page_width,
        page_height=page_height
    )


def create_danger_button(
    text: str,
    on_click,
    icon=None,
    width=None,
    height=None,
    disabled=False,
    page_width=None,
    page_height=None
):
    """Crear botón de peligro (rojo) - RESPONSIVE"""
    return create_large_button(
        text=text,
        on_click=on_click,
        icon=icon,
        bgcolor=Theme.ERROR,
        color=ft.Colors.WHITE,
        width=width,
        height=height,
        disabled=disabled,
        page_width=page_width,
        page_height=page_height
    )


def create_back_button(on_click, text="Volver", page_width=None, page_height=None):
    """
    Crear botón de retroceso estándar - RESPONSIVE

    Args:
        on_click: Función al hacer clic
        text: Texto del botón (default: "Volver")
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        Botón con ícono de flecha
    """
    # Calcular ancho responsive del botón de volver (más pequeño que los demás)
    btn_width = 180
    if page_width:
        btn_width = Theme.get_responsive_width(page_width, "button", "sm") * 1.2

    return create_outlined_button(
        text=text,
        on_click=on_click,
        icon=ft.Icons.ARROW_BACK,
        color=Theme.TEXT_SECONDARY,
        width=btn_width,
        page_width=page_width,
        page_height=page_height
    )
