"""
Dashboard Layout - Layout especializado para dashboards con estadísticas

Este layout extiende el base_layout y añade áreas predefinidas para:
- Tarjetas de estadísticas (stats cards)
- Gráficos y métricas
- Actividad reciente
- Widgets personalizados

Estructura:
┌─────────┬──────────────────────┐
│         │      HEADER          │
│ SIDEBAR ├──────────────────────┤
│         │   STATS CARDS        │
│         ├──────────────────────┤
│         │   MAIN CONTENT       │
│         │   (Grids/Charts)     │
│         ├──────────────────────┤
│         │   ACTIVITY FEED      │
└─────────┴──────────────────────┘
"""
import flet as ft
from config.theme import Theme
from .base_layout import create_base_layout


def create_dashboard_layout(
    page: ft.Page,
    role: str,
    current_section: str,
    on_section_click,
    user_info: dict,
    on_logout,
    stats_cards: list = None,
    main_content: ft.Control = None,
    activity_feed: ft.Control = None,
    widgets: list = None,
    show_back_button=False,
    on_back=None
):
    """
    Crear layout de dashboard con áreas predefinidas para stats y contenido

    Args:
        page: Instancia de ft.Page
        role: Rol del usuario ("admin" o "client")
        current_section: Sección actual activa
        on_section_click: Callback para cambiar de sección
        user_info: Información del usuario (dict con 'nombre', 'rol', etc.)
        on_logout: Callback para cerrar sesión
        stats_cards: Lista de tarjetas de estadísticas (opcional)
        main_content: Contenido principal del dashboard (opcional)
        activity_feed: Widget de actividad reciente (opcional)
        widgets: Lista de widgets adicionales (opcional)
        show_back_button: Mostrar botón de volver
        on_back: Callback para volver

    Returns:
        None (agrega directamente a page usando base_layout)

    Ejemplo:
        >>> from ui.components.molecules import create_stat_card
        >>>
        >>> stats = [
        ...     create_stat_card("Ingresos", "S/. 12,450", ft.Icons.ATTACH_MONEY, trend="+12%"),
        ...     create_stat_card("Clientes", "156", ft.Icons.PEOPLE, trend="+8%"),
        ...     create_stat_card("Asistencias", "342", ft.Icons.DIRECTIONS_RUN, trend="+5%"),
        ... ]
        >>>
        >>> content = ft.Column([
        ...     ft.Text("Gráfico de ventas aquí"),
        ...     # ... más contenido ...
        ... ])
        >>>
        >>> create_dashboard_layout(
        ...     page=page,
        ...     role="admin",
        ...     current_section="Dashboard",
        ...     on_section_click=navigate,
        ...     user_info={"nombre": "Juan", "rol": "Administrador"},
        ...     on_logout=logout,
        ...     stats_cards=stats,
        ...     main_content=content
        ... )
    """
    # Construir contenido del dashboard
    dashboard_content = _build_dashboard_content(
        stats_cards=stats_cards,
        main_content=main_content,
        activity_feed=activity_feed,
        widgets=widgets
    )

    # Usar base_layout para estructura general
    create_base_layout(
        page=page,
        role=role,
        current_section=current_section,
        on_section_click=on_section_click,
        content=dashboard_content,
        user_info=user_info,
        on_logout=on_logout,
        show_back_button=show_back_button,
        on_back=on_back
    )


