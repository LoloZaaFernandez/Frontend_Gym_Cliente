"""
Componentes de Cards Reutilizables
Tarjetas y contenedores optimizados para tablets
"""
import flet as ft
import sys
import os

# Agregar path del config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme


def create_card_container(
    content,
    padding=None,
    margin=None,
    bgcolor=None,
    border_color=None,
    shadow="md",
    on_click=None,
    width=None,
    height=None,
    expand=False,
    page_width=None
):
    """
    Crear contenedor de tarjeta básico - RESPONSIVE

    Args:
        content: Contenido de la tarjeta
        padding: Padding personalizado (sobreescribe cálculo responsive)
        margin: Margen personalizado
        bgcolor: Color de fondo
        border_color: Color del borde
        shadow: Nivel de sombra
        on_click: Función al hacer clic
        width: Ancho personalizado
        height: Alto personalizado
        expand: Si debe expandirse
        page_width: Ancho de la página para cálculo responsive

    Returns:
        ft.Container configurado
    """
    # Calcular padding responsive si no se proporciona
    card_padding = padding
    if page_width and not padding:
        card_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["2xl"])

    return ft.Container(
        content=content,
        padding=card_padding or Theme.SPACING["2xl"],
        margin=margin,
        bgcolor=bgcolor or Theme.CARD_BG,
        border_radius=Theme.RADIUS["xl"],
        border=ft.border.all(1, border_color or Theme.BORDER_DEFAULT),
        shadow=Theme.get_shadow(shadow),
        on_click=on_click,
        width=width,
        height=height,
        expand=expand,
    )


