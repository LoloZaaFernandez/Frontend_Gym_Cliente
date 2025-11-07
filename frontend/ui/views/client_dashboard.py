"""
Vista de dashboard para clientes con diseño mejorado y atractivo
"""

import flet as ft
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK

def show_client_dashboard(page: ft.Page, auth_service, on_logout, on_section_click):
    """
    Mostrar dashboard del cliente con diseño mejorado y visualmente atractivo
    """
    page.clean()
    page.title = "BLESSED GYM - Dashboard Cliente"

    client_data = auth_service.get_current_user()

    # Datos simulados (integrar con DB real)
    stats_cliente = {
        "asistencias_mes": 18,
        "racha_dias": 5,
        "dias_restantes_membresia": 25,
        "ultima_asistencia": "05/11/2025",
        "meta_mensual": 20,
        "progreso_meta": 75  # 18/20 = 90%
    }

    # Header mejorado con gradiente
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row([
                    # Avatar del cliente con efecto de gradiente
                    ft.Container(
                        content=ft.Stack([
                            ft.Container(
                                content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=ft.Colors.WHITE),
                                bgcolor=PRIMARY_COLOR,
                                border_radius=30,
                                padding=8
                            ),
                            ft.Container(
                                content=ft.Container(
                                    bgcolor=f"{PRIMARY_COLOR}44",
                                    border_radius=30,
                                    width=66,
                                    height=66
                                ),
                                border=ft.border.all(2, f"{PRIMARY_COLOR}88"),
                                border_radius=30
                            )
                        ]),
                        margin=ft.margin.only(right=15)
                    ),
                    ft.Column([
                        ft.Text("BLESSED GYM", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                        ft.Text(
                            f"{client_data['nombre']} {client_data['apellidos']}",
                            color=TEXT_PRIMARY, 
                            size=18, 
                            weight=ft.FontWeight.W_700
                        ),
                        ft.Text(f"DNI: {client_data['dni']}", color=TEXT_SECONDARY, size=12),
                    ], spacing=2),
                ], spacing=0),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Cerrar Sesión",
                        icon=ft.Icons.LOGOUT,
                        style=ft.ButtonStyle(
                            color=PRIMARY_COLOR,
                            bgcolor=ft.Colors.TRANSPARENT,
                            side=ft.border.all(1, PRIMARY_COLOR),
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        on_click=on_logout,
                        height=42
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.padding.symmetric(horizontal=25, vertical=20),
        bgcolor=CARD_BG,
        border_radius=16,
        margin=15,
        border=ft.border.all(1, f"{PRIMARY_COLOR}30"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4)
        )
    )

    def create_nav_card(text, icon, description, on_click):
        """Crear tarjeta de navegación con diseño moderno"""
        card = ft.Container(
            content=ft.Column([
                # Icono con gradiente
                ft.Container(
                    content=ft.Icon(icon, size=28, color=ft.Colors.WHITE),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[PRIMARY_COLOR, f"{PRIMARY_COLOR}DD"]
                    ),
                    border_radius=14,
                    padding=16,
                    width=60,
                    height=60,
                    alignment=ft.alignment.center,
                    animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT)
                ),
                ft.Container(height=12),
                # Texto principal
                ft.Text(
                    text,
                    size=15,
                    weight=ft.FontWeight.W_700,
                    color=TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=4),
                # Descripción
                ft.Text(
                    description,
                    size=11,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
            ),
            padding=20,
            bgcolor=CARD_BG,
            border_radius=16,
            border=ft.border.all(1, f"{PRIMARY_COLOR}20"),
            width=140,
            height=160,
            alignment=ft.alignment.center,
            animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
        )

        def on_hover(e):
            if e.data == "true":
                card.bgcolor = f"{PRIMARY_COLOR}08"
                card.border = ft.border.all(2, PRIMARY_COLOR)
                card.elevation = 8
                card.shadow = ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=25,
                    color=f"{PRIMARY_COLOR}44",
                    offset=ft.Offset(0, 8)
                )
                card.content.controls[0].scale = ft.Scale(1.1)
            else:
                card.bgcolor = CARD_BG
                card.border = ft.border.all(1, f"{PRIMARY_COLOR}20")
                card.elevation = 0
                card.shadow = None
                card.content.controls[0].scale = ft.Scale(1.0)
            card.update()

        card.on_hover = on_hover
        card.on_click = on_click
        return card

    # NAVEGACIÓN RÁPIDA MEJORADA
    nav_container = ft.Container(
        content=ft.Column([
            # Título con icono
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ROCKET_LAUNCH, size=24, color=PRIMARY_COLOR),
                    ft.Text(
                        "NAVEGACIÓN RÁPIDA",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_COLOR
                    ),
                ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=25)
            ),
            
            # Grid de navegación
            ft.ResponsiveRow([
                ft.Container(
                    create_nav_card(
                        "Dashboard", 
                        ft.Icons.DASHBOARD,
                        "Resumen general",
                        lambda _: show_client_dashboard(page, auth_service, on_logout, on_section_click)
                    ),
                    col={"sm": 6, "md": 3}
                ),
                ft.Container(
                    create_nav_card(
                        "Mi Perfil", 
                        ft.Icons.PERSON,
                        "Información personal",
                        lambda _: on_section_click("Mi Perfil")
                    ),
                    col={"sm": 6, "md": 3}
                ),
                ft.Container(
                    create_nav_card(
                        "Membresías", 
                        ft.Icons.CARD_MEMBERSHIP,
                        "Gestionar membresía",
                        lambda _: on_section_click("Membresías")
                    ),
                    col={"sm": 6, "md": 3}
                ),
                ft.Container(
                    create_nav_card(
                        "Asistencias", 
                        ft.Icons.DIRECTIONS_RUN,
                        "Historial de visitas",
                        lambda _: on_section_click("Asistencias")
                    ),
                    col={"sm": 6, "md": 3}
                ),
            ], 
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0
        ),
        padding=30,
        bgcolor=CARD_BG,
        border_radius=20,
        margin=15,
        border=ft.border.all(2, f"{PRIMARY_COLOR}40"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=25,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 6)
        )
    )

    # MI PROGRESO - DISEÑO MEJORADO
    def create_progress_card(title, value, subtitle, icon, color, progress=None):
        """Crear tarjeta de progreso con diseño moderno"""
        
        # Contenido principal
        content = [
            # Header con icono
            ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=20, color=color),
                    bgcolor=f"{color}20",
                    border_radius=10,
                    padding=8
                ),
                ft.Text(title, size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
            ], spacing=10),
            
            # Valor principal
            ft.Text(
                value,
                size=32,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
            ),
            
            # Subtítulo
            ft.Text(
                subtitle,
                size=12,
                color=TEXT_SECONDARY,
            ),
        ]
        
        # Agregar barra de progreso si se proporciona
        if progress is not None:
            content.append(
                ft.Container(
                    content=ft.Stack([
                        # Fondo de la barra
                        ft.Container(
                            bgcolor=f"{color}20",
                            border_radius=10,
                            height=6,
                            expand=True
                        ),
                        # Barra de progreso
                        ft.Container(
                            bgcolor=color,
                            border_radius=10,
                            height=6,
                            width=progress,
                            animate=ft.Animation(1000, ft.AnimationCurve.EASE_OUT)
                        ),
                    ]),
                    height=6,
                    margin=ft.margin.only(top=8)
                )
            )
            # Porcentaje
            content.append(
                ft.Text(
                    f"{int(progress)}%",
                    size=10,
                    color=color,
                    weight=ft.FontWeight.BOLD
                )
            )

        card = ft.Container(
            content=ft.Column(
                controls=content,
                spacing=8
            ),
            padding=20,
            bgcolor=CARD_BG,
            border_radius=16,
            border=ft.border.all(1, f"{color}30"),
            expand=True,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

        def on_hover(e):
            if e.data == "true":
                card.bgcolor = f"{color}08"
                card.border = ft.border.all(2, color)
                card.scale = ft.Scale(1.02)
            else:
                card.bgcolor = CARD_BG
                card.border = ft.border.all(1, f"{color}30")
                card.scale = ft.Scale(1.0)
            card.update()

        card.on_hover = on_hover
        return card

    # Sección MI PROGRESO mejorada
    progreso_container = ft.Container(
        content=ft.Column([
            # Header de sección
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.TRENDING_UP, size=24, color=PRIMARY_COLOR),
                    ft.Text(
                        "MI PROGRESO",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_COLOR
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        "Este mes",
                        size=12,
                        color=TEXT_SECONDARY,
                        weight=ft.FontWeight.W_500
                    )
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=20)
            ),
            
            # Grid de progreso
            ft.ResponsiveRow([
                ft.Container(
                    create_progress_card(
                        "Asistencias del Mes",
                        str(stats_cliente["asistencias_mes"]),
                        f"Meta: {stats_cliente['meta_mensual']} sesiones",
                        ft.Icons.FITNESS_CENTER,
                        PRIMARY_COLOR,
                        stats_cliente["progreso_meta"]
                    ),
                    col={"sm": 12, "md": 4}
                ),
                ft.Container(
                    create_progress_card(
                        "Racha Actual", 
                        f"{stats_cliente['racha_dias']} días",
                        "Días consecutivos",
                        ft.Icons.LOCAL_FIRE_DEPARTMENT,
                        "#FF6B35",
                        min(stats_cliente["racha_dias"] * 20, 100)  # Progreso simulado
                    ),
                    col={"sm": 12, "md": 4}
                ),
                ft.Container(
                    create_progress_card(
                        "Días Restantes",
                        str(stats_cliente["dias_restantes_membresia"]),
                        "Hasta renovación",
                        ft.Icons.CALENDAR_MONTH,
                        "#4CAF50"
                    ),
                    col={"sm": 12, "md": 4}
                ),
            ], 
            spacing=15,
            ),
        ], 
        spacing=0
        ),
        padding=25,
        bgcolor=CARD_BG,
        border_radius=20,
        margin=15,
        border=ft.border.all(1, f"{PRIMARY_COLOR}30"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 4)
        )
    )

    # INFORMACIÓN RÁPIDA - Tarjetas laterales mejoradas
    def crear_info_rapida():
        """Crear sección de información rápida"""
        
        # Tarjeta de membresía
        membresia_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=22, color=PRIMARY_COLOR),
                    ft.Text("MI MEMBRESÍA", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ], spacing=10),
                ft.Divider(height=1, color=f"{PRIMARY_COLOR}30"),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Membresía Mensual", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(height=8),
                        ft.Text("Vence: 30/11/2025", size=13, color=TEXT_SECONDARY),
                        ft.Container(height=12),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=ft.Colors.WHITE),
                                ft.Text("ACTIVA", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            bgcolor="#4CAF50",
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            border_radius=20,
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    alignment=ft.alignment.center
                ),
            ], spacing=0),
            padding=20,
            bgcolor=CARD_BG,
            border_radius=16,
            border=ft.border.all(1, f"{PRIMARY_COLOR}30"),
            expand=True
        )

        # Tarjeta de información personal
        def crear_info_item(icon, label, value, action_icon=None, on_action=None):
            item = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=18, color=PRIMARY_COLOR),
                        bgcolor=f"{PRIMARY_COLOR}15",
                        border_radius=8,
                        padding=8
                    ),
                    ft.Column([
                        ft.Text(label, size=11, color=TEXT_SECONDARY),
                        ft.Text(value, size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                    ], spacing=2, expand=True),
                    ft.IconButton(
                        icon=action_icon,
                        icon_size=16,
                        icon_color=PRIMARY_COLOR,
                        on_click=on_action,
                        visible=action_icon is not None
                    ) if action_icon else ft.Container()
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=12,
                bgcolor=CARD_BG,
                border_radius=12,
                border=ft.border.all(1, f"{PRIMARY_COLOR}20"),
            )

            def on_hover(e):
                if e.data == "true":
                    item.bgcolor = f"{PRIMARY_COLOR}08"
                    item.border = ft.border.all(1, PRIMARY_COLOR)
                else:
                    item.bgcolor = CARD_BG
                    item.border = ft.border.all(1, f"{PRIMARY_COLOR}20")
                item.update()

            item.on_hover = on_hover
            return item

        info_personal_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PERSON, size=22, color=PRIMARY_COLOR),
                    ft.Text("INFORMACIÓN PERSONAL", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ], spacing=10),
                ft.Divider(height=1, color=f"{PRIMARY_COLOR}30"),
                ft.Container(height=15),
                crear_info_item(ft.Icons.EMAIL, "Correo", client_data['correo'], ft.Icons.CONTENT_COPY, lambda _: page.set_clipboard(client_data['correo'])),
                ft.Container(height=10),
                crear_info_item(ft.Icons.PHONE, "Teléfono", client_data.get('telefono') or "No registrado"),
                ft.Container(height=10),
                crear_info_item(ft.Icons.ACCESS_TIME, "Última Asistencia", stats_cliente['ultima_asistencia']),
            ], spacing=0),
            padding=20,
            bgcolor=CARD_BG,
            border_radius=16,
            border=ft.border.all(1, f"{PRIMARY_COLOR}30"),
            expand=True
        )

        return ft.ResponsiveRow([
            ft.Container(membresia_card, col={"sm": 12, "md": 6}, padding=5),
            ft.Container(info_personal_card, col={"sm": 12, "md": 6}, padding=5),
        ], spacing=10)

    # Layout principal mejorado
    content = ft.Column([
        header,
        nav_container,
        progreso_container,
        ft.Container(
            content=crear_info_rapida(),
            margin=15
        ),
    ], 
    spacing=0, 
    scroll=ft.ScrollMode.ADAPTIVE, 
    expand=True
    )

    # Contenedor principal con fondo
    main_container = ft.Container(
        content=content,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BACKGROUND_DARK, f"{BACKGROUND_DARK}FF"]
        ),
        expand=True,
        padding=10
    )

    page.add(main_container)
    page.update()