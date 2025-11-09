"""
Componentes Molecule - Dialogs (Diálogos)
Diálogos y modales reutilizables
"""
import flet as ft
from config.theme import Theme


def create_confirmation_dialog(
    page: ft.Page,
    title: str,
    message: str,
    on_confirm,
    on_cancel=None,
    confirm_text="Confirmar",
    cancel_text="Cancelar",
    warning_message=None,
    is_danger=False
):
    """
    Crear diálogo de confirmación estándar

    Args:
        page: Instancia de ft.Page
        title: Título del diálogo
        message: Mensaje principal
        on_confirm: Función a ejecutar al confirmar
        on_cancel: Función a ejecutar al cancelar (opcional)
        confirm_text: Texto del botón de confirmación
        cancel_text: Texto del botón de cancelación
        warning_message: Mensaje de advertencia adicional
        is_danger: Si es una acción peligrosa (botón rojo)

    Returns:
        ft.AlertDialog configurado

    Ejemplo:
        >>> dialog = create_confirmation_dialog(
        ...     page,
        ...     title="Eliminar Cliente",
        ...     message="¿Estás seguro de eliminar este cliente?",
        ...     on_confirm=lambda e: delete_client(),
        ...     warning_message="Esta acción no se puede deshacer",
        ...     is_danger=True
        ... )
        >>> page.open(dialog)
    """
    from ..atoms.buttons import create_primary_button, create_text_button, create_danger_button

    def close_and_confirm(e):
        page.close(dialog)
        if on_confirm:
            on_confirm(e)

    def close_and_cancel(e):
        page.close(dialog)
        if on_cancel:
            on_cancel(e)

    # Contenido del diálogo
    content_controls = [
        ft.Text(
            message,
            size=Theme.FONT_SIZE["md"],
            color=Theme.TEXT_PRIMARY
        ),
    ]

    # Mensaje de advertencia (si existe)
    if warning_message:
        content_controls.append(ft.Container(height=Theme.SPACING["md"]))
        content_controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.WARNING_AMBER_ROUNDED,
                        size=Theme.ICON_SIZE["sm"],
                        color=Theme.WARNING
                    ),
                    ft.Text(
                        warning_message,
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.WARNING,
                        weight=Theme.FONT_WEIGHT["medium"],
                        expand=True
                    ),
                ], spacing=Theme.SPACING["sm"]),
                bgcolor=f"{Theme.WARNING}15",
                padding=Theme.SPACING["md"],
                border_radius=Theme.RADIUS["sm"],
                border=ft.border.all(1, Theme.WARNING)
            )
        )

    # Botones de acción
    actions = [
        create_text_button(cancel_text, close_and_cancel),
    ]

    if is_danger:
        actions.append(create_danger_button(confirm_text, close_and_confirm))
    else:
        actions.append(create_primary_button(confirm_text, close_and_confirm))

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(
                ft.Icons.HELP_OUTLINE if not is_danger else ft.Icons.WARNING_AMBER_ROUNDED,
                size=Theme.ICON_SIZE["md"],
                color=Theme.PRIMARY if not is_danger else Theme.ERROR
            ),
            ft.Text(
                title,
                size=Theme.FONT_SIZE["xl"],
                weight=Theme.FONT_WEIGHT["bold"]
            ),
        ], spacing=Theme.SPACING["md"]),
        content=ft.Column(
            content_controls,
            tight=True,
            spacing=Theme.SPACING["sm"]
        ),
        actions=actions,
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=Theme.CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["lg"]),
    )

    return dialog


def create_alert_dialog(
    page: ft.Page,
    title: str,
    message: str,
    type="info",
    button_text="Aceptar",
    on_close=None
):
    """
    Crear diálogo de alerta simple (info/warning/error/success)

    Args:
        page: Instancia de ft.Page
        title: Título del diálogo
        message: Mensaje del diálogo
        type: Tipo de alerta ("info", "warning", "error", "success")
        button_text: Texto del botón
        on_close: Función al cerrar

    Returns:
        ft.AlertDialog configurado

    Ejemplo:
        >>> dialog = create_alert_dialog(
        ...     page,
        ...     title="Éxito",
        ...     message="Cliente guardado correctamente",
        ...     type="success"
        ... )
        >>> page.open(dialog)
    """
    from ..atoms.buttons import create_primary_button

    # Mapeo de tipos a íconos y colores
    type_config = {
        "info": {"icon": ft.Icons.INFO_OUTLINE, "color": Theme.INFO},
        "warning": {"icon": ft.Icons.WARNING_AMBER_ROUNDED, "color": Theme.WARNING},
        "error": {"icon": ft.Icons.ERROR_OUTLINE, "color": Theme.ERROR},
        "success": {"icon": ft.Icons.CHECK_CIRCLE_OUTLINE, "color": Theme.SUCCESS},
    }

    config = type_config.get(type, type_config["info"])

    def close_dialog(e):
        page.close(dialog)
        if on_close:
            on_close(e)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(
                config["icon"],
                size=Theme.ICON_SIZE["md"],
                color=config["color"]
            ),
            ft.Text(
                title,
                size=Theme.FONT_SIZE["xl"],
                weight=Theme.FONT_WEIGHT["bold"]
            ),
        ], spacing=Theme.SPACING["md"]),
        content=ft.Text(
            message,
            size=Theme.FONT_SIZE["md"],
            color=Theme.TEXT_PRIMARY
        ),
        actions=[
            create_primary_button(button_text, close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=Theme.CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["lg"]),
    )

    return dialog


def create_form_dialog(
    page: ft.Page,
    title: str,
    form_fields: list,
    on_submit,
    on_cancel=None,
    submit_text="Guardar",
    cancel_text="Cancelar",
    width=400
):
    """
    Crear diálogo con formulario

    Args:
        page: Instancia de ft.Page
        title: Título del diálogo
        form_fields: Lista de campos del formulario (ft.TextField, ft.Dropdown, etc.)
        on_submit: Función a ejecutar al enviar el formulario
        on_cancel: Función a ejecutar al cancelar
        submit_text: Texto del botón de envío
        cancel_text: Texto del botón de cancelación
        width: Ancho del diálogo

    Returns:
        ft.AlertDialog configurado

    Ejemplo:
        >>> name_field = ft.TextField(label="Nombre")
        >>> email_field = ft.TextField(label="Email")
        >>> dialog = create_form_dialog(
        ...     page,
        ...     title="Nuevo Cliente",
        ...     form_fields=[name_field, email_field],
        ...     on_submit=lambda e: save_client(name_field.value, email_field.value)
        ... )
        >>> page.open(dialog)
    """
    from ..atoms.buttons import create_primary_button, create_outlined_button

    def close_and_submit(e):
        page.close(dialog)
        if on_submit:
            on_submit(e)

    def close_and_cancel(e):
        page.close(dialog)
        if on_cancel:
            on_cancel(e)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            title,
            size=Theme.FONT_SIZE["xl"],
            weight=Theme.FONT_WEIGHT["bold"]
        ),
        content=ft.Container(
            content=ft.Column(
                form_fields,
                spacing=Theme.SPACING["lg"],
                tight=True,
            ),
            width=width,
            padding=ft.padding.symmetric(vertical=Theme.SPACING["md"])
        ),
        actions=[
            create_outlined_button(cancel_text, close_and_cancel),
            create_primary_button(submit_text, close_and_submit),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=Theme.CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["lg"]),
    )

    return dialog
