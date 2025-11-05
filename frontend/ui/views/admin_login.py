"""
Vista de login para administradores
"""

import flet as ft
import os
from config.settings import (
    LOGO_PATH, BG_PATH, PRIMARY_COLOR, TEXT_SECONDARY,
    BACKGROUND_DARK, CARD_BG, TEXT_PRIMARY
)
from ui.components.common import create_text_field, create_primary_button


def show_admin_login(page: ft.Page, auth_service, on_success, on_back):
    """
    Mostrar pantalla de login para administradores

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_success: Callback para login exitoso
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Login Administrador"

    # Verificar si existen las imágenes
    logo_exists = os.path.exists(LOGO_PATH)
    bg_exists = os.path.exists(BG_PATH)

    username_field = create_text_field("Nombre de Usuario")
    password_field = create_text_field("Contraseña", password=True)

    def handle_login(e):
        if auth_service.login_admin(username_field.value, password_field.value):
            on_success()
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Credenciales incorrectas"),
                bgcolor=PRIMARY_COLOR
            )
            page.snack_bar.open = True
            page.update()

    # Panel izquierdo - Formulario de login
    login_panel = ft.Container(
        expand=1,
        bgcolor=BACKGROUND_DARK,
        padding=40,
        alignment=ft.alignment.center,
        content=ft.Column(
            width=400,
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=LOGO_PATH if logo_exists else None,
                        width=180,
                        height=180,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Column(
                            [
                                ft.Icon(ft.Icons.FITNESS_CENTER, size=50, color=PRIMARY_COLOR),
                                ft.Text("BLESSED", color=PRIMARY_COLOR, size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("FIT CLUB", color=PRIMARY_COLOR, size=18, weight=ft.FontWeight.BOLD)
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        )
                    ),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(bottom=20)
                ),

                ft.Text(
                    "CADA DESAFIO ES UNA OPORTUNIDAD",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=PRIMARY_COLOR
                ),
                ft.Text(
                    "TU MUNDO NUESTRO MUNDO",
                    size=12,
                    color=TEXT_SECONDARY
                ),
                ft.Container(height=30),

                ft.Text("Nombre de Usuario", color=TEXT_SECONDARY, size=12),
                username_field,
                ft.Container(height=15),

                ft.Text("Contraseña", color=TEXT_SECONDARY, size=12),
                password_field,
                ft.Container(height=25),

                create_primary_button("Login", handle_login),

                ft.Container(height=20),

                ft.TextButton(
                    "← Volver a selección de rol",
                    style=ft.ButtonStyle(color=PRIMARY_COLOR),
                    on_click=lambda _: on_back()
                )
            ]
        )
    )

    # Panel derecho - Imagen de fondo
    bg_panel = ft.Container(
        expand=2,
        content=ft.Image(
            src=BG_PATH if bg_exists else None,
            fit=ft.ImageFit.COVER,
            expand=True,
            error_content=ft.Container(
                bgcolor=BACKGROUND_DARK,
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.FITNESS_CENTER, size=100, color=PRIMARY_COLOR),
                        ft.Text("BLESSED GYM", size=24, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
    )

    page.add(ft.Row(controls=[login_panel, bg_panel], expand=True, spacing=0))
    page.update()
