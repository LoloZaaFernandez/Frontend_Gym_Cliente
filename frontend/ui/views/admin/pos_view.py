"""
Vista de POS (Punto de Venta) - Sistema Completo de Ventas de Productos
Incluye: Venta de productos, Carrito, Métodos de pago, Reportes en tiempo real
Diseño profesional siguiendo la filosofía UI/UX de BLESSED GYM
"""

import flet as ft
from datetime import datetime, timedelta
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button, create_icon_button, create_status_badge
from ui.components.molecules import create_card_container, create_empty_state
from ui.utils.messages import mostrar_exito, mostrar_error
from ui.utils.datetime_utils import get_now_local


def show_pos_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Vista de Punto de Venta con reportes integrados
    """
    page.title = "BLESSED GYM - Punto de Venta"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Estado
    productos_list = []
    carrito_items = []
    filtro_periodo = ["hoy"]  # hoy, semana, mes

    # Referencias
    productos_grid = ft.GridView(
        expand=True,
        runs_count=2,
        max_extent=220,
        child_aspect_ratio=0.75,
        spacing=10,
        run_spacing=10,
    )
    carrito_container = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("S/ 0.00", size=32, weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY)

    # Reporte
    reporte_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    stat_total_ventas = ft.Ref[ft.Container]()
    stat_efectivo = ft.Ref[ft.Container]()
    stat_yape = ft.Ref[ft.Container]()

    # ==========================================
    # FUNCIONES DE DATOS
    # ==========================================
    def load_productos():
        """Cargar productos activos desde la API"""
        nonlocal productos_list
        try:
            # Solo productos activos con stock
            productos_list = api.get_productos(estado="Activo")
            update_productos_grid()
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            productos_list = []
            update_productos_grid()

    def get_fechas_filtro():
        """Obtener fechas según el filtro seleccionado (con timezone local)"""
        hoy = get_now_local()

        if filtro_periodo[0] == "hoy":
            fecha_inicio = hoy.strftime("%Y-%m-%d")
            fecha_fin = hoy.strftime("%Y-%m-%d")
        elif filtro_periodo[0] == "semana":
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fecha_inicio = inicio_semana.strftime("%Y-%m-%d")
            fecha_fin = hoy.strftime("%Y-%m-%d")
        elif filtro_periodo[0] == "mes":
            fecha_inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
            fecha_fin = hoy.strftime("%Y-%m-%d")
        else:
            fecha_inicio = hoy.strftime("%Y-%m-%d")
            fecha_fin = hoy.strftime("%Y-%m-%d")

        return fecha_inicio, fecha_fin

    def load_reporte():
        """Cargar reporte de ventas"""
        try:
            fecha_inicio, fecha_fin = get_fechas_filtro()

            print(f"\n{'='*60}")
            print(f"📊 CARGANDO REPORTE DE VENTAS")
            print(f"{'='*60}")
            print(f"Período: {filtro_periodo[0]}")
            print(f"Desde: {fecha_inicio}")
            print(f"Hasta: {fecha_fin}")

            # Obtener ventas (listado ligero - sin detalles)
            ventas = api.get_ventas(fecha_desde=fecha_inicio, fecha_hasta=fecha_fin)

            print(f"Ventas recibidas del backend: {len(ventas) if ventas else 0}")

            # Si no hay ventas, mostrar vacío
            if not ventas:
                print(f"⚠️ No hay ventas en el período {fecha_inicio} - {fecha_fin}")
                print(f"{'='*60}\n")
                update_stats(0, 0, 0)
                update_reporte_tabla({}, 0)
                return

            print(f"\n📋 DETALLE DE VENTAS:")
            # Calcular totales de las ventas
            total_ventas = 0
            total_efectivo = 0
            total_yape = 0
            productos_vendidos = {}

            # Procesar cada venta y obtener sus detalles
            for idx, venta in enumerate(ventas, 1):
                venta_id = venta.get('id')
                total_venta = venta.get('total', 0)
                metodo_pago = venta.get('metodo_pago', 'Efectivo')
                fecha = venta.get('fecha_venta', venta.get('fecha', 'N/A'))
                folio = venta.get('folio', f"#{venta_id}")

                print(f"  Venta #{idx}:")
                print(f"    Folio: {folio}")
                print(f"    Fecha: {fecha}")
                print(f"    Total: S/ {total_venta:.2f}")
                print(f"    Método: {metodo_pago}")

                total_ventas += total_venta

                if metodo_pago.lower() in ['efectivo', 'cash']:
                    total_efectivo += total_venta
                elif metodo_pago.lower() in ['yape', 'transferencia']:
                    total_yape += total_venta

                # Obtener detalles completos de la venta (productos)
                # El listado NO trae items, hay que pedirlos individualmente
                if venta_id:
                    try:
                        venta_completa = api.get_venta_por_id(venta_id)
                        if venta_completa:
                            # Backend devuelve 'detalles' con los productos
                            items = venta_completa.get('detalles', [])
                            print(f"    Items: {len(items)}")

                            for item in items:
                                producto_id = item.get('id_producto')
                                nombre = item.get('nombre_producto', 'Desconocido')
                                cantidad = item.get('cantidad', 0)

                                print(f"      - {nombre}: {cantidad} unidades")

                                if producto_id in productos_vendidos:
                                    productos_vendidos[producto_id]['cantidad'] += cantidad
                                else:
                                    productos_vendidos[producto_id] = {
                                        'nombre': nombre,
                                        'cantidad': cantidad
                                    }
                        else:
                            print(f"    Items: No se pudieron obtener")
                    except Exception as e:
                        print(f"    Items: Error al obtener detalles - {e}")
                else:
                    print(f"    Items: ID de venta no disponible")

            print(f"\n💰 TOTALES:")
            print(f"  Total Ventas: S/ {total_ventas:.2f}")
            print(f"  Efectivo: S/ {total_efectivo:.2f}")
            print(f"  Yape: S/ {total_yape:.2f}")
            print(f"  Productos diferentes vendidos: {len(productos_vendidos)}")
            print(f"{'='*60}\n")

            # Actualizar stats
            update_stats(total_ventas, total_efectivo, total_yape)

            # Actualizar tabla de productos vendidos
            update_reporte_tabla(productos_vendidos, len(ventas))

        except ValueError as e:
            # Si el endpoint no existe (404), mostrar mensaje informativo
            error_str = str(e).lower()
            if "no encontrado" in error_str or "404" in error_str:
                print(f"⚠️ ADVERTENCIA: El backend aún no tiene el endpoint GET /api/ventas implementado.")
                print(f"   El reporte de ventas no estará disponible hasta que se implemente en el backend.")
                print(f"   Error: {e}")
            else:
                print(f"❌ Error al cargar reporte: {e}")
            print(f"{'='*60}\n")
            update_stats(0, 0, 0)
            update_reporte_tabla({}, 0)
        except Exception as e:
            print(f"❌ Error inesperado al cargar reporte: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            print(f"{'='*60}\n")
            update_stats(0, 0, 0)
            update_reporte_tabla({}, 0)

    def update_stats(total_ventas, total_efectivo, total_yape):
        """Actualizar estadísticas de ventas"""
        if stat_total_ventas.current:
            stat_total_ventas.current.content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SHOPPING_CART, size=24, color=Theme.PRIMARY),
                    ft.Text("Total Ventas", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                ], spacing=8),
                ft.Text(f"S/ {total_ventas:.2f}", size=Theme.FONT_SIZE["xl"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
            ], spacing=4)
            stat_total_ventas.current.update()

        if stat_efectivo.current:
            stat_efectivo.current.content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MONEY, size=24, color=Theme.SUCCESS),
                    ft.Text("Efectivo", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                ], spacing=8),
                ft.Text(f"S/ {total_efectivo:.2f}", size=Theme.FONT_SIZE["xl"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.SUCCESS),
            ], spacing=4)
            stat_efectivo.current.update()

        if stat_yape.current:
            stat_yape.current.content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PHONE_ANDROID, size=24, color=Theme.INFO),
                    ft.Text("Yape", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                ], spacing=8),
                ft.Text(f"S/ {total_yape:.2f}", size=Theme.FONT_SIZE["xl"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.INFO),
            ], spacing=4)
            stat_yape.current.update()

    def update_reporte_tabla(productos_vendidos, num_ventas):
        """Actualizar tabla de productos vendidos"""
        reporte_container.controls.clear()

        # Info general
        reporte_container.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.RECEIPT_LONG, size=20, color=Theme.INFO),
                    ft.Text(f"{num_ventas} venta(s) registrada(s)",
                           size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                ], spacing=8),
                padding=Theme.SPACING["sm"],
                bgcolor=f"{Theme.INFO}15",
                border_radius=Theme.RADIUS["sm"]
            )
        )

        if not productos_vendidos:
            reporte_container.controls.append(
                create_empty_state(
                    message="No hay ventas en este período",
                    icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                    secondary_message="Las ventas aparecerán aquí"
                )
            )
        else:
            # Encabezado
            reporte_container.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text("Producto", size=Theme.FONT_SIZE["sm"],
                               weight=Theme.FONT_WEIGHT["bold"], expand=True),
                        ft.Text("Cantidad", size=Theme.FONT_SIZE["sm"],
                               weight=Theme.FONT_WEIGHT["bold"], width=80, text_align=ft.TextAlign.CENTER),
                    ]),
                    bgcolor=f"{Theme.PRIMARY}22",
                    padding=Theme.SPACING["sm"],
                    border_radius=Theme.RADIUS["sm"]
                )
            )

            # Filas de productos
            for prod_data in sorted(productos_vendidos.values(),
                                   key=lambda x: x['cantidad'], reverse=True):
                reporte_container.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(prod_data['nombre'], size=Theme.FONT_SIZE["sm"],
                                   color=Theme.TEXT_PRIMARY, expand=True),
                            ft.Container(
                                content=ft.Text(str(prod_data['cantidad']),
                                              size=Theme.FONT_SIZE["md"],
                                              weight=Theme.FONT_WEIGHT["bold"],
                                              color=Theme.PRIMARY,
                                              text_align=ft.TextAlign.CENTER),
                                width=80,
                                bgcolor=f"{Theme.PRIMARY}15",
                                padding=Theme.SPACING["xs"],
                                border_radius=Theme.RADIUS["sm"]
                            ),
                        ]),
                        padding=Theme.SPACING["sm"],
                        border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
                    )
                )

        page.update()

    # ==========================================
    # FUNCIONES DE PRODUCTOS
    # ==========================================
    def update_productos_grid():
        """Actualizar grid de productos"""
        productos_grid.controls.clear()

        if not productos_list:
            productos_grid.controls.append(
                ft.Container(
                    content=create_empty_state(
                        message="No hay productos disponibles",
                        icon=ft.Icons.INVENTORY_2,
                        secondary_message="Los productos activos aparecerán aquí"
                    ),
                    expand=True
                )
            )
        else:
            for producto in productos_list:
                productos_grid.controls.append(crear_producto_card(producto))

        page.update()

    def crear_producto_card(producto):
        """Crear tarjeta de producto"""
        stock = producto.get('stock_actual', 0)
        precio = producto.get('precio_venta', producto.get('precio', 0))

        # Color según stock
        if stock <= 0:
            stock_color = Theme.ERROR
            stock_text = "Sin stock"
            disabled = True
        elif stock <= producto.get('stock_minimo', 5):
            stock_color = Theme.WARNING
            stock_text = f"Stock: {stock}"
            disabled = False
        else:
            stock_color = Theme.SUCCESS
            stock_text = f"Stock: {stock}"
            disabled = False

        return ft.Container(
            content=ft.Column([
                # Icono del producto
                ft.Container(
                    content=ft.Icon(ft.Icons.INVENTORY_2, size=36, color=Theme.PRIMARY),
                    bgcolor=f"{Theme.PRIMARY}22",
                    border_radius=Theme.RADIUS["md"],
                    padding=12,
                    alignment=ft.alignment.center
                ),
                # Nombre del producto
                ft.Text(
                    producto['nombre'],
                    size=Theme.FONT_SIZE["sm"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                # Precio
                ft.Text(
                    f"S/ {precio:.2f}",
                    size=Theme.FONT_SIZE["lg"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.PRIMARY,
                    text_align=ft.TextAlign.CENTER
                ),
                # Stock
                ft.Container(
                    content=ft.Text(
                        stock_text,
                        size=Theme.FONT_SIZE["xs"],
                        color=stock_color,
                        weight=Theme.FONT_WEIGHT["medium"]
                    ),
                    bgcolor=f"{stock_color}15",
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=Theme.RADIUS["sm"]
                ),
                # Botón agregar
                ft.ElevatedButton(
                    "Agregar",
                    icon=ft.Icons.ADD_SHOPPING_CART,
                    bgcolor=Theme.PRIMARY if not disabled else Theme.TEXT_SECONDARY,
                    color="white",
                    disabled=disabled,
                    on_click=lambda _, p=producto: agregar_al_carrito(p)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["md"],
            padding=Theme.SPACING["md"],
            border=ft.border.all(1, Theme.BORDER_DEFAULT)
        )

    # ==========================================
    # FUNCIONES DE CARRITO
    # ==========================================
    def agregar_al_carrito(producto):
        """Agregar producto al carrito"""
        # Verificar stock
        stock_disponible = producto.get('stock_actual', 0)

        # Buscar si ya existe en el carrito
        existe = False
        for item in carrito_items:
            if item['id'] == producto['id']:
                if item['cantidad'] >= stock_disponible:
                    mostrar_error(page, f"Stock insuficiente. Solo hay {stock_disponible} unidades disponibles.")
                    return
                item['cantidad'] += 1
                item['subtotal'] = item['cantidad'] * item['precio']
                existe = True
                break

        if not existe:
            if stock_disponible <= 0:
                mostrar_error(page, "Producto sin stock disponible")
                return

            carrito_items.append({
                'id': producto['id'],
                'nombre': producto['nombre'],
                'precio': producto.get('precio_venta', producto.get('precio', 0)),
                'cantidad': 1,
                'subtotal': producto.get('precio_venta', producto.get('precio', 0)),
                'stock_disponible': stock_disponible
            })

        actualizar_carrito()

    def quitar_del_carrito(producto_id):
        """Quitar producto del carrito"""
        nonlocal carrito_items
        carrito_items = [item for item in carrito_items if item['id'] != producto_id]
        actualizar_carrito()

    def actualizar_cantidad(producto_id, cambio):
        """Actualizar cantidad de un producto"""
        for item in carrito_items:
            if item['id'] == producto_id:
                nueva_cantidad = item['cantidad'] + cambio

                if nueva_cantidad <= 0:
                    quitar_del_carrito(producto_id)
                    return

                if nueva_cantidad > item['stock_disponible']:
                    mostrar_error(page, f"Stock insuficiente. Solo hay {item['stock_disponible']} unidades disponibles.")
                    return

                item['cantidad'] = nueva_cantidad
                item['subtotal'] = item['cantidad'] * item['precio']
                break
        actualizar_carrito()

    def actualizar_carrito():
        """Actualizar visualización del carrito"""
        carrito_container.controls.clear()

        if not carrito_items:
            carrito_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=50, color=Theme.TEXT_SECONDARY),
                        ft.Text("Carrito vacío", color=Theme.TEXT_SECONDARY, size=Theme.FONT_SIZE["md"]),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=40,
                    alignment=ft.alignment.center,
                    expand=True
                )
            )
            total_venta = 0.0
        else:
            total_venta = sum(item['subtotal'] for item in carrito_items)

            for item in carrito_items:
                carrito_container.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(
                                    item['nombre'],
                                    size=Theme.FONT_SIZE["sm"],
                                    weight=Theme.FONT_WEIGHT["bold"],
                                    color=Theme.TEXT_PRIMARY
                                ),
                                ft.Text(
                                    f"S/ {item['precio']:.2f}",
                                    size=Theme.FONT_SIZE["xs"],
                                    color=Theme.TEXT_SECONDARY
                                ),
                            ], spacing=2, expand=True),
                            ft.Row([
                                create_icon_button(
                                    ft.Icons.REMOVE,
                                    lambda _, id=item['id']: actualizar_cantidad(id, -1),
                                    tooltip="Disminuir",
                                    color=Theme.TEXT_SECONDARY
                                ),
                                ft.Text(
                                    str(item['cantidad']),
                                    size=Theme.FONT_SIZE["md"],
                                    weight=Theme.FONT_WEIGHT["bold"],
                                    color=Theme.TEXT_PRIMARY
                                ),
                                create_icon_button(
                                    ft.Icons.ADD,
                                    lambda _, id=item['id']: actualizar_cantidad(id, 1),
                                    tooltip="Aumentar",
                                    color=Theme.PRIMARY
                                ),
                            ], spacing=0),
                            ft.Text(
                                f"S/ {item['subtotal']:.2f}",
                                size=Theme.FONT_SIZE["md"],
                                weight=Theme.FONT_WEIGHT["bold"],
                                color=Theme.PRIMARY,
                                width=80,
                                text_align=ft.TextAlign.RIGHT
                            ),
                            create_icon_button(
                                ft.Icons.DELETE,
                                lambda _, id=item['id']: quitar_del_carrito(id),
                                tooltip="Eliminar",
                                color=Theme.ERROR
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=Theme.CARD_BG,
                        border_radius=Theme.RADIUS["sm"],
                        padding=Theme.SPACING["sm"],
                        border=ft.border.all(1, Theme.BORDER_DEFAULT),
                        margin=ft.margin.only(bottom=5)
                    )
                )

        total_text.value = f"S/ {total_venta:.2f}"
        page.update()

    def limpiar_carrito():
        """Limpiar el carrito"""
        carrito_items.clear()
        actualizar_carrito()

    def procesar_venta():
        """Mostrar diálogo para procesar la venta"""
        if not carrito_items:
            mostrar_error(page, "El carrito está vacío")
            return

        total_venta = sum(item['subtotal'] for item in carrito_items)

        # Dropdown de método de pago
        metodo_pago_dropdown = ft.Dropdown(
            label="Método de Pago *",
            options=[
                ft.dropdown.Option("Efectivo"),
                ft.dropdown.Option("Yape"),
            ],
            value="Efectivo",
            border_color=Theme.BORDER_DEFAULT,
            focused_border_color=Theme.PRIMARY,
            bgcolor=Theme.CARD_BG,
            color=Theme.TEXT_PRIMARY,
            width=250
        )

        def confirmar_venta(e):
            """Confirmar y registrar la venta"""
            metodo_pago = metodo_pago_dropdown.value

            if not metodo_pago:
                mostrar_error(page, "Selecciona un método de pago")
                return

            try:
                # Preparar productos en el formato correcto que espera el backend
                # Backend espera: productos con "id_producto" y "cantidad"
                # NO enviar precio_unitario - el backend lo calcula automáticamente
                productos = [
                    {
                        "id_producto": item['id'],  # Backend espera "id_producto" no "producto_id"
                        "cantidad": item['cantidad']
                        # NO incluir precio - el backend lo calcula según tipo de cliente
                    }
                    for item in carrito_items
                ]

                print(f"\n{'='*60}")
                print(f"🛒 PROCESANDO VENTA")
                print(f"{'='*60}")
                print(f"Método de pago: {metodo_pago}")
                print(f"Total esperado: S/ {total_venta:.2f}")
                print(f"Productos: {len(productos)}")
                for i, prod in enumerate(productos, 1):
                    # Buscar info del producto en el carrito para mostrar
                    item_carrito = next((x for x in carrito_items if x['id'] == prod['id_producto']), None)
                    if item_carrito:
                        print(f"  {i}. Producto ID {prod['id_producto']}: {prod['cantidad']} x S/ {item_carrito['precio']}")

                # Crear payload para enviar
                payload_info = {
                    "items": productos,
                    "cliente_id": None,
                    "tipo_cliente": "Publico",
                    "metodo_pago": metodo_pago,
                    "descuento": 0,
                    "notas": f"Venta POS - {len(productos)} producto(s)",
                    "usuario_creacion": current_user.get("nombre", "admin")
                }

                print(f"\n📤 DATOS A ENVIAR AL BACKEND:")
                import json
                print(json.dumps(payload_info, indent=2, ensure_ascii=False))
                print(f"{'='*60}\n")

                # Crear venta con la estructura correcta
                # tipo_cliente="Publico" por defecto (puedes cambiarlo si integras con clientes)
                resultado = api.crear_venta(**payload_info)

                print(f"✅ VENTA REGISTRADA EXITOSAMENTE")
                print(f"Respuesta del backend: {resultado}")
                print(f"{'='*60}\n")

                page.close(dialog)

                # Extraer información de la respuesta del backend
                folio = resultado.get('folio', 'N/A')
                total_real = resultado.get('total', total_venta)
                subtotal = resultado.get('subtotal', 0)
                iva = resultado.get('iva', 0)
                ganancia = resultado.get('ganancia', 0)
                estado = resultado.get('estado', 'Completada')

                # Mensaje de éxito con información completa
                mensaje_exito = f"""✅ Venta procesada exitosamente

