"""
Vista de Historial de Asistencias para Cliente
"""

import flet as ft
from datetime import datetime
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_cliente_asistencias_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de historial de asistencias para cliente

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Mis Asistencias"

    api = APIService()
    cliente_data = auth_service.get_current_user()
    cliente_id = cliente_data['id']

    # Estadísticas del cliente
    stats = {
        "total_asistencias": 0,
        "ultima_asistencia": None,
        "asistencias_mes_actual": 0,
        "asistencias_recientes": []
    }

    # Tarjetas de estadísticas
    total_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR)
    mes_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color="#4CAF50")
    ultima_text = ft.Text("Sin registros", size=16, weight=ft.FontWeight.W_500, color=TEXT_SECONDARY)

    # Lista de asistencias
    asistencias_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    asistencias_container = ft.Container(
        content=asistencias_list,
        height=500,
        padding=15,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333")
    )

    def cargar_datos():
        """Cargar datos del cliente"""
        nonlocal stats

        try:
            # Obtener estadísticas
            stats = api.get_estadisticas_cliente(cliente_id)

            # Actualizar textos de estadísticas
            total_text.value = str(stats.get('total_asistencias', 0))
            mes_text.value = str(stats.get('asistencias_mes_actual', 0))

            # Última asistencia
            ultima = stats.get('ultima_asistencia')
            if ultima:
                try:
                    fecha_dt = datetime.fromisoformat(ultima)
                    ultima_text.value = fecha_dt.strftime("%d/%m/%Y")
                except:
                    ultima_text.value = ultima
            else:
                ultima_text.value = "Sin registros"

            # Actualizar lista de asistencias
            actualizar_lista_asistencias()

        except Exception as e:
            print(f"Error al cargar datos: {e}")
            mostrar_mensaje("Error al cargar datos", error=True)

        page.update()

    def actualizar_lista_asistencias():
        """Actualizar lista de asistencias"""
        asistencias_list.controls.clear()

        asistencias = stats.get('asistencias_recientes', [])

        if not asistencias:
            asistencias_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.INBOX, size=80, color="#333333"),
                            ft.Text(
                                "No hay asistencias registradas",
                                color=TEXT_SECONDARY,
                                size=16,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Registra tu primera asistencia en el gimnasio",
                                color="#666666",
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )
        else:
            for asistencia in asistencias:
                asistencias_list.controls.append(crear_asistencia_card(asistencia))

    def crear_asistencia_card(asistencia):
        """Crear tarjeta de asistencia"""
        # Formatear fecha y hora
        fecha = asistencia.get('fecha_asistencia', '')
        hora = asistencia.get('hora_ingreso', '')[:8]  # Solo HH:MM:SS

        try:
            fecha_dt = datetime.fromisoformat(fecha)
            fecha_formatted = fecha_dt.strftime("%d %b %Y")
        except:
            fecha_formatted = fecha

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.CHECK_CIRCLE, size=28, color="#4CAF50"),
                        bgcolor="#4CAF5022",
                        border_radius=10,
                        padding=12
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                fecha_formatted,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=TEXT_SECONDARY),
                                    ft.Text(
                                        f"Hora de ingreso: {hora}",
                                        size=13,
                                        color=TEXT_SECONDARY
                                    ),
                                ],
                                spacing=5
                            ),
                        ],
                        spacing=5,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.FITNESS_CENTER, size=24, color=PRIMARY_COLOR),
                        padding=8
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=15,
            bgcolor="#1A1A1A",
            border_radius=10,
            border=ft.border.all(1, "#333333"),
            ink=True,
            on_hover=lambda e: hover_effect(e)
        )

    def hover_effect(e):
        """Efecto hover en cards"""
        if e.data == "true":
            e.control.border = ft.border.all(1, PRIMARY_COLOR)
        else:
            e.control.border = ft.border.all(1, "#333333")
        e.control.update()

    def mostrar_mensaje(mensaje, error=False):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#ef5350" if error else "#4CAF50"
        )
        page.snack_bar.open = True
        page.update()

    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=PRIMARY_COLOR,
                        on_click=lambda _: on_back(),
                        icon_size=24
                    ),
                    ft.Icon(ft.Icons.HISTORY, size=32, color=PRIMARY_COLOR),
                    ft.Text("Mi Historial de Asistencias", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ], spacing=10),
                ft.ElevatedButton(
                    "Actualizar",
                    icon=ft.Icons.REFRESH,
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        bgcolor=ft.Colors.TRANSPARENT,
                        side=ft.border.all(1, PRIMARY_COLOR)
                    ),
                    on_click=lambda _: cargar_datos(),
                    height=40
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Información del cliente
    info_cliente = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=PRIMARY_COLOR),
                    bgcolor=f"{PRIMARY_COLOR}22",
                    border_radius=25,
                    padding=10
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            f"{cliente_data['nombre']} {cliente_data['apellidos']}",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),
                        ft.Text(
                            f"DNI: {cliente_data['dni']}",
                            size=14,
                            color=TEXT_SECONDARY
                        ),
                    ],
                    spacing=3
                ),
            ],
            spacing=15
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333")
    )

    # Tarjetas de estadísticas
    stats_cards = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.FITNESS_CENTER, size=32, color=PRIMARY_COLOR),
                        total_text,
                        ft.Text("Total de Asistencias", size=13, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8
                ),
                bgcolor=CARD_BG,
                padding=25,
                border_radius=12,
                border=ft.border.all(1, "#333333"),
                expand=True
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CALENDAR_MONTH, size=32, color="#4CAF50"),
                        mes_text,
                        ft.Text("Asistencias Este Mes", size=13, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8
                ),
                bgcolor=CARD_BG,
                padding=25,
                border_radius=12,
                border=ft.border.all(1, "#333333"),
                expand=True
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.ACCESS_TIME, size=32, color="#2196F3"),
                        ultima_text,
                        ft.Text("Última Asistencia", size=13, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8
                ),
                bgcolor=CARD_BG,
                padding=25,
                border_radius=12,
                border=ft.border.all(1, "#333333"),
                expand=True
            ),
        ],
        spacing=15
    )

    # Panel de historial
    historial_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LIST_ALT, size=22, color=PRIMARY_COLOR),
                        ft.Text(
                            "Historial Reciente",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),
                    ],
                    spacing=10
                ),
                ft.Divider(height=1, color="#333333"),
                asistencias_container,
            ],
            spacing=15
        ),
        padding=25,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333"),
        margin=ft.margin.only(top=10)
    )

    # Layout principal
    main_content = ft.Column(
        controls=[
            header,
            ft.Container(
                content=ft.Column(
                    controls=[
                        info_cliente,
                        stats_cards,
                        historial_panel,
                    ],
                    spacing=15
                ),
                padding=ft.padding.symmetric(horizontal=10)
            ),
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    page.add(
        ft.Container(
            content=main_content,
            bgcolor=BACKGROUND_DARK,
            expand=True,
            padding=10
        )
    )

    # Cargar datos iniciales
    cargar_datos()
