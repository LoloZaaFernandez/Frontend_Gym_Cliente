"""
Componentes de Inputs Reutilizables
Campos de texto optimizados para tablets
"""
import flet as ft
import sys
import os

# Agregar path del config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme


def create_text_input(
    label: str,
    hint_text: str = "",
    icon=None,
    password=False,
    max_length=None,
    keyboard_type=None,
    on_change=None,
    on_submit=None,
    width=None,
    value="",
    page_width=None,
    page_height=None
):
    """
    Crear campo de texto para tablet - RESPONSIVE

    Args:
        label: Etiqueta del campo
        hint_text: Texto de ayuda
        icon: Ícono opcional
        password: Si es campo de contraseña
        max_length: Longitud máxima
        keyboard_type: Tipo de teclado (ft.KeyboardType.*)
        on_change: Función al cambiar el valor
        on_submit: Función al presionar Enter
        width: Ancho personalizado (sobreescribe cálculo responsive)
        value: Valor inicial
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        ft.TextField configurado
    """
    # Calcular dimensiones responsive si se proporciona page_width/page_height
    if page_width and not width:
        width = Theme.get_responsive_width(page_width, "input", "lg")

    input_height = Theme.DIMENSIONS["input_height"]
    if page_height:
        input_height = Theme.get_responsive_height(page_height, Theme.DIMENSIONS["input_height"])

    # Calcular tamaños de fuente y espaciado responsive
    text_size = Theme.FONT_SIZE["xl"]
    label_size = Theme.FONT_SIZE["lg"]
    h_padding = Theme.SPACING["xl"]
    v_padding = Theme.SPACING["lg"]

    if page_width:
        text_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["xl"])
        label_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["lg"])
        h_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["xl"])
        v_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["lg"])

    return ft.TextField(
        label=label,
        hint_text=hint_text,
        prefix_icon=icon,
        password=password,
        can_reveal_password=password,
        max_length=max_length,
        keyboard_type=keyboard_type,
        on_change=on_change,
        on_submit=on_submit,
        width=width or Theme.DIMENSIONS["input_width_lg"],
        height=input_height,
        value=value,
        text_size=text_size,
        label_style=ft.TextStyle(
            size=label_size,
            color=Theme.TEXT_SECONDARY
        ),
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        cursor_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        filled=True,
        border_radius=Theme.RADIUS["lg"],
        content_padding=ft.padding.symmetric(
            horizontal=h_padding,
            vertical=v_padding
        )
    )


def create_dni_input(on_change=None, on_submit=None, value="", page_width=None, page_height=None):
    """
    Crear campo específico para DNI - RESPONSIVE

    Args:
        on_change: Función al cambiar el valor
        on_submit: Función al presionar Enter
        value: Valor inicial
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        TextField configurado para DNI (8 dígitos numéricos)
    """
    return create_text_input(
        label="DNI",
        hint_text="Ingresa tu DNI (8 dígitos)",
        icon=ft.Icons.BADGE,
        max_length=8,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=on_change,
        on_submit=on_submit,
        value=value,
        page_width=page_width,
        page_height=page_height
    )


def create_phone_input(on_change=None, value="", page_width=None, page_height=None):
    """
    Crear campo específico para teléfono - RESPONSIVE

    Args:
        on_change: Función al cambiar el valor
        value: Valor inicial
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        TextField configurado para teléfono (9 dígitos, solo números)
    """
    def validate_numbers(e):
        """Validar que solo se ingresen números"""
        if e.control.value:
            # Filtrar solo dígitos
            filtered = ''.join(filter(str.isdigit, e.control.value))
            if filtered != e.control.value:
                e.control.value = filtered
                e.control.update()
        # Llamar al on_change original si existe
        if on_change:
            on_change(e)

    return create_text_input(
        label="Teléfono",
        hint_text="Ej: 987654321",
        icon=ft.Icons.PHONE,
        max_length=9,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=validate_numbers,
        value=value,
        page_width=page_width,
        page_height=page_height
    )


def create_email_input(on_change=None, value="", page_width=None, page_height=None):
    """
    Crear campo específico para email - RESPONSIVE

    Args:
        on_change: Función al cambiar el valor
        value: Valor inicial
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        TextField configurado para email
    """
    return create_text_input(
        label="Correo Electrónico",
        hint_text="ejemplo@email.com",
        icon=ft.Icons.EMAIL,
        keyboard_type=ft.KeyboardType.EMAIL,
        on_change=on_change,
        value=value,
        page_width=page_width,
        page_height=page_height
    )
