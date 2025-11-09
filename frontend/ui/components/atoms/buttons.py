"""
Componentes Atom - Botones
Botones reutilizables con estilos consistentes
"""
import flet as ft
from config.theme import Theme


def create_primary_button(
    text: str,
    on_click,
    icon=None,
    width=None,
    height=None,
    disabled=False
):
    """
    Crear botón primario (naranja, para acciones principales)

    Args:
        text: Texto del botón
        on_click: Función a ejecutar al hacer clic
        icon: Ícono opcional (ft.Icons.*)
        width: Ancho personalizado (default: auto)
        height: Alto personalizado (default: md)
        disabled: Si está deshabilitado

    Returns:
        ft.ElevatedButton configurado

    Ejemplo:
        >>> btn = create_primary_button("Guardar", on_save, icon=ft.Icons.SAVE)
    """
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width,
        height=height or Theme.DIMENSIONS["button_height_md"],
        disabled=disabled,
        style=ft.ButtonStyle(
            bgcolor=Theme.PRIMARY,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["sm"]),
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["xl"],
                vertical=Theme.SPACING["md"]
            ),
        )
    )


def create_outlined_button(
    text: str,
    on_click,
    icon=None,
    width=None,
    height=None,
    disabled=False,
    color=None
):
    """
    Crear botón con borde (para acciones secundarias)

    Args:
        text: Texto del botón
        on_click: Función a ejecutar al hacer clic
        icon: Ícono opcional
        width: Ancho personalizado
        height: Alto personalizado
        disabled: Si está deshabilitado
        color: Color personalizado (default: PRIMARY)

    Returns:
        ft.ElevatedButton configurado

    Ejemplo:
        >>> btn = create_outlined_button("Cancelar", on_cancel, icon=ft.Icons.CLOSE)
    """
    btn_color = color or Theme.PRIMARY

    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width,
        height=height or Theme.DIMENSIONS["button_height_md"],
        disabled=disabled,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.TRANSPARENT,
            color=btn_color,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["sm"]),
            side=ft.border.all(1, btn_color),
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["xl"],
                vertical=Theme.SPACING["md"]
            ),
        )
    )


def create_text_button(
    text: str,
    on_click,
    icon=None,
    color=None,
    disabled=False
):
    """
    Crear botón de texto simple (sin fondo ni borde)

    Args:
        text: Texto del botón
        on_click: Función a ejecutar al hacer clic
        icon: Ícono opcional
        color: Color del texto (default: PRIMARY)
        disabled: Si está deshabilitado

    Returns:
        ft.TextButton configurado

    Ejemplo:
        >>> btn = create_text_button("Más información", on_info)
    """
    return ft.TextButton(
        text=text,
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        style=ft.ButtonStyle(
            color=color or Theme.PRIMARY,
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["md"],
                vertical=Theme.SPACING["sm"]
            ),
        )
    )


def create_icon_button(
    icon,
    on_click,
    tooltip=None,
    color=None,
    size=None,
    disabled=False
):
    """
    Crear botón de solo ícono

    Args:
        icon: Ícono (ft.Icons.*)
        on_click: Función a ejecutar al hacer clic
        tooltip: Texto de ayuda al pasar el mouse
        color: Color del ícono (default: PRIMARY)
        size: Tamaño del ícono (default: md)
        disabled: Si está deshabilitado

    Returns:
        ft.IconButton configurado

    Ejemplo:
        >>> btn = create_icon_button(
        ...     ft.Icons.DELETE,
        ...     on_delete,
        ...     tooltip="Eliminar",
        ...     color=Theme.ERROR
        ... )
    """
    return ft.IconButton(
        icon=icon,
        on_click=on_click,
        tooltip=tooltip,
        icon_color=color or Theme.PRIMARY,
        icon_size=size or Theme.ICON_SIZE["md"],
        disabled=disabled,
    )


def create_danger_button(
    text: str,
    on_click,
    icon=None,
    width=None,
    height=None,
    disabled=False
):
    """
    Crear botón de peligro (rojo, para acciones destructivas)

    Args:
        text: Texto del botón
        on_click: Función a ejecutar al hacer clic
        icon: Ícono opcional
        width: Ancho personalizado
        height: Alto personalizado
        disabled: Si está deshabilitado

    Returns:
        ft.ElevatedButton configurado

    Ejemplo:
        >>> btn = create_danger_button("Eliminar", on_delete, icon=ft.Icons.DELETE)
    """
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width,
        height=height or Theme.DIMENSIONS["button_height_md"],
        disabled=disabled,
        style=ft.ButtonStyle(
            bgcolor=Theme.ERROR,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["sm"]),
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["xl"],
                vertical=Theme.SPACING["md"]
            ),
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
    """
    Crear botón de éxito (verde)

    Args:
        text: Texto del botón
        on_click: Función a ejecutar al hacer clic
        icon: Ícono opcional
        width: Ancho personalizado
        height: Alto personalizado
        disabled: Si está deshabilitado

    Returns:
        ft.ElevatedButton configurado

    Ejemplo:
        >>> btn = create_success_button("Aprobar", on_approve, icon=ft.Icons.CHECK)
    """
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        width=width,
        height=height or Theme.DIMENSIONS["button_height_md"],
        disabled=disabled,
        style=ft.ButtonStyle(
            bgcolor=Theme.SUCCESS,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["sm"]),
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["xl"],
                vertical=Theme.SPACING["md"]
            ),
        )
    )