📄 Folio: {folio}
💰 Subtotal: S/ {subtotal:.2f}
📊 IVA: S/ {iva:.2f}
💵 TOTAL: S/ {total_real:.2f}
💳 Método: {metodo_pago}
✅ Estado: {estado}
📈 Ganancia: S/ {ganancia:.2f}"""

                mostrar_exito(page, mensaje_exito)

                # Limpiar carrito
                limpiar_carrito()

                print(f"🔄 Recargando productos y reportes...")
                # Recargar productos (para actualizar stock)
                load_productos()
                # Recargar reporte (para mostrar la venta)
                load_reporte()
                print(f"✅ Productos y reportes recargados\n")

            except ValueError as ex:
                page.close(dialog)
                error_msg = str(ex)
                print(f"❌ ERROR ValueError: {error_msg}")
                if "no encontrado" in error_msg.lower() or "404" in error_msg:
                    mostrar_error(page, "⚠️ El backend aún no tiene el endpoint de ventas implementado.\n\nLa venta NO se registró. Contacta al desarrollador backend para implementar el endpoint POST /api/ventas")
                else:
                    mostrar_error(page, f"Error al procesar venta:\n\n{error_msg}")
            except Exception as ex:
                page.close(dialog)
                print(f"❌ ERROR inesperado: {type(ex).__name__}: {str(ex)}")
                import traceback
                traceback.print_exc()
                mostrar_error(page, f"Error inesperado al procesar venta:\n\n{str(ex)}")

        # Diálogo de confirmación
        dialog = ft.AlertDialog(
            title=ft.Text("Procesar Venta", color=Theme.TEXT_PRIMARY),
            content=ft.Container(
                content=ft.Column([
                    # Resumen de productos
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Resumen de la venta:", size=Theme.FONT_SIZE["sm"],
                                   weight=Theme.FONT_WEIGHT["bold"]),
                            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                            *[
                                ft.Row([
                                    ft.Text(f"{item['cantidad']}x", size=Theme.FONT_SIZE["xs"]),
                                    ft.Text(item['nombre'], size=Theme.FONT_SIZE["xs"], expand=True),
                                    ft.Text(f"S/ {item['subtotal']:.2f}", size=Theme.FONT_SIZE["xs"]),
                                ])
                                for item in carrito_items
                            ],
                        ], spacing=4),
                        bgcolor=f"{Theme.PRIMARY}15",
                        padding=Theme.SPACING["sm"],
                        border_radius=Theme.RADIUS["sm"],
                        border=ft.border.all(1, f"{Theme.PRIMARY}50")
                    ),
                    ft.Container(height=Theme.SPACING["md"]),
                    # Total
                    ft.Row([
                        ft.Text("TOTAL:", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"]),
                        ft.Text(f"S/ {total_venta:.2f}", size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=Theme.SPACING["md"]),
                    # Método de pago
                    metodo_pago_dropdown,
                ], tight=True, spacing=Theme.SPACING["sm"]),
                width=400
            ),
            actions=[
                create_outlined_button("Cancelar", lambda _: page.close(dialog), icon=ft.Icons.CLOSE),
                create_primary_button("Confirmar Venta", confirmar_venta, icon=ft.Icons.CHECK_CIRCLE),
            ],
            bgcolor=Theme.CARD_BG,
        )
        page.open(dialog)

    # ==========================================
    # FUNCIONES DE REPORTE
    # ==========================================
    def cambiar_filtro_periodo(periodo):
        """Cambiar filtro de período"""
        filtro_periodo[0] = periodo
        load_reporte()

    # ==========================================
    # CONTENIDO
    # ==========================================
    def update_view():
        """Actualizar vista completa"""
        page.clean()

        # Panel de productos
        productos_panel = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY_2, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Productos Disponibles", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ], spacing=Theme.SPACING["sm"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                productos_grid,
            ], spacing=Theme.SPACING["md"], expand=True),
            padding=Theme.SPACING["lg"],
            shadow="md"
        )

        # Panel de carrito
        carrito_panel = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SHOPPING_CART, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Carrito", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ], spacing=Theme.SPACING["sm"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                carrito_container,
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Row([
                    ft.Text("TOTAL:", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"]),
                    total_text,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=Theme.SPACING["sm"]),
                create_primary_button(
                    "PROCESAR VENTA",
                    lambda _: procesar_venta(),
                    icon=ft.Icons.POINT_OF_SALE,
                    width=300
                ),
                create_outlined_button(
                    "Limpiar Carrito",
                    lambda _: limpiar_carrito(),
                    icon=ft.Icons.CLEAR_ALL,
                    width=300
                ),
            ], spacing=Theme.SPACING["md"], expand=True),
            padding=Theme.SPACING["lg"],
            shadow="md"
        )

        # Panel de reporte
        reporte_panel = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ANALYTICS, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Reporte de Ventas", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY, expand=True),
                ], spacing=Theme.SPACING["sm"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                # Filtros
                ft.Row([
                    ft.ElevatedButton(
                        "Hoy",
                        bgcolor=Theme.PRIMARY if filtro_periodo[0] == "hoy" else Theme.CARD_BG,
                        color="white" if filtro_periodo[0] == "hoy" else Theme.TEXT_PRIMARY,
                        on_click=lambda _: cambiar_filtro_periodo("hoy")
                    ),
                    ft.ElevatedButton(
                        "Semana",
                        bgcolor=Theme.PRIMARY if filtro_periodo[0] == "semana" else Theme.CARD_BG,
                        color="white" if filtro_periodo[0] == "semana" else Theme.TEXT_PRIMARY,
                        on_click=lambda _: cambiar_filtro_periodo("semana")
                    ),
                    ft.ElevatedButton(
                        "Mes",
                        bgcolor=Theme.PRIMARY if filtro_periodo[0] == "mes" else Theme.CARD_BG,
                        color="white" if filtro_periodo[0] == "mes" else Theme.TEXT_PRIMARY,
                        on_click=lambda _: cambiar_filtro_periodo("mes")
                    ),
                ], spacing=Theme.SPACING["sm"]),
                # Stats
                ft.Row([
                    ft.Container(ref=stat_total_ventas, expand=True, bgcolor=f"{Theme.PRIMARY}15",
                                padding=Theme.SPACING["md"], border_radius=Theme.RADIUS["sm"]),
                ]),
                ft.Row([
                    ft.Container(ref=stat_efectivo, expand=True, bgcolor=f"{Theme.SUCCESS}15",
                                padding=Theme.SPACING["sm"], border_radius=Theme.RADIUS["sm"]),
                    ft.Container(ref=stat_yape, expand=True, bgcolor=f"{Theme.INFO}15",
                                padding=Theme.SPACING["sm"], border_radius=Theme.RADIUS["sm"]),
                ]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Text("Productos Vendidos", size=Theme.FONT_SIZE["md"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                reporte_container,
            ], spacing=Theme.SPACING["md"], expand=True),
            padding=Theme.SPACING["lg"],
            shadow="md"
        )

        # Layout con 3 columnas
        content_row = ft.Row([
            ft.Container(content=productos_panel, expand=2),
            ft.Container(content=carrito_panel, width=350),
            ft.Container(content=reporte_panel, width=350),
        ], spacing=Theme.SPACING["lg"], expand=True)

        # Contenido principal
        content = ft.Column([
            content_row
        ], spacing=0, expand=True)

        create_base_layout(
            page=page,
            role="admin",
            current_section=current_section,
            on_section_click=on_section_click,
            content=content,
            user_info=user_info,
            on_logout=lambda _: on_section_click("logout")
        )

        # Cargar datos iniciales
        load_productos()
        load_reporte()
        actualizar_carrito()

    # Inicializar vista
    update_view()
