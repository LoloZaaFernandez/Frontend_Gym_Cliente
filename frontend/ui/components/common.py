"""
Componentes de UI comunes y reutilizables con estilos UX/UI profesionales
"""
#ui/components/common.py
import flet as ft
from config.settings import (
    PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG,
    TEXT_PRIMARY, BACKGROUND_DARK
)


def create_info_card(title: str, value: str, icon, color: str = PRIMARY_COLOR):
    """
    Crear tarjeta de información para dashboards

    Args:
        title: Título de la tarjeta
        value: Valor a mostrar
        icon: Ícono de Flet
        color: Color del ícono

    Returns:
        Container con tarjeta de información
    """
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icon, size=35, color=color),
                    bgcolor=f"{color}22",
                    border_radius=10,
                    padding=12,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=12,
                            color=TEXT_SECONDARY,
                            weight=ft.FontWeight.W_400
                        ),
                        ft.Text(
                            value,
                            size=24,
                            color=TEXT_PRIMARY,
                            weight=ft.FontWeight.BOLD
                        ),
                    ],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START
        ),
        bgcolor=CARD_BG,
        border_radius=12,
        padding=20,
        border=ft.border.all(1, "#333333"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2)
        ),
        width=280,
        height=100
    )


def create_data_table(columns: list, rows: list):
    """
    Crear tabla de datos estilizada

    Args:
        columns: Lista de nombres de columnas
        rows: Lista de filas (cada fila es una lista de valores)

    Returns:
        DataTable configurada
    """
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
            for col in columns
        ],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(cell), color=TEXT_PRIMARY)) for cell in row]
            )
            for row in rows
        ],
        border=ft.border.all(1, "#333333"),
        border_radius=8,
        bgcolor=CARD_BG,
        horizontal_lines=ft.border.BorderSide(1, "#333333"),
        heading_row_color=f"{PRIMARY_COLOR}22",
        heading_row_height=50,
        data_row_min_height=45
    )


def create_role_card(title: str, description: str, icon, color: str, on_click):
    """
    Crear tarjeta de selección de rol

    Args:
        title: Título de la tarjeta
        description: Descripción del rol
        icon: Ícono de Flet
        color: Color de acento
        on_click: Función a ejecutar al hacer clic

    Returns:
        Container con la tarjeta de rol
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=40, color=color),
                ft.Text(
                    title,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    description,
                    size=14,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    text="Acceder",
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLACK,
                        bgcolor=color,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    on_click=on_click
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=CARD_BG,
        border_radius=12,
        width=300,
        height=280,
        padding=30,
        border=ft.border.all(1, "#333333"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK45,
            offset=ft.Offset(0, 4)
        )
    )


def create_nav_button(text: str, icon, on_click, color: str = PRIMARY_COLOR):
    """
    Crear botón de navegación para el dashboard

    Args:
        text: Texto del botón
        icon: Ícono de Flet
        on_click: Función a ejecutar al hacer clic
        color: Color del ícono

    Returns:
        Container con el botón de navegación
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=30, color=color),
                ft.Text(text, size=12, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        ),
        width=120,
        height=100,
        padding=15,
        bgcolor=CARD_BG,
        border_radius=12,
        on_click=on_click,
        border=ft.border.all(1, "#333333"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2)
        )
    )


def create_header(title: str, subtitle: str, on_logout):
    """
    Crear header común para dashboards

    Args:
        title: Título principal
        subtitle: Subtítulo o nombre de usuario
        on_logout: Función para cerrar sesión

    Returns:
        Container con el header
    """
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column([
                    ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    ft.Text(subtitle, color=TEXT_SECONDARY),
                ]),
                ft.ElevatedButton(
                    "Cerrar Sesión",
                    icon=ft.Icons.LOGOUT,
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        bgcolor=ft.Colors.TRANSPARENT,
                        side=ft.border.all(1, PRIMARY_COLOR)
                    ),
                    on_click=on_logout
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )


def create_text_field(label: str, password: bool = False, width: int = 320):
    """
    Crear campo de texto estilizado

    Args:
        label: Etiqueta del campo
        password: Si es campo de contraseña
        width: Ancho del campo

    Returns:
        TextField configurado
    """
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,
        border_radius=8,
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        height=50,
        text_size=14,
        content_padding=15,
        width=width,
        bgcolor=CARD_BG,
        border_width=1,
        color=TEXT_PRIMARY,
        label_style=ft.TextStyle(color=TEXT_SECONDARY)
    )


