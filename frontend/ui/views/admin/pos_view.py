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
    productos_filtrados = []  # Lista filtrada de productos
    carrito_items = []
    filtro_periodo = ["hoy"]  # hoy, semana, mes
    reporte_metodos_data = [{}]  # Almacenar datos del reporte de métodos
    categorias_list = []  # Lista de categorías para el filtro
    filtro_categoria = [""]  # Categoría seleccionada
    filtro_nombre = [""]  # Búsqueda por nombre

    # Referencias
    productos_grid = ft.GridView(
        expand=True,
        runs_count=2,
        max_extent=200,
        child_aspect_ratio=0.7,
        spacing=8,
        run_spacing=8,
    )
    carrito_container = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("S/ 0.00", size=32, weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY)

    # Reporte
    reporte_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    stat_total_ventas = ft.Ref[ft.Container]()
    stat_efectivo = ft.Ref[ft.Container]()
    stat_yape = ft.Ref[ft.Container]()

    # Estadísticas rápidas
    estadisticas_hoy_container = ft.Ref[ft.Container]()
    estadisticas_mes_container = ft.Ref[ft.Container]()

    # Referencias para filtros
    dropdown_categoria = ft.Ref[ft.Dropdown]()
    campo_busqueda = ft.Ref[ft.TextField]()

    # ==========================================
    # FUNCIONES DE DATOS
    # ==========================================
    def load_productos():
        """Cargar productos activos desde la API"""
        nonlocal productos_list, categorias_list
        try:
            # Solo productos activos con stock
            productos_list = api.get_productos(estado="Activo")

            # Extraer categorías únicas
            categorias_set = set()
            for producto in productos_list:
                cat = producto.get('nombre_categoria')
                if cat:
                    categorias_set.add(cat)
            categorias_list = sorted(list(categorias_set))

            # Actualizar dropdown de categorías
            if dropdown_categoria.current:
                dropdown_categoria.current.options = [ft.dropdown.Option("Todas")] + [
                    ft.dropdown.Option(cat) for cat in categorias_list
                ]
                dropdown_categoria.current.update()

            # Aplicar filtros
            aplicar_filtros()
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            productos_list = []
            categorias_list = []
            update_productos_grid()

    def aplicar_filtros():
        """Aplicar filtros de categoría y nombre a los productos"""
        nonlocal productos_filtrados

        # Empezar con todos los productos
        productos_filtrados = productos_list.copy()

        # Filtrar por categoría
        if filtro_categoria[0] and filtro_categoria[0] != "Todas":
            productos_filtrados = [
                p for p in productos_filtrados
                if p.get('nombre_categoria') == filtro_categoria[0]
            ]

        # Filtrar por nombre
        if filtro_nombre[0]:
            busqueda = filtro_nombre[0].lower()
            productos_filtrados = [
                p for p in productos_filtrados
                if busqueda in p.get('nombre', '').lower() or
                   busqueda in p.get('sku', '').lower()
            ]

        update_productos_grid()

    def cambiar_filtro_categoria(categoria):
        """Cambiar filtro de categoría"""
        filtro_categoria[0] = categoria
        aplicar_filtros()

    def cambiar_filtro_nombre(e):
        """Cambiar filtro de nombre"""
        filtro_nombre[0] = e.control.value
        aplicar_filtros()

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
        """Cargar reporte de ventas usando endpoint optimizado"""
        nonlocal reporte_metodos_data
        try:
            fecha_inicio, fecha_fin = get_fechas_filtro()

            print(f"\n{'='*60}")
            print(f"📊 CARGANDO REPORTE DE VENTAS")
            print(f"{'='*60}")
            print(f"Período: {filtro_periodo[0]}")
            print(f"Desde: {fecha_inicio}")
            print(f"Hasta: {fecha_fin}")

            # Obtener reporte optimizado por métodos de pago
            reporte_metodos = api.get_reporte_ventas_metodos_pago(
                fecha_desde=fecha_inicio,
                fecha_hasta=fecha_fin
            )

            # Guardar datos del reporte
            reporte_metodos_data[0] = reporte_metodos

            print(f"\n💳 REPORTE POR MÉTODOS DE PAGO:")
            print(f"  Total general: S/ {reporte_metodos.get('total_general', 0):.2f}")
            print(f"  Cantidad de ventas: {reporte_metodos.get('total_ventas', 0)}")

            # Extraer datos de métodos de pago
            efectivo_data = reporte_metodos.get('efectivo', {})
            yape_data = reporte_metodos.get('yape', {})
            otros_data = reporte_metodos.get('otros', {})

            total_general = reporte_metodos.get('total_general', 0)
            total_efectivo = efectivo_data.get('total', 0)
            total_yape = yape_data.get('total', 0)
            total_otros = otros_data.get('total', 0)

            print(f"  Efectivo: S/ {total_efectivo:.2f} ({efectivo_data.get('porcentaje', 0):.1f}%)")
            print(f"  Yape: S/ {total_yape:.2f} ({yape_data.get('porcentaje', 0):.1f}%)")
            if total_otros > 0:
                print(f"  Otros: S/ {total_otros:.2f} ({otros_data.get('porcentaje', 0):.1f}%)")

            # Si no hay ventas, mostrar vacío
            if total_general == 0:
                print(f"⚠️ No hay ventas en el período {fecha_inicio} - {fecha_fin}")
                print(f"{'='*60}\n")
                update_stats(0, 0, 0)
                update_reporte_tabla({}, 0)
                return

            # Obtener ventas para productos vendidos
            ventas = api.get_ventas(fecha_desde=fecha_inicio, fecha_hasta=fecha_fin)
            productos_vendidos = {}

            if ventas:
                print(f"\n📋 DETALLE DE VENTAS:")
                # Procesar cada venta para obtener productos
                for idx, venta in enumerate(ventas, 1):
                    venta_id = venta.get('id')
                    folio = venta.get('folio', f"#{venta_id}")
                    total_venta = venta.get('total', 0)
                    metodo_pago = venta.get('metodo_pago', 'Efectivo')
                    fecha = venta.get('fecha_venta', venta.get('fecha', 'N/A'))

                    print(f"  Venta #{idx}:")
                    print(f"    Folio: {folio}")
                    print(f"    Fecha: {fecha}")
                    print(f"    Total: S/ {total_venta:.2f}")
                    print(f"    Método: {metodo_pago}")

                    # Obtener detalles de productos
                    items = venta.get('detalles', venta.get('items', []))

                    # Si no vienen en el listado, pedirlos individualmente
                    if not items and venta_id:
                        try:
                            print(f"    Consultando detalles al backend...")
                            venta_completa = api.get_venta_por_id(venta_id)
                            if venta_completa:
                                items = venta_completa.get('detalles', venta_completa.get('items', []))
                        except ValueError as e:
                            error_msg = str(e).lower()
                            if "500" in error_msg or "error interno" in error_msg:
                                print(f"    ⚠️ Error 500 del backend al obtener detalles")
                                print(f"    Esto puede ser un bug en el endpoint GET /api/ventas/{venta_id}")
                            else:
                                print(f"    Items: Error - {e}")
                        except Exception as e:
                            print(f"    Items: Error inesperado - {type(e).__name__}: {e}")

                    # Procesar items si existen
                    if items:
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
                        print(f"    Items: No disponibles (el backend puede tener un error)")

                print(f"\n💰 RESUMEN:")
                print(f"  Total General: S/ {total_general:.2f}")
                print(f"  Efectivo: S/ {total_efectivo:.2f}")
                print(f"  Yape: S/ {total_yape:.2f}")
                if total_otros > 0:
                    print(f"  Otros: S/ {total_otros:.2f}")
                print(f"  Productos diferentes vendidos: {len(productos_vendidos)}")
                print(f"{'='*60}\n")

            # Actualizar stats con datos del reporte optimizado (incluyendo porcentajes)
            update_stats(
                total_general,
                total_efectivo,
                total_yape,
                porcentaje_efectivo=efectivo_data.get('porcentaje'),
                porcentaje_yape=yape_data.get('porcentaje')
            )

            # Actualizar tabla de productos vendidos
            update_reporte_tabla(productos_vendidos, reporte_metodos.get('total_ventas', 0))

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

    def update_stats(total_ventas, total_efectivo, total_yape, porcentaje_efectivo=None, porcentaje_yape=None):
        """Actualizar estadísticas de ventas con porcentajes opcionales"""
        # Obtener datos adicionales del reporte
        reporte = reporte_metodos_data[0] if reporte_metodos_data else {}
        efectivo_data = reporte.get('efectivo', {})
        yape_data = reporte.get('yape', {})
        total_ventas_count = reporte.get('total_ventas', 0)

        if stat_total_ventas.current:
            stat_total_ventas.current.content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SHOPPING_CART, size=24, color=Theme.PRIMARY),
                    ft.Text("Total Ventas", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                ], spacing=8),
                ft.Text(f"S/ {total_ventas:.2f}", size=Theme.FONT_SIZE["xl"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                ft.Text(
                    f"{total_ventas_count} venta(s)" if total_ventas_count > 0 else "",
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_SECONDARY
                ) if total_ventas_count > 0 else ft.Container(),
            ], spacing=4)
            stat_total_ventas.current.update()

        if stat_efectivo.current:
            # Calcular porcentaje si no se proporciona
            if porcentaje_efectivo is None and total_ventas > 0:
                porcentaje_efectivo = (total_efectivo / total_ventas) * 100

            # Cantidad de ventas en efectivo
            cantidad_efectivo = efectivo_data.get('cantidad_ventas', 0)

            stat_efectivo.current.content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MONEY, size=24, color=Theme.SUCCESS),
                    ft.Text("Efectivo", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                ], spacing=8),
                ft.Row([
                    ft.Text(f"S/ {total_efectivo:.2f}", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.SUCCESS),
                    ft.Container(
                        content=ft.Text(
                            f"{porcentaje_efectivo:.1f}%",
                            size=Theme.FONT_SIZE["sm"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color="white"
                        ),
                        bgcolor=Theme.SUCCESS,
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border_radius=Theme.RADIUS["sm"]
                    ) if porcentaje_efectivo is not None and porcentaje_efectivo > 0 else ft.Container(),
                ], spacing=8, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(
                    f"{cantidad_efectivo} venta(s)" if cantidad_efectivo > 0 else "",
                    size=Theme.FONT_SIZE["xs"],
                    color=Theme.TEXT_SECONDARY
                ) if cantidad_efectivo > 0 else ft.Container(),
            ], spacing=4)
            stat_efectivo.current.update()

        if stat_yape.current:
            # Calcular porcentaje si no se proporciona
            if porcentaje_yape is None and total_ventas > 0:
                porcentaje_yape = (total_yape / total_ventas) * 100

            # Cantidad de ventas en yape
            cantidad_yape = yape_data.get('cantidad_ventas', 0)

            stat_yape.current.content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PHONE_ANDROID, size=24, color=Theme.INFO),
                    ft.Text("Yape", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                ], spacing=8),
                ft.Row([
                    ft.Text(f"S/ {total_yape:.2f}", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.INFO),
                    ft.Container(
                        content=ft.Text(
                            f"{porcentaje_yape:.1f}%",
                            size=Theme.FONT_SIZE["sm"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color="white"
                        ),
                        bgcolor=Theme.INFO,
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border_radius=Theme.RADIUS["sm"]
                    ) if porcentaje_yape is not None and porcentaje_yape > 0 else ft.Container(),
                ], spacing=8, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(
                    f"{cantidad_yape} venta(s)" if cantidad_yape > 0 else "",
                    size=Theme.FONT_SIZE["xs"],
                    color=Theme.TEXT_SECONDARY
                ) if cantidad_yape > 0 else ft.Container(),
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

    def load_estadisticas_rapidas():
        """Cargar estadísticas rápidas de hoy y del mes"""
        try:
            # Obtener estadísticas de hoy
            stats_hoy = api.get_estadisticas_ventas_hoy()
            update_estadisticas_hoy(stats_hoy)

            # Obtener estadísticas del mes
            stats_mes = api.get_estadisticas_ventas_mes()
            update_estadisticas_mes(stats_mes)

        except Exception as e:
            print(f"Error al cargar estadísticas rápidas: {e}")
            update_estadisticas_hoy({})
            update_estadisticas_mes({})

    def update_estadisticas_hoy(stats):
        """Actualizar tarjeta de estadísticas de hoy"""
        if not estadisticas_hoy_container.current:
            return

        total_ventas = stats.get('total_ventas', 0)
        total = stats.get('total', 0)
        ganancia = stats.get('ganancia', 0)
        ticket_promedio = stats.get('ticket_promedio', 0)

        estadisticas_hoy_container.current.content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.TODAY, size=20, color=Theme.PRIMARY),
                ft.Text("Hoy", size=Theme.FONT_SIZE["md"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ], spacing=8),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Row([
                ft.Column([
                    ft.Text("Ventas", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(str(total_ventas), size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                ], spacing=2),
                ft.Column([
                    ft.Text("Total", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"S/ {total:.2f}", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.SUCCESS),
                ], spacing=2),
            ], spacing=Theme.SPACING["lg"], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Row([
                ft.Column([
                    ft.Text("Ganancia", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"S/ {ganancia:.2f}", size=Theme.FONT_SIZE["md"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.INFO),
                ], spacing=2),
                ft.Column([
                    ft.Text("Ticket Prom.", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"S/ {ticket_promedio:.2f}", size=Theme.FONT_SIZE["md"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.WARNING),
                ], spacing=2),
            ], spacing=Theme.SPACING["lg"], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ], spacing=Theme.SPACING["sm"])
        estadisticas_hoy_container.current.update()

    def update_estadisticas_mes(stats):
        """Actualizar tarjeta de estadísticas del mes"""
        if not estadisticas_mes_container.current:
            return

        mes = stats.get('mes', 'N/A')
        total_ventas = stats.get('total_ventas', 0)
        total = stats.get('total', 0)
        ganancia = stats.get('ganancia', 0)
        ticket_promedio = stats.get('ticket_promedio', 0)

        estadisticas_mes_container.current.content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.CALENDAR_MONTH, size=20, color=Theme.INFO),
                ft.Text(mes, size=Theme.FONT_SIZE["md"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ], spacing=8),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Row([
                ft.Column([
                    ft.Text("Ventas", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(str(total_ventas), size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                ], spacing=2),
                ft.Column([
                    ft.Text("Total", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"S/ {total:.2f}", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.SUCCESS),
                ], spacing=2),
            ], spacing=Theme.SPACING["lg"], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Row([
                ft.Column([
                    ft.Text("Ganancia", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"S/ {ganancia:.2f}", size=Theme.FONT_SIZE["md"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.INFO),
                ], spacing=2),
                ft.Column([
                    ft.Text("Ticket Prom.", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"S/ {ticket_promedio:.2f}", size=Theme.FONT_SIZE["md"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.WARNING),
                ], spacing=2),
            ], spacing=Theme.SPACING["lg"], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ], spacing=Theme.SPACING["sm"])
        estadisticas_mes_container.current.update()

    # ==========================================
    # FUNCIONES DE PRODUCTOS
    # ==========================================
    def update_productos_grid():
        """Actualizar grid de productos"""
        productos_grid.controls.clear()

        if not productos_filtrados:
            productos_grid.controls.append(
                ft.Container(
                    content=create_empty_state(
                        message="No hay productos" + (" que coincidan con el filtro" if (filtro_categoria[0] or filtro_nombre[0]) else " disponibles"),
                        icon=ft.Icons.INVENTORY_2,
                        secondary_message="Prueba cambiando los filtros" if (filtro_categoria[0] or filtro_nombre[0]) else "Los productos activos aparecerán aquí"
                    ),
                    expand=True
                )
            )
        else:
            for producto in productos_filtrados:
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
                # Icono del producto (más pequeño)
                ft.Container(
                    content=ft.Icon(ft.Icons.INVENTORY_2, size=28, color=Theme.PRIMARY),
                    bgcolor=f"{Theme.PRIMARY}22",
                    border_radius=Theme.RADIUS["md"],
                    padding=8,
                    alignment=ft.alignment.center
                ),
                # Nombre del producto
                ft.Text(
                    producto['nombre'],
                    size=Theme.FONT_SIZE["xs"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                # Precio
                ft.Text(
                    f"S/ {precio:.2f}",
                    size=Theme.FONT_SIZE["md"],
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
                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                    border_radius=Theme.RADIUS["sm"]
                ),
                # Botón agregar (compacto)
                ft.ElevatedButton(
                    "Agregar",
                    icon=ft.Icons.ADD,
                    icon_color="white",
                    bgcolor=Theme.PRIMARY if not disabled else Theme.TEXT_SECONDARY,
                    color="white",
                    disabled=disabled,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        text_style=ft.TextStyle(size=Theme.FONT_SIZE["xs"])
                    ),
                    on_click=lambda _, p=producto: agregar_al_carrito(p)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["md"],
            padding=10,
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
                        content=ft.Column([
                            # Primera fila: Nombre y botón eliminar
                            ft.Row([
                                ft.Text(
                                    item['nombre'],
                                    size=Theme.FONT_SIZE["sm"],
                                    weight=Theme.FONT_WEIGHT["bold"],
                                    color=Theme.TEXT_PRIMARY,
                                    expand=True,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                create_icon_button(
                                    ft.Icons.DELETE,
                                    lambda _, id=item['id']: quitar_del_carrito(id),
                                    tooltip="Eliminar",
                                    color=Theme.ERROR
                                ),
                            ], spacing=5),
                            # Segunda fila: Precio unitario, cantidad y subtotal
                            ft.Row([
                                ft.Text(
                                    f"S/ {item['precio']:.2f}",
                                    size=Theme.FONT_SIZE["xs"],
                                    color=Theme.TEXT_SECONDARY
                                ),
                                ft.Row([
                                    create_icon_button(
                                        ft.Icons.REMOVE,
                                        lambda _, id=item['id']: actualizar_cantidad(id, -1),
                                        tooltip="Disminuir",
                                        color=Theme.TEXT_SECONDARY
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            str(item['cantidad']),
                                            size=Theme.FONT_SIZE["sm"],
                                            weight=Theme.FONT_WEIGHT["bold"],
                                            color=Theme.TEXT_PRIMARY,
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        width=30,
                                        bgcolor=f"{Theme.PRIMARY}15",
                                        border_radius=Theme.RADIUS["sm"],
                                        padding=2
                                    ),
                                    create_icon_button(
                                        ft.Icons.ADD,
                                        lambda _, id=item['id']: actualizar_cantidad(id, 1),
                                        tooltip="Aumentar",
                                        color=Theme.PRIMARY
                                    ),
                                ], spacing=2),
                                ft.Text(
                                    f"S/ {item['subtotal']:.2f}",
                                    size=Theme.FONT_SIZE["sm"],
                                    weight=Theme.FONT_WEIGHT["bold"],
                                    color=Theme.PRIMARY,
                                    text_align=ft.TextAlign.RIGHT
                                ),
                            ], spacing=5, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ], spacing=5),
                        bgcolor=Theme.CARD_BG,
                        border_radius=Theme.RADIUS["sm"],
                        padding=8,
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

                # Crear venta con la estructura correcta
                # api.crear_venta() internamente convierte los parámetros al formato del backend
                resultado = api.crear_venta(
                    items=productos,
                    cliente_id=None,
                    tipo_cliente="Publico",
                    metodo_pago=metodo_pago,
                    descuento=0,
                    notas=f"Venta POS - {len(productos)} producto(s)",
                    usuario_creacion=current_user.get("nombre", "admin")
                )

                print(f"\n📤 Venta enviada al backend")
                print(f"  Items: {len(productos)}")
                print(f"  Método: {metodo_pago}")
                print(f"{'='*60}\n")

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

                print(f"🔄 Recargando productos, reportes y estadísticas...")
                # Recargar productos (para actualizar stock)
                load_productos()
                # Recargar reporte (para mostrar la venta)
                load_reporte()
                # Recargar estadísticas rápidas
                load_estadisticas_rapidas()
                print(f"✅ Productos, reportes y estadísticas recargados\n")

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

        # Panel de productos (totalmente estático)
        productos_panel = create_card_container(
            content=ft.Column([
                # Header (altura fija)
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INVENTORY_2, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                        ft.Text("Productos Disponibles", size=Theme.FONT_SIZE["lg"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),
                    height=40,
                ),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                # Filtros de búsqueda (altura fija)
                ft.Container(
                    content=ft.Row([
                        ft.Dropdown(
                            ref=dropdown_categoria,
                            label="Categoría",
                            hint_text="Todas",
                            options=[ft.dropdown.Option("Todas")],
                            value="Todas",
                            border_color=Theme.BORDER_DEFAULT,
                            focused_border_color=Theme.PRIMARY,
                            bgcolor=Theme.CARD_BG,
                            color=Theme.TEXT_PRIMARY,
                            width=160,
                            on_change=lambda e: cambiar_filtro_categoria(e.control.value)
                        ),
                        ft.TextField(
                            ref=campo_busqueda,
                            label="Buscar",
                            hint_text="Nombre o SKU",
                            prefix_icon=ft.Icons.SEARCH,
                            border_color=Theme.BORDER_DEFAULT,
                            focused_border_color=Theme.PRIMARY,
                            bgcolor=Theme.CARD_BG,
                            color=Theme.TEXT_PRIMARY,
                            expand=True,
                            on_change=cambiar_filtro_nombre
                        ),
                    ], spacing=8),
                    height=56,
                ),
                # Grid de productos (toma el resto del espacio)
                ft.Container(
                    content=productos_grid,
                    expand=True,
                ),
            ], spacing=8),
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
                # Estadísticas Rápidas
                ft.Text("Estadísticas Rápidas", size=Theme.FONT_SIZE["md"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Row([
                    ft.Container(
                        ref=estadisticas_hoy_container,
                        expand=True,
                        bgcolor=f"{Theme.PRIMARY}08",
                        padding=Theme.SPACING["md"],
                        border_radius=Theme.RADIUS["md"],
                        border=ft.border.all(1, f"{Theme.PRIMARY}30")
                    ),
                    ft.Container(
                        ref=estadisticas_mes_container,
                        expand=True,
                        bgcolor=f"{Theme.INFO}08",
                        padding=Theme.SPACING["md"],
                        border_radius=Theme.RADIUS["md"],
                        border=ft.border.all(1, f"{Theme.INFO}30")
                    ),
                ]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Text("Productos Vendidos", size=Theme.FONT_SIZE["md"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                reporte_container,
            ], spacing=Theme.SPACING["md"], expand=True),
            padding=Theme.SPACING["lg"],
            shadow="md"
        )

        # Layout con 3 columnas: Productos (izq) | Reporte (centro) | Carrito (derecha)
        content_row = ft.Row([
            ft.Container(content=productos_panel, expand=3),  # Productos - más grande
            ft.Container(content=reporte_panel, width=400),    # Reporte - mediano
            ft.Container(content=carrito_panel, width=320),    # Carrito - compacto pero funcional
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
        load_estadisticas_rapidas()
        actualizar_carrito()

    # Inicializar vista
    update_view()
