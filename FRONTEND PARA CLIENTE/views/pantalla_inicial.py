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
    Mostrar pantalla inicial con opciones de Registrarse y Asistencia

    Args:
        page: Instancia de la página de Flet
        on_navigate: Función para navegar (recibe "registro" o "asistencia")
    """
    page.clean()
    page.bgcolor = Theme.BACKGROUND_DARK

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
                width=140,
                height=140,
                fit=ft.ImageFit.CONTAIN,
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Título en verde lima
            ft.Text(
                "Registrarse",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=verde_lima_solido,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=Theme.SPACING["sm"]),

            # Descripción
            ft.Text(
                "Nuevo en el gimnasio",
                size=Theme.FONT_SIZE["md"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        ),
        width=360,
        height=340,
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(2, verde_success),
        border_radius=Theme.RADIUS["xl"],
        padding=Theme.SPACING["3xl"],
        on_click=ir_a_registro,
        animate=200,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
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
                width=140,
                height=140,
                fit=ft.ImageFit.CONTAIN,
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Título en verde lima
            ft.Text(
                "Asistencia",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=verde_lima_solido,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=Theme.SPACING["sm"]),

            # Descripción
            ft.Text(
                "Marcar mi entrada",
                size=Theme.FONT_SIZE["md"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        ),
        width=360,
        height=340,
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(2, verde_success),
        border_radius=Theme.RADIUS["xl"],
        padding=Theme.SPACING["3xl"],
        on_click=ir_a_asistencia,
        animate=200,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color="rgba(76, 175, 80, 0.4)",
            offset=ft.Offset(0, 0),
        ),
    )

    # Efectos hover con efecto glow intenso
    def animate_registro_hover(e):
        if e.data == "true":
            card_registro.scale = 1.02
            card_registro.border = ft.border.all(3, verde_success)
            card_registro.shadow = ft.BoxShadow(
                spread_radius=4,
                blur_radius=30,
                color="rgba(76, 175, 80, 0.7)",
                offset=ft.Offset(0, 0),
            )
        else:
            card_registro.scale = 1.0
            card_registro.border = ft.border.all(2, verde_success)
            card_registro.shadow = ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color="rgba(76, 175, 80, 0.4)",
                offset=ft.Offset(0, 0),
            )
        card_registro.update()

    def animate_asistencia_hover(e):
        if e.data == "true":
            card_asistencia.scale = 1.02
            card_asistencia.border = ft.border.all(3, verde_success)
            card_asistencia.shadow = ft.BoxShadow(
                spread_radius=4,
                blur_radius=30,
                color="rgba(76, 175, 80, 0.7)",
                offset=ft.Offset(0, 0),
            )
        else:
            card_asistencia.scale = 1.0
            card_asistencia.border = ft.border.all(2, verde_success)
            card_asistencia.shadow = ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
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
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                ) if logo_existe else ft.Icon(
                    ft.Icons.FITNESS_CENTER_ROUNDED,
                    size=80,
                    color=Theme.PRIMARY
                ),
                width=320,
                height=320,
                bgcolor="rgba(159, 255, 51, 0.03)" if logo_existe else "rgba(159, 255, 51, 0.1)",
                border_radius=160,
                border=ft.border.all(3, "rgba(159, 255, 51, 0.2)"),
                alignment=ft.alignment.center,
                padding=Theme.SPACING["lg"],
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=30,
                    color="rgba(159, 255, 51, 0.2)",
                    offset=ft.Offset(0, 4),
                ),
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Slogan minimal
            ft.Text(
                "Tu transformación empieza aquí",
                size=Theme.FONT_SIZE["xl"],
                weight=Theme.FONT_WEIGHT["medium"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        margin=ft.margin.only(bottom=Theme.SPACING["3xl"]),
    )

    # ==================== CONTENEDOR PRINCIPAL RESPONSIVE ====================

    contenido_principal = ft.Container(
        content=ft.Column([
            header_principal,

            # Título de sección
            ft.Text(
                "Selecciona una opción",
                size=Theme.FONT_SIZE["2xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Tarjetas lado a lado (responsive) - MÁS CERCANAS
            ft.Row([
                card_registro,
                card_asistencia,
            ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=Theme.SPACING["xl"],
                wrap=True,
            ),

            ft.Container(height=Theme.SPACING["3xl"]),

            # Footer con ayuda - MINIMAL
            ft.Row([
                ft.Icon(
                    ft.Icons.SUPPORT_AGENT_ROUNDED,
                    size=20,
                    color=Theme.TEXT_SECONDARY
                ),
                ft.Text(
                    "¿Necesitas ayuda? Consulta con el personal",
                    size=Theme.FONT_SIZE["md"],
                    color=Theme.TEXT_SECONDARY,
                ),
            ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=Theme.SPACING["sm"],
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        padding=Theme.SPACING["3xl"],
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