def _build_dashboard_content(
    stats_cards: list = None,
    main_content: ft.Control = None,
    activity_feed: ft.Control = None,
    widgets: list = None
):
    """
    Construir el contenido del dashboard con sus diferentes secciones

    Args:
        stats_cards: Lista de tarjetas de estadísticas
        main_content: Contenido principal
        activity_feed: Feed de actividad
        widgets: Widgets adicionales

    Returns:
        ft.Column con el contenido organizado
    """
    content_sections = []

    # Sección 1: Stats Cards (si existen)
    if stats_cards:
        stats_section = _create_stats_section(stats_cards)
        content_sections.append(stats_section)
        content_sections.append(ft.Container(height=Theme.SPACING["2xl"]))

    # Sección 2: Main Content (si existe)
    if main_content:
        main_section = ft.Container(
            content=main_content,
            expand=True,
        )
        content_sections.append(main_section)

    # Sección 3: Activity Feed / Widgets (si existen)
    if activity_feed or widgets:
        bottom_section = _create_bottom_section(activity_feed, widgets)
        content_sections.append(ft.Container(height=Theme.SPACING["2xl"]))
        content_sections.append(bottom_section)

    # Si no hay contenido, mostrar mensaje
    if not content_sections:
        from ..components.molecules import create_empty_state
        content_sections.append(
            create_empty_state(
                message="No hay contenido para mostrar",
                icon=ft.Icons.DASHBOARD,
                secondary_message="Configura tu dashboard agregando widgets y estadísticas"
            )
        )

    return ft.Column(
        content_sections,
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )


def _create_stats_section(stats_cards: list):
    """
    Crear sección de tarjetas de estadísticas con diseño responsive

    Args:
        stats_cards: Lista de tarjetas de estadísticas

    Returns:
        ft.Container con las tarjetas organizadas
    """
    # Organizar en filas de 3 cards (responsive)
    rows = []
    cards_per_row = 3

    for i in range(0, len(stats_cards), cards_per_row):
        row_cards = stats_cards[i:i + cards_per_row]

        # Crear fila con las cards
        row = ft.Row(
            row_cards,
            spacing=Theme.SPACING["xl"],
            wrap=True,
            alignment=ft.MainAxisAlignment.START
        )
        rows.append(row)

    return ft.Container(
        content=ft.Column(
            rows,
            spacing=Theme.SPACING["xl"]
        ),
        padding=0,
    )


