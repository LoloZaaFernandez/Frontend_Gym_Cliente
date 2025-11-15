"""
Vista de Alertas de Productos - Dashboard de Inventario
Muestra alertas de stock bajo, productos próximos a vencer y sin stock
"""

import flet as ft
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button, create_status_badge, create_icon_button
from ui.components.molecules import create_card_container, create_empty_state, create_stat_card
from ui.utils.messages import mostrar_exito, mostrar_error


def show_alertas_productos_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Dashboard de Alertas de Inventario
    """
    page.title = "BLESSED GYM - Alertas de Inventario"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Estado
    productos_stock_bajo = []
    productos_proximos_vencer = []
    productos_sin_stock = []
    dias_vencimiento = [30]  # Default: 30 días

    # Referencias
    stock_bajo_container = ft.Column(spacing=Theme.SPACING["md"], scroll=ft.ScrollMode.AUTO)
    proximos_vencer_container = ft.Column(spacing=Theme.SPACING["md"], scroll=ft.ScrollMode.AUTO)
    sin_stock_container = ft.Column(spacing=Theme.SPACING["md"], scroll=ft.ScrollMode.AUTO)

    # Stats
    stat_stock_bajo = ft.Ref[ft.Container]()
    stat_proximos_vencer = ft.Ref[ft.Container]()
    stat_sin_stock = ft.Ref[ft.Container]()

    # ==========================================
    # FUNCIONES DE CARGA DE DATOS
    # ==========================================
    def cargar_alertas():
        """Cargar todas las alertas desde la API"""
        nonlocal productos_stock_bajo, productos_proximos_vencer, productos_sin_stock

        try:
            # Cargar stock bajo
            productos_stock_bajo = api.get_productos_stock_bajo()
        except Exception as e:
            print(f"Error al cargar productos con stock bajo: {e}")
            productos_stock_bajo = []

        try:
            # Cargar próximos a vencer
            productos_proximos_vencer = api.get_productos_proximos_vencer(dias=dias_vencimiento[0])
        except Exception as e:
            print(f"Error al cargar productos próximos a vencer: {e}")
            productos_proximos_vencer = []

        try:
            # Cargar sin stock
            productos_sin_stock = api.get_productos_sin_stock()
        except Exception as e:
            print(f"Error al cargar productos sin stock: {e}")
            productos_sin_stock = []

        actualizar_stats()
        actualizar_listas()

    def actualizar_stats():
        """Actualizar tarjetas de estadísticas"""
        if stat_stock_bajo.current:
            stat_stock_bajo.current.content = create_stat_card(
                title="Stock Bajo",
                value=str(len(productos_stock_bajo)),
                icon=ft.Icons.WARNING_AMBER,
                color=Theme.WARNING
            ).content
            stat_stock_bajo.current.update()

        if stat_proximos_vencer.current:
            stat_proximos_vencer.current.content = create_stat_card(
                title=f"Próximos a Vencer ({dias_vencimiento[0]}d)",
                value=str(len(productos_proximos_vencer)),
                icon=ft.Icons.CALENDAR_TODAY,
                color=Theme.ERROR
            ).content
            stat_proximos_vencer.current.update()

        if stat_sin_stock.current:
            stat_sin_stock.current.content = create_stat_card(
                title="Sin Stock",
                value=str(len(productos_sin_stock)),
                icon=ft.Icons.INVENTORY_2,
                color=Theme.ERROR
            ).content
            stat_sin_stock.current.update()

    def crear_producto_card(producto, tipo_alerta):
        """Crear tarjeta de producto con alerta"""
        # Determinar color según tipo de alerta
        if tipo_alerta == "stock_bajo":
            color_alerta = Theme.WARNING
            icono_alerta = ft.Icons.WARNING_AMBER
            mensaje_alerta = f"Stock: {producto.get('stock_actual', 0)} / Mínimo: {producto.get('stock_minimo', 0)}"
        elif tipo_alerta == "vencer":
            color_alerta = Theme.ERROR
            icono_alerta = ft.Icons.CALENDAR_TODAY
            dias = producto.get('dias_para_vencer', 0)
            mensaje_alerta = f"Vence en {dias} días - {producto.get('fecha_vencimiento', 'N/A')}"
        else:  # sin_stock
            color_alerta = Theme.ERROR
            icono_alerta = ft.Icons.INVENTORY_2
            mensaje_alerta = "Producto agotado - Requiere reposición urgente"

        return ft.Container(
            content=ft.Row([
                # Indicador de alerta
                ft.Container(
                    content=ft.Icon(icono_alerta, color=color_alerta, size=32),
                    width=60,
                    alignment=ft.alignment.center
                ),
                # Información del producto
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                producto.get('nombre', 'Sin nombre'),
                                size=Theme.FONT_SIZE["md"],
                                weight=Theme.FONT_WEIGHT["bold"],
                                color=Theme.TEXT_PRIMARY
                            ),
                            ft.Container(
                                content=ft.Text(
                                    producto.get('sku', ''),
                                    size=Theme.FONT_SIZE["xs"],
                                    color=Theme.TEXT_SECONDARY
                                ),
                                bgcolor=f"{Theme.PRIMARY}15",
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=Theme.RADIUS["sm"]
                            ),
                        ], spacing=8),
                        ft.Text(
                            mensaje_alerta,
                            size=Theme.FONT_SIZE["sm"],
                            color=color_alerta,
                            weight=Theme.FONT_WEIGHT["medium"]
                        ),
                        ft.Row([
                            ft.Text(
                                f"Categoría: {producto.get('nombre_categoria', 'N/A')}",
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_SECONDARY
                            ),
                            ft.Text("|", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ft.Text(
                                f"Precio: S/ {producto.get('precio_venta', 0):.2f}",
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_SECONDARY
                            ),
                        ], spacing=8),
                    ], spacing=4),
                    expand=True
                ),
                # Acciones
                ft.Container(
                    content=ft.Row([
                        create_icon_button(
                            ft.Icons.ADD_SHOPPING_CART,
                            lambda e, p=producto: abrir_reposicion_dialog(p),
                            tooltip="Reabastecer",
                            color=Theme.SUCCESS
                        ),
                        create_icon_button(
                            ft.Icons.VISIBILITY,
                            lambda e, p=producto: ver_detalles(p),
                            tooltip="Ver detalles",
                            color=Theme.INFO
                        ),
                    ], spacing=4),
                    width=100
                ),
            ], spacing=Theme.SPACING["md"]),
            bgcolor=Theme.CARD_BG,
            padding=Theme.SPACING["lg"],
            border_radius=Theme.RADIUS["md"],
            border=ft.border.all(2, f"{color_alerta}30")
        )

    def actualizar_listas():
        """Actualizar todas las listas de alertas"""
        # Stock Bajo
        stock_bajo_container.controls.clear()
        if productos_stock_bajo:
            for producto in productos_stock_bajo:
                stock_bajo_container.controls.append(crear_producto_card(producto, "stock_bajo"))
        else:
            stock_bajo_container.controls.append(
                create_empty_state(
                    message="No hay productos con stock bajo",
                    icon=ft.Icons.CHECK_CIRCLE,
                    secondary_message="Todos los productos tienen stock suficiente"
                )
            )

        # Próximos a Vencer
        proximos_vencer_container.controls.clear()
        if productos_proximos_vencer:
            for producto in productos_proximos_vencer:
                proximos_vencer_container.controls.append(crear_producto_card(producto, "vencer"))
        else:
            proximos_vencer_container.controls.append(
                create_empty_state(
                    message=f"No hay productos próximos a vencer en {dias_vencimiento[0]} días",
                    icon=ft.Icons.CHECK_CIRCLE,
                    secondary_message="No hay alertas de vencimiento"
                )
            )

        # Sin Stock
        sin_stock_container.controls.clear()
        if productos_sin_stock:
            for producto in productos_sin_stock:
                sin_stock_container.controls.append(crear_producto_card(producto, "sin_stock"))
        else:
            sin_stock_container.controls.append(
                create_empty_state(
                    message="No hay productos sin stock",
                    icon=ft.Icons.CHECK_CIRCLE,
                    secondary_message="Todos los productos tienen inventario disponible"
                )
            )

        page.update()

    # ==========================================
    # ACCIONES
    # ==========================================
    def abrir_reposicion_dialog(producto):
        """Diálogo para reabastecer producto"""
        cantidad_field = ft.TextField(
            label="Cantidad a reabastecer",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            value=str(producto.get('stock_minimo', 10)),
            autofocus=True
        )

        costo_field = ft.TextField(
            label="Costo unitario (opcional)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            value=str(producto.get('precio_costo', 0))
        )

        lote_field = ft.TextField(
            label="Lote (opcional)",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            hint_text="LOT-2025-001"
        )

        def confirmar_reposicion(e):
            try:
                cantidad = int(cantidad_field.value)
                costo = float(costo_field.value) if costo_field.value else None
                lote = lote_field.value if lote_field.value else None

                if cantidad <= 0:
                    mostrar_error(page, "La cantidad debe ser mayor a 0")
                    return

                # Registrar entrada
                api.registrar_entrada_inventario(
                    producto_id=producto['id'],
                    cantidad=cantidad,
                    costo_unitario=costo,
                    lote=lote,
                    motivo=f"Reposición desde dashboard de alertas"
                )

                mostrar_exito(page, f"Producto '{producto['nombre']}' reabastecido correctamente")
                page.close(dialog)
                cargar_alertas()

            except ValueError:
                mostrar_error(page, "Valores inválidos. Verifica cantidad y costo")
            except Exception as ex:
                mostrar_error(page, f"Error al reabastecer: {str(ex)}")

        dialog = ft.AlertDialog(
            title=ft.Text(f"Reabastecer: {producto['nombre']}", color=Theme.TEXT_PRIMARY),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Stock actual:", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ft.Text(
                                str(producto.get('stock_actual', 0)),
                                size=Theme.FONT_SIZE["xl"],
                                weight=Theme.FONT_WEIGHT["bold"],
                                color=Theme.WARNING
                            ),
                        ], spacing=4),
                        bgcolor=f"{Theme.WARNING}15",
                        padding=Theme.SPACING["md"],
                        border_radius=Theme.RADIUS["sm"]
                    ),
                    cantidad_field,
                    costo_field,
                    lote_field,
                ], tight=True, spacing=Theme.SPACING["md"]),
                width=400
            ),
            actions=[
                create_outlined_button("Cancelar", lambda _: page.close(dialog)),
                create_primary_button("Reabastecer", confirmar_reposicion, icon=ft.Icons.ADD_SHOPPING_CART),
            ],
            bgcolor=Theme.CARD_BG,
        )
        page.open(dialog)

    def ver_detalles(producto):
        """Mostrar detalles del producto"""
        # Navegar a la vista de productos con el producto seleccionado
        on_section_click("Productos")

    def cambiar_dias_vencimiento(dias):
        """Cambiar rango de días para productos próximos a vencer"""
        dias_vencimiento[0] = dias
        cargar_alertas()

    def refrescar_alertas(e):
        """Refrescar todas las alertas"""
        cargar_alertas()
        mostrar_exito(page, "Alertas actualizadas correctamente")

    # ==========================================
    # CONTENIDO
    # ==========================================
    def build_view():
        """Construir vista completa"""
        page.clean()

        # Estadísticas (vertical)
        stats_column = ft.Column([
            ft.Container(ref=stat_stock_bajo),
            ft.Container(ref=stat_proximos_vencer),
            ft.Container(ref=stat_sin_stock),
        ], spacing=Theme.SPACING["lg"])

        # Header con acciones
        header = ft.Row([
            ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, size=Theme.ICON_SIZE["lg"], color=Theme.WARNING),
            ft.Text(
                "Dashboard de Alertas",
                size=Theme.FONT_SIZE["2xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY
            ),
            ft.Container(expand=True),
            create_outlined_button("Refrescar", refrescar_alertas, icon=ft.Icons.REFRESH),
        ], spacing=Theme.SPACING["md"])

        # Sección Stock Bajo
        stock_bajo_card = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.WARNING_AMBER, size=Theme.ICON_SIZE["md"], color=Theme.WARNING),
                    ft.Text(
                        "Productos con Stock Bajo",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                ], spacing=Theme.SPACING["sm"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                stock_bajo_container,
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        # Sección Próximos a Vencer
        proximos_vencer_card = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=Theme.ICON_SIZE["md"], color=Theme.ERROR),
                    ft.Text(
                        "Productos Próximos a Vencer",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                    ft.Container(expand=True),
                    # Selector de días
                    ft.Dropdown(
                        label="Días",
                        value=str(dias_vencimiento[0]),
                        options=[
                            ft.dropdown.Option("7"),
                            ft.dropdown.Option("15"),
                            ft.dropdown.Option("30"),
                            ft.dropdown.Option("60"),
                            ft.dropdown.Option("90"),
                        ],
                        width=100,
                        border_color=Theme.BORDER_DEFAULT,
                        focused_border_color=Theme.PRIMARY,
                        bgcolor=Theme.CARD_BG,
                        color=Theme.TEXT_PRIMARY,
                        on_change=lambda e: cambiar_dias_vencimiento(int(e.control.value))
                    ),
                ], spacing=Theme.SPACING["sm"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                proximos_vencer_container,
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        # Sección Sin Stock
        sin_stock_card = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY_2, size=Theme.ICON_SIZE["md"], color=Theme.ERROR),
                    ft.Text(
                        "Productos Sin Stock",
                        size=Theme.FONT_SIZE["lg"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                ], spacing=Theme.SPACING["sm"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                sin_stock_container,
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        # Layout completo
        content = ft.Column([
            header,
            ft.Container(height=Theme.SPACING["lg"]),
            stats_column,
            ft.Container(height=Theme.SPACING["xl"]),
            stock_bajo_card,
            ft.Container(height=Theme.SPACING["xl"]),
            proximos_vencer_card,
            ft.Container(height=Theme.SPACING["xl"]),
            sin_stock_card,
        ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

        create_base_layout(
            page=page,
            role="admin",
            current_section=current_section,
            on_section_click=on_section_click,
            content=content,
            user_info=user_info,
            on_logout=lambda _: on_section_click("logout")
        )

    # Inicializar
    cargar_alertas()
    build_view()
