"""
Componentes Molecule - Cards (Tarjetas)
Tarjetas y contenedores reutilizables con estilos consistentes
"""
import flet as ft
from config.theme import Theme


def create_card_container(
    content,
    padding=None,
    margin=None,
    shadow="md",
    border_radius=None,
    bgcolor=None,
    border_color=None,
    on_click=None,
    width=None,
    height=None,
    expand=False
):
    """
    Crear contenedor de tarjeta reutilizable (el más básico y versátil)

    Args:
        content: Contenido de la tarjeta (puede ser cualquier widget)
        padding: Padding personalizado (default: lg/16px)
        margin: Margen personalizado
        shadow: Nivel de sombra ("none", "sm", "md", "lg", "xl")
        border_radius: Radio de esquinas (default: lg/12px)
        bgcolor: Color de fondo (default: CARD_BG)
        border_color: Color del borde (default: BORDER_DEFAULT)
        on_click: Función para hacer la tarjeta clickeable
        width: Ancho personalizado
        height: Alto personalizado
        expand: Si debe expandirse

    Returns:
        ft.Container configurado

    Ejemplo:
        >>> card = create_card_container(
        ...     content=ft.Text("Hola Mundo"),
        ...     shadow="lg",
        ...     on_click=lambda e: print("Click!")
        ... )
    """
    return ft.Container(
        content=content,
        padding=padding or Theme.SPACING["lg"],
        margin=margin,
        bgcolor=bgcolor or Theme.CARD_BG,
        border_radius=border_radius or Theme.RADIUS["lg"],
        border=ft.border.all(1, border_color or Theme.BORDER_DEFAULT),
        shadow=Theme.get_shadow(shadow),
        on_click=on_click,
        width=width,
        height=height,
        expand=expand,
    )


def create_stat_card(
    title: str,
    value: str,
    icon,
    color=None,
    trend=None,
    trend_positive=True,
    width=None,
    on_click=None
):
    """
    Crear tarjeta de estadística con ícono y tendencia opcional

    Args:
        title: Título de la estadística
        value: Valor a mostrar
        icon: Ícono (ft.Icons.*)
        color: Color del ícono y acento (default: PRIMARY)
        trend: Tendencia opcional (ej: "+12%", "-3%")
        trend_positive: Si la tendencia es positiva (verde) o negativa (roja)
        width: Ancho personalizado
        on_click: Función al hacer clic

    Returns:
        ft.Container con la tarjeta de estadística

    Ejemplo:
        >>> card = create_stat_card(
        ...     title="Ingresos",
        ...     value="S/. 12,450",
        ...     icon=ft.Icons.ATTACH_MONEY,
        ...     color=Theme.SUCCESS,
        ...     trend="+12%"
        ... )
    """
    stat_color = color or Theme.PRIMARY

    # Construir contenido
    content_controls = [
        # Fila superior: Ícono + Título
        ft.Row([
            ft.Container(
                content=ft.Icon(icon, size=Theme.ICON_SIZE["lg"], color=stat_color),
                bgcolor=f"{stat_color}22",
                border_radius=Theme.RADIUS["md"],
                padding=Theme.SPACING["md"],
            ),
            ft.Container(expand=True),
            # Tendencia (si existe)
            ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.TRENDING_UP if trend_positive else ft.Icons.TRENDING_DOWN,
                        size=Theme.ICON_SIZE["sm"],
                        color=Theme.SUCCESS if trend_positive else Theme.ERROR
                    ),
                    ft.Text(
                        trend,
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.SUCCESS if trend_positive else Theme.ERROR,
                        weight=Theme.FONT_WEIGHT["semibold"]
                    ),
                ], spacing=Theme.SPACING["xs"], tight=True),
                visible=trend is not None
            ) if trend else ft.Container(),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

        ft.Container(height=Theme.SPACING["md"]),

        # Valor principal
        ft.Text(
            value,
            size=Theme.FONT_SIZE["4xl"],
            color=Theme.TEXT_PRIMARY,
            weight=Theme.FONT_WEIGHT["bold"]
        ),

        # Título
        ft.Text(
            title,
            size=Theme.FONT_SIZE["sm"],
            color=Theme.TEXT_SECONDARY,
            weight=Theme.FONT_WEIGHT["medium"]
        ),
    ]

    # Crear tarjeta con efecto hover
    card = create_card_container(
        content=ft.Column(content_controls, spacing=Theme.SPACING["xs"]),
        padding=Theme.SPACING["xl"],
        shadow="md",
        on_click=on_click,
        width=width or Theme.DIMENSIONS["card_width_md"],
        height=Theme.DIMENSIONS["card_height_md"],
    )

    # Efecto hover si es clickeable
    if on_click:
        def on_hover(e):
            if e.data == "true":
                card.scale = ft.Scale(1.02)
                card.shadow = Theme.get_shadow("lg")
            else:
                card.scale = ft.Scale(1.0)
                card.shadow = Theme.get_shadow("md")
            card.update()

        card.on_hover = on_hover
        card.animate_scale = Theme.STATES["transition_duration"]

    return card


