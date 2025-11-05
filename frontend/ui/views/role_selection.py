"""
Vista de selección de rol (Admin o Cliente)
"""

import flet as ft
import os
from config.settings import (
    LOGO_PATH, PRIMARY_COLOR, TEXT_PRIMARY, TEXT_SECONDARY,
    BACKGROUND_DARK, CARD_BG
)
from ui.components.common import create_role_card


def show_role_selection(page: ft.Page, on_admin_click, on_client_click):
    """
    Mostrar la pantalla de selección de rol

    Args:
        page: Página de Flet
        on_admin_click: Callback para cuando se selecciona Admin
        on_client_click: Callback para cuando se selecciona Cliente
    """
    page.clean()

    # Verificar si existe el logo
    logo_exists = os.path.exists(LOGO_PATH)

    main_container = ft.Container(
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
                                "BLESSED GYM",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=PRIMARY_COLOR,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Sistema de Gestión Integral",
                                size=16,
                                color=TEXT_SECONDARY,
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
        bgcolor=BACKGROUND_DARK,
        padding=40,
        expand=True
    )

    page.add(main_container)
    page.update()
