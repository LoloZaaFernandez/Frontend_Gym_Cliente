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
    # REFERENCIAS DE ESTADO PARA DIÁLOGO
    # ==========================================
    # Los campos del formulario se crearán dentro del diálogo
    # para evitar problemas de estado compartido

    # Campo de búsqueda general
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

    # Campo de búsqueda por código de barras
    codigo_barras_search = ft.TextField(
        hint_text="Escanear o ingresar código de barras...",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        prefix_icon=ft.Icons.QR_CODE_SCANNER,
        width=300,
        on_submit=lambda e: buscar_por_codigo_barras(e.control.value)
    )

    # Campo de búsqueda por SKU
    sku_search = ft.TextField(
        hint_text="Buscar por SKU...",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        prefix_icon=ft.Icons.TAG,
        width=250,
        on_submit=lambda e: buscar_por_sku(e.control.value)
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
            # El endpoint GET /api/productos ya devuelve TODA la información
            # incluyendo stock_actual, no necesitamos llamadas adicionales
            productos_list = api.get_productos()
            productos_filtrados = productos_list.copy()
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            productos_list = []
            productos_filtrados = []

        # Solo actualizar UI si está en la página
        if update_ui:
            update_stats()
            update_tabla()

    def load_categorias(update_ui=False):
        """Cargar categorías desde la API"""
        nonlocal categorias_list
        try:
            categorias_list = api.get_categorias()
            print(f"DEBUG: Categorías cargadas: {len(categorias_list)}")

            # Actualizar filtro de categorías solo si update_ui=True
            if update_ui and filtro_categoria:
                filtro_categoria.options = [ft.dropdown.Option(key="todos", text="Todas las categorías")]
                filtro_categoria.options.extend([
                    ft.dropdown.Option(key=str(cat['id']), text=cat['nombre'])
                    for cat in categorias_list
                ])
                try:
                    filtro_categoria.update()
                except:
                    pass  # Los controles podrían no estar en la página todavía

        except Exception as e:
            print(f"Error al cargar categorías: {e}")
            categorias_list = []

    def buscar_por_codigo_barras(codigo):
        """Buscar producto por código de barras usando la API"""
        if not codigo or not codigo.strip():
            return

        try:
            producto = api.get_producto_por_codigo_barras(codigo.strip())
            if producto:
                # Producto encontrado - mostrarlo en la tabla
                nonlocal productos_filtrados
                productos_filtrados = [producto]
                current_page[0] = 0
                update_tabla()
                mostrar_exito(page, f"Producto encontrado: {producto['nombre']}")
                # Limpiar campo de búsqueda
                codigo_barras_search.value = ""
                codigo_barras_search.update()
            else:
                mostrar_error(page, f"No se encontró producto con código de barras: {codigo}")
                codigo_barras_search.value = ""
                codigo_barras_search.update()
        except Exception as e:
            mostrar_error(page, f"Error al buscar: {str(e)}")
            codigo_barras_search.value = ""
            codigo_barras_search.update()

    def buscar_por_sku(sku):
        """Buscar producto por SKU usando la API"""
        if not sku or not sku.strip():
            return

        try:
            producto = api.get_producto_por_sku(sku.strip().upper())
            if producto:
                # Producto encontrado - mostrarlo en la tabla
                nonlocal productos_filtrados
                productos_filtrados = [producto]
                current_page[0] = 0
                update_tabla()
                mostrar_exito(page, f"Producto encontrado: {producto['nombre']}")
                # Limpiar campo de búsqueda
                sku_search.value = ""
                sku_search.update()
            else:
                mostrar_error(page, f"No se encontró producto con SKU: {sku.upper()}")
                sku_search.value = ""
                sku_search.update()
        except Exception as e:
            mostrar_error(page, f"Error al buscar: {str(e)}")
            sku_search.value = ""
            sku_search.update()

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
                    search_term in p.get('descripcion', '').lower() or
                    search_term in p.get('sku', '').lower() or
                    search_term in p.get('codigo_barras', '').lower())
            ]

        # Filtrar por categoría
        if categoria_filtro and categoria_filtro != "todos":
            # Buscar el nombre de la categoría seleccionada
            nombre_categoria_filtro = None
            for cat in categorias_list:
                if str(cat['id']) == categoria_filtro:
                    nombre_categoria_filtro = cat['nombre']
                    break

            # Filtrar por id_categoria o nombre_categoria
            productos_filtrados = [
                p for p in productos_filtrados
                if (str(p.get('id_categoria')) == categoria_filtro or
                    p.get('nombre_categoria') == nombre_categoria_filtro)
            ]

        current_page[0] = 0
        update_tabla()

    def update_stats():
        """Actualizar estadísticas usando la API"""
        try:
            # Usar endpoint de estadísticas de la API
            stats = api.get_estadisticas_productos()

            if stat_total.current:
                stat_total.current.content = create_stat_card(
                    title="Total Productos",
                    value=str(stats.get('total_productos', 0)),
                    icon=ft.Icons.INVENTORY_2,
                    color=Theme.PRIMARY
                ).content
                stat_total.current.update()

            if stat_bajo_stock.current:
                stat_bajo_stock.current.content = create_stat_card(
                    title="Bajo Stock",
                    value=str(stats.get('productos_con_stock_bajo', 0)),
                    icon=ft.Icons.WARNING,
                    color=Theme.WARNING
                ).content
                stat_bajo_stock.current.update()

            if stat_valor_inventario.current:
                valor_inventario = stats.get('valor_total_inventario', 0)
                stat_valor_inventario.current.content = create_stat_card(
                    title="Valor Inventario",
                    value=f"S/ {valor_inventario:,.2f}",
                    icon=ft.Icons.ATTACH_MONEY,
                    color=Theme.SUCCESS
                ).content
                stat_valor_inventario.current.update()

        except Exception as e:
            print(f"Error al actualizar estadísticas: {e}")
            # Fallback a cálculos manuales si la API falla
            total = len(productos_list)
            bajo_stock = sum(1 for p in productos_list if p.get('stock_actual', 0) <= p.get('stock_minimo', 0))
            valor_total = sum(p.get('precio_venta', p.get('precio', 0)) * p.get('stock_actual', 0) for p in productos_list)

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
            # El backend YA envía el nombre de la categoría en 'nombre_categoria'
            categoria_nombre = producto.get('nombre_categoria', 'Sin categoría')

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
                            f"S/ {producto.get('precio_venta', producto.get('precio', 0)):.2f}",
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
                        ft.Column([
                            ft.Row([
                                create_icon_button(
                                    ft.Icons.INFO_OUTLINE,
                                    lambda e, p=producto: ver_detalles_producto(p),
                                    tooltip="Ver Detalles",
                                    color=Theme.INFO
                                ),
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
                            ], spacing=2),
                            ft.Row([
                                create_icon_button(
                                    ft.Icons.HISTORY,
                                    lambda e, p=producto: ver_historial_producto(p),
                                    tooltip="Ver Historial",
                                    color=Theme.PRIMARY
                                ),
                                create_icon_button(
                                    ft.Icons.COPY_ALL,
                                    lambda e, p=producto: duplicar_producto(p),
                                    tooltip="Duplicar",
                                    color=Theme.SUCCESS
                                ),
                                create_icon_button(
                                    ft.Icons.SETTINGS,
                                    lambda e, p=producto: confirm_delete_producto(p),
                                    tooltip="Gestionar Estado",
                                    color=Theme.WARNING
                                ),
                            ], spacing=2),
                        ], spacing=2),
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
    # DIÁLOGO DE PRODUCTO
    # ==========================================
    def abrir_dialogo_producto(producto=None):
        """
        Abrir diálogo para crear/editar producto con ayudas descriptivas

        Args:
            producto: Si es None, crea nuevo producto. Si tiene valor, edita el producto.
        """
        print(f"DEBUG: abrir_dialogo_producto llamado con producto={producto}")

        # Recargar categorías para asegurar que estén disponibles
        load_categorias()

        # Determinar si es edición (tiene ID) o creación nueva (sin ID)
        es_edicion = producto is not None and 'id' in producto

        # Debug: Verificar que hay categorías
        print(f"DEBUG: Número de categorías disponibles: {len(categorias_list)}")
        if len(categorias_list) == 0:
            mostrar_error(page, "No hay categorías disponibles. Por favor, crea una categoría primero.")
            return

        # Crear todos los campos con ayudas descriptivas
        sku_field = ft.TextField(
            label="SKU (Código Único) *",
            hint_text="Ej: PROT-WH-001",
            helper_text="Código único de identificación del producto (se convierte a mayúsculas automáticamente)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            expand=True,
            value=producto.get('sku', '') if producto else ''
        )

        codigo_barras_field = ft.TextField(
            label="Código de Barras",
            hint_text="Ej: 7501234567890",
            helper_text="Código de barras EAN/UPC del producto (opcional, pero útil para escaneo rápido)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            expand=True,
            value=producto.get('codigo_barras', '') if producto else ''
        )

        nombre_field = ft.TextField(
            label="Nombre del Producto *",
            hint_text="Ej: Proteína Whey Gold 2kg Chocolate",
            helper_text="Nombre completo y descriptivo del producto",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            expand=True,
            value=producto['nombre'] if producto else ''
        )

        descripcion_field = ft.TextField(
            label="Descripción",
            hint_text="Describe las características principales del producto",
            helper_text="Descripción detallada que aparecerá en el catálogo (opcional)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=True,
            value=producto.get('descripcion', '') if producto else ''
        )

        # Buscar id_categoria si es producto existente y solo tenemos nombre_categoria
        categoria_value = None
        if producto:
            if 'id_categoria' in producto:
                categoria_value = str(producto['id_categoria'])
            elif 'nombre_categoria' in producto:
                # Buscar el ID por nombre
                for cat in categorias_list:
                    if cat['nombre'] == producto['nombre_categoria']:
                        categoria_value = str(cat['id'])
                        break

        categoria_dropdown = ft.Dropdown(
            label="Categoría *",
            hint_text="Seleccione una categoría",
            helper_text="Categoría a la que pertenece el producto (requerido)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            options=[
                ft.dropdown.Option(key=str(cat['id']), text=cat['nombre'])
                for cat in categorias_list
            ],
            expand=True,
            value=categoria_value
        )

        # PRECIOS
        precio_costo_field = ft.TextField(
            label="Precio de Costo (S/.) *",
            hint_text="0.00",
            helper_text="Precio al que compras el producto (debe ser menor o igual al precio de venta)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            suffix_text="S/.",
            value=str(producto.get('precio_costo', '')) if producto else ''
        )

        precio_venta_field = ft.TextField(
            label="Precio de Venta (S/.) *",
            hint_text="0.00",
            helper_text="Precio al que vendes el producto al público general",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            suffix_text="S/.",
            value=str(producto.get('precio_venta', producto.get('precio', ''))) if producto else ''
        )

        precio_miembro_field = ft.TextField(
            label="Precio para Miembros (S/.)",
            hint_text="0.00",
            helper_text="Precio especial para miembros (debe ser MENOR al precio de venta)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            suffix_text="S/.",
            value=str(producto.get('precio_miembro', '')) if producto and producto.get('precio_miembro') else ''
        )

        precio_mayorista_field = ft.TextField(
            label="Precio Mayorista (S/.)",
            hint_text="0.00",
            helper_text="Precio para ventas al por mayor (debe ser MENOR al precio de venta)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            suffix_text="S/.",
            value=str(producto.get('precio_mayorista', '')) if producto and producto.get('precio_mayorista') else ''
        )

        # INVENTARIO
        stock_field = ft.TextField(
            label="Stock Inicial",
            hint_text="0",
            helper_text="Cantidad inicial de unidades (solo para productos nuevos)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            visible=not es_edicion
        )

        stock_minimo_field = ft.TextField(
            label="Stock Mínimo",
            hint_text="5",
            helper_text="Cuando el stock llegue a este nivel, se generará una alerta",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            value=str(producto.get('stock_minimo', '')) if producto else ''
        )

        stock_maximo_field = ft.TextField(
            label="Stock Máximo",
            hint_text="100",
            helper_text="Capacidad máxima de almacenamiento para este producto",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            value=str(producto.get('stock_maximo', '')) if producto else ''
        )

        unidad_medida_dropdown = ft.Dropdown(
            label="Unidad de Medida",
            helper_text="Cómo se mide este producto (unidad, kg, litros, etc.)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            options=[
                ft.dropdown.Option("Unidad"),
                ft.dropdown.Option("Kg"),
                ft.dropdown.Option("Gramo"),
                ft.dropdown.Option("Litro"),
                ft.dropdown.Option("Ml"),
                ft.dropdown.Option("Caja"),
                ft.dropdown.Option("Paquete"),
            ],
            value=producto.get('unidad_medida', 'Unidad') if producto else "Unidad",
            expand=True
        )

        # INFORMACIÓN ADICIONAL
        marca_field = ft.TextField(
            label="Marca",
            hint_text="Ej: Optimum Nutrition",
            helper_text="Marca o fabricante del producto (opcional)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            expand=True,
            value=producto.get('marca', '') if producto else ''
        )

        fecha_vencimiento_field = ft.TextField(
            label="Fecha de Vencimiento",
            hint_text="YYYY-MM-DD (Ej: 2025-12-31)",
            helper_text="Fecha de caducidad del producto en formato Año-Mes-Día (opcional)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            expand=True,
            value=producto.get('fecha_vencimiento', '') if producto else ''
        )

        lote_field = ft.TextField(
            label="Lote",
            hint_text="Ej: LOT-2025-001",
            helper_text="Número de lote para control de inventario (opcional)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            expand=True,
            value=producto.get('lote', '') if producto else ''
        )

        imagen_url_field = ft.TextField(
            label="URL de Imagen",
            hint_text="https://ejemplo.com/imagen.jpg",
            helper_text="Link de la imagen del producto (opcional, para mostrar en catálogo)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            expand=True,
            value=producto.get('imagen_url', '') if producto else ''
        )

        # IMPUESTOS
        aplica_iva_checkbox = ft.Checkbox(
            label="Aplica IVA",
            value=producto.get('aplica_iva', True) if producto else True,
            fill_color=Theme.PRIMARY
        )

        porcentaje_iva_field = ft.TextField(
            label="% IVA",
            hint_text="16.0",
            helper_text="Porcentaje de IVA que se aplica al producto",
            value=str(producto.get('porcentaje_iva', 16.0)) if producto else "16.0",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            width=100
        )

        # VISIBILIDAD
        es_visible_checkbox = ft.Checkbox(
            label="Visible en tienda",
            value=producto.get('es_visible', True) if producto else True,
            fill_color=Theme.PRIMARY
        )

        es_destacado_checkbox = ft.Checkbox(
            label="Producto destacado",
            value=producto.get('es_destacado', False) if producto else False,
            fill_color=Theme.PRIMARY
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
            value=producto.get('estado', 'Activo') if producto else "Activo",
            expand=True,
            visible=es_edicion
        )

        def on_save_dialog(e):
            """Guardar producto desde el diálogo"""
            print(f"DEBUG: on_save_dialog llamado, es_edicion={es_edicion}")

            # Limpiar errores
            sku_field.error_text = None
            nombre_field.error_text = None
            precio_costo_field.error_text = None
            precio_venta_field.error_text = None
            categoria_dropdown.error_text = None

            # VALIDAR CAMPOS REQUERIDOS
            if not sku_field.value or not sku_field.value.strip():
                sku_field.error_text = "El SKU es requerido"
                sku_field.update()
                print("DEBUG: SKU vacío")
                return

            if not nombre_field.value or not nombre_field.value.strip():
                nombre_field.error_text = "El nombre es requerido"
                nombre_field.update()
                print("DEBUG: Nombre vacío")
                return

            if not categoria_dropdown.value:
                categoria_dropdown.error_text = "Seleccione una categoría"
                categoria_dropdown.update()
                print("DEBUG: Categoría no seleccionada")
                return

            if not precio_costo_field.value or not precio_costo_field.value.strip():
                precio_costo_field.error_text = "El precio costo es requerido"
                precio_costo_field.update()
                print("DEBUG: Precio costo vacío")
                return

            if not precio_venta_field.value or not precio_venta_field.value.strip():
                precio_venta_field.error_text = "El precio venta es requerido"
                precio_venta_field.update()
                print("DEBUG: Precio venta vacío")
                return

            # VALIDAR PRECIOS
            try:
                precio_costo = float(precio_costo_field.value)
                precio_venta = float(precio_venta_field.value)

                if precio_costo < 0:
                    precio_costo_field.error_text = "El precio debe ser positivo"
                    precio_costo_field.update()
                    return

                if precio_venta < 0:
                    precio_venta_field.error_text = "El precio debe ser positivo"
                    precio_venta_field.update()
                    return

                # Validación importante: precio_venta >= precio_costo
                if precio_venta < precio_costo:
                    precio_venta_field.error_text = "El precio de venta no puede ser menor al costo"
                    precio_venta_field.update()
                    return

            except ValueError:
                mostrar_error(page, "Los precios deben ser números válidos")
                return

            # VALIDAR PRECIOS ESPECIALES (si se proporcionan)
            # Validar precio_miembro
            if precio_miembro_field.value and precio_miembro_field.value.strip():
                try:
                    precio_miembro = float(precio_miembro_field.value)
                    if precio_miembro < 0:
                        precio_miembro_field.error_text = "El precio debe ser positivo"
                        precio_miembro_field.update()
                        return

                    # IMPORTANTE: El precio para miembros debe ser menor al precio de venta
                    if precio_miembro >= precio_venta:
                        precio_miembro_field.error_text = "El precio para miembros debe ser menor al precio de venta"
                        precio_miembro_field.update()
                        return
                except ValueError:
                    precio_miembro_field.error_text = "El precio debe ser un número válido"
                    precio_miembro_field.update()
                    return

            # Validar precio_mayorista
            if precio_mayorista_field.value and precio_mayorista_field.value.strip():
                try:
                    precio_mayorista = float(precio_mayorista_field.value)
                    if precio_mayorista < 0:
                        precio_mayorista_field.error_text = "El precio debe ser positivo"
                        precio_mayorista_field.update()
                        return

                    # El precio mayorista también debe ser menor al precio de venta
                    if precio_mayorista >= precio_venta:
                        precio_mayorista_field.error_text = "El precio mayorista debe ser menor al precio de venta"
                        precio_mayorista_field.update()
                        return
                except ValueError:
                    precio_mayorista_field.error_text = "El precio debe ser un número válido"
                    precio_mayorista_field.update()
                    return

            # VALIDAR STOCK (si se proporciona)
            stock_minimo = 5
            stock_maximo = 100
            if stock_minimo_field.value and stock_minimo_field.value.strip():
                try:
                    stock_minimo = int(stock_minimo_field.value)
                except ValueError:
                    mostrar_error(page, "El stock mínimo debe ser un número válido")
                    return

            if stock_maximo_field.value and stock_maximo_field.value.strip():
                try:
                    stock_maximo = int(stock_maximo_field.value)
                    if stock_maximo < stock_minimo:
                        mostrar_error(page, "El stock máximo no puede ser menor al stock mínimo")
                        return
                except ValueError:
                    mostrar_error(page, "El stock máximo debe ser un número válido")
                    return

            # Preparar datos según el schema de la API
            data = {
                # REQUERIDOS
                "sku": sku_field.value.strip().upper(),
                "nombre": nombre_field.value.strip(),
                "id_categoria": int(categoria_dropdown.value),
                "precio_costo": precio_costo,
                "precio_venta": precio_venta,

                # OPCIONALES
                "descripcion": descripcion_field.value.strip() if descripcion_field.value and descripcion_field.value.strip() else None,
                "codigo_barras": codigo_barras_field.value.strip() if codigo_barras_field.value and codigo_barras_field.value.strip() else None,

                # Precios opcionales
                "precio_miembro": float(precio_miembro_field.value) if precio_miembro_field.value and precio_miembro_field.value.strip() else None,
                "precio_mayorista": float(precio_mayorista_field.value) if precio_mayorista_field.value and precio_mayorista_field.value.strip() else None,

                # Inventario
                "stock_minimo": stock_minimo,
                "stock_maximo": stock_maximo,
                "unidad_medida": unidad_medida_dropdown.value if unidad_medida_dropdown.value else "Unidad",

                # Información adicional
                "marca": marca_field.value.strip() if marca_field.value and marca_field.value.strip() else None,
                "fecha_vencimiento": fecha_vencimiento_field.value if fecha_vencimiento_field.value and fecha_vencimiento_field.value.strip() else None,
                "lote": lote_field.value.strip() if lote_field.value and lote_field.value.strip() else None,
                "imagen_url": imagen_url_field.value.strip() if imagen_url_field.value and imagen_url_field.value.strip() else None,

                # Impuestos
                "aplica_iva": aplica_iva_checkbox.value,
                "porcentaje_iva": float(porcentaje_iva_field.value) if porcentaje_iva_field.value else 16.0,

                # Visibilidad
                "es_visible": es_visible_checkbox.value,
                "es_destacado": es_destacado_checkbox.value,
            }

            try:
                if es_edicion:
                    # Actualizar
                    print(f"DEBUG: Actualizando producto ID={producto['id']}")
                    print(f"DEBUG: Data a enviar={data}")
                    data['estado'] = estado_dropdown.value
                    resultado = api.actualizar_producto(producto['id'], data)
                    print(f"DEBUG: Resultado de actualización={resultado}")
                    page.close(dialog)
                    mostrar_exito(page, f"Producto '{data['nombre']}' actualizado correctamente")
                else:
                    # Crear
                    print(f"DEBUG: Creando nuevo producto")
                    print(f"DEBUG: Data a enviar={data}")
                    nuevo_producto = api.crear_producto(data)
                    print(f"DEBUG: Producto creado={nuevo_producto}")

                    # Registrar stock inicial si se proporcionó
                    if stock_field.value and stock_field.value.strip():
                        try:
                            stock_inicial = int(stock_field.value)
                            if stock_inicial > 0:
                                print(f"DEBUG: Registrando stock inicial={stock_inicial}")
                                api.registrar_entrada_inventario(
                                    producto_id=nuevo_producto['id'],
                                    cantidad=stock_inicial,
                                    costo_unitario=precio_costo,
                                    lote=lote_field.value if lote_field.value else None,
                                    fecha_vencimiento=fecha_vencimiento_field.value if fecha_vencimiento_field.value else None,
                                    motivo="Stock inicial"
                                )
                        except ValueError:
                            print(f"Error: stock_inicial no es un número válido")

                    page.close(dialog)
                    mostrar_exito(page, f"Producto '{data['nombre']}' creado correctamente")

                print("DEBUG: Recargando productos...")
                load_productos(update_ui=False)
                update_view()
                print("DEBUG: Productos recargados")

            except Exception as ex:
                # No cerrar el diálogo si hay error, para que el usuario vea qué falló
                print(f"ERROR: Excepción al guardar: {ex}")
                import traceback
                traceback.print_exc()
                mostrar_error(page, f"Error al guardar: {str(ex)}")

        # Crear contenido del diálogo con scroll
        dialog_content = ft.Container(
            content=ft.Column([
                # Información de ayuda general
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=Theme.INFO),
                        ft.Text(
                            "Los campos marcados con * son obligatorios. Coloca el cursor sobre cada campo para ver su descripción completa.",
                            size=Theme.FONT_SIZE["xs"],
                            color=Theme.TEXT_SECONDARY,
                            expand=True
                        ),
                    ], spacing=8),
                    bgcolor=f"{Theme.INFO}15",
                    padding=Theme.SPACING["sm"],
                    border_radius=Theme.RADIUS["sm"],
                    border=ft.border.all(1, f"{Theme.INFO}50")
                ),

                # SECCIÓN: Identificación
                ft.Text("📋 Identificación", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Row([sku_field, codigo_barras_field], spacing=Theme.SPACING["md"]),
                ft.Row([nombre_field, categoria_dropdown], spacing=Theme.SPACING["md"]),
                descripcion_field,

                # SECCIÓN: Precios
                ft.Container(height=Theme.SPACING["sm"]),
                ft.Text("💰 Precios", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Row([precio_costo_field, precio_venta_field], spacing=Theme.SPACING["md"]),
                ft.Row([precio_miembro_field, precio_mayorista_field], spacing=Theme.SPACING["md"]),

                # SECCIÓN: Inventario
                ft.Container(height=Theme.SPACING["sm"]),
                ft.Text("📦 Inventario", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Row([
                    stock_field if not es_edicion else ft.Container(),
                    stock_minimo_field,
                    stock_maximo_field,
                    unidad_medida_dropdown,
                ], spacing=Theme.SPACING["md"]),

                # SECCIÓN: Información Adicional
                ft.Container(height=Theme.SPACING["sm"]),
                ft.Text("ℹ️ Información Adicional", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Row([marca_field, fecha_vencimiento_field], spacing=Theme.SPACING["md"]),
                ft.Row([lote_field, imagen_url_field], spacing=Theme.SPACING["md"]),

                # SECCIÓN: Configuración
                ft.Container(height=Theme.SPACING["sm"]),
                ft.Text("⚙️ Configuración", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            aplica_iva_checkbox,
                            ft.Row([
                                ft.Text("Porcentaje:", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                                porcentaje_iva_field,
                            ], spacing=8),
                        ], spacing=8),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            es_visible_checkbox,
                            es_destacado_checkbox,
                        ], spacing=8),
                        expand=True
                    ),
                    estado_dropdown if es_edicion else ft.Container(expand=True),
                ], spacing=Theme.SPACING["md"]),

            ], tight=True, spacing=Theme.SPACING["md"], scroll=ft.ScrollMode.AUTO),
            width=900,
            height=700
        )

        # Crear diálogo
        dialog = ft.AlertDialog(
            title=ft.Text(
                f"{'Editar' if es_edicion else 'Nuevo'} Producto",
                color=Theme.TEXT_PRIMARY,
                size=Theme.FONT_SIZE["xl"],
                weight=Theme.FONT_WEIGHT["bold"]
            ),
            content=dialog_content,
            actions=[
                create_outlined_button("Cancelar", lambda _: page.close(dialog), icon=ft.Icons.CLOSE),
                create_primary_button(
                    "Actualizar" if es_edicion else "Crear",
                    on_save_dialog,
                    icon=ft.Icons.SAVE if es_edicion else ft.Icons.ADD
                ),
            ],
            bgcolor=Theme.CARD_BG,
        )

        page.open(dialog)

    # ==========================================
    # FUNCIONES CRUD (Simplificadas - usan el diálogo)
    # ==========================================
    def editar_producto(producto):
        """Abrir diálogo para editar producto - Obtiene datos completos primero"""
        try:
            # IMPORTANTE: Obtener TODOS los datos del producto desde el backend
            # La lista de productos puede no incluir todos los campos opcionales
            producto_completo = api.get_producto_by_id(producto['id'])
            if producto_completo:
                abrir_dialogo_producto(producto_completo)
            else:
                mostrar_error(page, f"No se pudo cargar el producto {producto['nombre']}")
        except Exception as ex:
            mostrar_error(page, f"Error al cargar producto: {str(ex)}")

    def confirm_delete_producto(producto):
        """Confirmar activación o desactivación de producto"""
        def on_cambiar_estado(e):
            """Cambiar estado del producto (Activo <-> Inactivo)"""
            try:
                # Obtener todos los datos del producto primero
                producto_completo = api.get_producto_by_id(producto['id'])

                if not producto_completo:
                    mostrar_error(page, "No se pudo obtener la información del producto")
                    return

                # Buscar id_categoria si no está presente
                id_categoria = producto_completo.get('id_categoria')
                if not id_categoria and 'nombre_categoria' in producto_completo:
                    for cat in categorias_list:
                        if cat['nombre'] == producto_completo['nombre_categoria']:
                            id_categoria = cat['id']
                            break

                # Determinar nuevo estado
                estado_actual = producto.get('estado', 'Activo')
                nuevo_estado = 'Inactivo' if estado_actual == 'Activo' else 'Activo'

                data = {
                    'sku': producto_completo.get('sku'),
                    'nombre': producto_completo.get('nombre'),
                    'id_categoria': id_categoria,
                    'precio_costo': producto_completo.get('precio_costo', 0),
                    'precio_venta': producto_completo.get('precio_venta', 0),
                    'estado': nuevo_estado
                }
                api.actualizar_producto(producto['id'], data)
                page.close(dialog)

                if nuevo_estado == 'Activo':
                    mostrar_exito(page, f"✅ Producto '{producto['nombre']}' activado correctamente.\n\nEl producto ahora aparecerá en ventas y catálogo.")
                else:
                    mostrar_exito(page, f"⏸️ Producto '{producto['nombre']}' desactivado correctamente.\n\nEl producto ya no aparecerá en ventas pero se mantiene su historial.")

                load_productos(update_ui=False)
                update_view()
            except Exception as ex:
                page.close(dialog)
                mostrar_error(page, f"Error al cambiar estado: {str(ex)}")

        # Determinar si el producto está activo o inactivo
        esta_activo = producto.get('estado', 'Activo') == 'Activo'

        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.SETTINGS, size=Theme.ICON_SIZE["md"], color=Theme.WARNING),
                ft.Text(
                    f"Gestionar Estado: {producto['nombre']}",
                    color=Theme.TEXT_PRIMARY,
                    size=Theme.FONT_SIZE["lg"],
                    expand=True
                ),
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=Theme.INFO),
                            ft.Text(
                                "Los productos NO se eliminan del sistema para preservar el historial, reportes y datos de ventas. Puedes activar o desactivar productos según sea necesario.",
                                size=Theme.FONT_SIZE["sm"],
                                color=Theme.TEXT_SECONDARY,
                                expand=True
                            ),
                        ], spacing=8),
                        bgcolor=f"{Theme.INFO}15",
                        padding=Theme.SPACING["sm"],
                        border_radius=Theme.RADIUS["sm"],
                        border=ft.border.all(1, f"{Theme.INFO}50")
                    ),
                    ft.Container(height=Theme.SPACING["md"]),
                    ft.Row([
                        ft.Text(
                            "Estado actual:",
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.TEXT_SECONDARY,
                            weight=Theme.FONT_WEIGHT["bold"]
                        ),
                        create_status_badge(
                            producto.get('estado', 'Activo'),
                            status="success" if esta_activo else "error"
                        ),
                    ], spacing=8),
                    ft.Container(height=Theme.SPACING["md"]),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(
                                    ft.Icons.CHECK_CIRCLE if not esta_activo else ft.Icons.PAUSE_CIRCLE,
                                    color=Theme.SUCCESS if not esta_activo else Theme.WARNING,
                                    size=24
                                ),
                                ft.Text(
                                    "ACTIVAR PRODUCTO" if not esta_activo else "DESACTIVAR PRODUCTO",
                                    weight=Theme.FONT_WEIGHT["bold"],
                                    color=Theme.SUCCESS if not esta_activo else Theme.WARNING,
                                    size=Theme.FONT_SIZE["md"]
                                ),
                            ], spacing=8),
                            ft.Container(height=4),
                            ft.Text(
                                "✓ El producto aparecerá en ventas y catálogo\n✓ Estará disponible para clientes\n✓ Se incluirá en reportes de productos activos\n✓ Mantiene todo su historial y datos" if not esta_activo else "✓ El producto se ocultará de ventas y catálogo\n✓ No estará disponible para nuevas ventas\n✓ Mantiene TODO su historial, datos y movimientos\n✓ Puedes reactivarlo cuando quieras sin perder nada",
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_SECONDARY
                            ),
                        ], spacing=4),
                        padding=Theme.SPACING["md"],
                        bgcolor=f"{Theme.SUCCESS if not esta_activo else Theme.WARNING}15",
                        border_radius=Theme.RADIUS["sm"],
                        border=ft.border.all(2, f"{Theme.SUCCESS if not esta_activo else Theme.WARNING}80")
                    ),
                ], tight=True, spacing=Theme.SPACING["sm"]),
                width=500
            ),
            actions=[
                create_outlined_button("Cancelar", lambda _: page.close(dialog), icon=ft.Icons.CLOSE),
                create_primary_button(
                    "✅ Activar Producto" if not esta_activo else "⏸️ Desactivar Producto",
                    on_cambiar_estado,
                    icon=ft.Icons.CHECK_CIRCLE if not esta_activo else ft.Icons.PAUSE_CIRCLE
                ),
            ],
            bgcolor=Theme.CARD_BG,
        )
        page.open(dialog)

    def ajustar_stock(producto):
        """Ajustar stock de un producto - Usando métodos específicos de la API"""
        cantidad_field = ft.TextField(
            label="Cantidad",
            hint_text="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True,
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY
        )

        tipo_dropdown = ft.Dropdown(
            label="Tipo de Movimiento",
            options=[
                ft.dropdown.Option("Entrada"),
                ft.dropdown.Option("Salida"),
                ft.dropdown.Option("Ajuste"),
                ft.dropdown.Option("Merma"),
            ],
            value="Entrada",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY
        )

        motivo_field = ft.TextField(
            label="Motivo * (mínimo 5 caracteres)",
            hint_text="Ej: Compra de proveedor, Venta, Conteo físico, Producto vencido",
            helper_text="Describe el motivo del movimiento de inventario (mínimo 5 caracteres)",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY
        )


        def on_save_stock(e):
            print(f"DEBUG: on_save_stock llamado para producto ID={producto['id']}")
            try:
                if not cantidad_field.value or not cantidad_field.value.strip():
                    print("DEBUG: Cantidad vacía")
                    mostrar_error(page, "La cantidad es requerida")
                    return

                cantidad = int(cantidad_field.value)
                tipo = tipo_dropdown.value
                print(f"DEBUG: Tipo={tipo}, Cantidad={cantidad}")

                # Para "Ajuste", permitir 0 (ajustar stock a 0)
                # Para otros tipos (Entrada, Salida, Merma), debe ser mayor a 0
                if tipo == "Ajuste":
                    if cantidad < 0:
                        print("DEBUG: Cantidad negativa para Ajuste")
                        mostrar_error(page, "El stock nuevo no puede ser negativo")
                        return
                else:
                    if cantidad <= 0:
                        print(f"DEBUG: Cantidad <= 0 para {tipo}")
                        mostrar_error(page, "La cantidad debe ser mayor a 0")
                        return

                if not motivo_field.value or not motivo_field.value.strip():
                    print("DEBUG: Motivo vacío")
                    mostrar_error(page, "El motivo es requerido")
                    return

                motivo = motivo_field.value.strip()

                # Validar longitud mínima del motivo (frontend requiere mínimo 5 caracteres)
                if len(motivo) < 5:
                    print(f"DEBUG: Motivo muy corto: {len(motivo)} caracteres")
                    mostrar_error(page, f"El motivo debe tener al menos 5 caracteres (actualmente tiene {len(motivo)})")
                    return

                print(f"DEBUG: Motivo={motivo}")

                # Usar los métodos específicos de la API según el tipo
                if tipo == "Entrada":
                    print(f"DEBUG: Llamando registrar_entrada_inventario")
                    resultado = api.registrar_entrada_inventario(
                        producto_id=producto['id'],
                        cantidad=cantidad,
                        costo_unitario=producto.get('precio_costo'),
                        motivo=motivo
                    )
                    print(f"DEBUG: Resultado Entrada={resultado}")
                elif tipo == "Salida":
                    print(f"DEBUG: Llamando registrar_salida_inventario")
                    resultado = api.registrar_salida_inventario(
                        producto_id=producto['id'],
                        cantidad=cantidad,
                        motivo=motivo
                    )
                    print(f"DEBUG: Resultado Salida={resultado}")
                elif tipo == "Ajuste":
                    # Para ajuste, la cantidad es el nuevo stock total
                    print(f"DEBUG: Llamando ajustar_inventario con stock_nuevo={cantidad}")
                    resultado = api.ajustar_inventario(
                        producto_id=producto['id'],
                        stock_nuevo=cantidad,
                        motivo=motivo
                    )
                    print(f"DEBUG: Resultado Ajuste={resultado}")
                elif tipo == "Merma":
                    print(f"DEBUG: Llamando registrar_merma")
                    resultado = api.registrar_merma(
                        producto_id=producto['id'],
                        cantidad=cantidad,
                        motivo=motivo
                    )
                    print(f"DEBUG: Resultado Merma={resultado}")

                # Cerrar el diálogo primero, luego mostrar mensaje de éxito
                print("DEBUG: Cerrando diálogo...")
                page.close(dialog)
                print("DEBUG: Mostrando mensaje de éxito...")
                mostrar_exito(page, f"Stock actualizado correctamente para {tipo}")
                print("DEBUG: Recargando productos...")
                load_productos(update_ui=False)
                update_view()
                print("DEBUG: Stock actualizado exitosamente")

            except ValueError as ve:
                # No cerrar el diálogo si hay error de validación del backend
                print(f"ERROR ValueError: {ve}")
                import traceback
                traceback.print_exc()
                mostrar_error(page, str(ve))
            except Exception as ex:
                # No cerrar el diálogo si hay error genérico
                print(f"ERROR Exception: {ex}")
                import traceback
                traceback.print_exc()
                mostrar_error(page, f"Error: {str(ex)}")

        dialog = ft.AlertDialog(
            title=ft.Text(f"Ajustar Stock: {producto['nombre']}", color=Theme.TEXT_PRIMARY),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Stock actual:", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ft.Text(
                                str(producto.get('stock_actual', 0)),
                                size=Theme.FONT_SIZE["xl"],
                                weight=Theme.FONT_WEIGHT["bold"],
                                color=Theme.PRIMARY
                            ),
                        ], spacing=4),
                        bgcolor=f"{Theme.PRIMARY}15",
                        padding=Theme.SPACING["md"],
                        border_radius=Theme.RADIUS["sm"]
                    ),
                    tipo_dropdown,
                    cantidad_field,
                    motivo_field,
                    ft.Container(
                        content=ft.Text(
                            "💡 Ajuste: establece stock a un valor específico\n💡 Entrada/Salida: suma o resta del stock actual\n💡 Merma: registra pérdidas (vencido/dañado)",
                            size=Theme.FONT_SIZE["xs"],
                            color=Theme.TEXT_SECONDARY,
                            text_align=ft.TextAlign.LEFT
                        ),
                        bgcolor=f"{Theme.WARNING}15",
                        padding=Theme.SPACING["sm"],
                        border_radius=Theme.RADIUS["sm"],
                        border=ft.border.all(1, f"{Theme.WARNING}50")
                    ),
                ], tight=True, spacing=Theme.SPACING["md"]),
                width=450
            ),
            actions=[
                create_outlined_button("Cancelar", lambda _: page.close(dialog)),
                create_primary_button("Guardar", on_save_stock, icon=ft.Icons.SAVE),
            ],
            bgcolor=Theme.CARD_BG,
        )
        page.open(dialog)

    def ver_detalles_producto(producto):
        """Ver detalles completos del producto"""
        # Formatear precios opcionales
        precio_miembro = f"S/ {producto.get('precio_miembro'):.2f}" if producto.get('precio_miembro') else 'N/A'
        precio_mayorista = f"S/ {producto.get('precio_mayorista'):.2f}" if producto.get('precio_mayorista') else 'N/A'

        detalles_text = f"""
📦 INFORMACIÓN GENERAL
━━━━━━━━━━━━━━━━━━━━━━━
SKU: {producto.get('sku', 'N/A')}
Código de Barras: {producto.get('codigo_barras', 'N/A')}
Nombre: {producto['nombre']}
Descripción: {producto.get('descripcion', 'Sin descripción')}
Categoría: {producto.get('nombre_categoria', 'Sin categoría')}
Marca: {producto.get('marca', 'N/A')}

💰 PRECIOS
━━━━━━━━━━━━━━━━━━━━━━━
Costo: S/ {producto.get('precio_costo', 0):.2f}
Venta: S/ {producto.get('precio_venta', 0):.2f}
Miembro: {precio_miembro}
Mayorista: {precio_mayorista}

📊 INVENTARIO
━━━━━━━━━━━━━━━━━━━━━━━
Stock Actual: {producto.get('stock_actual', 0)} {producto.get('unidad_medida', 'unidades')}
Stock Mínimo: {producto.get('stock_minimo', 0)}
Stock Máximo: {producto.get('stock_maximo', 0)}
Unidad: {producto.get('unidad_medida', 'Unidad')}

📝 INFORMACIÓN ADICIONAL
━━━━━━━━━━━━━━━━━━━━━━━
Estado: {producto.get('estado', 'Activo')}
Visible en tienda: {'Sí' if producto.get('es_visible', True) else 'No'}
Producto destacado: {'Sí' if producto.get('es_destacado', False) else 'No'}
Aplica IVA: {'Sí' if producto.get('aplica_iva', True) else 'No'} ({producto.get('porcentaje_iva', 16)}%)
Lote: {producto.get('lote', 'N/A')}
Fecha Vencimiento: {producto.get('fecha_vencimiento', 'N/A')}
"""

        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.INFO, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                ft.Text(f"Detalles: {producto['nombre']}", color=Theme.TEXT_PRIMARY, expand=True),
            ]),
            content=ft.Container(
                content=ft.Text(
                    detalles_text,
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_PRIMARY,
                    font_family="Courier New"
                ),
                width=600,
                height=500,
                padding=Theme.SPACING["md"]
            ),
            actions=[
                create_outlined_button("Cerrar", lambda _: page.close(dialog)),
                create_primary_button("Editar", lambda _: [page.close(dialog), editar_producto(producto)], icon=ft.Icons.EDIT),
            ],
            bgcolor=Theme.CARD_BG,
        )
        page.open(dialog)

    def ver_historial_producto(producto):
        """Ver historial de movimientos de inventario del producto"""
        try:
            print(f"DEBUG: Obteniendo historial para producto ID={producto['id']}")
            # Obtener movimientos de inventario del backend
            movimientos = api.get_movimientos_inventario(producto['id'], limit=50)
            print(f"DEBUG: Movimientos obtenidos: {len(movimientos)}")

            # Crear lista de movimientos
            movimientos_list = ft.Column(
                spacing=Theme.SPACING["xs"],
                scroll=ft.ScrollMode.AUTO,
                height=400
            )

            # Encabezado
            movimientos_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Producto: {producto['nombre']}", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"]),
                        ft.Text(f"SKU: {producto.get('sku', 'N/A')}", size=Theme.FONT_SIZE["sm"]),
                        ft.Text(f"Stock Actual: {producto.get('stock_actual', 0)} {producto.get('unidad_medida', 'unidades')}",
                               size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                    ], spacing=4),
                    bgcolor=f"{Theme.PRIMARY}15",
                    padding=Theme.SPACING["md"],
                    border_radius=Theme.RADIUS["sm"],
                    margin=ft.margin.only(bottom=Theme.SPACING["sm"])
                )
            )

            if not movimientos:
                movimientos_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INBOX, size=48, color=Theme.TEXT_SECONDARY),
                            ft.Text("No hay movimientos registrados", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                        padding=Theme.SPACING["xl"],
                        alignment=ft.alignment.center
                    )
                )
            else:
                from ui.utils.datetime_utils import parse_datetime_from_api, format_datetime_display

                for mov in movimientos:
                    tipo = mov.get('tipo_movimiento', 'Desconocido')
                    cantidad = mov.get('cantidad', 0)
                    fecha = mov.get('fecha_creacion', '')
                    motivo = mov.get('motivo', 'Sin motivo')
                    stock_anterior = mov.get('stock_anterior', 0)
                    stock_nuevo = mov.get('stock_nuevo', 0)

                    # Icono, color y descripción según tipo
                    if tipo == "Entrada":
                        icono = ft.Icons.ADD_CIRCLE
                        color = Theme.SUCCESS
                        signo = "+"
                        descripcion = "Incremento de inventario (compra, devolución, reabastecimiento)"
                    elif tipo == "Salida":
                        icono = ft.Icons.REMOVE_CIRCLE
                        color = Theme.ERROR
                        signo = "-"
                        descripcion = "Disminución de inventario (venta, consumo, despacho)"
                    elif tipo == "Ajuste":
                        icono = ft.Icons.TUNE
                        color = Theme.WARNING
                        signo = "="
                        descripcion = "Corrección manual de stock (conteo físico, inventario)"
                    elif tipo == "Merma":
                        icono = ft.Icons.DELETE_OUTLINE
                        color = "#FF6B6B"
                        signo = "-"
                        descripcion = "Pérdida de inventario (producto vencido, dañado, robado)"
                    else:
                        icono = ft.Icons.HELP_OUTLINE
                        color = Theme.TEXT_SECONDARY
                        signo = ""
                        descripcion = "Movimiento no especificado"

                    # Formatear fecha usando zona horaria local del sistema
                    try:
                        fecha_dt = parse_datetime_from_api(fecha)
                        fecha_formateada = format_datetime_display(fecha_dt, include_seconds=False)
                    except:
                        fecha_formateada = fecha[:16] if len(fecha) > 16 else fecha

                    movimientos_list.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(icono, color=color, size=20),
                                ft.Column([
                                    ft.Row([
                                        ft.Text(tipo, size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=color),
                                        ft.Text(f"{signo}{cantidad}", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=color),
                                    ], spacing=4),
                                    ft.Text(descripcion, size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY, italic=True),
                                    ft.Text(motivo, size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_PRIMARY),
                                    ft.Text(f"Stock: {stock_anterior} → {stock_nuevo}  •  {fecha_formateada}",
                                           size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                                ], spacing=2, expand=True),
                            ], spacing=8),
                            bgcolor=Theme.CARD_BG,
                            padding=Theme.SPACING["sm"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT),
                            border_radius=Theme.RADIUS["sm"],
                        )
                    )

            dialog = ft.AlertDialog(
                title=ft.Row([
                    ft.Icon(ft.Icons.HISTORY, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Historial de Inventario", color=Theme.TEXT_PRIMARY, expand=True),
                ]),
                content=ft.Container(
                    content=movimientos_list,
                    width=650,
                    padding=Theme.SPACING["sm"]
                ),
                actions=[
                    create_outlined_button("Cerrar", lambda _: page.close(dialog)),
                    create_primary_button("Ajustar Stock", lambda _: [page.close(dialog), ajustar_stock(producto)], icon=ft.Icons.ADD_BOX),
                ],
                bgcolor=Theme.CARD_BG,
            )
            page.open(dialog)
        except Exception as e:
            print(f"ERROR: Error al cargar historial: {e}")
            import traceback
            traceback.print_exc()
            mostrar_error(page, f"Error al cargar historial: {str(e)}")

    def duplicar_producto(producto):
        """Duplicar un producto existente con nuevo SKU"""
        # Crear una copia del producto pero SIN el ID (para que se trate como nuevo)
        producto_copiado = producto.copy()

        # IMPORTANTE: Eliminar el ID para que se cree como producto nuevo
        if 'id' in producto_copiado:
            del producto_copiado['id']

        # Generar nuevo SKU agregando "-COPY" al final
        producto_copiado['sku'] = f"{producto['sku']}-COPY"
        producto_copiado['nombre'] = f"{producto['nombre']} (Copia)"

        # Resetear el stock a 0 para que el usuario ingrese el stock inicial
        producto_copiado['stock_actual'] = 0

        # Abrir el diálogo de producto con los datos copiados (será tratado como creación)
        abrir_dialogo_producto(producto_copiado)

    def gestionar_categorias_dialog(e):
        """Diálogo para gestionar categorías (crear, editar, eliminar)"""
        print(f"DEBUG: gestionar_categorias_dialog llamado con e={e}")
        # Recargar categorías
        load_categorias()

        # Contenedor para la lista de categorías
        categorias_container = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO)

        def actualizar_lista_categorias():
            """Actualizar la lista de categorías en el diálogo"""
            categorias_container.controls.clear()

            if not categorias_list:
                categorias_container.controls.append(
                    create_empty_state(
                        message="No hay categorías",
                        icon=ft.Icons.CATEGORY,
                        secondary_message="Crea tu primera categoría"
                    )
                )
            else:
                for cat in categorias_list:
                    categorias_container.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CATEGORY, size=20, color=Theme.PRIMARY),
                                ft.Column([
                                    ft.Text(
                                        cat['nombre'],
                                        size=Theme.FONT_SIZE["md"],
                                        weight=Theme.FONT_WEIGHT["bold"],
                                        color=Theme.TEXT_PRIMARY
                                    ),
                                    ft.Text(
                                        cat.get('descripcion', 'Sin descripción'),
                                        size=Theme.FONT_SIZE["xs"],
                                        color=Theme.TEXT_SECONDARY
                                    ),
                                ], spacing=2, expand=True),
                                create_icon_button(
                                    ft.Icons.EDIT,
                                    lambda e, c=cat: editar_categoria(c),
                                    tooltip="Editar",
                                    color=Theme.INFO
                                ),
                                create_icon_button(
                                    ft.Icons.BLOCK,
                                    lambda e, c=cat: confirmar_eliminar_categoria(c),
                                    tooltip="Desactivar",
                                    color=Theme.WARNING
                                ),
                            ], spacing=Theme.SPACING["md"]),
                            padding=Theme.SPACING["md"],
                            bgcolor=Theme.CARD_BG,
                            border_radius=Theme.RADIUS["md"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT)
                        )
                    )

            # Solo actualizar si ya está en la página
            try:
                categorias_container.update()
            except AssertionError:
                pass  # El control aún no está en la página, se actualizará cuando se agregue

        def crear_categoria(e):
            """Crear nueva categoría"""
            nombre_cat_field = ft.TextField(
                label="Nombre de la categoría *",
                hint_text="Ej: Suplementos, Accesorios, Bebidas",
                autofocus=True,
                border_color=Theme.BORDER_DEFAULT,
                focused_border_color=Theme.PRIMARY
            )

            desc_cat_field = ft.TextField(
                label="Descripción",
                hint_text="Descripción de la categoría (opcional)",
                multiline=True,
                min_lines=2,
                border_color=Theme.BORDER_DEFAULT,
                focused_border_color=Theme.PRIMARY
            )

            def on_save(e):
                if not nombre_cat_field.value or not nombre_cat_field.value.strip():
                    nombre_cat_field.error_text = "El nombre es requerido"
                    nombre_cat_field.update()
                    return

                try:
                    api.crear_categoria(
                        nombre=nombre_cat_field.value.strip(),
                        descripcion=desc_cat_field.value.strip() if desc_cat_field.value else ""
                    )
                    page.close(crear_dialog)
                    mostrar_exito(page, "Categoría creada correctamente")

                    # Recargar categorías desde el backend
                    load_categorias()
                    # Actualizar la lista en el diálogo de gestión
                    actualizar_lista_categorias()

                except Exception as ex:
                    # No cerrar el diálogo si hay error
                    mostrar_error(page, f"Error: {str(ex)}")

            crear_dialog = ft.AlertDialog(
                title=ft.Text("Nueva Categoría", color=Theme.TEXT_PRIMARY),
                content=ft.Container(
                    content=ft.Column([
                        nombre_cat_field,
                        desc_cat_field,
                    ], tight=True, spacing=Theme.SPACING["md"]),
                    width=400
                ),
                actions=[
                    create_outlined_button("Cancelar", lambda _: page.close(crear_dialog)),
                    create_primary_button("Crear", on_save, icon=ft.Icons.ADD),
                ],
                bgcolor=Theme.CARD_BG,
            )
            page.open(crear_dialog)

        def editar_categoria(categoria):
            """Editar categoría existente"""
            nombre_cat_field = ft.TextField(
                label="Nombre de la categoría *",
                value=categoria['nombre'],
                border_color=Theme.BORDER_DEFAULT,
                focused_border_color=Theme.PRIMARY
            )

            desc_cat_field = ft.TextField(
                label="Descripción",
                value=categoria.get('descripcion', ''),
                multiline=True,
                min_lines=2,
                border_color=Theme.BORDER_DEFAULT,
                focused_border_color=Theme.PRIMARY
            )

            def on_update(e):
                if not nombre_cat_field.value or not nombre_cat_field.value.strip():
                    nombre_cat_field.error_text = "El nombre es requerido"
                    nombre_cat_field.update()
                    return

                try:
                    # Actualizar la categoría
                    api.actualizar_categoria(
                        categoria_id=categoria['id'],
                        nombre=nombre_cat_field.value.strip(),
                        descripcion=desc_cat_field.value.strip() if desc_cat_field.value else ""
                    )

                    page.close(editar_dialog)
                    mostrar_exito(page, "Categoría actualizada correctamente")

                    # Recargar categorías y productos para que reflejen el nuevo nombre
                    load_categorias()
                    load_productos(update_ui=False)
                    # Actualizar la lista en el diálogo de gestión
                    actualizar_lista_categorias()

                except Exception as ex:
                    # No cerrar el diálogo si hay error
                    mostrar_error(page, f"Error: {str(ex)}")

            editar_dialog = ft.AlertDialog(
                title=ft.Text("Editar Categoría", color=Theme.TEXT_PRIMARY),
                content=ft.Container(
                    content=ft.Column([
                        nombre_cat_field,
                        desc_cat_field,
                    ], tight=True, spacing=Theme.SPACING["md"]),
                    width=400
                ),
                actions=[
                    create_outlined_button("Cancelar", lambda _: page.close(editar_dialog)),
                    create_primary_button("Actualizar", on_update, icon=ft.Icons.SAVE),
                ],
                bgcolor=Theme.CARD_BG,
            )
            page.open(editar_dialog)

        def confirmar_eliminar_categoria(categoria):
            """Confirmar desactivación de categoría y productos asociados"""
            print(f"DEBUG: Confirmando desactivación de categoría ID={categoria['id']}, Nombre={categoria['nombre']}")

            # Contar productos de esta categoría
            productos_categoria = [p for p in productos_list if p.get('id_categoria') == categoria['id'] or p.get('nombre_categoria') == categoria['nombre']]
            num_productos = len(productos_categoria)
            print(f"DEBUG: Productos asociados encontrados: {num_productos}")

            def on_confirm(e):
                print(f"DEBUG: Confirmación aceptada, procediendo a desactivar...")
                try:
                    # Primero desactivar todos los productos de esta categoría
                    productos_desactivados = 0
                    for producto in productos_categoria:
                        try:
                            print(f"DEBUG: Desactivando producto ID={producto['id']}, Nombre={producto['nombre']}")

                            # Obtener datos completos del producto
                            producto_completo = api.get_producto_by_id(producto['id'])

                            if producto_completo:
                                # Actualizar estado a Inactivo
                                data_update = {
                                    'sku': producto_completo.get('sku'),
                                    'nombre': producto_completo.get('nombre'),
                                    'id_categoria': producto_completo.get('id_categoria'),
                                    'precio_costo': producto_completo.get('precio_costo', 0),
                                    'precio_venta': producto_completo.get('precio_venta', 0),
                                    'estado': 'Inactivo'
                                }
                                api.actualizar_producto(producto['id'], data_update)
                                productos_desactivados += 1
                                print(f"DEBUG: Producto desactivado exitosamente")
                        except Exception as ex:
                            print(f"ERROR al desactivar producto {producto['nombre']}: {ex}")

                    # Luego actualizar la categoría a Inactivo
                    print(f"DEBUG: Desactivando categoría ID={categoria['id']}")
                    try:
                        resultado = api.actualizar_categoria(
                            categoria_id=categoria['id'],
                            nombre=categoria['nombre'],
                            descripcion=categoria.get('descripcion', '')
                        )
                        print(f"DEBUG: Categoría desactivada, resultado={resultado}")
                    except Exception as ex:
                        print(f"ADVERTENCIA: No se pudo actualizar la categoría (podría no tener campo estado): {ex}")

                    # Cerrar diálogo primero
                    page.close(confirm_dialog)

                    # Mostrar mensaje de éxito
                    mensaje_exito = f"Categoría '{categoria['nombre']}' desactivada correctamente."
                    if productos_desactivados > 0:
                        mensaje_exito += f"\n{productos_desactivados} producto(s) asociado(s) fueron desactivados."
                    mensaje_exito += f"\n\nLos productos desactivados no aparecerán en el catálogo pero se mantienen en el sistema."
                    mostrar_exito(page, mensaje_exito)

                    # Recargar categorías y productos
                    print(f"DEBUG: Recargando categorías y productos...")
                    load_categorias()
                    load_productos(update_ui=False)
                    # Actualizar la lista en el diálogo de gestión
                    actualizar_lista_categorias()
                    print(f"DEBUG: Desactivación completada exitosamente")

                except Exception as ex:
                    print(f"ERROR FATAL al desactivar categoría: {ex}")
                    import traceback
                    traceback.print_exc()
                    page.close(confirm_dialog)
                    mostrar_error(page, f"Error al desactivar: {str(ex)}")

            mensaje = f"¿Está seguro de desactivar la categoría '{categoria['nombre']}'?"
            if num_productos > 0:
                mensaje += f"\n\n⚠️ ATENCIÓN: Esta categoría tiene {num_productos} producto(s) asociado(s)."
                mensaje += f"\n\nTodos los productos de esta categoría se DESACTIVARÁN automáticamente."
                mensaje += f"\n\nLos productos desactivados no aparecerán en el catálogo pero podrán reactivarse después."

            print(f"DEBUG: Abriendo diálogo de confirmación...")
            confirm_dialog = create_confirmation_dialog(
                page,
                title="⚠️ Desactivar Categoría y Productos",
                message=mensaje,
                on_confirm=on_confirm
            )
            page.open(confirm_dialog)
            print(f"DEBUG: Diálogo de confirmación abierto")

        # Diálogo principal
        def on_close_dialog(e):
            """Cerrar diálogo y actualizar vista principal"""
            page.close(dialog)
            # Actualizar la vista principal para reflejar los cambios en categorías
            update_view()

        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.CATEGORY, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                ft.Text("Gestionar Categorías", color=Theme.TEXT_PRIMARY, expand=True),
                create_primary_button("Nueva", crear_categoria, icon=ft.Icons.ADD),
            ]),
            content=ft.Container(
                content=categorias_container,
                width=600,
                height=400
            ),
            actions=[
                create_outlined_button("Cerrar", on_close_dialog),
            ],
            bgcolor=Theme.CARD_BG,
        )

        # Inicializar lista
        actualizar_lista_categorias()

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

        # Botón para crear nuevo producto
        nuevo_producto_button = create_card_container(
            content=ft.Row([
                ft.Icon(ft.Icons.ADD_BOX, size=Theme.ICON_SIZE["lg"], color=Theme.PRIMARY),
                ft.Column([
                    ft.Text(
                        "Crear Nuevo Producto",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                    ft.Text(
                        "Agrega productos al inventario con toda la información necesaria",
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.TEXT_SECONDARY
                    ),
                ], spacing=4, expand=True),
                create_primary_button(
                    "Nuevo Producto",
                    lambda e: abrir_dialogo_producto(),
                    icon=ft.Icons.ADD
                ),
                create_outlined_button(
                    "Gestionar Categorías",
                    lambda e: gestionar_categorias_dialog(e),
                    icon=ft.Icons.CATEGORY
                ),
            ], spacing=Theme.SPACING["lg"], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=Theme.SPACING["xl"],
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
                ], spacing=Theme.SPACING["md"]),
                ft.Row([
                    codigo_barras_search,
                    sku_search,
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
            nuevo_producto_button,
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

        # Actualizar filtro de categorías ahora que está en la página
        if categorias_list:
            filtro_categoria.options = [ft.dropdown.Option(key="todos", text="Todas las categorías")]
            filtro_categoria.options.extend([
                ft.dropdown.Option(key=str(cat['id']), text=cat['nombre'])
                for cat in categorias_list
            ])
            filtro_categoria.update()

    # Inicializar - Primero cargar datos, luego construir vista
    load_categorias()           # Solo carga datos, no actualiza controles
    load_productos(update_ui=False)  # Solo carga datos, sin actualizar UI
    update_view()               # Construye la vista con los datos cargados
