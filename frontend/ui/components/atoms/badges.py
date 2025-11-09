"""
Componentes Atom - Badges (Etiquetas)
Badges y etiquetas de estado reutilizables
"""
import flet as ft
from config.theme import Theme


def create_status_badge(text: str, status="success", icon=None):
    """
    Crear badge de estado con colores semánticos

    Args:
        text: Texto del badge
        status: Estado ("success", "warning", "error", "info", "default")
        icon: Ícono opcional (ft.Icons.*)

    Returns:
        ft.Container con el badge

    Ejemplo:
        >>> badge = create_status_badge("Activo", status="success", icon=ft.Icons.CHECK_CIRCLE)
        >>> badge = create_status_badge("Pendiente", status="warning")
        >>> badge = create_status_badge("Vencido", status="error")
    """
    # Mapeo de colores por estado
    status_colors = {
        "success": Theme.SUCCESS,
        "warning": Theme.WARNING,
        "error": Theme.ERROR,
        "danger": Theme.DANGER,
        "info": Theme.INFO,
        "primary": Theme.PRIMARY,
        "default": Theme.TEXT_SECONDARY,
    }

    bg_color = status_colors.get(status, status_colors["default"])

    controls = []
    if icon:
        controls.append(
            ft.Icon(icon, size=Theme.ICON_SIZE["xs"], color=ft.Colors.WHITE)
        )

    controls.append(
        ft.Text(
            text,
            size=Theme.FONT_SIZE["xs"],
            color=ft.Colors.WHITE,
            weight=Theme.FONT_WEIGHT["bold"]
        )
    )

    return ft.Container(
        content=ft.Row(
            controls=controls,
            spacing=Theme.SPACING["xs"],
            tight=True,
        ),
        bgcolor=bg_color,
        padding=ft.padding.symmetric(
            horizontal=Theme.SPACING["md"],
            vertical=Theme.SPACING["xs"]
        ),
        border_radius=Theme.RADIUS["2xl"],
    )


def create_info_badge(text: str, icon=None, color=None):
    """
    Crear badge informativo personalizado

    Args:
        text: Texto del badge
        icon: Ícono opcional
        color: Color personalizado (default: PRIMARY)

    Returns:
        ft.Container con el badge

    Ejemplo:
        >>> badge = create_info_badge("Nuevo", icon=ft.Icons.STAR, color=Theme.PRIMARY)
    """
    bg_color = color or Theme.PRIMARY

    controls = []
    if icon:
        controls.append(
            ft.Icon(icon, size=Theme.ICON_SIZE["xs"], color=ft.Colors.WHITE)
        )

    controls.append(
        ft.Text(
            text,
            size=Theme.FONT_SIZE["xs"],
            color=ft.Colors.WHITE,
            weight=Theme.FONT_WEIGHT["bold"]
        )
    )

    return ft.Container(
        content=ft.Row(
            controls=controls,
            spacing=Theme.SPACING["xs"],
            tight=True,
        ),
        bgcolor=bg_color,
        padding=ft.padding.symmetric(
            horizontal=Theme.SPACING["md"],
            vertical=Theme.SPACING["xs"]
        ),
        border_radius=Theme.RADIUS["2xl"],
    )


def create_count_badge(count: int, color=None, max_count=99):
    """
    Crear badge de contador (usado en notificaciones, carritos, etc.)

    Args:
        count: Número a mostrar
        color: Color de fondo (default: ERROR/rojo)
        max_count: Número máximo antes de mostrar "99+"

    Returns:
        ft.Container con el badge

    Ejemplo:
        >>> badge = create_count_badge(5)  # Muestra "5"
        >>> badge = create_count_badge(150)  # Muestra "99+"
    """
    bg_color = color or Theme.ERROR
    display_count = f"{max_count}+" if count > max_count else str(count)

    return ft.Container(
        content=ft.Text(
            display_count,
            size=Theme.FONT_SIZE["xs"],
            color=ft.Colors.WHITE,
            weight=Theme.FONT_WEIGHT["bold"],
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=bg_color,
        padding=ft.padding.symmetric(
            horizontal=Theme.SPACING["xs"] if count < 10 else Theme.SPACING["sm"],
            vertical=Theme.SPACING["xs"]
        ),
        border_radius=Theme.RADIUS["full"],
        min_width=20,
        height=20,
        alignment=ft.alignment.center,
    )


def create_outline_badge(text: str, color=None, icon=None):
    """
    Crear badge con solo borde (sin relleno)

    Args:
        text: Texto del badge
        color: Color del borde y texto (default: PRIMARY)
        icon: Ícono opcional

    Returns:
        ft.Container con el badge

    Ejemplo:
        >>> badge = create_outline_badge("Premium", color=Theme.PRIMARY)
    """
    badge_color = color or Theme.PRIMARY

    controls = []
    if icon:
        controls.append(
            ft.Icon(icon, size=Theme.ICON_SIZE["xs"], color=badge_color)
        )

    controls.append(
        ft.Text(
            text,
            size=Theme.FONT_SIZE["xs"],
            color=badge_color,
            weight=Theme.FONT_WEIGHT["semibold"]
        )
    )

    return ft.Container(
        content=ft.Row(
            controls=controls,
            spacing=Theme.SPACING["xs"],
            tight=True,
        ),
        bgcolor=ft.Colors.TRANSPARENT,
        padding=ft.padding.symmetric(
            horizontal=Theme.SPACING["md"],
            vertical=Theme.SPACING["xs"]
        ),
        border_radius=Theme.RADIUS["2xl"],
        border=ft.border.all(1, badge_color),
    )