def _create_bottom_section(activity_feed=None, widgets=None):
    """
    Crear sección inferior con activity feed y/o widgets

    Args:
        activity_feed: Widget de actividad reciente
        widgets: Lista de widgets adicionales

    Returns:
        ft.Container con el contenido organizado
    """
    content_parts = []

    # Si hay activity feed, ponerlo a la izquierda (2/3)
    if activity_feed:
        activity_container = ft.Container(
            content=activity_feed,
            expand=2,
        )
        content_parts.append(activity_container)

    # Si hay widgets, ponerlos a la derecha (1/3)
    if widgets:
        widgets_column = ft.Column(
            widgets,
            spacing=Theme.SPACING["xl"],
            expand=1,
        )
        content_parts.append(widgets_column)

    # Si solo hay una parte, no usar Row
    if len(content_parts) == 1:
        return content_parts[0]

    # Si hay ambas, usar Row
    return ft.Row(
        content_parts,
        spacing=Theme.SPACING["2xl"],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def create_stats_grid(stats_cards: list, columns=3):
    """
    Crear grid de estadísticas con número personalizado de columnas
    (Función helper para casos específicos)

    Args:
        stats_cards: Lista de tarjetas de estadísticas
        columns: Número de columnas (default: 3)

    Returns:
        ft.Column con las tarjetas organizadas en grid

    Ejemplo:
        >>> stats = [
        ...     create_stat_card("Ingresos", "S/. 12,450", ft.Icons.ATTACH_MONEY),
        ...     create_stat_card("Clientes", "156", ft.Icons.PEOPLE),
        ...     create_stat_card("Asistencias", "342", ft.Icons.DIRECTIONS_RUN),
        ...     create_stat_card("Productos", "89", ft.Icons.INVENTORY),
        ... ]
        >>> grid = create_stats_grid(stats, columns=2)  # Grid de 2 columnas
    """
    rows = []

    for i in range(0, len(stats_cards), columns):
        row_cards = stats_cards[i:i + columns]

        row = ft.Row(
            row_cards,
            spacing=Theme.SPACING["xl"],
            wrap=True,
            alignment=ft.MainAxisAlignment.START
        )
        rows.append(row)

    return ft.Column(
        rows,
        spacing=Theme.SPACING["xl"]
    )


def create_activity_widget(
    title: str,
    items: list,
    icon=None,
    empty_message="No hay actividad reciente"
):
    """
    Crear widget de actividad reciente / historial

    Args:
        title: Título del widget
        items: Lista de items a mostrar (cada item es un ft.Control)
        icon: Ícono del título (opcional)
        empty_message: Mensaje cuando no hay items

    Returns:
        ft.Container con el widget de actividad

    Ejemplo:
        >>> items = [
        ...     ft.ListTile(
        ...         leading=ft.Icon(ft.Icons.PERSON_ADD, color=Theme.SUCCESS),
        ...         title=ft.Text("Nuevo cliente: Juan Pérez"),
        ...         subtitle=ft.Text("Hace 5 minutos")
        ...     ),
        ...     ft.ListTile(
        ...         leading=ft.Icon(ft.Icons.PAYMENT, color=Theme.PRIMARY),
        ...         title=ft.Text("Pago recibido: S/. 150"),
        ...         subtitle=ft.Text("Hace 1 hora")
        ...     ),
        ... ]
        >>> activity = create_activity_widget(
        ...     title="Actividad Reciente",
        ...     items=items,
        ...     icon=ft.Icons.HISTORY
        ... )
    """
    from ..components.molecules import create_card_container, create_empty_state

    # Header del widget
    header = ft.Row([
        ft.Icon(icon or ft.Icons.HISTORY, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
        ft.Text(
            title,
            size=Theme.FONT_SIZE["lg"],
            weight=Theme.FONT_WEIGHT["bold"],
            color=Theme.TEXT_PRIMARY
        ),
    ], spacing=Theme.SPACING["md"])

    # Contenido
    if items and len(items) > 0:
        content = ft.Column([
            header,
            ft.Container(height=Theme.SPACING["lg"]),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Container(height=Theme.SPACING["sm"]),
            ft.Column(
                items,
                spacing=Theme.SPACING["sm"],
                scroll=ft.ScrollMode.AUTO,
            )
        ], spacing=0)
    else:
        # Estado vacío
        content = ft.Column([
            header,
            ft.Container(height=Theme.SPACING["xl"]),
            create_empty_state(
                message=empty_message,
                icon=ft.Icons.INBOX,
            )
        ], spacing=0)

    return create_card_container(
        content=content,
        padding=Theme.SPACING["xl"],
        shadow="md"
    )


def create_quick_actions_widget(title: str, actions: list):
    """
    Crear widget de acciones rápidas (botones)

    Args:
        title: Título del widget
        actions: Lista de tuplas (texto, ícono, callback)

    Returns:
        ft.Container con el widget de acciones

    Ejemplo:
        >>> actions = [
        ...     ("Nuevo Cliente", ft.Icons.PERSON_ADD, lambda e: add_client()),
        ...     ("Nueva Venta", ft.Icons.SHOPPING_CART, lambda e: new_sale()),
        ...     ("Registrar Asistencia", ft.Icons.DIRECTIONS_RUN, lambda e: register_attendance()),
        ... ]
        >>> quick_actions = create_quick_actions_widget("Acciones Rápidas", actions)
    """
    from ..components.molecules import create_card_container
    from ..components.atoms import create_outlined_button

    # Header del widget
    header = ft.Row([
        ft.Icon(ft.Icons.FLASH_ON, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
        ft.Text(
            title,
            size=Theme.FONT_SIZE["lg"],
            weight=Theme.FONT_WEIGHT["bold"],
            color=Theme.TEXT_PRIMARY
        ),
    ], spacing=Theme.SPACING["md"])

    # Botones de acciones
    action_buttons = []
    for text, icon, callback in actions:
        btn = create_outlined_button(
            text,
            callback,
            icon=icon,
            width=None  # Full width
        )
        action_buttons.append(btn)

    content = ft.Column([
        header,
        ft.Container(height=Theme.SPACING["lg"]),
        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
        ft.Container(height=Theme.SPACING["md"]),
        ft.Column(
            action_buttons,
            spacing=Theme.SPACING["md"],
        )
    ], spacing=0)

    return create_card_container(
        content=content,
        padding=Theme.SPACING["xl"],
        shadow="md"
    )
