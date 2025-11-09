"""
Vista de Gestión de Membresías para Administrador - Refactorizado con Sistema de Componentes
REFACTOR: Uso de MembershipCard unificado para diseño consistente con vista de cliente
"""

import flet as ft
from datetime import datetime
from config.theme import Theme
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, TEXT_PRIMARY, CARD_BG, BACKGROUND_DARK
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.organisms import MembershipCard


def show_admin_membresias_view(page: ft.Page, auth_service, on_section_click, current_section):
    """Vista mejorada de gestión de membresías con diseño PREMIUM unificado"""
    page.clean()
    page.title = "BLESSED GYM - Gestión de Membresías"
    page.padding = 0
    page.spacing = 0

    api = APIService()

    # Contenedor de membresías
    membresias_container = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.START
    )

    def cargar_membresias():
        """Cargar todas las membresías con sus precios"""
        membresias_container.controls.clear()

        try:
            membresias = api.get_membresias()  # Todas las membresías (activas e inactivas)

            if not membresias:
                membresias_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INBOX, size=80, color="#333333"),
                            ft.Text("No hay membresías registradas", color=TEXT_SECONDARY, size=16),
                            ft.Text("Crea tu primera membresía", color="#666666", size=14),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        padding=40,
                        alignment=ft.alignment.center
                    )
                )
            else:
                for membresia in membresias:
                    # Obtener precio actual
                    precio_actual = 0.0
                    try:
                        precio_data = api.get_precio_membresia(membresia['id'])
                        if precio_data and precio_data.get('precio_actual'):
                            precio_actual = float(precio_data['precio_actual'])
                    except:
                        pass

                    # Usar componente unificado MembershipCard en modo admin
                    card = MembershipCard.create(
                        membresia=membresia,
                        precio_actual=precio_actual,
                        mode="admin",
                        on_edit_click=lambda e, m=membresia: editar_membresia(m),
                        on_price_click=lambda e, m=membresia: gestionar_precio(m),
                        on_status_click=lambda e, m=membresia: cambiar_estado(m)
                    )
                    membresias_container.controls.append(card)

        except Exception as e:
            print(f"Error al cargar membresías: {e}")
            mostrar_mensaje("Error al cargar membresías", error=True)

        page.update()

    def crear_nueva_membresia():
        """Diálogo para crear nueva membresía"""
        nombre_field = ft.TextField(
            label="Nombre de la Membresía",
            hint_text="Ej: Membresía Premium Mensual",
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR,
            width=350
        )

        tipo_dropdown = ft.Dropdown(
            label="Tipo de Membresía",
            options=[
                ft.dropdown.Option("Dia", "Diaria (1 día)"),
                ft.dropdown.Option("Mensual", "Mensual (30 días)"),
                ft.dropdown.Option("Trimestral", "Trimestral (90 días)"),
                ft.dropdown.Option("Semestral", "Semestral (180 días)"),
                ft.dropdown.Option("Anual", "Anual (365 días)"),
            ],
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR,
            width=350
        )

        precio_field = ft.TextField(
            label="Precio (S/.)",
            hint_text="150.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR,
            prefix_text="S/. ",
            width=350
        )

        def guardar(e):
            # Validaciones
            if not nombre_field.value or not tipo_dropdown.value or not precio_field.value:
                mostrar_mensaje("⚠ Por favor completa todos los campos", error=True)
                return

            try:
                precio = float(precio_field.value)
                if precio <= 0:
                    mostrar_mensaje("⚠ El precio debe ser mayor a 0", error=True)
                    return

                # Crear membresía
                membresia_data = {
                    "nombre_membresia": nombre_field.value,
                    "tipo_membresia": tipo_dropdown.value,
                    "usuario_creacion": auth_service.get_current_user()['nombre']
                }

                nueva_membresia = api.crear_membresia(membresia_data)

                # Crear precio
                precio_data = {
                    "id_membresia": nueva_membresia['id'],
                    "precio_actual": precio,
                    "usuario_creacion": auth_service.get_current_user()['nombre']
                }

                api.crear_precio_membresia(precio_data)

                page.close(dialog)
                mostrar_mensaje(f"✓ Membresía '{nombre_field.value}' creada exitosamente", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"✗ Error: {str(ex)}", error=True)
            except Exception as ex:
                print(f"Error inesperado: {ex}")
                mostrar_mensaje(f"✗ Error: {str(ex)}", error=True)

        def cerrar(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ADD_CIRCLE, color=PRIMARY_COLOR),
                ft.Text("Nueva Membresía", color=TEXT_PRIMARY)
            ], spacing=10),
            content=ft.Column([
                nombre_field,
                tipo_dropdown,
                precio_field,
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color="#2196F3"),
                        ft.Text(
                           "El precio se puede modificar después",
                            size=12,
                            color=TEXT_SECONDARY,
                            italic=True
                        ),
                    ], spacing=5),
                    margin=ft.margin.only(top=10)
                )
            ], tight=True, spacing=15, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.ElevatedButton(
                    "Crear Membresía",
                    icon=ft.Icons.CHECK,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=PRIMARY_COLOR),
                    on_click=guardar
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)

    def editar_membresia(membresia):
        """Diálogo para editar membresía"""
        nombre_field = ft.TextField(
            label="Nombre de la Membresía",
            value=membresia['nombre_membresia'],
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR,
            width=350
        )

        def guardar(e):
            if not nombre_field.value:
                mostrar_mensaje("⚠ El nombre no puede estar vacío", error=True)
                return

            try:
                data = {
                    "nombre_membresia": nombre_field.value,
                    "tipo_membresia": membresia['tipo_membresia'],
                    "usuario_modificacion": auth_service.get_current_user()['nombre']
                }

                api.actualizar_membresia(membresia['id'], data)

                page.close(dialog)
                mostrar_mensaje(f"✓ Membresía actualizada", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"❌ Error: {str(ex)}", error=True)
            except Exception as ex:
                mostrar_mensaje(f"❌ Error: {str(ex)}", error=True)
        def cerrar(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.EDIT, color=PRIMARY_COLOR),
                ft.Text(f"Editar: {membresia['nombre_membresia']}", color=TEXT_PRIMARY)
            ], spacing=10),
            content=ft.Column([
                nombre_field,
                ft.Text(
                    f"Tipo: {membresia['tipo_membresia']} (no se puede cambiar)",
                    size=13,
                    color=TEXT_SECONDARY
                )
            ], tight=True, spacing=15, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.ElevatedButton(
                    "Guardar",
                    icon=ft.Icons.CHECK,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=PRIMARY_COLOR),
                    on_click=guardar
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)

    def gestionar_precio(membresia):
        """Diálogo para gestionar precio"""
        # Obtener precio actual
        try:
            precio_data = api.get_precio_membresia(membresia['id'])
            precio_actual = float(precio_data.get('precio_actual', 0.0)) if precio_data else 0.0
        except:
            precio_actual = 0.0

        precio_field = ft.TextField(
            label="Nuevo Precio (S/.)",
            value=str(precio_actual),
            keyboard_type=ft.KeyboardType.NUMBER,
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR,
            prefix_text="S/. ",
            width=350
        )

        def guardar(e):
            if not precio_field.value:
                mostrar_mensaje("⚠ El precio no puede estar vacío", error=True)
                return

            try:
                nuevo_precio = float(precio_field.value)
                if nuevo_precio <= 0:
                    mostrar_mensaje("⚠ El precio debe ser mayor a 0", error=True)
                    return

                precio_data = {
                    "id_membresia": membresia['id'],
                    "precio_actual": nuevo_precio,
                    "precio_anterior": precio_actual,
                    "usuario_creacion": auth_service.get_current_user()['nombre']
                }

                api.crear_precio_membresia(precio_data)

                page.close(dialog)
                mostrar_mensaje(f"✓ Precio actualizado a S/. {nuevo_precio:.2f}", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"❌ Error: {str(ex)}", error=True)
            except Exception as ex:
                mostrar_mensaje(f"❌ Error: {str(ex)}", error=True)
        def cerrar(e):
            page.close(dialog)
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ATTACH_MONEY, color="#4CAF50"),
                ft.Text(f"Precio: {membresia['nombre_membresia']}", color=TEXT_PRIMARY)
            ], spacing=10),
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Precio Actual", size=12, color=TEXT_SECONDARY),
                        ft.Text(f"S/. {precio_actual:.2f}", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=10,
                    bgcolor="#1A1A1A",
                    border_radius=8,
                    border=ft.border.all(1, "#333333")
                ),
                precio_field,
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.HISTORY, size=16, color="#2196F3"),
                        ft.Text(
                            "Se mantendrá el historial de precios",
                            size=12,
                            color=TEXT_SECONDARY,
                            italic=True
                        ),
                    ], spacing=5),
                    margin=ft.margin.only(top=5)
                )
            ], tight=True, spacing=15, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.ElevatedButton(
                    "Actualizar Precio",
                    icon=ft.Icons.CHECK,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor="#4CAF50"),
                    on_click=guardar
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)

    def cambiar_estado(membresia):
        """Cambiar estado de la membresía"""
        nuevo_estado = "Inactiva" if membresia['estado'] == "Activa" else "Activa"
        accion = "desactivar" if nuevo_estado == "Inactiva" else "activar"

        def confirmar(e):
            try:
                data = {
                    "nombre_membresia": membresia['nombre_membresia'],
                    "tipo_membresia": membresia['tipo_membresia'],
                    "estado": nuevo_estado,
                    "usuario_modificacion": auth_service.get_current_user()['nombre']
                }

                api.actualizar_membresia(membresia['id'], data)

                page.close(dialog)
                mostrar_mensaje(f"✓ Membresía {accion}da correctamente", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"✗ Error: {str(ex)}", error=True)
            except Exception as ex:
                mostrar_mensaje(f"✗ Error: {str(ex)}", error=True)

        def cerrar(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.TOGGLE_ON if nuevo_estado == "Activa" else ft.Icons.TOGGLE_OFF,
                    color="#4CAF50" if nuevo_estado == "Activa" else "#ef5350"),
                ft.Text(f"{accion.capitalize()} Membresía", color=TEXT_PRIMARY)
            ], spacing=10),
            content=ft.Column([
                ft.Text(
                    f"¿Estás seguro de {accion} la membresía '{membresia['nombre_membresia']}'?",
                    color=TEXT_SECONDARY
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color="#2196F3"),
                        ft.Text(
                            "Las membresías inactivas no aparecen para los clientes",
                            size=12,
                            color=TEXT_SECONDARY,
                            italic=True
                        ),
                    ], spacing=5),
                    margin=ft.margin.only(top=10)
                ) if nuevo_estado == "Inactiva" else ft.Container()
            ], tight=True, spacing=10, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.ElevatedButton(
                    accion.capitalize(),
                    icon=ft.Icons.CHECK,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor="#4CAF50" if nuevo_estado == "Activa" else "#ef5350"
                    ),
                    on_click=confirmar
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)

    def mostrar_mensaje(mensaje, error=False):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#ef5350" if error else "#4CAF50",
            duration=3000
        )
        page.snack_bar.open = True
        page.update()

    # Obtener usuario actual
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Header con acciones
    header = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=32, color=Theme.PRIMARY),
                ft.Text("Gestión de Membresías", size=Theme.FONT_SIZE["2xl"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ], spacing=Theme.SPACING["md"]),
            ft.Row([
                ft.ElevatedButton(
                    "Nueva Membresía",
                    icon=ft.Icons.ADD_CIRCLE,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=Theme.PRIMARY,
                        shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["md"])
                    ),
                    on_click=lambda _: crear_nueva_membresia(),
                    height=45
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    icon_color=Theme.PRIMARY,
                    icon_size=28,
                    on_click=lambda _: cargar_membresias(),
                    tooltip="Actualizar"
                ),
            ], spacing=Theme.SPACING["md"])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=Theme.SPACING["xl"],
        bgcolor=Theme.CARD_BG,
        border_radius=Theme.RADIUS["lg"],
        border=ft.border.all(1, Theme.BORDER_DEFAULT)
    )

    # Contenido principal
    content = ft.Column([
        header,
        ft.Container(
            content=membresias_container,
            padding=Theme.SPACING["md"],
            expand=True
        ),
    ], spacing=Theme.SPACING["lg"], scroll=ft.ScrollMode.AUTO, expand=True)

    # Usar base_layout para mantener sidebar consistente
    create_base_layout(
        page=page,
        role="admin",
        current_section=current_section,
        on_section_click=on_section_click,
        content=ft.Container(content=content, padding=Theme.SPACING["xl"]),
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )

    # Cargar datos iniciales
    cargar_membresias()
