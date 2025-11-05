"""
Vista de login para clientes
"""

import flet as ft
from config.settings import (
    PRIMARY_COLOR, TEXT_SECONDARY, BACKGROUND_DARK, CARD_BG, TEXT_PRIMARY
)
from ui.components.common import create_text_field


def show_client_login(page: ft.Page, auth_service, on_success, on_back):
    """
    Mostrar pantalla de login para clientes

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_success: Callback para login exitoso
        on_back: Callback para volver atrás
    """
    page.clean()

    dni_field = ft.TextField(
        label="Ingrese su DNI",
        border_radius=8,
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        height=50,
        text_size=14,
        content_padding=15,
        width=400,
        bgcolor=CARD_BG,
        border_width=1,
        color=TEXT_PRIMARY,
        label_style=ft.TextStyle(color=TEXT_SECONDARY)
    )

    def handle_client_login(e):
        if auth_service.login_cliente(dni_field.value):
            on_success()
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Cliente no encontrado o inactivo. Contacte al administrador."),
                bgcolor=PRIMARY_COLOR
            )
            page.snack_bar.open = True
            page.update()

    main_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=80),
                ft.Text(
                    "BLESSED GYM",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=PRIMARY_COLOR,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Acceso Cliente",
                    size=18,
                    color=TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=40),

                ft.Container(
                    content=ft.Column([
                        dni_field,
                        ft.Container(height=25),
                        ft.ElevatedButton(
                            content=ft.Text(
                                "Ingresar con DNI",
                                size=16,
                                weight=ft.FontWeight.W_600
                            ),
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLACK,
                                bgcolor=PRIMARY_COLOR,
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=handle_client_login,
                            width=400
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=CARD_BG,
                    padding=40,
                    border_radius=12,
                    border=ft.border.all(1, "#333333"),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.BLACK45,
                        offset=ft.Offset(0, 4)
                    )
                ),

                ft.Container(height=40),
                ft.TextButton(
                    "← Volver a selección de rol",
                    style=ft.ButtonStyle(color=PRIMARY_COLOR),
                    on_click=lambda _: on_back()
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        bgcolor=BACKGROUND_DARK,
        padding=40
    )

    page.add(main_container)
    page.update()
