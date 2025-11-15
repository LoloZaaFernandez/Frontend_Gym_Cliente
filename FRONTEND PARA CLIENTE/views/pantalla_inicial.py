"""
Vista de Pantalla Inicial
Muestra dos opciones principales: Registrarse o Marcar Asistencia
Diseño adaptado del client_login del frontend principal
"""
import flet as ft
import sys
import os

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme


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


    # ==================== FORMULARIO FLOTANTE (DERECHA) ====================

    # Botón Registrarse (responsive)
    btn_registro = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.PERSON_ADD, size=Theme.ICON_SIZE["xl"], color=Theme.PRIMARY),
            ft.Container(height=Theme.SPACING["md"]),
            ft.Text(
                "Registrarse",
                size=Theme.FONT_SIZE["2xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Soy nuevo cliente",
                size=Theme.FONT_SIZE["md"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=Theme.SPACING["xs"]
        ),
        width=320,  # Reducido un poco
        height=200,  # Altura fija para que sean iguales
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(2, Theme.PRIMARY),
        border_radius=Theme.RADIUS["xl"],
        padding=Theme.SPACING["2xl"],
        on_click=ir_a_registro,
        animate=200,
    )

    # Botón Asistencia (responsive)
    btn_asistencia = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.CHECK_CIRCLE, size=Theme.ICON_SIZE["xl"], color=Theme.SUCCESS),
            ft.Container(height=Theme.SPACING["md"]),
            ft.Text(
                "Asistencia",
                size=Theme.FONT_SIZE["2xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Ya soy cliente",
                size=Theme.FONT_SIZE["md"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER
            ),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=Theme.SPACING["xs"]
        ),
        width=320,  # Reducido un poco
        height=200,  # Altura fija para que sean iguales
        bgcolor=Theme.CARD_BG,
        border=ft.border.all(2, Theme.SUCCESS),
        border_radius=Theme.RADIUS["xl"],
        padding=Theme.SPACING["2xl"],
        on_click=ir_a_asistencia,
        animate=200,
    )

    # Efectos hover para los botones
    def animate_registro_hover(e):
        if e.data == "true":
            btn_registro.bgcolor = Theme.CARD_BG_LIGHT
            btn_registro.scale = ft.Scale(1.05)
            btn_registro.shadow = Theme.get_shadow("xl")
        else:
            btn_registro.bgcolor = Theme.CARD_BG
            btn_registro.scale = ft.Scale(1.0)
            btn_registro.shadow = None
        btn_registro.update()

    def animate_asistencia_hover(e):
        if e.data == "true":
            btn_asistencia.bgcolor = Theme.CARD_BG_LIGHT
            btn_asistencia.scale = ft.Scale(1.05)
            btn_asistencia.shadow = Theme.get_shadow("xl")
        else:
            btn_asistencia.bgcolor = Theme.CARD_BG
            btn_asistencia.scale = ft.Scale(1.0)
            btn_asistencia.shadow = None
        btn_asistencia.update()

    btn_registro.on_hover = animate_registro_hover
    btn_asistencia.on_hover = animate_asistencia_hover

    # Panel flotante con las opciones (CENTRADO Y RESPONSIVE)
    floating_form = ft.Container(
        content=ft.Column([
            # Logo/Header
            ft.Container(
                content=ft.Column([
                    ft.Icon(
                        ft.Icons.FITNESS_CENTER,
                        size=70,  # Reducido un poco
                        color=Theme.PRIMARY
                    ),
                    ft.Text(
                        "BLESSED GYM",
                        size=Theme.FONT_SIZE["3xl"],  # Reducido un poco
                        weight=Theme.FONT_WEIGHT["extrabold"],
                        color=Theme.PRIMARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=Theme.SPACING["2xl"]),
            ),

            # Contenido del formulario
            ft.Container(
                content=ft.Column([
                    # Título
                    ft.Text(
                        "Bienvenido",
                        size=Theme.FONT_SIZE["2xl"],  # Reducido
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Selecciona una opción para continuar",
                        size=Theme.FONT_SIZE["md"],
                        color=Theme.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Container(height=Theme.SPACING["2xl"]),  # Reducido

                    # Botones de opciones LADO A LADO
                    ft.Row([
                        btn_registro,
                        btn_asistencia,
                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=Theme.SPACING["2xl"],
                        wrap=True,  # Permite que se envuelvan en pantallas pequeñas
                    ),

                    ft.Container(height=Theme.SPACING["2xl"]),  # Reducido

                    # Separador
                    ft.Container(
                        content=ft.Row([
                            ft.Container(expand=True, height=1, bgcolor=Theme.BORDER_DEFAULT),
                            ft.Text(" o ", color=Theme.TEXT_SECONDARY, size=Theme.FONT_SIZE["xs"]),
                            ft.Container(expand=True, height=1, bgcolor=Theme.BORDER_DEFAULT),
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=Theme.SPACING["md"]),
                    ),

                    # Mensaje de ayuda
                    ft.Container(
                        content=ft.Text(
                            "¿Problemas? Consulta con el personal del gimnasio",
                            size=Theme.FONT_SIZE["xs"],
                            color=Theme.TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER
                        ),
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=Theme.SPACING["2xl"],  # Reducido
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["xl"],
                border=ft.border.all(1, Theme.BORDER_DEFAULT),
                shadow=Theme.get_shadow("xl")
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
        width=None,  # Sin ancho fijo - responsive
        padding=Theme.SPACING["2xl"],  # Reducido
        bgcolor=Theme.CARD_BG,
        border_radius=Theme.RADIUS["xl"],
        border=ft.border.all(1, "#404040"),
        shadow=Theme.get_shadow("2xl"),
    )

    # ==================== LAYOUT PRINCIPAL ====================
    main_container = ft.Container(
        content=ft.Row([
            floating_form
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=Theme.BACKGROUND_DARK,
        alignment=ft.alignment.center,
        padding=Theme.SPACING["xl"],  # Padding reducido
    )

    # Limpiar y mostrar
    page.controls.clear()
    page.add(main_container)
    page.update()