def create_option_card(
    title: str,
    subtitle: str,
    icon,
    on_click,
    color=None,
    width=None,
    height=None,
    page_width=None,
    page_height=None
):
    """
    Crear tarjeta de opción clickeable (para pantalla inicial) - RESPONSIVE

    Args:
        title: Título principal
        subtitle: Subtítulo descriptivo
        icon: Ícono grande
        on_click: Función al hacer clic
        color: Color del ícono (default: PRIMARY)
        width: Ancho personalizado (sobreescribe cálculo responsive)
        height: Alto personalizado (sobreescribe cálculo responsive)
        page_width: Ancho de la página para cálculo responsive
        page_height: Altura de la página para cálculo responsive

    Returns:
        Card interactiva con efecto hover
    """
    card_color = color or Theme.PRIMARY

    # Calcular dimensiones responsive
    if page_width and not width:
        width = Theme.get_responsive_width(page_width, "card", "lg")
    if page_height and not height:
        height = Theme.get_responsive_height(page_height, Theme.DIMENSIONS["card_height_lg"])

    # Calcular tamaños responsive
    icon_size = Theme.ICON_SIZE["2xl"]
    title_size = Theme.FONT_SIZE["3xl"]
    subtitle_size = Theme.FONT_SIZE["lg"]
    card_padding = Theme.SPACING["4xl"]
    spacing_xl = Theme.SPACING["xl"]
    spacing_sm = Theme.SPACING["sm"]
    icon_padding = Theme.SPACING["2xl"]

    if page_width:
        icon_size = int(Theme.ICON_SIZE["2xl"] * (page_width / Theme.BASE_WIDTH))
        title_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["3xl"])
        subtitle_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["lg"])
        card_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["4xl"])
        spacing_xl = Theme.get_responsive_spacing(page_width, Theme.SPACING["xl"])
        spacing_sm = Theme.get_responsive_spacing(page_width, Theme.SPACING["sm"])
        icon_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["2xl"])

    # Contenido de la card
    content = ft.Column([
        # Ícono
        ft.Container(
            content=ft.Icon(
                icon,
                size=icon_size,
                color=card_color
            ),
            bgcolor=f"{card_color}22",
            border_radius=Theme.RADIUS["xl"],
            padding=icon_padding,
            alignment=ft.alignment.center,
        ),

        ft.Container(height=spacing_xl),

        # Título
        ft.Text(
            title,
            size=title_size,
            color=Theme.TEXT_PRIMARY,
            weight=Theme.FONT_WEIGHT["bold"],
            text_align=ft.TextAlign.CENTER
        ),

        # Subtítulo
        ft.Text(
            subtitle,
            size=subtitle_size,
            color=Theme.TEXT_SECONDARY,
            weight=Theme.FONT_WEIGHT["normal"],
            text_align=ft.TextAlign.CENTER
        ),
    ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=spacing_sm
    )

    # Crear card con efectos
    card = create_card_container(
        content=content,
        padding=card_padding,
        shadow="lg",
        on_click=on_click,
        width=width or Theme.DIMENSIONS["card_width_lg"],
        height=height or Theme.DIMENSIONS["card_height_lg"],
        page_width=page_width
    )

    # Efecto hover
    def on_hover(e):
        if e.data == "true":
            card.scale = ft.Scale(1.05)
            card.shadow = Theme.get_shadow("xl")
            card.bgcolor = Theme.CARD_BG_LIGHT
        else:
            card.scale = ft.Scale(1.0)
            card.shadow = Theme.get_shadow("lg")
            card.bgcolor = Theme.CARD_BG
        card.update()

    card.on_hover = on_hover
    card.animate_scale = Theme.STATES["transition_duration"]
    card.animate = Theme.STATES["transition_duration"]

    return card


def create_info_card(
    title: str,
    value: str,
    icon=None,
    color=None,
    width=None,
    page_width=None
):
    """
    Crear tarjeta de información - RESPONSIVE

    Args:
        title: Título
        value: Valor a mostrar
        icon: Ícono opcional
        color: Color del ícono
        width: Ancho personalizado (sobreescribe cálculo responsive)
        page_width: Ancho de la página para cálculo responsive

    Returns:
        Card de información
    """
    info_color = color or Theme.PRIMARY

    # Calcular dimensiones responsive
    if page_width and not width:
        width = Theme.get_responsive_width(page_width, "card", "md")

    # Calcular tamaños responsive
    icon_size = Theme.ICON_SIZE["lg"]
    title_size = Theme.FONT_SIZE["md"]
    value_size = Theme.FONT_SIZE["2xl"]
    card_padding = Theme.SPACING["xl"]
    icon_padding = Theme.SPACING["lg"]
    spacing_lg = Theme.SPACING["lg"]
    spacing_xs = Theme.SPACING["xs"]

    if page_width:
        icon_size = int(Theme.ICON_SIZE["lg"] * (page_width / Theme.BASE_WIDTH))
        title_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["md"])
        value_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["2xl"])
        card_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["xl"])
        icon_padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["lg"])
        spacing_lg = Theme.get_responsive_spacing(page_width, Theme.SPACING["lg"])
        spacing_xs = Theme.get_responsive_spacing(page_width, Theme.SPACING["xs"])

    content_items = []

    if icon:
        content_items.append(
            ft.Container(
                content=ft.Icon(icon, size=icon_size, color=info_color),
                bgcolor=f"{info_color}22",
                border_radius=Theme.RADIUS["md"],
                padding=icon_padding,
            )
        )

    content_items.extend([
        ft.Column([
            ft.Text(
                title,
                size=title_size,
                color=Theme.TEXT_SECONDARY,
                weight=Theme.FONT_WEIGHT["medium"]
            ),
            ft.Text(
                value,
                size=value_size,
                color=Theme.TEXT_PRIMARY,
                weight=Theme.FONT_WEIGHT["bold"]
            ),
        ], spacing=spacing_xs),
    ])

    return create_card_container(
        content=ft.Row(
            content_items,
            spacing=spacing_lg,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=card_padding,
        width=width or Theme.DIMENSIONS["card_width_md"],
        shadow="sm",
        page_width=page_width
    )


def create_alert_card(
    message: str,
    alert_type: str = "warning",
    icon=None,
    page_width=None
):
    """
    Crear tarjeta de alerta minimalista - RESPONSIVE

    Args:
        message: Mensaje de la alerta
        alert_type: Tipo ("success", "warning", "error", "info")
        icon: Ícono personalizado (opcional)
        page_width: Ancho de la página para cálculo responsive

    Returns:
        Card de alerta minimalista sin colores de fondo
    """
    # Configuración por tipo
    config = {
        "success": {
            "color": Theme.SUCCESS,
            "icon": icon or ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
        },
        "warning": {
            "color": Theme.WARNING,
            "icon": icon or ft.Icons.WARNING_AMBER_ROUNDED,
        },
        "error": {
            "color": Theme.ERROR,
            "icon": icon or ft.Icons.ERROR_OUTLINE_ROUNDED,
        },
        "info": {
            "color": Theme.TEXT_SECONDARY,
            "icon": icon or ft.Icons.INFO_OUTLINE_ROUNDED,
        }
    }

    cfg = config.get(alert_type, config["info"])

    # Calcular tamaños responsive
    icon_size = 24
    text_size = Theme.FONT_SIZE["lg"]
    padding = Theme.SPACING["xl"]
    spacing = Theme.SPACING["md"]

    if page_width:
        icon_size = int(24 * (page_width / Theme.BASE_WIDTH))
        text_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["lg"])
        padding = Theme.get_responsive_spacing(page_width, Theme.SPACING["xl"])
        spacing = Theme.get_responsive_spacing(page_width, Theme.SPACING["md"])

    return ft.Container(
        content=ft.Row([
            ft.Icon(
                cfg["icon"],
                size=icon_size,
                color=cfg["color"]
            ),
            ft.Text(
                message,
                size=text_size,
                color=Theme.TEXT_PRIMARY,
                weight=Theme.FONT_WEIGHT["medium"],
                expand=True
            ),
        ], spacing=spacing),
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(1, Theme.BORDER_LIGHT),
        border_radius=Theme.RADIUS["lg"],
        padding=padding,
        shadow=Theme.get_shadow("sm"),
    )
