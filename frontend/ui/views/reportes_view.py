"""
Vista de Reportes y Estadísticas con visualización de datos
"""

import flet as ft
from datetime import datetime
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from ui.components.common import create_info_card


def show_reportes_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de reportes y estadísticas

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Reportes y Estadísticas"

    # Datos simulados (integrar con DB real)
    estadisticas = {
        "total_clientes": 150,
        "clientes_activos": 142,
        "asistencias_hoy": 45,
        "asistencias_mes": 1250,
        "ingresos_hoy": 850.00,
        "ingresos_mes": 22500.00,
        "membresías_activas": 138,
        "membresías_vencidas": 12
    }

    ventas_recientes = [
        {"fecha": "05/11/2025 14:30", "producto": "Membresía Mensual", "monto": 150.00, "cliente": "Juan Pérez"},
        {"fecha": "05/11/2025 15:15", "producto": "Proteína Whey 1kg", "monto": 80.00, "cliente": "María García"},
        {"fecha": "05/11/2025 16:00", "producto": "Membresía Trimestral", "monto": 400.00, "cliente": "Carlos López"},
        {"fecha": "05/11/2025 16:45", "producto": "Guantes de Gym", "monto": 35.00, "cliente": "Ana Martínez"},
        {"fecha": "05/11/2025 17:20", "producto": "Shaker", "monto": 15.00, "cliente": "Luis Torres"},
    ]

    productos_top = [
        {"producto": "Membresía Mensual", "cantidad": 45, "ingresos": 6750.00},
        {"producto": "Membresía Trimestral", "cantidad": 28, "ingresos": 11200.00},
        {"producto": "Proteína Whey 1kg", "cantidad": 35, "ingresos": 2800.00},
        {"producto": "Membresía Anual", "cantidad": 8, "ingresos": 12000.00},
        {"producto": "Creatina 300g", "cantidad": 22, "ingresos": 990.00},
    ]

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=PRIMARY_COLOR,
                on_click=lambda _: on_back()
            ),
            ft.Text(
                "Reportes y Estadísticas - BLESSED GYM",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
        ]),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Tarjetas de estadísticas principales
    stats_row_1 = ft.Row([
        create_info_card(
            "Total Clientes",
            str(estadisticas["total_clientes"]),
            ft.Icons.PEOPLE,
            PRIMARY_COLOR
        ),
        create_info_card(
            "Clientes Activos",
            str(estadisticas["clientes_activos"]),
            ft.Icons.PERSON_ADD,
            "#4CAF50"
        ),
        create_info_card(
            "Asistencias Hoy",
            str(estadisticas["asistencias_hoy"]),
            ft.Icons.TODAY,
            "#2196F3"
        ),
        create_info_card(
            "Asistencias Mes",
            str(estadisticas["asistencias_mes"]),
            ft.Icons.CALENDAR_MONTH,
            "#9C27B0"
        ),
    ], spacing=15, scroll=ft.ScrollMode.AUTO, wrap=True)

    stats_row_2 = ft.Row([
        create_info_card(
            "Ingresos Hoy",
            f"S/. {estadisticas['ingresos_hoy']:.0f}",
            ft.Icons.ATTACH_MONEY,
            PRIMARY_COLOR
        ),
        create_info_card(
            "Ingresos Mes",
            f"S/. {estadisticas['ingresos_mes']:.0f}",
            ft.Icons.MONETIZATION_ON,
            "#4CAF50"
        ),
        create_info_card(
            "Membresías Activas",
            str(estadisticas["membresías_activas"]),
            ft.Icons.CARD_MEMBERSHIP,
            "#2196F3"
        ),
        create_info_card(
            "Membresías Vencidas",
            str(estadisticas["membresías_vencidas"]),
            ft.Icons.WARNING,
            "#ef5350"
        ),
    ], spacing=15, scroll=ft.ScrollMode.AUTO, wrap=True)

    stats_section = ft.Container(
        content=ft.Column([
            ft.Text(
                "Estadísticas Generales",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            stats_row_1,
            ft.Container(height=10),
            stats_row_2,
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Ventas recientes
    ventas_container = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, height=250)

    for venta in ventas_recientes:
        ventas_container.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(
                            venta['producto'],
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),
                        ft.Text(
                            venta['cliente'],
                            size=11,
                            color=TEXT_SECONDARY
                        ),
                    ], spacing=2, expand=True),
                    ft.Column([
                        ft.Text(
                            f"S/. {venta['monto']:.2f}",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_COLOR,
                            text_align=ft.TextAlign.RIGHT
                        ),
                        ft.Text(
                            venta['fecha'],
                            size=10,
                            color=TEXT_SECONDARY,
                            text_align=ft.TextAlign.RIGHT
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=2),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=CARD_BG,
                border_radius=8,
                padding=12,
                border=ft.border.all(1, "#333333"),
                margin=ft.margin.only(bottom=5)
            )
        )

    ventas_section = ft.Container(
        content=ft.Column([
            ft.Text(
                "Ventas Recientes",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            ventas_container,
        ], spacing=10),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=True
    )

    # Top productos
    productos_container = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, height=250)

    for idx, producto in enumerate(productos_top, 1):
        # Calcular porcentaje para barra visual
        max_ingresos = max(p['ingresos'] for p in productos_top)
        porcentaje = (producto['ingresos'] / max_ingresos) * 100

        productos_container.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(
                                str(idx),
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY
                            ),
                            bgcolor=PRIMARY_COLOR if idx <= 3 else TEXT_SECONDARY,
                            border_radius=6,
                            width=30,
                            height=30,
                            alignment=ft.alignment.center
                        ),
                        ft.Column([
                            ft.Text(
                                producto['producto'],
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY
                            ),
                            ft.Text(
                                f"{producto['cantidad']} unidades vendidas",
                                size=11,
                                color=TEXT_SECONDARY
                            ),
                        ], spacing=2, expand=True),
                        ft.Text(
                            f"S/. {producto['ingresos']:.2f}",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_COLOR
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(
                        content=ft.Container(
                            bgcolor=PRIMARY_COLOR,
                            border_radius=4,
                            height=6,
                        ),
                        width=f"{porcentaje}%",
                        bgcolor=f"{PRIMARY_COLOR}22",
                        border_radius=4,
                        height=6,
                        margin=ft.margin.only(top=5)
                    ),
                ], spacing=5),
                bgcolor=CARD_BG,
                border_radius=8,
                padding=12,
                border=ft.border.all(1, "#333333"),
                margin=ft.margin.only(bottom=5)
            )
        )

    productos_section = ft.Container(
        content=ft.Column([
            ft.Text(
                "Productos Más Vendidos",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            productos_container,
        ], spacing=10),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=True
    )

    # Row con dos columnas para ventas y productos
    bottom_row = ft.Row([
        ventas_section,
        productos_section
    ], spacing=0, expand=True)

    # Botones de acción
    actions_row = ft.Row([
        ft.ElevatedButton(
            "Exportar a Excel",
            icon=ft.Icons.FILE_DOWNLOAD,
            bgcolor=PRIMARY_COLOR,
            color=ft.Colors.BLACK,
            on_click=lambda _: mostrar_mensaje("Exportación a Excel en desarrollo")
        ),
        ft.ElevatedButton(
            "Generar PDF",
            icon=ft.Icons.PICTURE_AS_PDF,
            bgcolor="#4CAF50",
            color=ft.Colors.BLACK,
            on_click=lambda _: mostrar_mensaje("Generación de PDF en desarrollo")
        ),
        ft.ElevatedButton(
            "Actualizar Datos",
            icon=ft.Icons.REFRESH,
            bgcolor="#2196F3",
            color=ft.Colors.BLACK,
            on_click=lambda _: mostrar_mensaje("Datos actualizados")
        ),
    ], spacing=15)

    actions_section = ft.Container(
        content=actions_row,
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    def mostrar_mensaje(mensaje):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=PRIMARY_COLOR
        )
        page.snack_bar.open = True
        page.update()

    # Layout principal
    main_content = ft.Column([
        header,
        stats_section,
        actions_section,
        bottom_row
    ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

    page.add(
        ft.Container(
            content=main_content,
            bgcolor=BACKGROUND_DARK,
            expand=True
        )
    )
