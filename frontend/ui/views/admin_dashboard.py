"""
Vista de dashboard para administradores - Diseño Moderno con Menú Lateral Persistente Mejorado
"""

import flet as ft
from config.settings import (
    PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, 
    BACKGROUND_DARK, SECONDARY_COLOR, LOGO_PATH
)
from datetime import datetime

def show_admin_dashboard(page: ft.Page, auth_service, on_logout, on_section_click):
    """
    Mostrar dashboard del administrador con diseño moderno y menú lateral persistente mejorado
    """
    # Limpiar página
    page.clean()
    
    page.title = "BLESSED GYM - Dashboard Administrador"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    current_user = auth_service.get_current_user()

    # Estado para controlar la vista actual
    current_section = ft.Text("Dashboard", size=16, weight=ft.FontWeight.BOLD)

    # PALETA DE COLORES MODERNA
    ACCENT_COLOR = PRIMARY_COLOR  # #F05D23 - Naranja principal
    SUCCESS_COLOR = "#00C853"     # Verde moderno
    WARNING_COLOR = "#FF9100"     # Naranja suave
    INFO_COLOR = "#2979FF"        # Azul moderno
    DANGER_COLOR = "#FF5252"      # Rojo moderno
    
    # Colores de fondo modernos
    DARK_BG = "#121212"          # Fondo principal
    CARD_BG_DARK = "#1E1E1E"     # Fondo de tarjetas
    CARD_BORDER = "#333333"       # Borde de tarjetas
    SIDEBAR_BG = "#1A1A1A"       # Fondo del menú lateral
    SIDEBAR_ACCENT = "#252525"    # Accento del menú
    
    # Función para cambiar sección
    def change_section(section_name, section_title):
        current_section.value = section_title
        current_section.update()
        on_section_click(section_name)

    # HEADER MODERNO
    header = ft.Container(
        content=ft.Row([
            # Información del usuario
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
                    ft.Text(f"Bienvenido, {current_user['nombre']}", size=14, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                    ft.Text("Administrador", size=11, color=TEXT_SECONDARY),
                ], spacing=1),
            ], spacing=12),
            
            ft.Container(expand=True),
            
            # Sección actual
            ft.Container(
                content=current_section,
                padding=ft.padding.symmetric(horizontal=15),
            ),
            
            # Información de fecha y hora
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, size=16, color=ACCENT_COLOR),
                    ft.Column([
                        ft.Text(datetime.now().strftime("%H:%M"), 
                               size=14, weight=ft.FontWeight.W_700, color=ACCENT_COLOR),
                        ft.Text(datetime.now().strftime("%d/%m/%Y"), 
                               size=10, color=TEXT_SECONDARY),
                    ], spacing=0),
                ], spacing=8),
            ),
            
            # Botón de logout moderno
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
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=25, vertical=15),
        bgcolor=SIDEBAR_BG,
        border_radius=0,
        border=ft.border.only(bottom=ft.border.BorderSide(1, CARD_BORDER)),
    )

    # MENÚ LATERAL MODERNO MEJORADO
    def create_nav_item(text, icon, section_name, section_title, is_active=False):
        """Crear item de navegación con diseño moderno mejorado"""
        item = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=20, color=ACCENT_COLOR if is_active else TEXT_SECONDARY),
                    width=40,
                    height=40,
                    alignment=ft.alignment.center,
                    border_radius=10,
                    bgcolor=ACCENT_COLOR if is_active else "transparent",
                ),
                ft.Text(
                    text,
                    size=14,
                    color=TEXT_PRIMARY if is_active else TEXT_SECONDARY,
                    weight=ft.FontWeight.W_600,
                    expand=True,
                ),
            ], spacing=12),
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            border_radius=10,
            bgcolor=f"{ACCENT_COLOR}15" if is_active else "transparent",
            border=ft.border.all(1, ACCENT_COLOR if is_active else "transparent"),
            on_click=lambda e: change_section(section_name, section_title),
        )

        def on_hover(e):
            if e.data == "true" and not is_active:
                item.bgcolor = f"{ACCENT_COLOR}10"
                item.border = ft.border.all(1, f"{ACCENT_COLOR}40")
            else:
                item.bgcolor = f"{ACCENT_COLOR}15" if is_active else "transparent"
                item.border = ft.border.all(1, ACCENT_COLOR if is_active else "transparent")
            item.update()

        item.on_hover = on_hover
        return item

    # Menú lateral moderno mejorado
    nav_menu = ft.Container(
        content=ft.Column([
            # Logo solo - sin texto
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Image(
                            src=LOGO_PATH,
                            width=60,
                            height=60,
                            fit=ft.ImageFit.CONTAIN,
                            error_content=ft.Container(
                                content=ft.Icon(
                                    ft.Icons.FITNESS_CENTER, 
                                    size=28, 
                                    color=ACCENT_COLOR
                                ),
                                width=60,
                                height=60,
                                alignment=ft.alignment.center,
                            ),
                        ),
                        alignment=ft.alignment.center,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.symmetric(vertical=25, horizontal=10),
            ),
            
            # Separador sutil
            ft.Container(
                content=ft.Divider(height=1, color=CARD_BORDER),
                padding=ft.padding.symmetric(horizontal=15),
            ),
            ft.Container(height=20),
            
            # Navegación principal
            create_nav_item("Dashboard", ft.Icons.DASHBOARD, "Dashboard", "Dashboard", is_active=True),
            create_nav_item("Clientes", ft.Icons.PEOPLE, "Clientes", "Gestión de Clientes"),
            create_nav_item("Membresías", ft.Icons.CARD_MEMBERSHIP, "Membresias", "Gestión de Membresías"),
            create_nav_item("Asistencia", ft.Icons.DIRECTIONS_RUN, "Asistencia", "Control de Asistencia"),
            
            ft.Container(height=10),
            
            create_nav_item("Punto de Venta", ft.Icons.SHOPPING_CART, "POS", "Punto de Venta"),
            create_nav_item("Productos", ft.Icons.INVENTORY_2, "Productos", "Inventario de Productos"),
            
            ft.Container(height=10),
            
            create_nav_item("Reportes", ft.Icons.ANALYTICS, "Reportes", "Reportes y Estadísticas"),
            create_nav_item("Finanzas", ft.Icons.ATTACH_MONEY, "Finanzas", "Gestión Financiera"),
            
            ft.Container(expand=True),
            
            # Footer del menú
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Divider(height=1, color=CARD_BORDER),
                        padding=ft.padding.symmetric(horizontal=15),
                    ),
                    ft.Container(height=15),
                    create_nav_item("Configuración", ft.Icons.SETTINGS, "Configuracion", "Configuración del Sistema"),
                    create_nav_item("Ayuda", ft.Icons.HELP, "Soporte", "Centro de Ayuda"),
                    ft.Container(height=10),
                ], spacing=0),
            )
        ], spacing=0),
        width=250,
        padding=0,
        bgcolor=SIDEBAR_BG,
        border=ft.border.only(right=ft.border.BorderSide(1, CARD_BORDER)),
    )

    # TARJETAS DE ESTADÍSTICAS MODERNAS
    def create_stat_card(title, value, icon, color, subtitle="", trend=None):
        """Crear tarjeta de estadística con diseño moderno"""
        trend_indicator = None
        if trend:
            trend_icon = ft.Icons.TRENDING_UP if trend > 0 else ft.Icons.TRENDING_DOWN
            trend_color = SUCCESS_COLOR if trend > 0 else DANGER_COLOR
            trend_text = f"+{trend}%" if trend > 0 else f"{trend}%"
            
            trend_indicator = ft.Container(
                content=ft.Row([
                    ft.Icon(trend_icon, size=14, color=trend_color),
                    ft.Text(trend_text, size=11, color=trend_color, weight=ft.FontWeight.BOLD),
                ], spacing=3),
                bgcolor=f"{trend_color}15",
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=6
            )

        card = ft.Container(
            content=ft.Column([
                ft.Row([
                    # Icono moderno
                    ft.Container(
                        content=ft.Icon(icon, size=22, color=ft.Colors.WHITE),
                        bgcolor=color,
                        border_radius=12,
                        padding=12,
                        width=48,
                        height=48,
                    ),
                    ft.Container(expand=True),
                    trend_indicator if trend_indicator else ft.Container()
                ]),
                ft.Container(height=15),
                ft.Text(value, size=26, weight=ft.FontWeight.W_800, color=TEXT_PRIMARY),
                ft.Text(title, size=14, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                ft.Text(subtitle, size=12, color=color, weight=ft.FontWeight.W_600) if subtitle else ft.Container(),
            ], spacing=0),
            padding=22,
            height=150,
            border_radius=14,
            bgcolor=CARD_BG_DARK,
            border=ft.border.all(1, CARD_BORDER),
        )

        def on_hover(e):
            if e.data == "true":
                card.border = ft.border.all(1, color)
                card.scale = ft.Scale(1.02)
            else:
                card.border = ft.border.all(1, CARD_BORDER)
                card.scale = ft.Scale(1.0)
            card.update()

        card.on_hover = on_hover
        return card

    # GRID DE ESTADÍSTICAS MODERNO
    stats_grid = ft.ResponsiveRow([
        ft.Container(create_stat_card("Total Clientes", "150", ft.Icons.PEOPLE, ACCENT_COLOR, "+3 este mes", 2.0), 
                    col={"sm": 12, "md": 6, "lg": 3}, padding=6),
        ft.Container(create_stat_card("Clientes Activos", "142", ft.Icons.PERSON_ADD, SUCCESS_COLOR, "94.7% activos", 1.5), 
                    col={"sm": 12, "md": 6, "lg": 3}, padding=6),
        ft.Container(create_stat_card("Asistencias Hoy", "45", ft.Icons.FITNESS_CENTER, INFO_COLOR, "Promedio: 52/día", -5.0), 
                    col={"sm": 12, "md": 6, "lg": 3}, padding=6),
        ft.Container(create_stat_card("Ingresos Hoy", "S/. 850", ft.Icons.ATTACH_MONEY, WARNING_COLOR, "+15% vs ayer", 15.0), 
                    col={"sm": 12, "md": 6, "lg": 3}, padding=6),
    ], spacing=6)

    # SECCIÓN DE ACTIVIDAD RECIENTE MODERNA
    actividades = [
        {"texto": "Nuevo cliente: Juan Pérez", "icono": ft.Icons.PERSON_ADD, "hora": "10:30", "color": SUCCESS_COLOR},
        {"texto": "Venta: Membresía Premium - S/. 200.00", "icono": ft.Icons.POINT_OF_SALE, "hora": "11:15", "color": ACCENT_COLOR},
        {"texto": "Asistencia: María García", "icono": ft.Icons.FITNESS_CENTER, "hora": "12:00", "color": INFO_COLOR},
        {"texto": "Membresía renovada: Carlos López", "icono": ft.Icons.AUTORENEW, "hora": "13:45", "color": WARNING_COLOR},
        {"texto": "Producto: Proteína Whey - S/. 85.00", "icono": ft.Icons.SHOPPING_BAG, "hora": "14:20", "color": SUCCESS_COLOR},
    ]

    def create_activity_item(actividad):
        item = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(actividad['icono'], size=18, color=ft.Colors.WHITE),
                    bgcolor=actividad['color'],
                    border_radius=8,
                    padding=8,
                    width=36,
                    height=36,
                ),
                ft.Column([
                    ft.Text(actividad['texto'], size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                    ft.Text(actividad['hora'], size=11, color=TEXT_SECONDARY),
                ], spacing=1, expand=True),
            ], spacing=12),
            padding=14,
            bgcolor=CARD_BG_DARK,
            border_radius=10,
            border=ft.border.all(1, CARD_BORDER),
        )

        def on_hover(e):
            if e.data == "true":
                item.border = ft.border.all(1, ACCENT_COLOR)
                item.bgcolor = f"{ACCENT_COLOR}08"
            else:
                item.border = ft.border.all(1, CARD_BORDER)
                item.bgcolor = CARD_BG_DARK
            item.update()

        item.on_hover = on_hover
        return item

    # BOTÓN MODERNO
    def create_action_button(text, icon, section_name, section_title):
        return ft.ElevatedButton(
            text,
            icon=icon,
            style=ft.ButtonStyle(
                color=ACCENT_COLOR,
                bgcolor=ft.Colors.TRANSPARENT,
                side=ft.border.all(1, ACCENT_COLOR),
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
            ),
            height=44,
            on_click=lambda _: change_section(section_name, section_title)
        )

    # CONTENIDO PRINCIPAL MODERNO
    main_content = ft.Container(
        content=ft.Column([
            # Título de bienvenida
            ft.Container(
                content=ft.Column([
                    ft.Text("Panel de Control", 
                           size=26, weight=ft.FontWeight.W_800, color=TEXT_PRIMARY),
                    ft.Text("Resumen general del sistema", 
                           size=14, color=TEXT_SECONDARY),
                ], spacing=4),
                padding=ft.padding.only(bottom=25)
            ),

            # Estadísticas principales
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INSERT_CHART, size=22, color=ACCENT_COLOR),
                            ft.Text("Métricas Principales", size=16, weight=ft.FontWeight.W_700, color=ACCENT_COLOR),
                        ], spacing=10),
                        padding=ft.padding.only(bottom=20)
                    ),
                    stats_grid,
                ]),
                padding=25,
                bgcolor=CARD_BG_DARK,
                border_radius=12,
                margin=ft.margin.only(bottom=20),
                border=ft.border.all(1, CARD_BORDER),
            ),

            # Grid inferior
            ft.ResponsiveRow([
                # Actividad reciente
                ft.Container(
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.HISTORY, size=20, color=ACCENT_COLOR),
                                    ft.Text("Actividad Reciente", size=16, weight=ft.FontWeight.W_700, color=ACCENT_COLOR),
                                ], spacing=10),
                                padding=ft.padding.only(bottom=20)
                            ),
                            ft.Column([create_activity_item(act) for act in actividades], spacing=8),
                        ]),
                        padding=25,
                        bgcolor=CARD_BG_DARK,
                        border_radius=12,
                        border=ft.border.all(1, CARD_BORDER),
                    ),
                    col={"sm": 12, "md": 8},
                    padding=5
                ),

                # Acciones rápidas
                ft.Container(
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.FLASH_ON, size=20, color=ACCENT_COLOR),
                                    ft.Text("Acciones Rápidas", size=16, weight=ft.FontWeight.W_700, color=ACCENT_COLOR),
                                ], spacing=10),
                                padding=ft.padding.only(bottom=20)
                            ),
                            create_action_button("Generar Reporte", ft.Icons.ANALYTICS, "Reportes", "Reportes y Estadísticas"),
                            ft.Container(height=10),
                            create_action_button("Registrar Cliente", ft.Icons.PERSON_ADD, "Clientes", "Gestión de Clientes"),
                            ft.Container(height=10),
                            create_action_button("Nueva Venta", ft.Icons.SHOPPING_CART, "POS", "Punto de Venta"),
                            ft.Container(height=10),
                            create_action_button("Registrar Asistencia", ft.Icons.DIRECTIONS_RUN, "Asistencia", "Control de Asistencia"),
                        ]),
                        padding=25,
                        bgcolor=CARD_BG_DARK,
                        border_radius=12,
                        border=ft.border.all(1, CARD_BORDER),
                    ),
                    col={"sm": 12, "md": 4},
                    padding=5
                ),
            ], spacing=0),
        ], scroll=ft.ScrollMode.ADAPTIVE),
        expand=True,
        padding=25
    )

    # LAYOUT PRINCIPAL CON MENÚ PERSISTENTE MEJORADO
    main_layout = ft.Row([
        # Menú lateral persistente
        nav_menu,
        
        # Contenido principal
        ft.Container(
            content=ft.Column([
                header,
                main_content,
            ], spacing=0, expand=True),
            expand=True,
            bgcolor=DARK_BG,
        ),
    ], spacing=0, expand=True)

    # CONTENEDOR PRINCIPAL
    page.add(
        ft.Container(
            content=main_layout,
            bgcolor=DARK_BG,
            expand=True,
        )
    )
    
    page.update()