def create_info_card(
    title: str,
    value: str,
    icon,
    color=None,
    subtitle=None,
    width=None
):
    """
    Crear tarjeta de información simple (compatible con common.py)

    Args:
        title: Título de la información
        value: Valor a mostrar
        icon: Ícono (ft.Icons.*)
        color: Color del ícono (default: PRIMARY)
        subtitle: Subtítulo opcional
        width: Ancho personalizado

    Returns:
        ft.Container con la tarjeta

    Ejemplo:
        >>> card = create_info_card(
        ...     title="Clientes",
        ...     value="156",
        ...     icon=ft.Icons.PEOPLE
        ... )
    """
    info_color = color or Theme.PRIMARY

    return create_card_container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(icon, size=Theme.ICON_SIZE["lg"], color=info_color),
                bgcolor=f"{info_color}22",
                border_radius=Theme.RADIUS["md"],
                padding=Theme.SPACING["md"],
            ),
            ft.Column([
                ft.Text(
                    title,
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_SECONDARY,
                    weight=Theme.FONT_WEIGHT["normal"]
                ),
                ft.Text(
                    value,
                    size=Theme.FONT_SIZE["3xl"],
                    color=Theme.TEXT_PRIMARY,
                    weight=Theme.FONT_WEIGHT["bold"]
                ),
                ft.Text(
                    subtitle,
                    size=Theme.FONT_SIZE["xs"],
                    color=Theme.TEXT_MUTED,
                    visible=subtitle is not None
                ) if subtitle else ft.Container(),
            ], spacing=Theme.SPACING["xs"]),
        ], spacing=Theme.SPACING["lg"], alignment=ft.MainAxisAlignment.START),
        padding=Theme.SPACING["xl"],
        width=width or Theme.DIMENSIONS["card_width_md"],
        height=Theme.DIMENSIONS["card_height_sm"],
        shadow="sm",
    )


def create_empty_state(
    message: str,
    icon=None,
    action_text=None,
    on_action=None,
    secondary_message=None
):
    """
    Crear estado vacío cuando no hay datos

    Args:
        message: Mensaje principal
        icon: Ícono opcional (default: INBOX)
        action_text: Texto del botón de acción (opcional)
        on_action: Función al hacer clic en el botón
        secondary_message: Mensaje secundario/ayuda

    Returns:
        ft.Container con el estado vacío

    Ejemplo:
        >>> empty = create_empty_state(
        ...     message="No hay clientes registrados",
        ...     icon=ft.Icons.PEOPLE_OUTLINE,
        ...     action_text="Agregar Cliente",
        ...     on_action=lambda e: print("Agregar"),
        ...     secondary_message="Comienza agregando tu primer cliente"
        ... )
    """
    from ..atoms.buttons import create_primary_button

    controls = [
        ft.Icon(
            icon or ft.Icons.INBOX,
            size=Theme.ICON_SIZE["2xl"] * 1.5,
            color=Theme.TEXT_DISABLED
        ),
        ft.Container(height=Theme.SPACING["lg"]),
        ft.Text(
            message,
            size=Theme.FONT_SIZE["xl"],
            color=Theme.TEXT_SECONDARY,
            weight=Theme.FONT_WEIGHT["semibold"],
            text_align=ft.TextAlign.CENTER
        ),
    ]

    if secondary_message:
        controls.append(
            ft.Text(
                secondary_message,
                size=Theme.FONT_SIZE["md"],
                color=Theme.TEXT_MUTED,
                text_align=ft.TextAlign.CENTER
            )
        )

    if action_text and on_action:
        controls.append(ft.Container(height=Theme.SPACING["xl"]))
        controls.append(
            create_primary_button(action_text, on_action)
        )

    return create_card_container(
        content=ft.Column(
            controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=Theme.SPACING["sm"],
        ),
        padding=Theme.SPACING["4xl"],
        width=Theme.DIMENSIONS["card_width_lg"],
        shadow="sm",
    )
