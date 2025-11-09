"""
CRUD Layout - Layout especializado para vistas CRUD (Crear/Leer/Actualizar/Eliminar)

Este layout extiende el base_layout y añade:
- Área de formulario (create/update)
- Área de listado/tabla
- Botones de acción CRUD
- Estados de carga

Estructura:
┌─────────┬──────────────────────┐
│         │      HEADER          │
│ SIDEBAR ├──────────────────────┤
│         │   FORM AREA          │
│         ├──────────────────────┤
│         │   TABLE/LIST AREA    │
└─────────┴──────────────────────┘
"""
import flet as ft
from config.theme import Theme
from .base_layout import create_base_layout


def create_crud_layout(
    page: ft.Page,
    role: str,
    current_section: str,
    on_section_click,
    user_info: dict,
    on_logout,
    form_fields: list = None,
    list_content: ft.Control = None,
    on_create=None,
    on_update=None,
    on_cancel=None,
    form_title="Nuevo Registro",
    list_title="Lista de Registros",
    show_form=True,
    edit_mode=False
):
    """
    Crear layout CRUD con formulario y listado

    Args:
        page: Instancia de ft.Page
        role: Rol del usuario ("admin" o "client")
        current_section: Sección actual activa
        on_section_click: Callback para cambiar de sección
        user_info: Información del usuario
        on_logout: Callback para cerrar sesión
        form_fields: Lista de campos del formulario (ft.TextField, ft.Dropdown, etc.)
        list_content: Contenido del listado (tabla, cards, etc.)
        on_create: Callback para crear nuevo registro
        on_update: Callback para actualizar registro
        on_cancel: Callback para cancelar edición
        form_title: Título del formulario
        list_title: Título del listado
        show_form: Mostrar/ocultar formulario
        edit_mode: Si está en modo edición (cambia botón de "Crear" a "Actualizar")

    Returns:
        None (agrega directamente a page usando base_layout)

    Ejemplo:
        >>> fields = [
        ...     ft.TextField(label="Nombre"),
        ...     ft.TextField(label="Email"),
        ... ]
        >>> list_content = ft.DataTable(...)
        >>> create_crud_layout(
        ...     page=page,
        ...     role="admin",
        ...     current_section="Clientes",
        ...     on_section_click=navigate,
        ...     user_info=user_data,
        ...     on_logout=logout,
        ...     form_fields=fields,
        ...     list_content=list_content,
        ...     on_create=save_client,
        ...     form_title="Nuevo Cliente"
        ... )
    """
    from ..components.atoms import create_primary_button, create_outlined_button
    from ..components.molecules import create_card_container

    # ==========================================
    # ÁREA DE FORMULARIO
    # ==========================================
    form_area = None
    if show_form and form_fields:
        # Botones del formulario
        form_buttons = []

        if on_cancel:
            form_buttons.append(
                create_outlined_button(
                    "Cancelar",
                    on_cancel,
                    icon=ft.Icons.CLOSE
                )
            )

        if edit_mode and on_update:
            form_buttons.append(
                create_primary_button(
                    "Actualizar",
                    on_update,
                    icon=ft.Icons.SAVE
                )
            )
        elif on_create:
            form_buttons.append(
                create_primary_button(
                    "Crear",
                    on_create,
                    icon=ft.Icons.ADD
                )
            )

        # Contenedor del formulario
        form_content = ft.Column([
            # Título del formulario
            ft.Row([
                ft.Icon(
                    ft.Icons.EDIT if edit_mode else ft.Icons.ADD_CIRCLE,
                    size=Theme.ICON_SIZE["md"],
                    color=Theme.PRIMARY
                ),
                ft.Text(
                    form_title,
                    size=Theme.FONT_SIZE["lg"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_PRIMARY
                ),
            ], spacing=Theme.SPACING["md"]),

            ft.Container(height=Theme.SPACING["lg"]),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Container(height=Theme.SPACING["lg"]),

            # Campos del formulario en grid responsive
            ft.ResponsiveRow(
                [ft.Container(field, col={"sm": 12, "md": 6, "lg": 4})
                 for field in form_fields],
                spacing=Theme.SPACING["md"]
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Botones de acción
            ft.Row(
                form_buttons,
                spacing=Theme.SPACING["md"],
                alignment=ft.MainAxisAlignment.END
            ),
        ], spacing=0)

        form_area = create_card_container(
            content=form_content,
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

    # ==========================================
    # ÁREA DE LISTADO
    # ==========================================
    list_area = None
    if list_content:
        list_area = ft.Container(
            content=ft.Column([
                # Título del listado
                ft.Row([
                    ft.Icon(
                        ft.Icons.LIST,
                        size=Theme.ICON_SIZE["md"],
                        color=Theme.PRIMARY
                    ),
                    ft.Text(
                        list_title,
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                ], spacing=Theme.SPACING["md"]),

                ft.Container(height=Theme.SPACING["lg"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Container(height=Theme.SPACING["lg"]),

                # Contenido del listado
                list_content,
            ], spacing=0),
            padding=Theme.SPACING["2xl"],
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["lg"],
            border=ft.border.all(1, Theme.BORDER_DEFAULT),
        )

    # ==========================================
    # CONTENIDO COMPLETO
    # ==========================================
    content_sections = []

    if form_area:
        content_sections.append(form_area)
        content_sections.append(ft.Container(height=Theme.SPACING["2xl"]))

    if list_area:
        content_sections.append(list_area)

    crud_content = ft.Column(
        content_sections,
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    # ==========================================
    # USAR BASE LAYOUT
    # ==========================================
    create_base_layout(
        page=page,
        role=role,
        current_section=current_section,
        on_section_click=on_section_click,
        content=crud_content,
        user_info=user_info,
        on_logout=on_logout
    )


def create_simple_list_layout(
    page: ft.Page,
    role: str,
    current_section: str,
    on_section_click,
    user_info: dict,
    on_logout,
    list_content: ft.Control,
    list_title="Lista",
    action_button_text=None,
    on_action=None
):
    """
    Crear layout simple con solo listado (sin formulario)

    Útil para vistas de solo lectura o con diálogos modales para edición

    Args:
        page: Instancia de ft.Page
        role: Rol del usuario
        current_section: Sección actual
        on_section_click: Callback navegación
        user_info: Info del usuario
        on_logout: Callback logout
        list_content: Contenido a mostrar
        list_title: Título del listado
        action_button_text: Texto del botón de acción (opcional)
        on_action: Callback del botón de acción (opcional)

    Returns:
        None (agrega directamente a page)

    Ejemplo:
        >>> create_simple_list_layout(
        ...     page=page,
        ...     role="admin",
        ...     current_section="Reportes",
        ...     on_section_click=navigate,
        ...     user_info=user_data,
        ...     on_logout=logout,
        ...     list_content=my_table,
        ...     list_title="Reportes Mensuales",
        ...     action_button_text="Generar Reporte",
        ...     on_action=generate_report
        ... )
    """
    from ..components.atoms import create_primary_button
    from ..components.molecules import create_card_container

    # Contenido del listado con botón opcional
    list_controls = [
        # Header con título y botón opcional
        ft.Row([
            ft.Icon(
                ft.Icons.LIST,
                size=Theme.ICON_SIZE["md"],
                color=Theme.PRIMARY
            ),
            ft.Text(
                list_title,
                size=Theme.FONT_SIZE["lg"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY,
                expand=True
            ),
            create_primary_button(
                action_button_text,
                on_action,
                icon=ft.Icons.ADD
            ) if action_button_text and on_action else ft.Container(),
        ], spacing=Theme.SPACING["md"], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

        ft.Container(height=Theme.SPACING["lg"]),
        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
        ft.Container(height=Theme.SPACING["lg"]),

        # Contenido
        list_content,
    ]

    list_area = create_card_container(
        content=ft.Column(list_controls, spacing=0),
        padding=Theme.SPACING["2xl"],
        shadow="md"
    )

    # Usar base layout
    create_base_layout(
        page=page,
        role=role,
        current_section=current_section,
        on_section_click=on_section_click,
        content=list_area,
        user_info=user_info,
        on_logout=on_logout
    )
