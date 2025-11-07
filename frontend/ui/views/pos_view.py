"""
Vista de POS (Punto de Venta) con sistema de ventas
"""

import flet as ft
from datetime import datetime
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK


def show_pos_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de punto de venta

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Punto de Venta"

    # Carrito de compras
    carrito_items = []
    total_venta = 0.0

    # Productos disponibles (simulación - integrar con DB)
    productos = [
        {"id": 1, "nombre": "Membresía Mensual", "precio": 150.00, "tipo": "membresia"},
        {"id": 2, "nombre": "Membresía Trimestral", "precio": 400.00, "tipo": "membresia"},
        {"id": 3, "nombre": "Membresía Anual", "precio": 1500.00, "tipo": "membresia"},
        {"id": 4, "nombre": "Proteína Whey 1kg", "precio": 80.00, "tipo": "suplemento"},
        {"id": 5, "nombre": "Creatina 300g", "precio": 45.00, "tipo": "suplemento"},
        {"id": 6, "nombre": "Shaker", "precio": 15.00, "tipo": "accesorio"},
        {"id": 7, "nombre": "Toalla Deportiva", "precio": 25.00, "tipo": "accesorio"},
        {"id": 8, "nombre": "Guantes de Gym", "precio": 35.00, "tipo": "accesorio"},
    ]

    # Contenedores
    productos_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=200,
        child_aspect_ratio=0.85,
        spacing=10,
        run_spacing=10,
        padding=10
    )

    carrito_container = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, height=300)
    total_text = ft.Text("S/. 0.00", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR)

    # Cliente seleccionado
    cliente_selected = None
    cliente_info_text = ft.Text(
        "No hay cliente seleccionado",
        size=12,
        color=TEXT_SECONDARY
    )

    def crear_producto_card(producto):
        """Crear tarjeta de producto"""
        icon_map = {
            "membresia": ft.Icons.CARD_MEMBERSHIP,
            "suplemento": ft.Icons.LOCAL_DRINK,
            "accesorio": ft.Icons.SHOPPING_BAG
        }

        color_map = {
            "membresia": PRIMARY_COLOR,
            "suplemento": "#4CAF50",
            "accesorio": "#2196F3"
        }

        icon = icon_map.get(producto['tipo'], ft.Icons.SHOPPING_CART)
        color = color_map.get(producto['tipo'], PRIMARY_COLOR)

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, size=40, color=color),
                    bgcolor=f"{color}22",
                    border_radius=10,
                    padding=15,
                    alignment=ft.alignment.center
                ),
                ft.Text(
                    producto['nombre'],
                    size=13,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                ft.Text(
                    f"S/. {producto['precio']:.2f}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.ElevatedButton(
                    "Agregar",
                    icon=ft.Icons.ADD_SHOPPING_CART,
                    bgcolor=color,
                    color=ft.Colors.BLACK,
                    width=150,
                    height=35,
                    on_click=lambda _, p=producto: agregar_al_carrito(p)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            bgcolor=CARD_BG,
            border_radius=12,
            padding=15,
            border=ft.border.all(1, "#333333")
        )

    def agregar_al_carrito(producto):
        """Agregar producto al carrito"""
        nonlocal total_venta

        # Buscar si ya existe en el carrito
        existe = False
        for item in carrito_items:
            if item['id'] == producto['id']:
                item['cantidad'] += 1
                item['subtotal'] = item['cantidad'] * item['precio']
                existe = True
                break

        if not existe:
            carrito_items.append({
                'id': producto['id'],
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'cantidad': 1,
                'subtotal': producto['precio']
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
                item['cantidad'] += cambio
                if item['cantidad'] <= 0:
                    quitar_del_carrito(producto_id)
                    return
                item['subtotal'] = item['cantidad'] * item['precio']
                break
        actualizar_carrito()

    def actualizar_carrito():
        """Actualizar visualización del carrito"""
        nonlocal total_venta
        carrito_container.controls.clear()

        if not carrito_items:
            carrito_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=50, color=TEXT_SECONDARY),
                        ft.Text("Carrito vacío", color=TEXT_SECONDARY, size=14),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=40,
                    alignment=ft.alignment.center
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
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY
                                ),
                                ft.Text(
                                    f"S/. {item['precio']:.2f}",
                                    size=11,
                                    color=TEXT_SECONDARY
                                ),
                            ], spacing=2, expand=True),
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.REMOVE,
                                    icon_size=16,
                                    icon_color=TEXT_SECONDARY,
                                    on_click=lambda _, id=item['id']: actualizar_cantidad(id, -1)
                                ),
                                ft.Text(
                                    str(item['cantidad']),
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    icon_size=16,
                                    icon_color=PRIMARY_COLOR,
                                    on_click=lambda _, id=item['id']: actualizar_cantidad(id, 1)
                                ),
                            ], spacing=0),
                            ft.Text(
                                f"S/. {item['subtotal']:.2f}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=PRIMARY_COLOR,
                                width=80,
                                text_align=ft.TextAlign.RIGHT
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_size=18,
                                icon_color="#ef5350",
                                on_click=lambda _, id=item['id']: quitar_del_carrito(id)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=CARD_BG,
                        border_radius=8,
                        padding=10,
                        border=ft.border.all(1, "#333333"),
                        margin=ft.margin.only(bottom=5)
                    )
                )

        total_text.value = f"S/. {total_venta:.2f}"
        page.update()

    def procesar_venta():
        """Procesar la venta"""
        if not carrito_items:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("El carrito está vacío"),
                bgcolor="#ef5350"
            )
            page.snack_bar.open = True
            page.update()
            return

        # Aquí procesarías la venta en la BD
        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"Venta procesada exitosamente - Total: S/. {total_venta:.2f}"
            ),
            bgcolor=PRIMARY_COLOR,
            duration=3000
        )
        page.snack_bar.open = True

        # Limpiar carrito
        carrito_items.clear()
        actualizar_carrito()

    def limpiar_carrito():
        """Limpiar el carrito"""
        carrito_items.clear()
        actualizar_carrito()

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=PRIMARY_COLOR,
                on_click=lambda _: on_back()
            ),
            ft.Text(
                "Punto de Venta - BLESSED GYM",
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

    # Cargar productos en el grid
    for producto in productos:
        productos_grid.controls.append(crear_producto_card(producto))

    # Panel de productos
    productos_panel = ft.Container(
        content=ft.Column([
            ft.Text(
                "Productos Disponibles",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            productos_grid,
        ], spacing=10),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        expand=2
    )

    # Panel de carrito
    carrito_panel = ft.Container(
        content=ft.Column([
            ft.Text(
                "Carrito de Compras",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=PRIMARY_COLOR
            ),
            ft.Divider(height=1, color="#333333"),
            carrito_container,
            ft.Divider(height=1, color="#333333"),
            ft.Row([
                ft.Text("TOTAL:", size=18, weight=ft.FontWeight.BOLD, color=TEXT_SECONDARY),
                total_text,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            ft.ElevatedButton(
                "PROCESAR VENTA",
                icon=ft.Icons.POINT_OF_SALE,
                bgcolor=PRIMARY_COLOR,
                color=ft.Colors.BLACK,
                width=280,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                on_click=lambda _: procesar_venta()
            ),
            ft.TextButton(
                "Limpiar Carrito",
                icon=ft.Icons.CLEAR_ALL,
                style=ft.ButtonStyle(color=TEXT_SECONDARY),
                on_click=lambda _: limpiar_carrito()
            ),
        ], spacing=10),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333"),
        width=350
    )

    # Layout principal con dos columnas
    content_row = ft.Row([
        productos_panel,
        carrito_panel
    ], spacing=0, expand=True)

    main_content = ft.Column([
        header,
        content_row
    ], spacing=0, expand=True)

    page.add(
        ft.Container(
            content=main_content,
            bgcolor=BACKGROUND_DARK,
            expand=True
        )
    )

    # Inicializar carrito vacío
    actualizar_carrito()
