"""
Vista de Perfil de Cliente - CORREGIDA
Incluye redirección correcta del botón "Renovar Membresía"
"""

import flet as ft
from datetime import datetime
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK


def show_perfil_cliente_view(page: ft.Page, auth_service, on_back, on_navigate_membresias=None):
    """
    Mostrar vista de perfil del cliente - CORREGIDA

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
        on_navigate_membresias: ✅ NUEVO - Callback para ir a membresías
    """
    page.clean()
    page.title = "BLESSED GYM - Mi Perfil"

    cliente = auth_service.get_current_user()

    # Datos simulados adicionales (integrar con DB real)
    datos_adicionales = {
        "fecha_registro": "15/01/2024",
        "fecha_ultima_asistencia": "05/11/2025",
        "total_asistencias": 87,
        "racha_dias": 5,
        "membresia_tipo": "Mensual",
        "membresia_vencimiento": "30/11/2025",
        "membresia_estado": "Activa"
    }

    def crear_campo_info(label, valor, icon):
        """Crear campo de información"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20, color=PRIMARY_COLOR),
                ft.Text(f"{label}:", size=13, color=TEXT_SECONDARY, width=150),
                ft.Text(valor, size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
            ], spacing=10),
            padding=10,
            bgcolor=f"{CARD_BG}",
            border_radius=8,
            border=ft.border.all(1, "#333333")
        )

    def crear_stat_card(titulo, valor, icon, color):
        """Crear tarjeta de estadística"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(valor, size=24, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(titulo, size=12, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor=f"{color}11",
            border_radius=12,
            padding=20,
            border=ft.border.all(1, color),
            width=200,
            height=150
        )

    def mostrar_mensaje(mensaje):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(content=ft.Text(mensaje), bgcolor=PRIMARY_COLOR)
        page.snack_bar.open = True
        page.update()

    # ✅ FUNCIÓN CORREGIDA: Redirigir a membresías
    def ir_a_membresias(e):
        """Navegar a la vista de membresías"""
        if on_navigate_membresias:
            on_navigate_membresias()  
        else:
            mostrar_mensaje("⚠ Función de navegación no disponible")

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=PRIMARY_COLOR, on_click=lambda _: on_back()),
            ft.Text("Mi Perfil - BLESSED GYM", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
        ]),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Foto de perfil y nombre
    profile_header = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=PRIMARY_COLOR),
                bgcolor=f"{PRIMARY_COLOR}22",
                border_radius=60,
                width=120,
                height=120,
                alignment=ft.alignment.center
            ),
            ft.Text(
                f"{cliente['nombre']} {cliente['apellidos']}",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(
                content=ft.Text("MIEMBRO ACTIVO", size=12, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                bgcolor=PRIMARY_COLOR,
                padding=ft.padding.symmetric(horizontal=15, vertical=5),
                border_radius=12
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        padding=30,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Información personal
    info_personal = ft.Container(
        content=ft.Column([
            ft.Text("Información Personal", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Divider(height=1, color="#333333"),
            crear_campo_info("DNI", cliente['dni'], ft.Icons.BADGE),
            crear_campo_info("Correo Electrónico", cliente['correo'], ft.Icons.EMAIL),
            crear_campo_info("Teléfono", cliente.get('telefono', 'No registrado'), ft.Icons.PHONE),
            crear_campo_info("Fecha de Registro", datos_adicionales['fecha_registro'], ft.Icons.CALENDAR_TODAY),
            crear_campo_info("Última Asistencia", datos_adicionales['fecha_ultima_asistencia'], ft.Icons.ACCESS_TIME),
        ], spacing=12),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=True
    )

    # Estadísticas de actividad
    stats_actividad = ft.Container(
        content=ft.Column([
            ft.Text("Mi Actividad", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Divider(height=1, color="#333333"),
            ft.Row([
                crear_stat_card("Total Asistencias", str(datos_adicionales['total_asistencias']), ft.Icons.FITNESS_CENTER, PRIMARY_COLOR),
                crear_stat_card("Racha Actual", f"{datos_adicionales['racha_dias']} días", ft.Icons.LOCAL_FIRE_DEPARTMENT, "#FF6F00"),
            ], spacing=15, wrap=True),
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=True
    )

    # Información de membresía
    estado_color = PRIMARY_COLOR if datos_adicionales['membresia_estado'] == "Activa" else "#ef5350"

    info_membresia = ft.Container(
        content=ft.Column([
            ft.Text("Mi Membresía", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ft.Divider(height=1, color="#333333"),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=50, color=PRIMARY_COLOR),
                    ft.Column([
                        ft.Text(
                            f"Membresía {datos_adicionales['membresia_tipo']}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),
                        ft.Text(f"Vence: {datos_adicionales['membresia_vencimiento']}", size=14, color=TEXT_SECONDARY),
                        ft.Container(
                            content=ft.Text(datos_adicionales['membresia_estado'], size=12, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                            bgcolor=estado_color,
                            padding=ft.padding.symmetric(horizontal=12, vertical=4),
                            border_radius=6,
                            margin=ft.margin.only(top=5)
                        ),
                    ], spacing=5, expand=True),
                ], spacing=20),
                bgcolor=f"{PRIMARY_COLOR}11",
                border_radius=12,
                padding=20,
                border=ft.border.all(1, PRIMARY_COLOR)
            ),
            ft.Container(height=10),
            # ✅ BOTÓN CORREGIDO: Ahora redirige correctamente
            ft.ElevatedButton(
                "Renovar Membresía",
                icon=ft.Icons.AUTORENEW,
                bgcolor=PRIMARY_COLOR,
                color=ft.Colors.BLACK,
                width=300,
                height=45,
                on_click=ir_a_membresias  # ✅ Usar la función de redirección
            ),
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Layout con dos columnas
    left_column = ft.Column([profile_header, info_membresia], spacing=0, expand=True)
    right_column = ft.Column([info_personal, stats_actividad], spacing=0, expand=True)
    content_row = ft.Row([left_column, right_column], spacing=0, expand=True)

    # Layout principal
    main_content = ft.Column([header, content_row], spacing=0, expand=True)

    page.add(ft.Container(content=main_content, bgcolor=BACKGROUND_DARK, expand=True))