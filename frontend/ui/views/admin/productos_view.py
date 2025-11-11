"""
Vista de Gestión de Productos - Sistema Completo de Inventario
Incluye: CRUD de productos, Categorías, Control de Stock, Búsqueda y Paginación
Diseño profesional siguiendo la filosofía UI/UX de BLESSED GYM
"""

import flet as ft
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button, create_status_badge, create_icon_button
from ui.components.molecules import create_card_container, create_confirmation_dialog, create_empty_state, create_stat_card
from ui.utils.messages import mostrar_exito, mostrar_error


def show_productos_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Vista de gestión de productos con diseño profesional
    """
    page.title = "BLESSED GYM - Productos"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Estado
    productos_list = []
    productos_filtrados = []
    categorias_list = []
    edit_mode = [False]
    producto_actual = [None]

    # Paginación
    items_per_page = 8
    current_page = [0]

    # ==========================================
    # COMPONENTES DE FORMULARIO
    # ==========================================
    nombre_field = ft.TextField(
        label="Nombre del producto",
        hint_text="Ej: Proteína Whey Gold",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        expand=True
    )

    descripcion_field = ft.TextField(
        label="Descripción",
        hint_text="Descripción detallada del producto",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        multiline=True,
        min_lines=2,
        max_lines=3,
        expand=True
    )

    categoria_dropdown = ft.Dropdown(
        label="Categoría",
        hint_text="Seleccione una categoría",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        options=[],
        expand=True
    )

    precio_field = ft.TextField(
        label="Precio (S/.)",
        hint_text="0.00",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    stock_field = ft.TextField(
        label="Stock Inicial",
        hint_text="0",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    stock_minimo_field = ft.TextField(
        label="Stock Mínimo",
        hint_text="5",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    estado_dropdown = ft.Dropdown(
        label="Estado",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        options=[
            ft.dropdown.Option("Activo"),
            ft.dropdown.Option("Inactivo"),
        ],
        value="Activo",
        expand=True,
        visible=False
    )

    # Campo de búsqueda
    search_field = ft.TextField(
        hint_text="Buscar producto por nombre o categoría...",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=lambda e: filtrar_productos(e.control.value)
    )

    # Filtro de categoría
    filtro_categoria = ft.Dropdown(
        hint_text="Todas las categorías",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        options=[ft.dropdown.Option(key="todos", text="Todas las categorías")],
        value="todos",
        width=250,
        on_change=lambda e: filtrar_productos()
    )

    tabla_container = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
    pagination_text = ft.Text("", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY)

    # Stats refs
    stat_total = ft.Ref[ft.Container]()
    stat_bajo_stock = ft.Ref[ft.Container]()
    stat_valor_inventario = ft.Ref[ft.Container]()

    # ==========================================
    # FUNCIONES DE DATOS
    # ==========================================
    def load_productos(update_ui=True):
        """Cargar productos desde la API"""
        nonlocal productos_list, productos_filtrados
        try:
            productos_list = api.get_productos()

            # Enriquecer con información de stock
            for producto in productos_list:
                stock_info = api.get_stock_producto(producto['id'])
                producto['stock_actual'] = stock_info.get('stock_actual', 0)

            productos_filtrados = productos_list.copy()
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            productos_list = []
            productos_filtrados = []

        # Solo actualizar UI si está en la página
        if update_ui:
            update_stats()
            update_tabla()

    def load_categorias():
        """Cargar categorías desde la API"""
        nonlocal categorias_list
        try:
            categorias_list = api.get_categorias()

            # Actualizar dropdown de categorías
            categoria_dropdown.options = [
                ft.dropdown.Option(key=str(cat['id']), text=cat['nombre'])
                for cat in categorias_list
            ]

            # Actualizar filtro de categorías
            filtro_categoria.options = [ft.dropdown.Option(key="todos", text="Todas las categorías")]
            filtro_categoria.options.extend([
                ft.dropdown.Option(key=str(cat['id']), text=cat['nombre'])
                for cat in categorias_list
            ])

            # No llamar update() aquí porque los controles aún no están en la página
        except Exception as e:
            print(f"Error al cargar categorías: {e}")
            categorias_list = []

    def filtrar_productos(search_term=""):
        """Filtrar productos por búsqueda y categoría"""
        nonlocal productos_filtrados
        search_term = search_term.lower().strip() if search_term else search_field.value.lower().strip()
        categoria_filtro = filtro_categoria.value

        productos_filtrados = productos_list.copy()

        # Filtrar por búsqueda
        if search_term:
            productos_filtrados = [
                p for p in productos_filtrados
                if (search_term in p.get('nombre', '').lower() or
                    search_term in p.get('descripcion', '').lower())
            ]

        # Filtrar por categoría
        if categoria_filtro and categoria_filtro != "todos":
            productos_filtrados = [
                p for p in productos_filtrados
                if str(p.get('id_categoria')) == categoria_filtro
            ]

        current_page[0] = 0
        update_tabla()

    def update_stats():
        """Actualizar estadísticas"""
        total = len(productos_list)
        bajo_stock = sum(1 for p in productos_list if p.get('stock_actual', 0) <= p.get('stock_minimo', 0))
        valor_total = sum(p.get('precio', 0) * p.get('stock_actual', 0) for p in productos_list)

        if stat_total.current:
            stat_total.current.content = create_stat_card(
                title="Total Productos",
                value=str(total),
                icon=ft.Icons.INVENTORY_2,
                color=Theme.PRIMARY
            ).content
            stat_total.current.update()

        if stat_bajo_stock.current:
            stat_bajo_stock.current.content = create_stat_card(
                title="Bajo Stock",
                value=str(bajo_stock),
                icon=ft.Icons.WARNING,
                color=Theme.WARNING
            ).content
            stat_bajo_stock.current.update()

        if stat_valor_inventario.current:
            stat_valor_inventario.current.content = create_stat_card(
                title="Valor Inventario",
                value=f"S/ {valor_total:,.2f}",
                icon=ft.Icons.ATTACH_MONEY,
                color=Theme.SUCCESS
            ).content
            stat_valor_inventario.current.update()

    def update_tabla():
        """Actualizar tabla de productos"""
        tabla_container.controls.clear()

        if not productos_filtrados:
            tabla_container.controls.append(
                create_empty_state(
                    message="No hay productos para mostrar",
                    icon=ft.Icons.INVENTORY_2,
                    secondary_message="Crea tu primer producto usando el formulario"
                )
            )
            pagination_text.value = "Mostrando 0 de 0 productos"
            page.update()
            return

        # Paginación
        total_items = len(productos_filtrados)
        start_idx = current_page[0] * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        productos_pagina = productos_filtrados[start_idx:end_idx]

        # Encabezado
        header = ft.Container(
            content=ft.Row([
                ft.Container(ft.Text("Producto", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=3),
                ft.Container(ft.Text("Categoría", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=2),
                ft.Container(ft.Text("Precio", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Stock", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Estado", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Acciones", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=2),
            ], spacing=Theme.SPACING["sm"]),
            bgcolor=f"{Theme.PRIMARY}22",
            padding=Theme.SPACING["md"],
            border_radius=Theme.RADIUS["sm"]
        )
        tabla_container.controls.append(header)

        # Filas
        for producto in productos_pagina:
            # Obtener nombre de categoría
            categoria_nombre = "Sin categoría"
            for cat in categorias_list:
                if cat['id'] == producto.get('id_categoria'):
                    categoria_nombre = cat['nombre']
                    break

            # Stock con indicador de alerta
            stock_actual = producto.get('stock_actual', 0)
            stock_minimo = producto.get('stock_minimo', 0)
            stock_color = Theme.SUCCESS if stock_actual > stock_minimo else Theme.ERROR

            fila = ft.Container(
                content=ft.Row([
                    # Producto
                    ft.Container(
                        ft.Column([
                            ft.Text(
                                producto['nombre'],
                                size=Theme.FONT_SIZE["sm"],
                                color=Theme.TEXT_PRIMARY,
                                weight=Theme.FONT_WEIGHT["bold"]
                            ),
                            ft.Text(
                                producto.get('descripcion', '')[:50] + ('...' if len(producto.get('descripcion', '')) > 50 else ''),
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_SECONDARY
                            ),
                        ], spacing=2),
                        expand=3
                    ),
                    # Categoría
                    ft.Container(
                        ft.Container(
                            content=ft.Text(
                                categoria_nombre,
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_PRIMARY
                            ),
                            bgcolor=f"{Theme.PRIMARY}15",
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=Theme.RADIUS["sm"]
                        ),
                        expand=2
                    ),
                    # Precio
                    ft.Container(
                        ft.Text(
                            f"S/ {producto.get('precio', 0):.2f}",
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.PRIMARY,
                            weight=Theme.FONT_WEIGHT["bold"]
                        ),
                        expand=1
                    ),
                    # Stock
                    ft.Container(
                        ft.Row([
                            ft.Icon(
                                ft.Icons.INVENTORY if stock_actual > stock_minimo else ft.Icons.WARNING,
                                size=14,
                                color=stock_color
                            ),
                            ft.Text(
                                str(stock_actual),
                                size=Theme.FONT_SIZE["sm"],
                                color=stock_color,
                                weight=Theme.FONT_WEIGHT["bold"]
                            ),
                        ], spacing=4),
                        expand=1
                    ),
                    # Estado
                    ft.Container(
                        create_status_badge(
                            producto.get('estado', 'Activo'),
                            status="success" if producto.get('estado') == 'Activo' else "error"
                        ),
                        expand=1
                    ),
                    # Acciones
                    ft.Container(
                        ft.Row([
                            create_icon_button(
                                ft.Icons.EDIT,
                                lambda e, p=producto: editar_producto(p),
                                tooltip="Editar",
                                color=Theme.INFO
                            ),
                            create_icon_button(
                                ft.Icons.ADD_BOX,
                                lambda e, p=producto: ajustar_stock(p),
                                tooltip="Ajustar Stock",
                                color=Theme.SUCCESS
                            ),
                            create_icon_button(
                                ft.Icons.DELETE,
                                lambda e, p=producto: confirm_delete_producto(p),
                                tooltip="Eliminar",
                                color=Theme.ERROR
                            ),
                        ], spacing=4),
                        expand=2
                    ),
                ], spacing=Theme.SPACING["sm"]),
                padding=Theme.SPACING["md"],
                border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
            )
            tabla_container.controls.append(fila)

        pagination_text.value = f"Mostrando {start_idx + 1} a {end_idx} de {total_items} productos"
        page.update()

    def cambiar_pagina(direccion):
        """Cambiar de página"""
        total_pages = max(1, (len(productos_filtrados) + items_per_page - 1) // items_per_page)

        if direccion == "prev" and current_page[0] > 0:
            current_page[0] -= 1
            update_view()
        elif direccion == "next" and current_page[0] < total_pages - 1:
            current_page[0] += 1
            update_view()

    # ==========================================
    # FUNCIONES CRUD
    # ==========================================
    def save_producto(e):
        """Guardar (crear o actualizar) producto"""
        # Validar campos
        nombre_field.error_text = None
        precio_field.error_text = None
        categoria_dropdown.error_text = None

        if not nombre_field.value or not nombre_field.value.strip():
            nombre_field.error_text = "El nombre es requerido"
            nombre_field.update()
            return

        if not precio_field.value or not precio_field.value.strip():
            precio_field.error_text = "El precio es requerido"
            precio_field.update()
            return

        if not categoria_dropdown.value:
            categoria_dropdown.error_text = "Seleccione una categoría"
            categoria_dropdown.update()
            return

        try:
            precio = float(precio_field.value)
            if precio < 0:
                precio_field.error_text = "El precio debe ser positivo"
                precio_field.update()
                return
        except ValueError:
            precio_field.error_text = "Precio inválido"
            precio_field.update()
            return

        # Preparar datos según el schema del backend
        data = {
            "nombre": nombre_field.value.strip(),
            "descripcion": descripcion_field.value.strip() if descripcion_field.value else None,
            "id_categoria": int(categoria_dropdown.value),  # Backend espera id_categoria, no categoria_id
            "usuario_creacion": current_user.get('username', 'admin')
        }

        try:
            if edit_mode[0]:
                # Actualizar
                data['estado'] = estado_dropdown.value
                api.actualizar_producto(producto_actual[0]['id'], data)
                mostrar_exito(page, f"Producto '{data['nombre']}' actualizado correctamente")
            else:
                # Crear
                print(f"DEBUG: Enviando datos al backend: {data}")  # Debug
                nuevo_producto = api.crear_producto(data)
                print(f"DEBUG: Producto creado: {nuevo_producto}")  # Debug

                # Registrar stock inicial si se proporcionó
                if stock_field.value and stock_field.value.strip():
                    try:
                        stock_inicial = int(stock_field.value)
                        if stock_inicial > 0:
                            api.registrar_movimiento_inventario({
                                "id_producto": nuevo_producto['id'],  # Backend espera id_producto
                                "tipo_movimiento": "Entrada",
                                "cantidad": stock_inicial,
                                "motivo": "Stock inicial",
                                "usuario_creacion": current_user.get('username', 'admin')
                            })
                    except ValueError:
                        print(f"Error: stock_inicial no es un número válido")

                mostrar_exito(page, f"Producto '{data['nombre']}' creado correctamente")

            clear_form()
            load_productos(update_ui=False)  # Recargar productos desde API
            update_view()  # Reconstruir vista completa para actualizar tabla

        except Exception as e:
            mostrar_error(page, f"Error al guardar: {str(e)}")

    def editar_producto(producto):
        """Cargar producto para editar"""
        edit_mode[0] = True
        producto_actual[0] = producto

        nombre_field.value = producto['nombre']
        descripcion_field.value = producto.get('descripcion', '')
        categoria_dropdown.value = str(producto['id_categoria'])
        precio_field.value = str(producto['precio'])
        stock_minimo_field.value = str(producto.get('stock_minimo', 5))
        estado_dropdown.value = producto.get('estado', 'Activo')
        estado_dropdown.visible = True
        stock_field.visible = False

        update_view()

    def confirm_delete_producto(producto):
        """Confirmar eliminación de producto"""
        def on_confirm(e):
            try:
                api.eliminar_producto(producto['id'])
                mostrar_exito(page, f"Producto '{producto['nombre']}' eliminado correctamente")
                load_productos(update_ui=False)
                update_view()
            except Exception as ex:
                mostrar_error(page, f"Error al eliminar: {str(ex)}")
            page.close(dialog)

        dialog = create_confirmation_dialog(
            page,
            title="Eliminar Producto",
            message=f"¿Está seguro de eliminar el producto '{producto['nombre']}'?",
            on_confirm=on_confirm
        )
        page.open(dialog)

    def clear_form():
        """Limpiar formulario"""
        edit_mode[0] = False
        producto_actual[0] = None
        nombre_field.value = ""
        descripcion_field.value = ""
        categoria_dropdown.value = None
        precio_field.value = ""
        stock_field.value = ""
        stock_minimo_field.value = ""
        estado_dropdown.visible = False
        stock_field.visible = True

        nombre_field.error_text = None
        precio_field.error_text = None
        categoria_dropdown.error_text = None

        page.update()

    def ajustar_stock(producto):
        """Ajustar stock de un producto"""
        cantidad_field = ft.TextField(
            label="Cantidad",
            hint_text="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True
        )

        tipo_dropdown = ft.Dropdown(
            label="Tipo de Movimiento",
            options=[
                ft.dropdown.Option("Entrada"),
                ft.dropdown.Option("Salida"),
            ],
            value="Entrada"
        )

        motivo_field = ft.TextField(
            label="Motivo",
            hint_text="Ej: Compra de proveedor, Venta, Ajuste de inventario",
            multiline=True
        )

        def on_save_stock(e):
            try:
                cantidad = int(cantidad_field.value)
                if cantidad <= 0:
                    mostrar_error(page, "La cantidad debe ser mayor a 0")
                    return

                data = {
                    "id_producto": producto['id'],  # Backend espera id_producto
                    "tipo_movimiento": tipo_dropdown.value,
                    "cantidad": cantidad,
                    "motivo": motivo_field.value if motivo_field.value else tipo_dropdown.value,
                    "usuario_creacion": current_user.get('username', 'admin')
                }

                api.registrar_movimiento_inventario(data)
                mostrar_exito(page, f"Stock actualizado correctamente")
                page.close(dialog)
                load_productos(update_ui=False)
                update_view()

            except ValueError:
                mostrar_error(page, "Cantidad inválida")
            except Exception as ex:
                mostrar_error(page, f"Error: {str(ex)}")

        dialog = ft.AlertDialog(
            title=ft.Text(f"Ajustar Stock: {producto['nombre']}", color=Theme.TEXT_PRIMARY),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Stock actual: {producto.get('stock_actual', 0)}", color=Theme.TEXT_SECONDARY),
                    tipo_dropdown,
                    cantidad_field,
                    motivo_field,
                ], tight=True, spacing=Theme.SPACING["md"]),
                width=400
            ),
            actions=[
                create_outlined_button("Cancelar", lambda _: page.close(dialog)),
                create_primary_button("Guardar", on_save_stock, icon=ft.Icons.SAVE),
            ],
            bgcolor=Theme.CARD_BG,
        )
        page.open(dialog)

    def crear_categoria_dialog(e):
        """Diálogo para crear nueva categoría"""
        nombre_cat_field = ft.TextField(
            label="Nombre de la categoría",
            hint_text="Ej: Suplementos, Accesorios, Bebidas",
            autofocus=True
        )

        desc_cat_field = ft.TextField(
            label="Descripción",
            multiline=True
        )

        def on_save_categoria(e):
            if not nombre_cat_field.value or not nombre_cat_field.value.strip():
                mostrar_error(page, "El nombre es requerido")
                return

            try:
                api.crear_categoria(
                    nombre=nombre_cat_field.value.strip(),
                    descripcion=desc_cat_field.value.strip() if desc_cat_field.value else ""
                )
                mostrar_exito(page, "Categoría creada correctamente")
                page.close(dialog)
                load_categorias()
                update_view()  # Reconstruir vista para actualizar dropdowns
            except Exception as ex:
                mostrar_error(page, f"Error: {str(ex)}")

        dialog = ft.AlertDialog(
            title=ft.Text("Nueva Categoría", color=Theme.TEXT_PRIMARY),
            content=ft.Container(
                content=ft.Column([
                    nombre_cat_field,
                    desc_cat_field,
                ], tight=True, spacing=Theme.SPACING["md"]),
                width=400
            ),
            actions=[
                create_outlined_button("Cancelar", lambda _: page.close(dialog)),
                create_primary_button("Crear", on_save_categoria, icon=ft.Icons.ADD),
            ],
            bgcolor=Theme.CARD_BG,
        )
        page.open(dialog)

    # ==========================================
    # CONTENIDO
    # ==========================================
    def update_view():
        """Actualizar vista completa"""
        page.clean()

        # Calcular paginación
        total_productos = len(productos_filtrados)
        total_pages = max(1, (total_productos + items_per_page - 1) // items_per_page)
        current_page_display = current_page[0] + 1

        if current_page[0] >= total_pages and total_pages > 0:
            current_page[0] = total_pages - 1

        # Estadísticas
        stats_row = ft.Row([
            ft.Container(ref=stat_total, expand=True),
            ft.Container(ref=stat_bajo_stock, expand=True),
            ft.Container(ref=stat_valor_inventario, expand=True),
        ], spacing=Theme.SPACING["xl"])

        # Formulario
        form_title = "Editar Producto" if edit_mode[0] else "Nuevo Producto"
        form_buttons = [create_outlined_button("Cancelar", lambda _: clear_form(), icon=ft.Icons.CLOSE)]
        if edit_mode[0]:
            form_buttons.append(create_primary_button("Actualizar", save_producto, icon=ft.Icons.SAVE))
        else:
            form_buttons.append(create_primary_button("Crear", save_producto, icon=ft.Icons.ADD))

        form_area = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ADD_BOX, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text(form_title, size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ft.Container(expand=True),
                    create_outlined_button("+ Categoría", crear_categoria_dialog, icon=ft.Icons.CATEGORY),
                ], spacing=Theme.SPACING["md"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Row([nombre_field, categoria_dropdown], spacing=Theme.SPACING["md"]),
                descripcion_field,
                ft.Row([
                    precio_field,
                    stock_field if not edit_mode[0] else ft.Container(),
                    stock_minimo_field,
                    estado_dropdown if edit_mode[0] else ft.Container(),
                ], spacing=Theme.SPACING["md"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Row(form_buttons, spacing=Theme.SPACING["md"], alignment=ft.MainAxisAlignment.END),
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        # Tabla de productos
        list_area = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY_2, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Lista de Productos", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INVENTORY_2, size=16, color=Theme.PRIMARY),
                            ft.Text(
                                f"{total_productos} productos",
                                size=Theme.FONT_SIZE["sm"],
                                color=Theme.TEXT_SECONDARY,
                                weight=Theme.FONT_WEIGHT["medium"]
                            ),
                        ], spacing=4),
                        bgcolor=f"{Theme.PRIMARY}15",
                        padding=8,
                        border_radius=Theme.RADIUS["sm"]
                    ),
                ], spacing=Theme.SPACING["md"]),
                ft.Row([
                    search_field,
                    filtro_categoria,
                ], spacing=Theme.SPACING["md"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                tabla_container,
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Container(
                    content=ft.Row([
                        ft.Container(content=pagination_text, expand=True),
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS,
                                    icon_size=16,
                                    icon_color=Theme.PRIMARY if current_page[0] > 0 else Theme.TEXT_SECONDARY,
                                    tooltip="Página anterior",
                                    on_click=lambda _: cambiar_pagina("prev"),
                                    disabled=current_page[0] == 0
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"Página {current_page_display} de {total_pages}",
                                        size=Theme.FONT_SIZE["sm"],
                                        color=Theme.TEXT_PRIMARY,
                                        weight=Theme.FONT_WEIGHT["medium"]
                                    ),
                                    bgcolor=f"{Theme.PRIMARY}15",
                                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                    border_radius=Theme.RADIUS["sm"]
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_FORWARD_IOS,
                                    icon_size=16,
                                    icon_color=Theme.PRIMARY if current_page[0] < total_pages - 1 else Theme.TEXT_SECONDARY,
                                    tooltip="Página siguiente",
                                    on_click=lambda _: cambiar_pagina("next"),
                                    disabled=current_page[0] >= total_pages - 1
                                ),
                            ], spacing=8),
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.symmetric(vertical=8)
                ),
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        # Layout completo
        content = ft.Column([
            stats_row,
            ft.Container(height=Theme.SPACING["xl"]),
            form_area,
            ft.Container(height=Theme.SPACING["xl"]),
            list_area,
        ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

        create_base_layout(
            page=page,
            role="admin",
            current_section="Productos",
            on_section_click=on_section_click,
            content=content,
            user_info=user_info,
            on_logout=lambda _: on_section_click("logout")
        )

        # Actualizar stats y tabla ahora que los controles están en la página
        update_stats()
        update_tabla()

    # Inicializar - Primero cargar datos, luego construir vista
    load_categorias()           # Solo carga datos, no actualiza controles
    load_productos(update_ui=False)  # Solo carga datos, sin actualizar UI
    update_view()               # Construye la vista con los datos cargados
