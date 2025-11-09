"""
Base Layout - Layout Universal con Sidebar + Header + Content

Este layout es la base para TODAS las vistas del sistema.
Incluye sidebar fijo, header con información del usuario, y área de contenido dinámica.

Estructura:
┌─────────┬──────────────────────┐
│         │      HEADER          │
│ SIDEBAR ├──────────────────────┤
│         │                      │
│         │      CONTENT         │
│         │                      │
└─────────┴──────────────────────┘
"""
import flet as ft
from datetime import datetime
from config.theme import Theme
from config.settings import LOGO_PATH


def create_base_layout(
    page: ft.Page,
    role: str,
    current_section: str,
    on_section_click,
    content,
    user_info: dict,
    on_logout,
    show_back_button=False,
    on_back=None
):
    """
    Crear layout base con sidebar + header + content

    OPTIMIZADO: Solo reconstruye si no existe, sino solo actualiza el contenido

    Args:
        page: Instancia de ft.Page
        role: Rol del usuario ("admin" o "client")
        current_section: Sección actual activa
        on_section_click: Callback para cambiar de sección
        content: Contenido dinámico de la vista (ft.Control)
        user_info: Información del usuario (dict con 'nombre', 'rol', etc.)
        on_logout: Callback para cerrar sesión
        show_back_button: Mostrar botón de volver en el header
        on_back: Callback para volver

    Returns:
        None (agrega directamente a page)
    """
    # Configurar página COMPLETAMENTE PEGADA
    page.padding = 0
    page.spacing = 0
    page.bgcolor = Theme.BACKGROUND_DARK

    # ESTRATEGIA ULTRA SIMPLE: Reconstruir siempre pero RÁPIDO
    page.controls.clear()

    # Crear sidebar
    sidebar = _create_sidebar(role, current_section, on_section_click)

    # Crear header
    header = _create_header(user_info, current_section, on_logout, show_back_button, on_back)

    # Área de contenido
    content_area = ft.Container(
        content=ft.Column([
            header,
            content
        ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO),
        expand=True,
        bgcolor=Theme.BACKGROUND_DARK,
        padding=0,
        margin=0,
    )

    # Layout principal - SIMPLE Y DIRECTO
    page.add(
        ft.Row(
            controls=[sidebar, content_area],
            spacing=0,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )

    # Update una sola vez al final
    page.update()


def _create_sidebar(role: str, current_section: str, on_section_click):
    """
    Crear sidebar con navegación según el rol

    Args:
        role: Rol del usuario ("admin" o "client")
        current_section: Sección actual activa
        on_section_click: Callback para cambiar de sección

    Returns:
        ft.Container con el sidebar
    """
    # Definir navegación según el rol
    if role == "admin":
        nav_items = [
            {"text": "Dashboard", "icon": ft.Icons.DASHBOARD, "section": "Dashboard"},
            {"text": "Clientes", "icon": ft.Icons.PEOPLE, "section": "Clientes"},
            {"text": "Membresías", "icon": ft.Icons.CARD_MEMBERSHIP, "section": "Membresias"},
            {"text": "Asistencia", "icon": ft.Icons.DIRECTIONS_RUN, "section": "Asistencia"},
            {"text": "Punto de Venta", "icon": ft.Icons.SHOPPING_CART, "section": "POS"},
            {"text": "Productos", "icon": ft.Icons.INVENTORY_2, "section": "Productos"},
            {"text": "Reportes", "icon": ft.Icons.ANALYTICS, "section": "Reportes"},
            {"text": "Finanzas", "icon": ft.Icons.ATTACH_MONEY, "section": "Finanzas"},
        ]
        footer_items = [
            {"text": "Configuración", "icon": ft.Icons.SETTINGS, "section": "Configuracion"},
            {"text": "Ayuda", "icon": ft.Icons.HELP, "section": "Soporte"},
        ]
    else:  # client
        nav_items = [
            {"text": "Mi Dashboard", "icon": ft.Icons.DASHBOARD, "section": "Dashboard"},
            {"text": "Mi Perfil", "icon": ft.Icons.PERSON, "section": "Mi Perfil"},
            {"text": "Membresías", "icon": ft.Icons.CARD_MEMBERSHIP, "section": "Membresías"},
            {"text": "Asistencias", "icon": ft.Icons.DIRECTIONS_RUN, "section": "Asistencias"},
            {"text": "Mis Rutinas", "icon": ft.Icons.FITNESS_CENTER, "section": "Rutinas"},
            {"text": "Pagos", "icon": ft.Icons.PAYMENT, "section": "Pagos"},
            {"text": "Mi Progreso", "icon": ft.Icons.TRENDING_UP, "section": "Progreso"},
            {"text": "Horarios", "icon": ft.Icons.SCHEDULE, "section": "Horarios"},
        ]
        footer_items = [
            {"text": "Configuración", "icon": ft.Icons.SETTINGS, "section": "Configuracion"},
            {"text": "Ayuda", "icon": ft.Icons.HELP, "section": "Soporte"},
        ]

    def create_nav_item(text, icon, section, is_active=False):
        """Crear item de navegación con diseño moderno"""
        item = ft.Container(
            content=ft.Row([
                ft.Icon(
                    icon,
                    size=Theme.ICON_SIZE["md"],
                    color=Theme.PRIMARY if is_active else Theme.TEXT_SECONDARY,
                ),
                ft.Text(
                    text,
                    size=Theme.FONT_SIZE["md"],
                    color=Theme.TEXT_PRIMARY if is_active else Theme.TEXT_SECONDARY,
                    weight=Theme.FONT_WEIGHT["semibold"] if is_active else Theme.FONT_WEIGHT["medium"],
                    expand=True,
                ),
            ], spacing=Theme.SPACING["md"]),
            padding=ft.padding.symmetric(
                horizontal=Theme.SPACING["lg"],
                vertical=Theme.SPACING["md"]
            ),
            border_radius=Theme.RADIUS["md"],
            bgcolor=f"{Theme.PRIMARY}20" if is_active else "transparent",
            border=ft.border.only(
                left=ft.border.BorderSide(3, Theme.PRIMARY) if is_active else ft.border.BorderSide(3, "transparent")
            ),
            on_click=lambda e: on_section_click(section),
            animate=Theme.STATES["transition_duration"],
        )

        def on_hover(e):
            if e.data == "true":
                if not is_active:
                    item.bgcolor = f"{Theme.PRIMARY}10"
                    item.border = ft.border.only(
                        left=ft.border.BorderSide(3, f"{Theme.PRIMARY}60")
                    )
            else:
                item.bgcolor = f"{Theme.PRIMARY}20" if is_active else "transparent"
                item.border = ft.border.only(
                    left=ft.border.BorderSide(3, Theme.PRIMARY) if is_active else ft.border.BorderSide(3, "transparent")
                )
            item.update()

        item.on_hover = on_hover
        return item

    # Logo section
    logo_content = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.FITNESS_CENTER,
                    size=Theme.ICON_SIZE["xl"],
                    color=Theme.PRIMARY
                ),
                bgcolor=f"{Theme.PRIMARY}20",
                border_radius=Theme.RADIUS["lg"],
                padding=Theme.SPACING["md"],
                alignment=ft.alignment.center,
            ),
            ft.Text(
                "BLESSED GYM",
                size=Theme.FONT_SIZE["xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(
                content=ft.Text(
                    "Sistema de Gestión",
                    size=Theme.FONT_SIZE["xs"],
                    color=Theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER
                ),
                margin=ft.margin.only(top=-Theme.SPACING["xs"])
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),
        padding=ft.padding.symmetric(vertical=Theme.SPACING["xl"], horizontal=Theme.SPACING["md"]),
    )

    # Construir items de navegación
    nav_controls = []
    for item in nav_items:
        nav_controls.append(
            create_nav_item(
                item["text"],
                item["icon"],
                item["section"],
                is_active=(item["section"] == current_section)
            )
        )

    # Footer items
    footer_controls = [
        ft.Container(
            content=ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            padding=ft.padding.symmetric(horizontal=Theme.SPACING["xs"]),
            margin=ft.margin.only(bottom=Theme.SPACING["sm"], top=Theme.SPACING["xs"])
        ),
    ]

    for item in footer_items:
        footer_controls.append(
            create_nav_item(
                item["text"],
                item["icon"],
                item["section"],
                is_active=(item["section"] == current_section)
            )
        )

    footer_controls.append(ft.Container(height=Theme.SPACING["lg"]))

    # Sidebar completo - COMPLETAMENTE PEGADO SIN ESPACIOS
    sidebar = ft.Container(
        content=ft.Column([
            logo_content,
            ft.Container(
                content=ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"]),
                margin=ft.margin.only(bottom=Theme.SPACING["md"])
            ),
            ft.Container(
                content=ft.Column(nav_controls, spacing=Theme.SPACING["xs"]),
                padding=ft.padding.symmetric(horizontal=Theme.SPACING["md"]),
            ),
            ft.Container(height=Theme.SPACING["md"]),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Column(footer_controls, spacing=Theme.SPACING["xs"]),
                padding=ft.padding.symmetric(horizontal=Theme.SPACING["md"]),
            )
        ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True),
        width=Theme.DIMENSIONS["sidebar_width"],
        padding=0,
        margin=0,  # SIN MARGEN
        bgcolor=Theme.SIDEBAR_BG,
        border=ft.border.only(right=ft.border.BorderSide(1, f"{Theme.BORDER_DEFAULT}80")),
        expand=False,  # NO expandir horizontalmente (ancho fijo)
    )

    return sidebar


