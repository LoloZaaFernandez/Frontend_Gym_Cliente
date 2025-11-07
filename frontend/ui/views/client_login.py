"""
Vista de login para clientes - Diseño con Formulario Flotante Responsive
"""

import flet as ft
from config.settings import (
    LOGO_PATH, PRIMARY_COLOR, TEXT_SECONDARY, BACKGROUND_DARK, 
    CARD_BG, TEXT_PRIMARY, SECONDARY_COLOR, BG_PATH_CLIENT
)
from ui.components.common import create_text_field


def show_client_login(page: ft.Page, auth_service, on_success, on_back):
    """
    Mostrar pantalla de login para clientes - Diseño con Formulario Flotante Responsive

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_success: Callback para login exitoso
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Login Cliente"
    
    # Variables para animaciones
    is_loading = False

    def validate_dni(e):
        # Solo permitir números y máximo 8 caracteres
        if e.control.value:
            # Remover caracteres no numéricos
            cleaned_value = ''.join(filter(str.isdigit, e.control.value))
            # Limitar a 8 caracteres
            if len(cleaned_value) > 8:
                cleaned_value = cleaned_value[:8]
            # Actualizar el valor si cambió
            if cleaned_value != e.control.value:
                e.control.value = cleaned_value
                e.control.update()

    # Campo DNI mejorado con validación - RESPONSIVE
    dni_field = ft.TextField(
        label="Ingrese su DNI (8 dígitos)",
        border_radius=12,
        border_color="transparent",
        focused_border_color=PRIMARY_COLOR,
        height=56,
        text_size=16,
        content_padding=ft.padding.only(left=20, top=16, right=20, bottom=16),
        bgcolor="#2A2A2A",
        border_width=2,
        color=TEXT_PRIMARY,
        label_style=ft.TextStyle(
            color=TEXT_SECONDARY,
            size=14
        ),
        cursor_color=PRIMARY_COLOR,
        selection_color=PRIMARY_COLOR + "40",
        prefix_icon=ft.Icon(ft.Icons.BADGE_OUTLINED, color=TEXT_SECONDARY),
        filled=True,
        fill_color="#2A2A2A",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=8,
        on_change=validate_dni,
        input_filter=ft.NumbersOnlyInputFilter(),
        expand=True,  # Hacerlo responsive
    )

    # Botón de login con estado de carga - RESPONSIVE
    login_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.FINGERPRINT, color=BACKGROUND_DARK, size=20),
            ft.Text(
                "Ingresar con DNI",
                size=16,
                weight=ft.FontWeight.W_700,
                color=BACKGROUND_DARK
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        height=56,
        border_radius=12,
        bgcolor=PRIMARY_COLOR,
        alignment=ft.alignment.center,
        animate=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),
        expand=True,  # Hacerlo responsive
    )

    # Contenedor de carga - RESPONSIVE
    loading_indicator = ft.Container(
        content=ft.ProgressRing(
            width=24,
            height=24,
            stroke_width=2,
            color=BACKGROUND_DARK
        ),
        height=56,
        border_radius=12,
        bgcolor=PRIMARY_COLOR,
        alignment=ft.alignment.center,
        visible=False,
        expand=True,  # Hacerlo responsive
    )

    def animate_button_hover(e):
        if not is_loading:
            if e.data == "true":
                # Efecto de hover sin transform
                login_button.bgcolor = "#F57247"  # Color más claro
                login_button.elevation = 4
            else:
                login_button.bgcolor = PRIMARY_COLOR
                login_button.elevation = 2
            login_button.update()

    def handle_client_login(e):
        nonlocal is_loading
        
        if not dni_field.value or len(dni_field.value) != 8:
            # Animación de shake para campo vacío o incompleto
            dni_field.border_color = "#FF4444"
            dni_field.update()
            page.update()
            
            # Snackbar de error
            page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.WARNING_AMBER, color=SECONDARY_COLOR),
                    ft.Text(" El DNI debe tener 8 dígitos", color=SECONDARY_COLOR),
                ]),
                bgcolor="#D32F2F",
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
                margin=20,
                elevation=8
            )
            page.snack_bar.open = True
            page.update()
            
            # Reset del borde después de un tiempo
            def reset_border():
                import time
                time.sleep(2)
                dni_field.border_color = "transparent"
                dni_field.update()
            
            import threading
            threading.Thread(target=reset_border, daemon=True).start()
            return
        
        # Mostrar loading
        is_loading = True
        login_button.visible = False
        loading_indicator.visible = True
        page.update()
        
        # Simular delay para mejor UX
        import time
        time.sleep(1)  # Remover esto en producción
        
        if auth_service.login_cliente(dni_field.value):
            # Animación de éxito antes del callback
            login_button.visible = True
            loading_indicator.visible = False
            login_button.bgcolor = "#4CAF50"  # Verde de éxito
            login_button.content = ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=BACKGROUND_DARK, size=20),
                ft.Text("¡Acceso Concedido!", size=16, weight=ft.FontWeight.W_700, color=BACKGROUND_DARK),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            login_button.update()
            
            # Delay para mostrar el éxito
            time.sleep(0.5)
            on_success()
        else:
            # Error handling con animación
            is_loading = False
            login_button.visible = True
            loading_indicator.visible = False
            page.update()
            
            # Snackbar mejorado
            page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color=SECONDARY_COLOR),
                    ft.Text(" Cliente no encontrado o inactivo", color=SECONDARY_COLOR),
                ]),
                bgcolor="#D32F2F",
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
                margin=20,
                elevation=8
            )
            page.snack_bar.open = True
            page.update()

    # Asignar eventos
    login_button.on_hover = animate_button_hover
    login_button.on_click = handle_client_login

    # CONTENIDO DEL LADO IZQUIERDO
    left_panel_content = ft.Container(
        content=ft.Column([
            ft.Container(height=100),
            
            # Títulos principales
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Transforma tu",
                        size=48,
                        weight=ft.FontWeight.W_900,
                        color=SECONDARY_COLOR,
                    ),
                    ft.Text(
                        "cuerpo",
                        size=48,
                        weight=ft.FontWeight.W_900,
                        color=PRIMARY_COLOR,
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "Fortalece tu mente",
                        size=28,
                        weight=ft.FontWeight.W_700,
                        color=SECONDARY_COLOR,
                    ),
                ]),
                padding=ft.padding.only(left=80, right=80),
            ),
            
            ft.Container(height=60),
            
            # Lista de beneficios simple
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.FITNESS_CENTER, color=PRIMARY_COLOR, size=28),
                        ft.Text("Equipamiento de última generación", 
                               size=18, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                    ]),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Icon(ft.Icons.GROUPS, color=PRIMARY_COLOR, size=28),
                        ft.Text("Comunidad activa y motivadora", 
                               size=18, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                    ]),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Icon(ft.Icons.SCHEDULE, color=PRIMARY_COLOR, size=28),
                        ft.Text("Horarios flexibles 24/7", 
                               size=18, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                    ]),
                ]),
                padding=ft.padding.only(left=80, right=80),
            ),
        ]),
        expand=True,
        alignment=ft.alignment.top_left,
    )

    # FORMULARIO FLOTANTE A LA DERECHA - RESPONSIVE
    floating_form = ft.Container(
        content=ft.Column([
            # Logo y título - RESPONSIVE
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Image(
                            src=LOGO_PATH,
                            width=90,
                            height=90,
                            fit=ft.ImageFit.CONTAIN,
                            error_content=ft.Icon(
                                ft.Icons.FITNESS_CENTER, 
                                size=60, 
                                color=PRIMARY_COLOR
                            ),
                        ),
                        margin=ft.margin.only(bottom=15),
                    ),
                    ft.Text(
                        "Acceso para Clientes",
                        size=24,
                        weight=ft.FontWeight.W_900,
                        color=PRIMARY_COLOR,
                    ),
                    
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=40),
            ),
            
            # Formulario - RESPONSIVE
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Bienvenido de vuelta",
                        size=24,
                        weight=ft.FontWeight.W_700,
                        color=TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Ingresa con tu DNI para acceder a tu cuenta",
                        size=14,
                        color=TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    
                    ft.Container(height=40),
                    
                    # Campos del formulario - CONTENEDOR RESPONSIVE
                    ft.Container(
                        content=ft.Column([
                            dni_field,
                            ft.Container(height=10),
                            ft.Text(
                                "Solo números - 8 dígitos",
                                size=12,
                                color=TEXT_SECONDARY,
                                text_align=ft.TextAlign.LEFT,
                            ),
                        ], spacing=0),
                        margin=ft.margin.only(bottom=30),
                    ),
                    
                    # Botones - CONTENEDOR RESPONSIVE
                    ft.Container(
                        content=ft.Stack([
                            login_button,
                            loading_indicator
                        ]),
                        margin=ft.margin.only(bottom=25),
                        height=56,
                    ),
                    
                    # Separador - RESPONSIVE
                    ft.Container(
                        content=ft.Row([
                            ft.Container(expand=True, height=1, bgcolor="#333333"),
                            ft.Text(" o ", color=TEXT_SECONDARY, size=12),
                            ft.Container(expand=True, height=1, bgcolor="#333333"),
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=25),
                    ),
                    
                    # Botón volver - RESPONSIVE
                    ft.Container(
                        content=ft.TextButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW, size=16, color=PRIMARY_COLOR),
                                ft.Text("Volver a selección de rol", color=PRIMARY_COLOR, weight=ft.FontWeight.W_500),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            style=ft.ButtonStyle(
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=lambda _: on_back()
                        ),
                        alignment=ft.alignment.center
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
                ),
                padding=40,
                bgcolor=CARD_BG,
                border_radius=20,
                border=ft.border.all(1, "#333333"),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=35,
                    color=ft.Colors.BLACK87,
                    offset=ft.Offset(0, 10)
                )
            ),
            
            ft.Container(height=40),
            
            # Footer
            ft.Container(
                content=ft.Text(
                    "¿Problemas para acceder? Contacta al administrador",
                    size=12,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=20
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.ADAPTIVE,  # Scroll para pantallas pequeñas
        ),
        width=480,  # Ancho base para desktop
        padding=40,
        bgcolor=CARD_BG,
        border_radius=20,
        border=ft.border.all(1, "#404040"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=60,
            color=ft.Colors.BLACK87,
            offset=ft.Offset(0, 20)
        ),
        margin=ft.margin.only(right=60, top=40, bottom=40),
    )

    # CONTENEDOR RESPONSIVE PARA EL FORMULARIO
    responsive_form_container = ft.Container(
        content=floating_form,
        alignment=ft.alignment.center_right,
        expand=True,
        padding=ft.padding.only(right=20),
    )

    # LAYOUT PRINCIPAL CON CONTENIDO IZQUIERDO Y FORMULARIO FLOTANTE A LA DERECHA
    main_container = ft.Container(
        content=ft.Stack([
            # Fondo de imagen completo con overlay
            ft.Container(
                content=ft.Stack([
                    ft.Image(
                        src=BG_PATH_CLIENT,
                        fit=ft.ImageFit.COVER,
                        expand=True,
                    ),
                    # Overlay para mejor contraste del texto izquierdo
                    ft.Container(
                        bgcolor=ft.Colors.BLACK45,
                        expand=True,
                    ),
                    # Contenido del lado izquierdo
                    left_panel_content,
                ]),
                expand=True,
            ),
            
            # Formulario flotante a la derecha - RESPONSIVE
            responsive_form_container
        ]),
        expand=True,
        bgcolor=BACKGROUND_DARK,
    )

    page.add(main_container)
    page.update()