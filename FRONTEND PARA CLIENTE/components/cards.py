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
    expand=False
):
    """
    Crear contenedor de tarjeta básico

    Args:
        content: Contenido de la tarjeta
        padding: Padding personalizado
        margin: Margen personalizado
        bgcolor: Color de fondo
        border_color: Color del borde
        shadow: Nivel de sombra
        on_click: Función al hacer clic
        width: Ancho personalizado
        height: Alto personalizado
        expand: Si debe expandirse

    Returns:
        ft.Container configurado
    """
    return ft.Container(
        content=content,
        padding=padding or Theme.SPACING["2xl"],
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
    height=None
):
    """
    Crear tarjeta de opción clickeable (para pantalla inicial)

    Args:
        title: Título principal
        subtitle: Subtítulo descriptivo
        icon: Ícono grande
        on_click: Función al hacer clic
        color: Color del ícono (default: PRIMARY)
        width: Ancho personalizado
        height: Alto personalizado

    Returns:
        Card interactiva con efecto hover
    """
    card_color = color or Theme.PRIMARY

    # Contenido de la card
    content = ft.Column([
        # Ícono
        ft.Container(
            content=ft.Icon(
                icon,
                size=Theme.ICON_SIZE["2xl"],
                color=card_color
            ),
            bgcolor=f"{card_color}22",
            border_radius=Theme.RADIUS["xl"],
            padding=Theme.SPACING["2xl"],
            alignment=ft.alignment.center,
        ),

        ft.Container(height=Theme.SPACING["xl"]),

        # Título
        ft.Text(
            title,
            size=Theme.FONT_SIZE["3xl"],
            color=Theme.TEXT_PRIMARY,
            weight=Theme.FONT_WEIGHT["bold"],
            text_align=ft.TextAlign.CENTER
        ),

        # Subtítulo
        ft.Text(
            subtitle,
            size=Theme.FONT_SIZE["lg"],
            color=Theme.TEXT_SECONDARY,
            weight=Theme.FONT_WEIGHT["normal"],
            text_align=ft.TextAlign.CENTER
        ),
    ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=Theme.SPACING["sm"]
    )

    # Crear card con efectos
    card = create_card_container(
        content=content,
        padding=Theme.SPACING["4xl"],
        shadow="lg",
        on_click=on_click,
        width=width or Theme.DIMENSIONS["card_width_lg"],
        height=height or Theme.DIMENSIONS["card_height_lg"],
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
    width=None
):
    """
    Crear tarjeta de información

    Args:
        title: Título
        value: Valor a mostrar
        icon: Ícono opcional
        color: Color del ícono
        width: Ancho personalizado

    Returns:
        Card de información
    """
    info_color = color or Theme.PRIMARY

    content_items = []

    if icon:
        content_items.append(
            ft.Container(
                content=ft.Icon(icon, size=Theme.ICON_SIZE["lg"], color=info_color),
                bgcolor=f"{info_color}22",
                border_radius=Theme.RADIUS["md"],
                padding=Theme.SPACING["lg"],
            )
        )

    content_items.extend([
        ft.Column([
            ft.Text(
                title,
                size=Theme.FONT_SIZE["md"],
                color=Theme.TEXT_SECONDARY,
                weight=Theme.FONT_WEIGHT["medium"]
            ),
            ft.Text(
                value,
                size=Theme.FONT_SIZE["2xl"],
                color=Theme.TEXT_PRIMARY,
                weight=Theme.FONT_WEIGHT["bold"]
            ),
        ], spacing=Theme.SPACING["xs"]),
    ])

    return create_card_container(
        content=ft.Row(
            content_items,
            spacing=Theme.SPACING["lg"],
            alignment=ft.MainAxisAlignment.START
        ),
        padding=Theme.SPACING["xl"],
        width=width or Theme.DIMENSIONS["card_width_md"],
        shadow="sm",
    )


def create_alert_card(
    message: str,
    alert_type: str = "warning",
    icon=None
):
    """
    Crear tarjeta de alerta minimalista

    Args:
        message: Mensaje de la alerta
        alert_type: Tipo ("success", "warning", "error", "info")
        icon: Ícono personalizado (opcional)

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

    return ft.Container(
        content=ft.Row([
            ft.Icon(
                cfg["icon"],
                size=24,
                color=cfg["color"]
            ),
            ft.Text(
                message,
                size=Theme.FONT_SIZE["lg"],
                color=Theme.TEXT_PRIMARY,
                weight=Theme.FONT_WEIGHT["medium"],
                expand=True
            ),
        ], spacing=Theme.SPACING["md"]),
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(1, Theme.BORDER_LIGHT),
        border_radius=Theme.RADIUS["lg"],
        padding=Theme.SPACING["xl"],
        shadow=Theme.get_shadow("sm"),
    )
