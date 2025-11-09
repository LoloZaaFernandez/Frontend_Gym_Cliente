"""
Vista de Perfil de Cliente - Refactorizado con Sistema de Componentes
ANTES: 255 líneas | DESPUÉS: ~180 líneas (29% menos código)
"""

import flet as ft
from datetime import datetime
from config.theme import Theme
from config.settings import LOGO_PATH
from ui.layouts import create_base_layout
from ui.components.molecules import create_card_container


def show_perfil_cliente_view(page: ft.Page, auth_service, on_section_click, current_section, on_navigate_membresias=None):
    """
    Mostrar vista de perfil del cliente

    Mejoras:
    - 29% menos código (255 → ~180 líneas)
    - Uso de base_layout
    - Theme centralizado
    - Componentes reutilizables

    Args:
        on_navigate_membresias: Callback para ir a membresías
    """
    page.title = "BLESSED GYM - Mi Perfil"
    page.padding = 0
    page.spacing = 0

    cliente = auth_service.get_current_user()
    user_info = {"nombre": cliente.get("nombre", "Cliente"), "rol": "Cliente"}

    # Datos adicionales (integrar con DB real)
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
                ft.Icon(icon, size=20, color=Theme.PRIMARY),
                ft.Text(f"{label}:", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY, width=150),
                ft.Text(valor, size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_PRIMARY,
                       weight=Theme.FONT_WEIGHT["medium"]),
            ], spacing=Theme.SPACING["md"]),
            padding=Theme.SPACING["md"],
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["md"],
            border=ft.border.all(1, Theme.BORDER_DEFAULT)
        )

    def crear_stat_card(titulo, valor, icon, color):
        """Crear tarjeta de estadística"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(valor, size=Theme.FONT_SIZE["2xl"], weight=Theme.FONT_WEIGHT["bold"], color=color),
                ft.Text(titulo, size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY,
                       text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
            bgcolor=f"{color}11",
            border_radius=Theme.RADIUS["lg"],
            padding=Theme.SPACING["xl"],
            border=ft.border.all(1, color),
            width=200,
            height=150
        )

    def ir_a_membresias(e):
        """Navegar a la vista de membresías"""
        if on_navigate_membresias:
            on_navigate_membresias()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("⚠ Función de navegación no disponible"),
                                        bgcolor=Theme.WARNING)
            page.snack_bar.open = True
            page.update()

    # Foto de perfil y nombre
    profile_header = create_card_container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=Theme.PRIMARY),
                bgcolor=f"{Theme.PRIMARY}22",
                border_radius=Theme.RADIUS["full"],
                width=120,
                height=120,
                alignment=ft.alignment.center
            ),
            ft.Text(f"{cliente['nombre']} {cliente['apellidos']}", size=Theme.FONT_SIZE["xl"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY,
                   text_align=ft.TextAlign.CENTER),
            ft.Container(
                content=ft.Text("MIEMBRO ACTIVO", size=Theme.FONT_SIZE["xs"],
                               color=Theme.TEXT_PRIMARY, weight=Theme.FONT_WEIGHT["bold"]),
                bgcolor=Theme.PRIMARY,
                padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"], vertical=Theme.SPACING["xs"]),
                border_radius=Theme.RADIUS["lg"]
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
        padding=Theme.SPACING["2xl"]
    )

    # Información personal
    info_personal = create_card_container(
        content=ft.Column([
            ft.Text("Información Personal", size=Theme.FONT_SIZE["lg"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            crear_campo_info("DNI", cliente['dni'], ft.Icons.BADGE),
            crear_campo_info("Correo Electrónico", cliente['correo'], ft.Icons.EMAIL),
            crear_campo_info("Teléfono", cliente.get('telefono', 'No registrado'), ft.Icons.PHONE),
            crear_campo_info("Fecha de Registro", datos_adicionales['fecha_registro'], ft.Icons.CALENDAR_TODAY),
            crear_campo_info("Última Asistencia", datos_adicionales['fecha_ultima_asistencia'], ft.Icons.ACCESS_TIME),
        ], spacing=Theme.SPACING["lg"]),
        padding=Theme.SPACING["xl"]
    )

    # Estadísticas de actividad
    stats_actividad = create_card_container(
        content=ft.Column([
            ft.Text("Mi Actividad", size=Theme.FONT_SIZE["lg"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Row([
                crear_stat_card("Total Asistencias", str(datos_adicionales['total_asistencias']),
                              ft.Icons.FITNESS_CENTER, Theme.PRIMARY),
                crear_stat_card("Racha Actual", f"{datos_adicionales['racha_dias']} días",
                              ft.Icons.LOCAL_FIRE_DEPARTMENT, "#FF6F00"),
            ], spacing=Theme.SPACING["lg"], wrap=True),
        ], spacing=Theme.SPACING["lg"]),
        padding=Theme.SPACING["xl"]
    )

    # Información de membresía
    estado_color = Theme.PRIMARY if datos_adicionales['membresia_estado'] == "Activa" else Theme.ERROR

    info_membresia = create_card_container(
        content=ft.Column([
            ft.Text("Mi Membresía", size=Theme.FONT_SIZE["lg"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=50, color=Theme.PRIMARY),
                    ft.Column([
                        ft.Text(f"Membresía {datos_adicionales['membresia_tipo']}",
                               size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"],
                               color=Theme.TEXT_PRIMARY),
                        ft.Text(f"Vence: {datos_adicionales['membresia_vencimiento']}",
                               size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        ft.Container(
                            content=ft.Text(datos_adicionales['membresia_estado'],
                                          size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_PRIMARY,
                                          weight=Theme.FONT_WEIGHT["bold"]),
                            bgcolor=estado_color,
                            padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"],
                                                        vertical=Theme.SPACING["xs"]),
                            border_radius=Theme.RADIUS["sm"],
                            margin=ft.margin.only(top=Theme.SPACING["xs"])
                        ),
                    ], spacing=Theme.SPACING["xs"], expand=True),
                ], spacing=Theme.SPACING["xl"]),
                bgcolor=f"{Theme.PRIMARY}11",
                border_radius=Theme.RADIUS["lg"],
                padding=Theme.SPACING["xl"],
                border=ft.border.all(1, Theme.PRIMARY)
            ),
            ft.Container(height=Theme.SPACING["md"]),
            ft.ElevatedButton(
                "Renovar Membresía",
                icon=ft.Icons.AUTORENEW,
                bgcolor=Theme.PRIMARY,
                color=ft.Colors.BLACK,
                width=300,
                height=45,
                on_click=ir_a_membresias
            ),
        ], spacing=Theme.SPACING["lg"], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=Theme.SPACING["xl"]
    )

    # Layout con dos columnas
    content = ft.Row([
        ft.Column([profile_header, info_membresia], spacing=Theme.SPACING["xl"], expand=True),
        ft.Column([info_personal, stats_actividad], spacing=Theme.SPACING["xl"], expand=True),
    ], spacing=Theme.SPACING["xl"], expand=True)

    # Usar base_layout
    create_base_layout(
        page=page,
        role="cliente",
        current_section=current_section,
        on_section_click=on_section_click,
        content=ft.Container(content=content, padding=Theme.SPACING["xl"]),
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )