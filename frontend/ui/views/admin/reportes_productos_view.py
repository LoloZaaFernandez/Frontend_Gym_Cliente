"""
Vista de Reportes de Productos
Muestra reportes de valor de inventario, margen de ganancia y estadísticas por categoría
"""

import flet as ft
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button
from ui.components.molecules import create_card_container, create_empty_state
from ui.utils.messages import mostrar_error


def show_reportes_productos_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Vista de Reportes de Productos
    """
    page.title = "BLESSED GYM - Reportes de Productos"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Estado
    tab_actual = [0]  # 0: Valor Inventario, 1: Margen Ganancia, 2: Por Categoría

    # ==========================================
    # TAB 1: VALOR DE INVENTARIO
    # ==========================================
    def crear_tab_valor_inventario():
        """Tab de valor de inventario"""
        container = ft.Column(spacing=Theme.SPACING["lg"], scroll=ft.ScrollMode.AUTO)

        def cargar_reporte():
            container.controls.clear()
            try:
                reporte = api.get_reporte_valor_inventario()

                # Resumen
                resumen_card = create_card_container(
                    content=ft.Column([
                        ft.Text(
                            "Resumen de Inventario",
                            size=Theme.FONT_SIZE["xl"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=Theme.TEXT_PRIMARY
                        ),
                        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Total Productos", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                                    ft.Text(
                                        str(reporte.get('total_productos', 0)),
                                        size=Theme.FONT_SIZE["2xl"],
                                        weight=Theme.FONT_WEIGHT["bold"],
                                        color=Theme.PRIMARY
                                    ),
                                ], spacing=4),
                                expand=True,
                                padding=Theme.SPACING["md"],
                                bgcolor=f"{Theme.PRIMARY}10",
                                border_radius=Theme.RADIUS["md"]
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Valor Costo", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                                    ft.Text(
                                        f"S/ {reporte.get('valor_total_costo', 0):,.2f}",
                                        size=Theme.FONT_SIZE["2xl"],
                                        weight=Theme.FONT_WEIGHT["bold"],
                                        color=Theme.INFO
                                    ),
                                ], spacing=4),
                                expand=True,
                                padding=Theme.SPACING["md"],
                                bgcolor=f"{Theme.INFO}10",
                                border_radius=Theme.RADIUS["md"]
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Valor Venta", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                                    ft.Text(
                                        f"S/ {reporte.get('valor_total_venta', 0):,.2f}",
                                        size=Theme.FONT_SIZE["2xl"],
                                        weight=Theme.FONT_WEIGHT["bold"],
                                        color=Theme.SUCCESS
                                    ),
                                ], spacing=4),
                                expand=True,
                                padding=Theme.SPACING["md"],
                                bgcolor=f"{Theme.SUCCESS}10",
                                border_radius=Theme.RADIUS["md"]
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Ganancia Potencial", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                                    ft.Text(
                                        f"S/ {reporte.get('ganancia_potencial_total', 0):,.2f}",
                                        size=Theme.FONT_SIZE["2xl"],
                                        weight=Theme.FONT_WEIGHT["bold"],
                                        color=Theme.WARNING
                                    ),
                                ], spacing=4),
                                expand=True,
                                padding=Theme.SPACING["md"],
                                bgcolor=f"{Theme.WARNING}10",
                                border_radius=Theme.RADIUS["md"]
                            ),
                        ], spacing=Theme.SPACING["md"]),
                    ], spacing=Theme.SPACING["md"]),
                    padding=Theme.SPACING["2xl"],
                    shadow="md"
                )
                container.controls.append(resumen_card)

                # Tabla de productos
                productos = reporte.get('productos', [])
                if productos:
                    tabla_card = create_card_container(
                        content=ft.Column([
                            ft.Text(
                                f"Desglose por Producto ({len(productos)} items)",
                                size=Theme.FONT_SIZE["lg"],
                                weight=Theme.FONT_WEIGHT["bold"],
                                color=Theme.TEXT_PRIMARY
                            ),
                            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                            crear_tabla_valor_inventario(productos),
                        ], spacing=Theme.SPACING["md"]),
                        padding=Theme.SPACING["2xl"],
                        shadow="md"
                    )
                    container.controls.append(tabla_card)

            except Exception as e:
                container.controls.append(
                    create_empty_state(
                        message="Error al cargar reporte",
                        icon=ft.Icons.ERROR,
                        secondary_message=str(e)
                    )
                )

            page.update()

        cargar_reporte()
        return container

    def crear_tabla_valor_inventario(productos):
        """Crear tabla de valor de inventario"""
        tabla = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)

        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Text("Producto", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=3),
                ft.Text("SKU", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Stock", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Costo Unit.", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Venta Unit.", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Valor Costo", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Valor Venta", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Ganancia", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
            ], spacing=8),
            bgcolor=f"{Theme.PRIMARY}20",
            padding=Theme.SPACING["md"],
            border_radius=Theme.RADIUS["sm"]
        )
        tabla.controls.append(header)

        # Filas
        for p in productos[:50]:  # Limitar a 50 para performance
            fila = ft.Container(
                content=ft.Row([
                    ft.Text(p.get('nombre', ''), size=Theme.FONT_SIZE["sm"], expand=3, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(p.get('sku', ''), size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY, expand=1),
                    ft.Text(str(p.get('stock_actual', 0)), size=Theme.FONT_SIZE["sm"], expand=1),
                    ft.Text(f"S/ {p.get('precio_costo', 0):.2f}", size=Theme.FONT_SIZE["sm"], expand=1),
                    ft.Text(f"S/ {p.get('precio_venta', 0):.2f}", size=Theme.FONT_SIZE["sm"], color=Theme.SUCCESS, expand=1),
                    ft.Text(f"S/ {p.get('valor_inventario_costo', 0):,.2f}", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["medium"], expand=1),
                    ft.Text(f"S/ {p.get('valor_inventario_venta', 0):,.2f}", size=Theme.FONT_SIZE["sm"], color=Theme.SUCCESS, weight=Theme.FONT_WEIGHT["medium"], expand=1),
                    ft.Text(f"S/ {p.get('ganancia_potencial', 0):,.2f}", size=Theme.FONT_SIZE["sm"], color=Theme.WARNING, weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ], spacing=8),
                padding=Theme.SPACING["sm"],
                border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
            )
            tabla.controls.append(fila)

        return tabla

    # ==========================================
    # TAB 2: MARGEN DE GANANCIA
    # ==========================================
    def crear_tab_margen_ganancia():
        """Tab de productos por margen de ganancia"""
        container = ft.Column(spacing=Theme.SPACING["lg"], scroll=ft.ScrollMode.AUTO)

        def cargar_reporte():
            container.controls.clear()
            try:
                productos = api.get_productos_por_margen()

                if productos:
                    # Header
                    header_card = create_card_container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.TRENDING_UP, size=Theme.ICON_SIZE["lg"], color=Theme.SUCCESS),
                            ft.Text(
                                "Productos Más Rentables",
                                size=Theme.FONT_SIZE["xl"],
                                weight=Theme.FONT_WEIGHT["bold"],
                                color=Theme.TEXT_PRIMARY
                            ),
                            ft.Container(expand=True),
                            ft.Text(
                                f"{len(productos)} productos",
                                size=Theme.FONT_SIZE["md"],
                                color=Theme.TEXT_SECONDARY
                            ),
                        ], spacing=Theme.SPACING["md"]),
                        padding=Theme.SPACING["xl"]
                    )
                    container.controls.append(header_card)

                    # Top 10
                    top10_card = create_card_container(
                        content=ft.Column([
                            ft.Text("Top 10 Más Rentables", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"]),
                            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                            crear_tabla_margen(productos[:10]),
                        ], spacing=Theme.SPACING["md"]),
                        padding=Theme.SPACING["2xl"],
                        shadow="md"
                    )
                    container.controls.append(top10_card)

                    # Todos
                    if len(productos) > 10:
                        todos_card = create_card_container(
                            content=ft.Column([
                                ft.Text("Todos los Productos", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"]),
                                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                                crear_tabla_margen(productos),
                            ], spacing=Theme.SPACING["md"]),
                            padding=Theme.SPACING["2xl"],
                            shadow="md"
                        )
                        container.controls.append(todos_card)
                else:
                    container.controls.append(
                        create_empty_state(
                            message="No hay datos de margen",
                            icon=ft.Icons.TRENDING_DOWN
                        )
                    )

            except Exception as e:
                container.controls.append(
                    create_empty_state(
                        message="Error al cargar reporte",
                        icon=ft.Icons.ERROR,
                        secondary_message=str(e)
                    )
                )

            page.update()

        cargar_reporte()
        return container

    def crear_tabla_margen(productos):
        """Crear tabla de margen de ganancia"""
        tabla = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)

        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Text("#", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], width=40),
                ft.Text("Producto", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=3),
                ft.Text("SKU", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Costo", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Venta", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Margen %", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
                ft.Text("Ganancia S/", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], expand=1),
            ], spacing=8),
            bgcolor=f"{Theme.PRIMARY}20",
            padding=Theme.SPACING["md"],
            border_radius=Theme.RADIUS["sm"]
        )
        tabla.controls.append(header)

        # Filas
        for idx, p in enumerate(productos[:50], 1):
            margen = p.get('margen_porcentaje', 0)
            color_margen = Theme.SUCCESS if margen > 50 else Theme.WARNING if margen > 25 else Theme.ERROR

            fila = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text(
                            str(idx),
                            size=Theme.FONT_SIZE["sm"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=Theme.PRIMARY
                        ),
                        width=40,
                        alignment=ft.alignment.center,
                        bgcolor=f"{Theme.PRIMARY}15",
                        border_radius=Theme.RADIUS["sm"]
                    ),
                    ft.Text(p.get('nombre', ''), size=Theme.FONT_SIZE["sm"], expand=3, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(p.get('sku', ''), size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY, expand=1),
                    ft.Text(f"S/ {p.get('precio_costo', 0):.2f}", size=Theme.FONT_SIZE["sm"], expand=1),
                    ft.Text(f"S/ {p.get('precio_venta', 0):.2f}", size=Theme.FONT_SIZE["sm"], color=Theme.SUCCESS, expand=1),
                    ft.Text(
                        f"{margen:.1f}%",
                        size=Theme.FONT_SIZE["sm"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=color_margen,
                        expand=1
                    ),
                    ft.Text(
                        f"S/ {p.get('ganancia_unitaria', 0):.2f}",
                        size=Theme.FONT_SIZE["sm"],
                        weight=Theme.FONT_WEIGHT["medium"],
                        color=Theme.WARNING,
                        expand=1
                    ),
                ], spacing=8),
                padding=Theme.SPACING["sm"],
                border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
            )
            tabla.controls.append(fila)

        return tabla

    # ==========================================
    # TAB 3: POR CATEGORÍA
    # ==========================================
    def crear_tab_por_categoria():
        """Tab de estadísticas por categoría"""
        container = ft.Column(spacing=Theme.SPACING["lg"], scroll=ft.ScrollMode.AUTO)

        def cargar_reporte():
            container.controls.clear()
            try:
                categorias = api.get_estadisticas_por_categoria()

                if categorias:
                    for cat in categorias:
                        card = create_card_container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.CATEGORY, color=Theme.PRIMARY, size=32),
                                    ft.Text(
                                        cat.get('nombre_categoria', 'Sin nombre'),
                                        size=Theme.FONT_SIZE["xl"],
                                        weight=Theme.FONT_WEIGHT["bold"],
                                        color=Theme.TEXT_PRIMARY,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            f"{cat.get('total_productos', 0)} productos",
                                            size=Theme.FONT_SIZE["sm"],
                                            color=Theme.TEXT_PRIMARY
                                        ),
                                        bgcolor=f"{Theme.PRIMARY}15",
                                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                        border_radius=Theme.RADIUS["full"]
                                    ),
                                ], spacing=Theme.SPACING["md"]),
                                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Valor Inventario (Costo)", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                                            ft.Text(
                                                f"S/ {cat.get('valor_inventario', 0):,.2f}",
                                                size=Theme.FONT_SIZE["lg"],
                                                weight=Theme.FONT_WEIGHT["bold"],
                                                color=Theme.INFO
                                            ),
                                        ], spacing=4),
                                        expand=True,
                                        padding=Theme.SPACING["md"],
                                        bgcolor=f"{Theme.INFO}10",
                                        border_radius=Theme.RADIUS["md"]
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Valor Venta", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                                            ft.Text(
                                                f"S/ {cat.get('valor_venta_inventario', 0):,.2f}",
                                                size=Theme.FONT_SIZE["lg"],
                                                weight=Theme.FONT_WEIGHT["bold"],
                                                color=Theme.SUCCESS
                                            ),
                                        ], spacing=4),
                                        expand=True,
                                        padding=Theme.SPACING["md"],
                                        bgcolor=f"{Theme.SUCCESS}10",
                                        border_radius=Theme.RADIUS["md"]
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Ganancia Potencial", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                                            ft.Text(
                                                f"S/ {cat.get('ganancia_potencial', 0):,.2f}",
                                                size=Theme.FONT_SIZE["lg"],
                                                weight=Theme.FONT_WEIGHT["bold"],
                                                color=Theme.WARNING
                                            ),
                                        ], spacing=4),
                                        expand=True,
                                        padding=Theme.SPACING["md"],
                                        bgcolor=f"{Theme.WARNING}10",
                                        border_radius=Theme.RADIUS["md"]
                                    ),
                                ], spacing=Theme.SPACING["md"]),
                            ], spacing=Theme.SPACING["md"]),
                            padding=Theme.SPACING["2xl"],
                            shadow="md"
                        )
                        container.controls.append(card)
                else:
                    container.controls.append(
                        create_empty_state(
                            message="No hay categorías",
                            icon=ft.Icons.CATEGORY
                        )
                    )

            except Exception as e:
                container.controls.append(
                    create_empty_state(
                        message="Error al cargar reporte",
                        icon=ft.Icons.ERROR,
                        secondary_message=str(e)
                    )
                )

            page.update()

        cargar_reporte()
        return container

    # ==========================================
    # TABS
    # ==========================================
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Valor de Inventario",
                icon=ft.Icons.ATTACH_MONEY,
                content=ft.Container(
                    content=crear_tab_valor_inventario(),
                    padding=Theme.SPACING["2xl"]
                )
            ),
            ft.Tab(
                text="Margen de Ganancia",
                icon=ft.Icons.TRENDING_UP,
                content=ft.Container(
                    content=crear_tab_margen_ganancia(),
                    padding=Theme.SPACING["2xl"]
                )
            ),
            ft.Tab(
                text="Por Categoría",
                icon=ft.Icons.CATEGORY,
                content=ft.Container(
                    content=crear_tab_por_categoria(),
                    padding=Theme.SPACING["2xl"]
                )
            ),
        ],
        expand=True
    )

    # Layout completo
    content = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.ANALYTICS, size=Theme.ICON_SIZE["lg"], color=Theme.PRIMARY),
            ft.Text(
                "Reportes de Productos",
                size=Theme.FONT_SIZE["2xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.TEXT_PRIMARY
            ),
        ], spacing=Theme.SPACING["md"]),
        ft.Container(height=Theme.SPACING["lg"]),
        tabs,
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
