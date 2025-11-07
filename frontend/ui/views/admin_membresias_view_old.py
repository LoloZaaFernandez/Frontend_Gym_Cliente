"""
Vista de Administración de Membresías para Administradores
Permite crear, editar y gestionar membresías y precios
"""

import flet as ft
from datetime import datetime
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_admin_membresias_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de administración de membresías

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Gestión de Membresías"

    api = APIService()

    # Contenedor principal de membresías
    membresias_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def cargar_membresias():
        """Cargar todas las membresías desde el backend"""
        membresias_container.controls.clear()

        try:
            membresias = api.get_membresias()

            if not membresias:
                membresias_container.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "No hay membresías registradas",
                            color=TEXT_SECONDARY,
                            size=16
                        ),
                        padding=40,
                        alignment=ft.alignment.center
                    )
                )
            else:
                for membresia in membresias:
                    membresias_container.controls.append(
                        crear_membresia_card(membresia)
                    )
        except Exception as e:
            print(f"Error al cargar membresías: {e}")
            mostrar_mensaje("Error al cargar membresías", error=True)

        page.update()

    def crear_membresia_card(membresia):
        """Crear tarjeta de membresía para administración"""
        estado_color = "#4CAF50" if membresia['estado'] == "Activa" else "#ef5350"

        # Mapeo de tipos de membresía a información visual
        tipo_info = {
            "Dia": {"color": "#FF9800", "duracion": "1 día"},
            "Mensual": {"color": PRIMARY_COLOR, "duracion": "30 días"},
            "Trimestral": {"color": "#4CAF50", "duracion": "90 días"},
            "Semestral": {"color": "#2196F3", "duracion": "180 días"},
            "Anual": {"color": "#9C27B0", "duracion": "365 días"}
        }

        info = tipo_info.get(membresia['tipo_membresia'], {"color": PRIMARY_COLOR, "duracion": "N/A"})

        return ft.Container(
            content=ft.Row([
                # Información principal
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    membresia['tipo_membresia'],
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=info['color'],
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=5
                            ),
                            ft.Container(
                                content=ft.Text(
                                    membresia['estado'],
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=estado_color,
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=5
                            ),
                        ], spacing=10),
                        ft.Text(
                            membresia['nombre_membresia'],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),
                        ft.Text(
                            f"Duración: {info['duracion']}",
                            size=13,
                            color=TEXT_SECONDARY
                        ),
                        ft.Text(
                            f"ID: {membresia['id']}",
                            size=11,
                            color=TEXT_SECONDARY
                        ),
                    ], spacing=8),
                    expand=True
                ),
                # Botones de acción
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ATTACH_MONEY,
                        icon_color="#4CAF50",
                        tooltip="Gestionar Precios",
                        on_click=lambda _, m=membresia: gestionar_precios(m)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=PRIMARY_COLOR,
                        tooltip="Editar",
                        on_click=lambda _, m=membresia: editar_membresia(m)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.TOGGLE_ON if membresia['estado'] == "Activa" else ft.Icons.TOGGLE_OFF,
                        icon_color="#4CAF50" if membresia['estado'] == "Activa" else "#ef5350",
                        tooltip="Cambiar Estado",
                        on_click=lambda _, m=membresia: cambiar_estado(m)
                    ),
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=CARD_BG,
            border_radius=10,
            padding=15,
            border=ft.border.all(1, "#333333")
        )

    def crear_nueva_membresia():
        """Mostrar diálogo para crear nueva membresía"""
        nombre_field = ft.TextField(
            label="Nombre de Membresía",
            hint_text="Ej: Membresía Mensual Premium",
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR
        )

        tipo_dropdown = ft.Dropdown(
            label="Tipo de Membresía",
            options=[
                ft.dropdown.Option("Dia"),
                ft.dropdown.Option("Mensual"),
                ft.dropdown.Option("Trimestral"),
                ft.dropdown.Option("Semestral"),
                ft.dropdown.Option("Anual"),
            ],
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR
        )

        precio_field = ft.TextField(
            label="Precio",
            hint_text="0.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR
        )

        def guardar_membresia(e):
            if not nombre_field.value or not tipo_dropdown.value or not precio_field.value:
                mostrar_mensaje("Por favor completa todos los campos", error=True)
                return

            try:
                # Crear membresía usando el API service
                membresia_data = {
                    "nombre_membresia": nombre_field.value,
                    "tipo_membresia": tipo_dropdown.value,
                    "usuario_creacion": auth_service.get_current_user()['nombre']
                }

                nueva_membresia = api.crear_membresia(membresia_data)

                # Crear precio para la membresía
                precio_data = {
                    "id_membresia": nueva_membresia['id'],
                    "precio_actual": float(precio_field.value),
                    "usuario_creacion": auth_service.get_current_user()['nombre']
                }

                api.crear_precio_membresia(precio_data)

                dialog.open = False
                page.update()
                mostrar_mensaje("✓ Membresía creada exitosamente", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"Error: {str(ex)}", error=True)
            except Exception as ex:
                print(f"Error inesperado: {ex}")
                mostrar_mensaje(f"Error inesperado: {str(ex)}", error=True)

        def cerrar_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nueva Membresía", color=TEXT_PRIMARY),
            content=ft.Column([
                nombre_field,
                tipo_dropdown,
                precio_field,
                ft.Text(
                    "El precio se puede modificar posteriormente",
                    size=12,
                    color=TEXT_SECONDARY,
                    italic=True
                )
            ], tight=True, spacing=15, height=300),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.ElevatedButton(
                    "Crear",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=PRIMARY_COLOR
                    ),
                    on_click=guardar_membresia
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def editar_membresia(membresia):
        """Editar membresía existente"""
        nombre_field = ft.TextField(
            label="Nombre de Membresía",
            value=membresia['nombre_membresia'],
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR
        )

        def guardar_cambios(e):
            if not nombre_field.value:
                mostrar_mensaje("El nombre no puede estar vacío", error=True)
                return

            try:
                data = {
                    "nombre_membresia": nombre_field.value,
                    "tipo_membresia": membresia['tipo_membresia'],
                    "usuario_modificacion": auth_service.get_current_user()['nombre']
                }

                api.actualizar_membresia(membresia['id'], data)

                dialog.open = False
                page.update()
                mostrar_mensaje("✓ Membresía actualizada exitosamente", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"Error: {str(ex)}", error=True)
            except Exception as ex:
                print(f"Error inesperado: {ex}")
                mostrar_mensaje(f"Error inesperado: {str(ex)}", error=True)

        def cerrar_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Membresía", color=TEXT_PRIMARY),
            content=ft.Column([
                nombre_field,
                ft.Text(
                    f"Tipo: {membresia['tipo_membresia']} (no editable)",
                    size=13,
                    color=TEXT_SECONDARY
                )
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.ElevatedButton(
                    "Guardar",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=PRIMARY_COLOR
                    ),
                    on_click=guardar_cambios
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def gestionar_precios(membresia):
        """Gestionar precios de la membresía"""
        # Obtener precio actual
        try:
            precio_actual = api.get_precio_membresia(membresia['id'])
            precio_valor = precio_actual.get('precio_actual', 0.0) if precio_actual else 0.0
        except:
            precio_valor = 0.0

        precio_field = ft.TextField(
            label="Nuevo Precio",
            value=str(precio_valor),
            keyboard_type=ft.KeyboardType.NUMBER,
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=PRIMARY_COLOR,
            prefix_text="S/. "
        )

        def actualizar_precio(e):
            if not precio_field.value:
                mostrar_mensaje("El precio no puede estar vacío", error=True)
                return

            try:
                precio_data = {
                    "id_membresia": membresia['id'],
                    "precio_actual": float(precio_field.value),
                    "precio_anterior": precio_valor,
                    "usuario_creacion": auth_service.get_current_user()['nombre']
                }

                api.crear_precio_membresia(precio_data)

                dialog.open = False
                page.update()
                mostrar_mensaje("✓ Precio actualizado exitosamente", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"Error: {str(ex)}", error=True)
            except Exception as ex:
                print(f"Error inesperado: {ex}")
                mostrar_mensaje(f"Error inesperado: {str(ex)}", error=True)

        def cerrar_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Gestionar Precio - {membresia['nombre_membresia']}", color=TEXT_PRIMARY),
            content=ft.Column([
                ft.Text(
                    f"Precio actual: S/. {precio_valor:.2f}",
                    size=14,
                    color=TEXT_SECONDARY
                ),
                precio_field,
                ft.Text(
                    "El historial de precios se mantendrá",
                    size=12,
                    color=TEXT_SECONDARY,
                    italic=True
                )
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.ElevatedButton(
                    "Actualizar Precio",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor="#4CAF50"
                    ),
                    on_click=actualizar_precio
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def cambiar_estado(membresia):
        """Cambiar estado de la membresía (Activa/Inactiva)"""
        nuevo_estado = "Inactiva" if membresia['estado'] == "Activa" else "Activa"

        def confirmar_cambio(e):
            try:
                data = {
                    "nombre_membresia": membresia['nombre_membresia'],
                    "tipo_membresia": membresia['tipo_membresia'],
                    "estado": nuevo_estado,
                    "usuario_modificacion": auth_service.get_current_user()['nombre']
                }

                api.actualizar_membresia(membresia['id'], data)

                dialog.open = False
                page.update()
                mostrar_mensaje(f"✓ Membresía {nuevo_estado.lower()}", error=False)
                cargar_membresias()

            except ValueError as ex:
                mostrar_mensaje(f"Error: {str(ex)}", error=True)
            except Exception as ex:
                print(f"Error inesperado: {ex}")
                mostrar_mensaje(f"Error inesperado: {str(ex)}", error=True)

        def cerrar_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cambiar Estado", color=TEXT_PRIMARY),
            content=ft.Text(
                f"¿Deseas cambiar el estado de '{membresia['nombre_membresia']}' a {nuevo_estado}?",
                color=TEXT_SECONDARY
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.ElevatedButton(
                    "Confirmar",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=PRIMARY_COLOR
                    ),
                    on_click=confirmar_cambio
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def mostrar_mensaje(mensaje, error=False):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#ef5350" if error else "#4CAF50",
            duration=3000
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
                    ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=32, color=PRIMARY_COLOR),
                    ft.Text("Gestión de Membresías", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ], spacing=10),
                ft.Row([
                    ft.ElevatedButton(
                        "Nueva Membresía",
                        icon=ft.Icons.ADD,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=PRIMARY_COLOR
                        ),
                        on_click=lambda _: crear_nueva_membresia(),
                        height=40
                    ),
                    ft.ElevatedButton(
                        "Actualizar",
                        icon=ft.Icons.REFRESH,
                        style=ft.ButtonStyle(
                            color=PRIMARY_COLOR,
                            bgcolor=ft.Colors.TRANSPARENT,
                            side=ft.border.all(1, PRIMARY_COLOR)
                        ),
                        on_click=lambda _: cargar_membresias(),
                        height=40
                    )
                ], spacing=10)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Layout principal
    main_content = ft.Column(
        controls=[
            header,
            ft.Container(
                content=membresias_container,
                padding=20,
                expand=True
            ),
        ],
        spacing=0,
        expand=True
    )

    page.add(
        ft.Container(
            content=main_content,
            bgcolor=BACKGROUND_DARK,
            expand=True
        )
    )

    # Cargar datos iniciales
    cargar_membresias()
