"""
Vista de selección de rol (Admin o Cliente)
"""

import flet as ft
import os
from config.settings import (
    LOGO_PATH, PRIMARY_COLOR, TEXT_PRIMARY, TEXT_SECONDARY,
    BACKGROUND_DARK, CARD_BG, BG_PATH_ROL
)
from ui.components.common import create_role_card


def show_role_selection(page: ft.Page, on_admin_click, on_client_click):
    """
    Mostrar la pantalla de selección de rol
    """
    page.clean()
    page.title = "BLESSED GYM - Selección de Rol"

    # Verificar si existen las imágenes
    logo_exists = os.path.exists(LOGO_PATH)
    bg_exists = os.path.exists(BG_PATH_ROL)

    # Configurar fondo de página
    if bg_exists:
        page.bgcolor = BACKGROUND_DARK  # Color de respaldo
        # Agregar imagen de fondo usando Stack
        background_image = ft.Container(
            content=ft.Image(
                src=BG_PATH_ROL,
                fit=ft.ImageFit.COVER,
                expand=True,
            ),
            expand=True,
        )
    else:
        background_image = ft.Container(bgcolor=BACKGROUND_DARK, expand=True)

    # Contenido principal
    content = ft.Container(
        content=ft.Column(
            controls=[
                # Header con logo
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src=LOGO_PATH if logo_exists else None,
                                    width=120,
                                    height=120,
                                    fit=ft.ImageFit.CONTAIN,
                                    error_content=ft.Column(
                                        [
                                            ft.Icon(ft.Icons.FITNESS_CENTER, size=50, color=PRIMARY_COLOR),
                                            ft.Text("BLESSED GYM", color=PRIMARY_COLOR, size=16, weight=ft.FontWeight.BOLD)
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    )
                                ),
                                alignment=ft.alignment.center,
                                margin=ft.margin.only(bottom=20)
                            ),
                            ft.Text(
                                "Sistema de Gestión Integral",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=PRIMARY_COLOR,
                                text_align=ft.TextAlign.CENTER
                            ),

                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5
                    ),
                    padding=ft.padding.only(top=40, bottom=40)
                ),

                # Subtítulo
                ft.Container(
                    content=ft.Text(
                        "Selecciona tu tipo de acceso:",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=ft.padding.only(bottom=40)
                ),

                # Tarjetas de selección
                ft.Row(
                    controls=[
                        create_role_card(
                            "Administrador",
                            "Gestión completa del gimnasio",
                            ft.Icons.ADMIN_PANEL_SETTINGS,
                            PRIMARY_COLOR,
                            lambda _: on_admin_click()
                        ),
                        create_role_card(
                            "Cliente",
                            "Portal personal del cliente",
                            ft.Icons.PERSON,
                            "#4CAF50",
                            lambda _: on_client_click()
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40
                ),

                # Footer
                ft.Container(
                    content=ft.Text(
                        "© 2025 Blessed Gym - Todos los derechos reservados",
                        size=12,
                        color=TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    margin=ft.margin.only(top=80)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=40,
        expand=True
    )

    # Usar Stack para superponer contenido sobre el fondo
    if bg_exists:
        main_container = ft.Stack(
            controls=[
                background_image,
                content
            ],
            expand=True
        )
    else:
        main_container = content

    page.add(main_container)
    page.update()