def _create_header(user_info: dict, current_section: str, on_logout, show_back=False, on_back=None):
    """
    Crear header con información del usuario

    Args:
        user_info: Información del usuario
        current_section: Sección actual
        on_logout: Callback para logout
        show_back: Mostrar botón de volver
        on_back: Callback para volver

    Returns:
        ft.Container con el header
    """
    from ..components.atoms import create_outlined_button, create_icon_button

    header_controls = []

    # Botón de volver (opcional)
    if show_back and on_back:
        header_controls.append(
            create_icon_button(
                ft.Icons.ARROW_BACK,
                on_back,
                tooltip="Volver",
                color=Theme.PRIMARY
            )
        )
        header_controls.append(ft.Container(width=Theme.SPACING["md"]))

    # Información del usuario
    header_controls.append(
        ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.PERSON, size=Theme.ICON_SIZE["sm"], color=Theme.PRIMARY),
                bgcolor=f"{Theme.PRIMARY}20",
                border_radius=Theme.RADIUS["md"],
                padding=Theme.SPACING["md"],
                width=42,
                height=42,
            ),
            ft.Column([
                ft.Text(
                    f"Bienvenido, {user_info.get('nombre', 'Usuario')}",
                    size=Theme.FONT_SIZE["md"],
                    weight=Theme.FONT_WEIGHT["semibold"],
                    color=Theme.TEXT_PRIMARY
                ),
                ft.Text(
                    user_info.get('rol', 'Usuario'),
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_SECONDARY
                ),
            ], spacing=1),
        ], spacing=Theme.SPACING["md"])
    )

    header_controls.append(ft.Container(expand=True))

    # Título de sección
    header_controls.append(
        ft.Container(
            content=ft.Column([
                ft.Text(
                    current_section,
                    size=Theme.FONT_SIZE["xl"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_PRIMARY
                ),
            ], spacing=2),
            padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"]),
        )
    )

    # Información de fecha y hora
    header_controls.append(
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ACCESS_TIME, size=Theme.ICON_SIZE["sm"], color=Theme.PRIMARY),
                ft.Column([
                    ft.Text(
                        datetime.now().strftime("%H:%M"),
                        size=Theme.FONT_SIZE["md"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.PRIMARY
                    ),
                    ft.Text(
                        datetime.now().strftime("%d/%m/%Y"),
                        size=Theme.FONT_SIZE["xs"],
                        color=Theme.TEXT_SECONDARY
                    ),
                ], spacing=0),
            ], spacing=Theme.SPACING["sm"]),
        )
    )

    # Botón de logout
    header_controls.append(
        ft.Container(
            content=create_outlined_button(
                "Cerrar Sesión",
                on_logout,
                icon=ft.Icons.LOGOUT,
                color=Theme.PRIMARY
            ),
            margin=ft.margin.only(left=Theme.SPACING["lg"])
        )
    )

    return ft.Container(
        content=ft.Row(
            header_controls,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.padding.symmetric(horizontal=Theme.SPACING["2xl"], vertical=Theme.SPACING["lg"]),
        bgcolor=Theme.SIDEBAR_BG,
        border_radius=0,
        border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT)),
    )
