"""
Vista de Pantalla Inicial - REDISEÑADA PARA TABLET - RESPONSIVE & MODERNA
Muestra dos opciones principales: Registrarse o Marcar Asistencia
Diseño moderno con background personalizado y efectos visuales premium
"""
import flet as ft
import sys
import os

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme
from config.settings import BACKGROUND_IMAGE


def show_pantalla_inicial(page: ft.Page, on_navigate):
    """
    Mostrar pantalla inicial con opciones de Registrarse y Asistencia - RESPONSIVE

    Args:
        page: Instancia de la página de Flet
        on_navigate: Función para navegar (recibe "registro" o "asistencia")
    """
    page.clean()
    page.bgcolor = Theme.BACKGROUND_DARK

    # Obtener dimensiones de la página para cálculos responsive
    page_width = page.window.width or page.width or Theme.BASE_WIDTH
    page_height = page.window.height or page.height or Theme.BASE_HEIGHT

    # Calcular factor de escala
    scale = page_width / Theme.BASE_WIDTH
    scale = max(0.75, min(1.25, scale))

    # Calcular dimensiones responsive
    card_width = int(360 * scale)
    card_height = int(340 * scale)
    img_size = int(140 * scale)
    logo_size = int(300 * scale)
    logo_container_size = int(320 * scale)
    logo_icon_size = int(80 * scale)

    title_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["4xl"])
    subtitle_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["md"])
    section_title_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["2xl"])
    slogan_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["xl"])
    help_size = Theme.get_responsive_font_size(page_width, Theme.FONT_SIZE["md"])

    spacing_xl = Theme.get_responsive_spacing(page_width, Theme.SPACING["xl"])
    spacing_sm = Theme.get_responsive_spacing(page_width, Theme.SPACING["sm"])
    spacing_2xl = Theme.get_responsive_spacing(page_width, Theme.SPACING["2xl"])
    spacing_3xl = Theme.get_responsive_spacing(page_width, Theme.SPACING["3xl"])
    spacing_lg = Theme.get_responsive_spacing(page_width, Theme.SPACING["lg"])

    border_radius_xl = int(Theme.RADIUS["xl"] * scale)
    border_width = int(2 * scale)
    border_width_hover = int(3 * scale)
    shadow_blur = int(20 * scale)
    shadow_blur_hover = int(30 * scale)

    def ir_a_registro(e):
        """Navegar a la pantalla de registro"""
        on_navigate("registro")

    def ir_a_asistencia(e):
        """Navegar a la pantalla de asistencia"""
        on_navigate("asistencia")


    # ==================== TARJETAS DE ACCIÓN MINIMAL & MODERNA ====================

    # Rutas de imágenes personalizadas
    img_registro_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "HOVER_REGISTRO.png")
    img_asistencia_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "HOVER_ASISTENCIA.png")

    # Color verde (SUCCESS) para bordes
    verde_border = "rgba(76, 175, 80, 0.6)"  # Verde translúcido para borde
    verde_lima_solido = "#9FFF33"  # Verde lima sólido para texto
    verde_success = Theme.SUCCESS  # Verde sólido

    # Tarjeta Registrarse
    card_registro = ft.Container(
        content=ft.Column([
            # Imagen personalizada más grande
            ft.Image(
                src=img_registro_path,
                width=img_size,
                height=img_size,
                fit=ft.ImageFit.CONTAIN,
            ),

            ft.Container(height=spacing_xl),

            # Título en verde lima
            ft.Text(
                "Registrarse",
                size=title_size,
                weight=Theme.FONT_WEIGHT["bold"],
                color=verde_lima_solido,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=spacing_sm),

            # Descripción
            ft.Text(
                "Nuevo en el gimnasio",
                size=subtitle_size,
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        ),
        width=card_width,
        height=card_height,
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(border_width, verde_success),
        border_radius=border_radius_xl,
        padding=spacing_3xl,
        on_click=ir_a_registro,
        animate=200,
        shadow=ft.BoxShadow(
            spread_radius=border_width,
            blur_radius=shadow_blur,
            color="rgba(76, 175, 80, 0.4)",
            offset=ft.Offset(0, 0),
        ),
    )

    # Tarjeta Asistencia
    card_asistencia = ft.Container(
        content=ft.Column([
            # Imagen personalizada más grande
            ft.Image(
                src=img_asistencia_path,
                width=img_size,
                height=img_size,
                fit=ft.ImageFit.CONTAIN,
            ),

            ft.Container(height=spacing_xl),

            # Título en verde lima
            ft.Text(
                "Asistencia",
                size=title_size,
                weight=Theme.FONT_WEIGHT["bold"],
                color=verde_lima_solido,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=spacing_sm),

            # Descripción
            ft.Text(
                "Marcar mi entrada",
                size=subtitle_size,
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        ),
        width=card_width,
        height=card_height,
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(border_width, verde_success),
        border_radius=border_radius_xl,
        padding=spacing_3xl,
        on_click=ir_a_asistencia,
        animate=200,
        shadow=ft.BoxShadow(
            spread_radius=border_width,
            blur_radius=shadow_blur,
            color="rgba(76, 175, 80, 0.4)",
            offset=ft.Offset(0, 0),
        ),
    )

    # Efectos hover con efecto glow intenso
    def animate_registro_hover(e):
        if e.data == "true":
            card_registro.scale = 1.02
            card_registro.border = ft.border.all(border_width_hover, verde_success)
            card_registro.shadow = ft.BoxShadow(
                spread_radius=int(4 * scale),
                blur_radius=shadow_blur_hover,
                color="rgba(76, 175, 80, 0.7)",
                offset=ft.Offset(0, 0),
            )
        else:
            card_registro.scale = 1.0
            card_registro.border = ft.border.all(border_width, verde_success)
            card_registro.shadow = ft.BoxShadow(
                spread_radius=border_width,
                blur_radius=shadow_blur,
                color="rgba(76, 175, 80, 0.4)",
                offset=ft.Offset(0, 0),
            )
        card_registro.update()

    def animate_asistencia_hover(e):
        if e.data == "true":
            card_asistencia.scale = 1.02
            card_asistencia.border = ft.border.all(border_width_hover, verde_success)
            card_asistencia.shadow = ft.BoxShadow(
                spread_radius=int(4 * scale),
                blur_radius=shadow_blur_hover,
                color="rgba(76, 175, 80, 0.7)",
                offset=ft.Offset(0, 0),
            )
        else:
            card_asistencia.scale = 1.0
            card_asistencia.border = ft.border.all(border_width, verde_success)
            card_asistencia.shadow = ft.BoxShadow(
                spread_radius=border_width,
                blur_radius=shadow_blur,
                color="rgba(76, 175, 80, 0.4)",
                offset=ft.Offset(0, 0),
            )
        card_asistencia.update()

    # Activar animaciones
    card_registro.on_hover = animate_registro_hover
    card_registro.animate_scale = 150

    card_asistencia.on_hover = animate_asistencia_hover
    card_asistencia.animate_scale = 150

    # ==================== HEADER PRINCIPAL ====================

    # Verificar si existe el logo
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "logo.png")
    logo_existe = os.path.exists(logo_path)

    header_principal = ft.Container(
        content=ft.Column([
            # Logo del gimnasio con efecto premium
            ft.Container(
                content=ft.Image(
                    src=logo_path if logo_existe else None,
                    width=logo_size,
                    height=logo_size,
                    fit=ft.ImageFit.CONTAIN,
                ) if logo_existe else ft.Icon(
                    ft.Icons.FITNESS_CENTER_ROUNDED,
                    size=logo_icon_size,
                    color=Theme.PRIMARY
                ),
                width=logo_container_size,
                height=logo_container_size,
                bgcolor="rgba(159, 255, 51, 0.03)" if logo_existe else "rgba(159, 255, 51, 0.1)",
                border_radius=int(logo_container_size / 2),
                border=ft.border.all(border_width_hover, "rgba(159, 255, 51, 0.2)"),
                alignment=ft.alignment.center,
                padding=spacing_lg,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=shadow_blur_hover,
                    color="rgba(159, 255, 51, 0.2)",
                    offset=ft.Offset(0, int(4 * scale)),
                ),
            ),

            ft.Container(height=spacing_xl),

            # Slogan minimal
            ft.Text(
                "Tu transformación empieza aquí",
                size=slogan_size,
                weight=Theme.FONT_WEIGHT["medium"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        margin=ft.margin.only(bottom=spacing_3xl),
    )

    # ==================== CONTENEDOR PRINCIPAL RESPONSIVE ====================

    contenido_principal = ft.Container(
        content=ft.Column([
            header_principal,

            # Título de sección
            ft.Text(
                "Selecciona una opción",
                size=section_title_size,
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=spacing_2xl),

            # Tarjetas lado a lado (responsive) - MÁS CERCANAS
            ft.Row([
                card_registro,
                card_asistencia,
            ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=spacing_xl,
                wrap=True,
            ),

            ft.Container(height=spacing_3xl),

            # Footer con ayuda - MINIMAL
            ft.Row([
                ft.Icon(
                    ft.Icons.SUPPORT_AGENT_ROUNDED,
                    size=int(20 * scale),
                    color=Theme.TEXT_SECONDARY
                ),
                ft.Text(
                    "¿Necesitas ayuda? Consulta con el personal",
                    size=help_size,
                    color=Theme.TEXT_SECONDARY,
                ),
            ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=spacing_sm,
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        padding=spacing_3xl,
        alignment=ft.alignment.center,
    )

    # ==================== LAYOUT CON BACKGROUND ====================

    # Verificar si existe el archivo de background
    background_existe = os.path.exists(BACKGROUND_IMAGE)

    if background_existe:
        # Layout con imagen de fondo usando Stack
        main_container = ft.Stack([
            # Imagen de fondo
            ft.Image(
                src=BACKGROUND_IMAGE,
                fit=ft.ImageFit.COVER,
                width=float('inf'),
                height=float('inf'),
            ),
            # Overlay oscuro para mejorar legibilidad
            ft.Container(
                bgcolor=Theme.OVERLAY_DARK,
                expand=True,
            ),
            # Contenido principal con scroll
            ft.Container(
                content=ft.Column(
                    [contenido_principal],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
                alignment=ft.alignment.center,
            ),
        ],
            expand=True,
        )
    else:
        # Fallback sin imagen de fondo
        main_container = ft.Container(
            content=ft.Column(
                [contenido_principal],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=Theme.BACKGROUND_DARK,
            alignment=ft.alignment.center,
        )

    # Limpiar y mostrar
    page.controls.clear()
    page.add(main_container)
    page.update()
