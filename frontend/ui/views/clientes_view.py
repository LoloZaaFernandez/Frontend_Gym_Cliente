"""
Vista de Gestión de Clientes (CRUD completo) - CORREGIDA
Con validaciones completas y gestión de estados
"""

import flet as ft
import re
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_clientes_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de gestión de clientes - CORREGIDA
    """
    page.clean()
    page.title = "BLESSED GYM - Gestión de Clientes"

    api = APIService()

    # Variables de estado
    clientes_list = []
    selected_cliente = None

    #  VALIDACIONES DE CAMPOS
    def validar_solo_numeros(e):
        """Solo permitir números"""
        if e.control.value:
            e.control.value = ''.join(filter(str.isdigit, e.control.value))
            e.control.update()

    def validar_solo_letras(e):
        """Solo permitir letras, espacios y tildes"""
        if e.control.value:
            # Permitir letras, espacios, tildes y ñ
            e.control.value = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', e.control.value)
            e.control.update()

    def validar_telefono(e):
        """Solo permitir números y símbolos de teléfono"""
        if e.control.value:
            # Permitir números, +, -, (, ), espacios
            e.control.value = re.sub(r'[^0-9+\-() ]', '', e.control.value)
            e.control.update()

    #  CAMPOS DE FORMULARIO CON VALIDACIONES
    dni_field = ft.TextField(
        label="DNI *",
        hint_text="8 dígitos",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=200,
        max_length=8,
        counter_text="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=validar_solo_numeros,
        prefix_icon=ft.Icons.BADGE
    )

    nombre_field = ft.TextField(
        label="Nombre *",
        hint_text="Solo letras",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=200,
        on_change=validar_solo_letras,
        prefix_icon=ft.Icons.PERSON
    )

    apellidos_field = ft.TextField(
        label="Apellidos *",
        hint_text="Solo letras",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=250,
        on_change=validar_solo_letras,
        prefix_icon=ft.Icons.PERSON_OUTLINE
    )

    correo_field = ft.TextField(
        label="Correo *",
        hint_text="ejemplo@correo.com",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL
    )

    telefono_field = ft.TextField(
        label="Teléfono",
        hint_text="999 999 999",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=200,
        keyboard_type=ft.KeyboardType.PHONE,
        on_change=validar_telefono,
        prefix_icon=ft.Icons.PHONE
    )

    #  DROPDOWN DE ESTADO (solo visible al editar)
    estado_dropdown = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("Activo"),
            ft.dropdown.Option("Inactivo"),
            ft.dropdown.Option("Congelado"),
        ],
         
        value="Activo",
        color=TEXT_PRIMARY,
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        width=200,
        visible=False  # Oculto por defecto
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
            clientes_list = []

        clientes_container.controls.clear()

        if not clientes_list:
            clientes_container.controls.append(
                ft.Container(
                    content=ft.Text("No hay clientes registrados", color=TEXT_SECONDARY, size=14),
                    padding=20,
                    alignment=ft.alignment.center
                )
            )
        else:
            for cliente in clientes_list:
                clientes_container.controls.append(create_cliente_card(cliente))
        
        page.update()

    def create_cliente_card(cliente):
        """ CORREGIDO: Crear tarjeta de cliente con estados"""
        estado = cliente.get('estado', 'Activo')
        
        #  Configuración de colores por estado
        estado_config = {
            "Activo": {"color": "#4CAF50", "icono": ft.Icons.CHECK_CIRCLE},
            "Inactivo": {"color": "#ef5350", "icono": ft.Icons.CANCEL},
            "Congelado": {"color": "#FF9800", "icono": ft.Icons.AC_UNIT}
        }
        
        config = estado_config.get(estado, estado_config["Activo"])
        
        #  Información adicional
        fecha_membresia = cliente.get('fecha_membresia')
        info_membresia = "Sin membresía"
        
        if fecha_membresia:
            try:
                from datetime import datetime
                fecha_venc = datetime.fromisoformat(fecha_membresia)
                dias_restantes = (fecha_venc - datetime.now()).days
                if dias_restantes >= 0:
                    info_membresia = f"Vence en {dias_restantes} días"
                else:
                    info_membresia = f"Vencida hace {abs(dias_restantes)} días"
            except:
                info_membresia = "Fecha inválida"

        return ft.Container(
            content=ft.Row([
                # Información principal
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, size=30, color=PRIMARY_COLOR),
                    bgcolor=f"{PRIMARY_COLOR}22",
                    border_radius=8,
                    padding=8
                ),
                ft.Column([
                    ft.Text(
                        f"{cliente['nombre']} {cliente['apellidos']}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY
                    ),
                    ft.Row([
                        ft.Text(f"DNI: {cliente['dni']}", size=12, color=TEXT_SECONDARY),
                        ft.Text("•", size=12, color=TEXT_SECONDARY),
                        ft.Text(cliente['correo'], size=12, color=TEXT_SECONDARY),
                    ], spacing=5),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=12, color=TEXT_SECONDARY),
                        ft.Text(cliente.get('telefono') or 'Sin teléfono', size=11, color=TEXT_SECONDARY),
                        ft.Text("•", size=12, color=TEXT_SECONDARY),
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=12, color=TEXT_SECONDARY),
                        ft.Text(info_membresia, size=11, color=TEXT_SECONDARY),
                    ], spacing=3),
                ], spacing=2, expand=True),
                
                #  Badge de estado
                ft.Container(
                    content=ft.Row([
                        ft.Icon(config['icono'], size=14, color=ft.Colors.WHITE),
                        ft.Text(estado, size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                    ], spacing=5),
                    bgcolor=config['color'],
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=20
                ),
                
                #  Botones de acción
                ft.Row([
                    # Botón Editar
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=PRIMARY_COLOR,
                        icon_size=20,
                        tooltip="Editar",
                        on_click=lambda _, c=cliente: edit_cliente(c)
                    ),
                    # Botón Cambiar Estado
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        icon_color=TEXT_SECONDARY,
                        icon_size=20,
                        tooltip="Opciones",
                        items=[
                            ft.PopupMenuItem(
                                text="Activar",
                                icon=ft.Icons.CHECK_CIRCLE,
                                on_click=lambda _, c=cliente: cambiar_estado(c, "Activo")
                            ),
                            ft.PopupMenuItem(
                                text="Congelar",
                                icon=ft.Icons.AC_UNIT,
                                on_click=lambda _, c=cliente: cambiar_estado(c, "Congelado")
                            ),
                            ft.PopupMenuItem(
                                text="Desactivar",
                                icon=ft.Icons.CANCEL,
                                on_click=lambda _, c=cliente: cambiar_estado(c, "Inactivo")
                            ),
                            ft.PopupMenuItem(),  # Separador
                            ft.PopupMenuItem(
                                text="Eliminar",
                                icon=ft.Icons.DELETE,
                                on_click=lambda _, c=cliente: confirm_delete_cliente(c)
                            ),
                        ]
                    ),
                ], spacing=0)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
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
        dni_field.error_text = None
        nombre_field.error_text = None
        apellidos_field.error_text = None
        correo_field.error_text = None
        telefono_field.error_text = None
        estado_dropdown.visible = False
        save_button.text = "Guardar Cliente"
        page.update()

    def validar_email(email):
        """Validar formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    def save_cliente(e):
        """ CORREGIDO: Guardar o actualizar cliente"""
        # Limpiar errores previos
        dni_field.error_text = None
        nombre_field.error_text = None
        apellidos_field.error_text = None
        correo_field.error_text = None

        # Validar campos obligatorios
        errores = []
        
        if not dni_field.value:
            dni_field.error_text = "Campo obligatorio"
            errores.append("DNI")
        elif len(dni_field.value) != 8:
            dni_field.error_text = "Debe tener 8 dígitos"
            errores.append("DNI")
            
        if not nombre_field.value:
            nombre_field.error_text = "Campo obligatorio"
            errores.append("Nombre")
            
        if not apellidos_field.value:
            apellidos_field.error_text = "Campo obligatorio"
            errores.append("Apellidos")
            
        if not correo_field.value:
            correo_field.error_text = "Campo obligatorio"
            errores.append("Correo")
        elif not validar_email(correo_field.value):
            correo_field.error_text = "Correo inválido"
            errores.append("Correo")

        if errores:
            mostrar_mensaje(f"⚠ Complete correctamente: {', '.join(errores)}", error=True)
            page.update()
            return

        try:
            if selected_cliente:
                #  Actualizar cliente
                data = {
                    "nombre": nombre_field.value.strip(),
                    "apellidos": apellidos_field.value.strip(),
                    "correo": correo_field.value.strip().lower(),
                    "telefono": telefono_field.value.strip() if telefono_field.value else None,
                }
                
                #  Incluir estado si se modificó
                if estado_dropdown.visible:
                    data["estado"] = estado_dropdown.value
                
                api.actualizar_cliente(selected_cliente['id'], data)
                mostrar_mensaje(f"✓ Cliente {nombre_field.value} actualizado", error=False)
            else:
                #  Crear nuevo cliente
                data = {
                    "dni": dni_field.value.strip(),
                    "nombre": nombre_field.value.strip(),
                    "apellidos": apellidos_field.value.strip(),
                    "correo": correo_field.value.strip().lower(),
                    "telefono": telefono_field.value.strip() if telefono_field.value else None,
                    "usuario_creacion": auth_service.get_current_user().get('nombre', 'admin')
                }
                
                api.crear_cliente(data)
                mostrar_mensaje(f"✓ Cliente {nombre_field.value} creado", error=False)

            clear_form()
            load_clientes()

        except Exception as e:
            error_msg = str(e).lower()
            
            if "dni" in error_msg and ("existe" in error_msg or "registrado" in error_msg):
                dni_field.error_text = "DNI ya registrado"
                mostrar_mensaje("❌ Este DNI ya está registrado", error=True)
            elif "correo" in error_msg and ("existe" in error_msg or "registrado" in error_msg):
                correo_field.error_text = "Correo ya registrado"
                mostrar_mensaje("❌ Este correo ya está registrado", error=True)
            else:
                mostrar_mensaje(f"❌ Error: {str(e)}", error=True)
            
            page.update()

    def edit_cliente(cliente):
        """ CORREGIDO: Cargar datos del cliente para editar"""
        nonlocal selected_cliente
        selected_cliente = cliente
        
        #  Cargar todos los campos
        dni_field.value = cliente['dni']
        dni_field.disabled = True  # No permitir cambiar DNI
        nombre_field.value = cliente['nombre']
        apellidos_field.value = cliente['apellidos']
        correo_field.value = cliente['correo']
        telefono_field.value = cliente.get('telefono', '')
        
        # Mostrar dropdown de estado
        estado_dropdown.value = cliente.get('estado', 'Activo')
        estado_dropdown.visible = True
        
        save_button.text = "Actualizar Cliente"
        
        # Scroll al formulario
        page.scroll = "auto"
        page.update()

    def cambiar_estado(cliente, nuevo_estado):
        """ NUEVO: Cambiar estado del cliente"""
        try:
            data = {
                "nombre": cliente['nombre'],
                "apellidos": cliente['apellidos'],
                "correo": cliente['correo'],
                "telefono": cliente.get('telefono'),
                "estado": nuevo_estado
            }
            
            api.actualizar_cliente(cliente['id'], data)
            
            emoji = {
                "Activo": "✓",
                "Congelado": "❄️",
                "Inactivo": "⏸"
            }.get(nuevo_estado, "✓")
            
            mostrar_mensaje(f"{emoji} Cliente {cliente['nombre']} ahora está {nuevo_estado}", error=False)
            load_clientes()
            
        except Exception as e:
            mostrar_mensaje(f"❌ Error: {str(e)}", error=True)

    def confirm_delete_cliente(cliente):
        """Confirmar eliminación (cambia a Inactivo)"""
        def close_dialog(e):
            page.close(dialog)

        def delete_confirmed(e):
            try:
                # Eliminar = Cambiar a Inactivo
                api.eliminar_cliente(cliente['id'])
                page.close(dialog)
                mostrar_mensaje(f"✓ Cliente {cliente['nombre']} desactivado", error=False)
                load_clientes()
            except Exception as error:
                page.close(dialog)
                mostrar_mensaje(f"❌ Error: {str(error)}", error=True)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Desactivación", color=TEXT_PRIMARY),
            content=ft.Column([
                ft.Text(
                    f"¿Desactivar a {cliente['nombre']} {cliente['apellidos']}?",
                    color=TEXT_SECONDARY
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color="#2196F3"),
                        ft.Text(
                            "El cliente pasará a estado 'Inactivo'",
                            size=12,
                            color=TEXT_SECONDARY,
                            italic=True
                        ),
                    ], spacing=5),
                    margin=ft.margin.only(top=10)
                )
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton(
                    "Desactivar",
                    style=ft.ButtonStyle(color="#ef5350"),
                    on_click=delete_confirmed
                ),
            ],
            bgcolor=CARD_BG,
        )
        
        page.open(dialog)

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
        content=ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=PRIMARY_COLOR, on_click=lambda _: on_back()),
            ft.Text("Gestión de Clientes - BLESSED GYM", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
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
            ft.Row([
                ft.Icon(ft.Icons.PERSON_ADD, size=20, color=PRIMARY_COLOR),
                ft.Text("Formulario de Cliente", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            ], spacing=10),
            ft.Divider(height=1, color="#333333"),
            ft.Row([dni_field, nombre_field, apellidos_field], spacing=15, wrap=True),
            ft.Row([correo_field, telefono_field, estado_dropdown], spacing=15, wrap=True),
            ft.Text("* Campos obligatorios", size=11, color=TEXT_SECONDARY, italic=True),
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
                ft.Row([
                    ft.Icon(ft.Icons.PEOPLE, size=20, color=PRIMARY_COLOR),
                    ft.Text("Lista de Clientes", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                ], spacing=10, expand=True),
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
    main_content = ft.Column([header, form_card, list_card], spacing=0, expand=True)

    page.add(ft.Container(content=main_content, bgcolor=BACKGROUND_DARK, expand=True))

    # Cargar clientes al inicio
    load_clientes()