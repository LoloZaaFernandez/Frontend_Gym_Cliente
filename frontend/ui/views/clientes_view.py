"""
Vista de Gestión de Clientes (CRUD completo) - Conectada con API
"""

import flet as ft
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_clientes_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de gestión de clientes

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Gestión de Clientes"

    api = APIService()

    # Variables de estado
    clientes_list = []
    selected_cliente = None

    # Campos de formulario
    dni_field = ft.TextField(
        label="DNI",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=200
    )
    nombre_field = ft.TextField(
        label="Nombre",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=200
    )
    apellidos_field = ft.TextField(
        label="Apellidos",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=250
    )
    correo_field = ft.TextField(
        label="Correo",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=300
    )
    telefono_field = ft.TextField(
        label="Teléfono",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=200
    )

    # Lista de clientes
    clientes_container = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, height=400)

    def load_clientes():
        """Cargar todos los clientes"""
        nonlocal clientes_list
        try:
            clientes_list = api.get_clientes()
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            # Fallback a DB local
            from database.db_manager import DatabaseManager
            db = DatabaseManager()
            clientes_list = db.get_todos_clientes()

        clientes_container.controls.clear()

        if not clientes_list:
            clientes_container.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay clientes registrados",
                        color=TEXT_SECONDARY,
                        size=14
                    ),
                    padding=20,
                    alignment=ft.alignment.center
                )
            )
        else:
            for cliente in clientes_list:
                clientes_container.controls.append(
                    create_cliente_card(cliente)
                )
        page.update()

    def create_cliente_card(cliente):
        """Crear tarjeta de cliente"""
        # El backend devuelve 'estado' como 'Activo'/'Inactivo', no un booleano 'activo'
        estado_text = cliente.get('estado', 'Activo')
        estado_color = PRIMARY_COLOR if estado_text == 'Activo' else TEXT_SECONDARY

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, size=30, color=PRIMARY_COLOR),
                        bgcolor=f"{PRIMARY_COLOR}22",
                        border_radius=8,
                        padding=8
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"{cliente['nombre']} {cliente['apellidos']}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY
                            ),
                            ft.Text(
                                f"DNI: {cliente['dni']} | {cliente['correo']}",
                                size=12,
                                color=TEXT_SECONDARY
                            ),
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Text(
                            estado_text,
                            size=11,
                            color=estado_color,
                            weight=ft.FontWeight.BOLD
                        ),
                        bgcolor=f"{estado_color}22",
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=6
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=PRIMARY_COLOR,
                                icon_size=20,
                                tooltip="Editar",
                                on_click=lambda _, c=cliente: edit_cliente(c)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="#ef5350",
                                icon_size=20,
                                tooltip="Eliminar",
                                on_click=lambda _, c=cliente: confirm_delete_cliente(c)
                            ),
                        ],
                        spacing=2
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor=CARD_BG,
            border_radius=8,
            padding=15,
            border=ft.border.all(1, "#333333"),
            margin=ft.margin.only(bottom=8)
        )

    def clear_form():
        """Limpiar formulario"""
        nonlocal selected_cliente
        selected_cliente = None
        dni_field.value = ""
        nombre_field.value = ""
        apellidos_field.value = ""
        correo_field.value = ""
        telefono_field.value = ""
        dni_field.disabled = False
        save_button.text = "Guardar Cliente"
        page.update()

    def save_cliente(e):
        """Guardar o actualizar cliente"""
        if not all([dni_field.value, nombre_field.value, apellidos_field.value, correo_field.value]):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor complete todos los campos obligatorios"),
                bgcolor="#ef5350"
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            if selected_cliente:
                # Actualizar
                api.actualizar_cliente(
                    selected_cliente['id'],
                    {
                        "nombre": nombre_field.value,
                        "apellidos": apellidos_field.value,
                        "correo": correo_field.value,
                        "telefono": telefono_field.value
                    }
                )
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Cliente actualizado exitosamente"),
                    bgcolor=PRIMARY_COLOR
                )
            else:
                # Crear nuevo
                api.crear_cliente({
                    "dni": dni_field.value,
                    "nombre": nombre_field.value,
                    "apellidos": apellidos_field.value,
                    "correo": correo_field.value,
                    "telefono": telefono_field.value,
                    "usuario_creacion": auth_service.get_current_user().get('usuario', 'admin')
                })
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Cliente creado exitosamente"),
                    bgcolor=PRIMARY_COLOR
                )
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(e)}"),
                bgcolor="#ef5350"
            )

        page.snack_bar.open = True
        clear_form()
        load_clientes()

    def edit_cliente(cliente):
        """Editar cliente"""
        nonlocal selected_cliente
        selected_cliente = cliente
        dni_field.value = cliente['dni']
        dni_field.disabled = True
        nombre_field.value = cliente['nombre']
        apellidos_field.value = cliente['apellidos']
        correo_field.value = cliente['correo']
        telefono_field.value = cliente['telefono'] or ""
        save_button.text = "Actualizar Cliente"
        page.update()

    def confirm_delete_cliente(cliente):
        """Confirmar eliminación de cliente"""
        def close_dialog(e):
            dialog.open = False
            page.update()

        def delete_confirmed(e):
            try:
                api.eliminar_cliente(cliente['id'])
                dialog.open = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Cliente eliminado exitosamente"),
                    bgcolor=PRIMARY_COLOR
                )
                page.snack_bar.open = True
                load_clientes()
            except Exception as error:
                dialog.open = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error al eliminar: {str(error)}"),
                    bgcolor="#ef5350"
                )
                page.snack_bar.open = True
                page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación", color=TEXT_PRIMARY),
            content=ft.Text(
                f"¿Está seguro de eliminar a {cliente['nombre']} {cliente['apellidos']}?",
                color=TEXT_SECONDARY
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color="#ef5350"),
                    on_click=delete_confirmed
                ),
            ],
            bgcolor=CARD_BG,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=PRIMARY_COLOR,
                on_click=lambda _: on_back()
            ),
            ft.Text(
                "Gestión de Clientes - BLESSED GYM",
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

    # Botón guardar
    save_button = ft.ElevatedButton(
        text="Guardar Cliente",
        icon=ft.Icons.SAVE,
        bgcolor=PRIMARY_COLOR,
        color=ft.Colors.BLACK,
        on_click=save_cliente,
        height=45
    )

    # Formulario
    form_card = ft.Container(
        content=ft.Column([
            ft.Text(
                "Formulario de Cliente",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            ft.Row([dni_field, nombre_field, apellidos_field], spacing=15, wrap=True),
            ft.Row([correo_field, telefono_field], spacing=15, wrap=True),
            ft.Row([
                save_button,
                ft.TextButton(
                    "Cancelar",
                    icon=ft.Icons.CANCEL,
                    style=ft.ButtonStyle(color=TEXT_SECONDARY),
                    on_click=lambda _: clear_form()
                ),
            ], spacing=10),
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=ft.margin.only(left=10, right=10, bottom=10),
        border=ft.border.all(1, "#333333")
    )

    # Lista de clientes
    list_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(
                    "Lista de Clientes",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=PRIMARY_COLOR,
                    expand=True
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    icon_color=PRIMARY_COLOR,
                    tooltip="Recargar",
                    on_click=lambda _: load_clientes()
                ),
            ]),
            ft.Divider(height=1, color="#333333"),
            clientes_container,
        ], spacing=10),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=True
    )

    # Layout principal
    main_content = ft.Column([
        header,
        form_card,
        list_card
    ], spacing=0, expand=True)

    page.add(
        ft.Container(
            content=main_content,
            bgcolor=BACKGROUND_DARK,
            expand=True
        )
    )

    # Cargar clientes al inicio
    load_clientes()