def create_primary_button(text: str, on_click, width: int = 320):
    """
    Crear botón primario estilizado

    Args:
        text: Texto del botón
        on_click: Función a ejecutar al hacer clic
        width: Ancho del botón

    Returns:
        ElevatedButton configurado
    """
    return ft.ElevatedButton(
        text=text,
        width=width,
        height=45,
        bgcolor=PRIMARY_COLOR,
        color=ft.Colors.BLACK,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=on_click
    )


def create_modern_sidebar(
    role: str,
    current_section: str,
    on_section_click,
    logo_path: str = None,
    user_info: dict = None
):
    """
    Crear sidebar moderno y reutilizable para todas las vistas

    Args:
        role: Rol del usuario ('admin' o 'cliente')
        current_section: Sección actual activa
        on_section_click: Callback para cambiar de sección
        logo_path: Ruta del logo (opcional)
        user_info: Información del usuario (opcional)

    Returns:
        Container con el sidebar completo
    """
    # Colores modernos
    ACCENT_COLOR = PRIMARY_COLOR
    CARD_BORDER = "#333333"
    SIDEBAR_BG = "#1A1A1A"

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
    else:  # cliente
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
        """Crear item de navegación con diseño moderno mejorado"""
        # Colores más sutiles y profesionales
        item = ft.Container(
            content=ft.Row([
                ft.Icon(
                    icon,
                    size=22,
                    color=ACCENT_COLOR if is_active else TEXT_SECONDARY,
                ),
                ft.Text(
                    text,
                    size=14,
                    color=TEXT_PRIMARY if is_active else TEXT_SECONDARY,
                    weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_500,
                    expand=True,
                ),
            ], spacing=12),
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            border_radius=10,
            bgcolor=f"{ACCENT_COLOR}20" if is_active else "transparent",
            border=ft.border.only(
                left=ft.border.BorderSide(3, ACCENT_COLOR) if is_active else ft.border.BorderSide(3, "transparent")
            ),
            on_click=lambda e: on_section_click(section),
            animate=100,
        )

        def on_hover(e):
            if e.data == "true":
                if not is_active:
                    item.bgcolor = f"{ACCENT_COLOR}10"
                    item.border = ft.border.only(
                        left=ft.border.BorderSide(3, f"{ACCENT_COLOR}60")
                    )
                # Si está activo, mantener el estilo
            else:
                item.bgcolor = f"{ACCENT_COLOR}20" if is_active else "transparent"
                item.border = ft.border.only(
                    left=ft.border.BorderSide(3, ACCENT_COLOR) if is_active else ft.border.BorderSide(3, "transparent")
                )
            item.update()

        item.on_hover = on_hover
        return item

    # Logo section mejorada
    logo_content = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.FITNESS_CENTER,
                    size=35,
                    color=ACCENT_COLOR
                ),
                bgcolor=f"{ACCENT_COLOR}20",
                border_radius=15,
                padding=12,
                alignment=ft.alignment.center,
            ),
            ft.Text(
                "BLESSED GYM",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(
                content=ft.Text(
                    "Sistema de Gestión",
                    size=10,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER
                ),
                margin=ft.margin.only(top=-5)
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        padding=ft.padding.symmetric(vertical=20, horizontal=10),
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
            content=ft.Divider(height=1, color=CARD_BORDER),
            padding=ft.padding.symmetric(horizontal=5),
            margin=ft.margin.only(bottom=8, top=5)
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

    footer_controls.append(ft.Container(height=15))

    # Sidebar completo con diseño mejorado - ANCHO FIJO
    sidebar = ft.Container(
        content=ft.Column([
            logo_content,
            ft.Container(
                content=ft.Divider(height=1, color=CARD_BORDER),
                padding=ft.padding.symmetric(horizontal=15),
                margin=ft.margin.only(bottom=10)
            ),
            ft.Container(
                content=ft.Column(nav_controls, spacing=4),
                padding=ft.padding.symmetric(horizontal=10),
            ),
            ft.Container(height=10),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Column(footer_controls, spacing=4),
                padding=ft.padding.symmetric(horizontal=10),
            )
        ], spacing=0, scroll=ft.ScrollMode.AUTO),
        width=260,
        padding=0,
        bgcolor=SIDEBAR_BG,
        border=ft.border.only(right=ft.border.BorderSide(1, f"{CARD_BORDER}80")),
        expand=False,  # IMPORTANTE: Evita que se redimensione
    )

    return sidebar


def create_modern_header(
    title: str,
    subtitle: str,
    user_info: dict,
    on_logout,
    show_back_button: bool = False,
    on_back = None,
    logo_path: str = None
):
    """
    Crear header moderno y reutilizable

    Args:
        title: Título principal
        subtitle: Subtítulo o descripción
        user_info: Información del usuario
        on_logout: Callback para cerrar sesión
        show_back_button: Mostrar botón de volver
        on_back: Callback para volver
        logo_path: Ruta del logo del gimnasio

    Returns:
        Container con el header
    """
    from datetime import datetime

    ACCENT_COLOR = PRIMARY_COLOR
    CARD_BORDER = "#333333"
    SIDEBAR_BG = "#1A1A1A"

    header_controls = []

    # Logo del gimnasio en la parte superior izquierda
    if logo_path:
        header_controls.append(
            ft.Container(
                content=ft.Image(
                    src=logo_path,
                    width=45,
                    height=45,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Container(
                        content=ft.Icon(
                            ft.Icons.FITNESS_CENTER,
                            size=24,
                            color=ACCENT_COLOR
                        ),
                        bgcolor=f"{ACCENT_COLOR}20",
                        border_radius=10,
                        padding=10,
                        width=45,
                        height=45,
                        alignment=ft.alignment.center,
                    ),
                ),
                border_radius=10,
                bgcolor=f"{ACCENT_COLOR}15",
                padding=5,
                margin=ft.margin.only(right=15)
            )
        )

    # Botón de volver (opcional)
    if show_back_button and on_back:
        header_controls.append(
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=ACCENT_COLOR,
                icon_size=24,
                on_click=on_back,
                tooltip="Volver"
            )
        )

    # Información del usuario
    header_controls.append(
        ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.PERSON, size=20, color=ACCENT_COLOR),
                bgcolor=f"{ACCENT_COLOR}20",
                border_radius=10,
                padding=10,
                width=42,
                height=42,
            ),
            ft.Column([
                ft.Text(
                    f"Bienvenido, {user_info.get('nombre', 'Usuario')}",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_PRIMARY
                ),
                ft.Text(
                    user_info.get('rol', 'Usuario'),
                    size=11,
                    color=TEXT_SECONDARY
                ),
            ], spacing=1),
        ], spacing=12)
    )

    header_controls.append(ft.Container(expand=True))

    # Título de sección
    header_controls.append(
        ft.Container(
            content=ft.Column([
                ft.Text(
                    title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY
                ),
                ft.Text(
                    subtitle,
                    size=11,
                    color=TEXT_SECONDARY
                ) if subtitle else ft.Container(),
            ], spacing=2),
            padding=ft.padding.symmetric(horizontal=15),
        )
    )

    # Información de fecha y hora
    header_controls.append(
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ACCESS_TIME, size=16, color=ACCENT_COLOR),
                ft.Column([
                    ft.Text(
                        datetime.now().strftime("%H:%M"),
                        size=14,
                        weight=ft.FontWeight.W_700,
                        color=ACCENT_COLOR
                    ),
                    ft.Text(
                        datetime.now().strftime("%d/%m/%Y"),
                        size=10,
                        color=TEXT_SECONDARY
                    ),
                ], spacing=0),
            ], spacing=8),
        )
    )

    # Botón de logout
    header_controls.append(
        ft.Container(
            content=ft.ElevatedButton(
                "Cerrar Sesión",
                icon=ft.Icons.LOGOUT,
                style=ft.ButtonStyle(
                    color=ACCENT_COLOR,
                    bgcolor=ft.Colors.TRANSPARENT,
                    side=ft.border.all(1, ACCENT_COLOR),
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                ),
                on_click=on_logout,
            ),
            margin=ft.margin.only(left=15)
        )
    )

    return ft.Container(
        content=ft.Row(
            header_controls,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.padding.symmetric(horizontal=25, vertical=15),
        bgcolor=SIDEBAR_BG,
        border_radius=0,
        border=ft.border.only(bottom=ft.border.BorderSide(1, CARD_BORDER)),
    )
