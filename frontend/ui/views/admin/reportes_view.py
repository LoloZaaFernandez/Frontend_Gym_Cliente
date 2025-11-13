"""
Vista de Reportes y Estadísticas - Sistema Completo
Incluye: Reportes de Pagos, Clientes y Asistencias con datos reales de la API
"""

import flet as ft
from datetime import datetime, timedelta
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button
from ui.components.molecules import create_card_container, create_stat_card
from ui.utils.messages import mostrar_exito, mostrar_error
from ui.utils.datetime_utils import parse_datetime_from_api, format_datetime_display, get_now_local


def show_reportes_view(page: ft.Page, auth_service, on_section_click, current_section):
    """Vista de reportes y estadísticas con datos reales"""
    page.title = "BLESSED GYM - Reportes"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Referencias para actualizar contenido
    content_ref = ft.Ref[ft.Container]()
    selected_tab = [0]  # 0: Pagos, 1: Clientes, 2: Asistencias

    # ==========================================
    # REPORTE DE PAGOS
    # ==========================================
    def create_reporte_pagos():
        """Crear vista de reportes de pagos"""
        periodo_seleccionado = ["dia"]  # dia, semana, mes, anio
        datos_reporte = [{}]

        def obtener_datos_ejemplo():
            """Retornar datos de ejemplo si el backend no responde"""
            from datetime import datetime
            return {
                'total_pagos': 0,
                'total_monto': 0.0,
                'total_clientes': 0,
                'desglose_metodo_pago': [],
                'pagos': []
            }

        def cargar_reporte_pagos():
            """Cargar datos del reporte según el período"""
            try:
                print(f"DEBUG REPORTES: Cargando reporte de pagos - período: {periodo_seleccionado[0]}")

                if periodo_seleccionado[0] == "dia":
                    datos_reporte[0] = api.get_reporte_pagos_dia()
                elif periodo_seleccionado[0] == "semana":
                    datos_reporte[0] = api.get_reporte_pagos_semana()
                elif periodo_seleccionado[0] == "mes":
                    datos_reporte[0] = api.get_reporte_pagos_mes()
                elif periodo_seleccionado[0] == "anio":
                    datos_reporte[0] = api.get_reporte_pagos_anio()

                print(f"DEBUG REPORTES: Datos recibidos: {datos_reporte[0]}")
                print(f"DEBUG REPORTES: Tipo de datos: {type(datos_reporte[0])}")
                print(f"DEBUG REPORTES: Claves disponibles: {datos_reporte[0].keys() if isinstance(datos_reporte[0], dict) else 'No es un dict'}")

                # Si la API retorna vacío, usar datos de ejemplo
                if not datos_reporte[0] or len(datos_reporte[0]) == 0:
                    print("ADVERTENCIA REPORTES: La API retornó datos vacíos. Mostrando estructura vacía.")
                    datos_reporte[0] = obtener_datos_ejemplo()

                actualizar_vista_pagos()
            except Exception as e:
                print(f"ERROR REPORTES: Error al cargar reporte de pagos: {e}")
                import traceback
                traceback.print_exc()
                mostrar_error(page, f"Error al cargar reporte: {str(e)}")

        def cambiar_periodo(periodo):
            """Cambiar período del reporte"""
            periodo_seleccionado[0] = periodo
            cargar_reporte_pagos()

        def get_icono_metodo_pago(metodo):
            """Obtener icono específico según método de pago"""
            metodo_lower = metodo.lower() if metodo else ""

            if "yape" in metodo_lower:
                return ft.Icons.PHONE_ANDROID  # Icono de teléfono para Yape
            elif "efectivo" in metodo_lower:
                return ft.Icons.PAYMENTS  # Icono de dinero para efectivo
            elif "tarjeta" in metodo_lower or "visa" in metodo_lower or "mastercard" in metodo_lower:
                return ft.Icons.CREDIT_CARD
            elif "transferencia" in metodo_lower:
                return ft.Icons.ACCOUNT_BALANCE
            else:
                return ft.Icons.PAYMENT  # Icono genérico

        def actualizar_vista_pagos():
            """Actualizar la vista con los datos del reporte"""
            reporte = datos_reporte[0]

            print(f"DEBUG VISTA PAGOS: Actualizando vista con reporte: {reporte}")

            # Estadísticas principales
            total_pagos = reporte.get('total_pagos', 0)
            total_monto = reporte.get('total_monto', 0.0)
            total_clientes = reporte.get('total_clientes', 0)

            print(f"DEBUG VISTA PAGOS: total_pagos={total_pagos}, total_monto={total_monto}, total_clientes={total_clientes}")

            # Desglose por método de pago
            desglose_metodo = reporte.get('desglose_metodo_pago', [])
            print(f"DEBUG VISTA PAGOS: desglose_metodo={desglose_metodo}")

            # Crear cards de estadísticas
            stats = ft.Row([
                create_stat_card("Total Pagos", str(total_pagos), ft.Icons.RECEIPT, Theme.PRIMARY),
                create_stat_card("Total Recaudado", f"S/ {total_monto:,.2f}", ft.Icons.ATTACH_MONEY, Theme.SUCCESS),
                create_stat_card("Clientes", str(total_clientes), ft.Icons.PEOPLE, Theme.INFO),
            ], spacing=Theme.SPACING["xl"], wrap=True)

            # Desglose por método de pago
            metodos_container = ft.Column(spacing=Theme.SPACING["md"])

            if desglose_metodo:
                for metodo_data in desglose_metodo:
                    metodo = metodo_data.get('metodo_pago', 'Desconocido')
                    cantidad = metodo_data.get('cantidad', 0)
                    monto = metodo_data.get('monto_total', 0.0)
                    porcentaje = (cantidad / total_pagos * 100) if total_pagos > 0 else 0

                    # Color según método
                    if "Yape" in metodo:
                        color = "#9C27B0"  # Morado para Yape
                    elif "Efectivo" in metodo:
                        color = Theme.SUCCESS  # Verde para Efectivo
                    else:
                        color = Theme.PRIMARY

                    # Obtener icono específico
                    icono = get_icono_metodo_pago(metodo)

                    metodos_container.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Column([
                                        ft.Icon(icono, size=32, color=color),
                                    ], alignment=ft.MainAxisAlignment.CENTER, width=50),
                                    ft.Column([
                                        ft.Text(metodo, size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                        ft.Text(f"{cantidad} pagos ({porcentaje:.1f}%)", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                                    ], spacing=4, expand=True),
                                    ft.Column([
                                        ft.Text(f"S/ {monto:,.2f}", size=Theme.FONT_SIZE["xl"], weight=Theme.FONT_WEIGHT["bold"], color=color, text_align=ft.TextAlign.RIGHT),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.END),
                                ], spacing=Theme.SPACING["lg"]),
                                # Barra de progreso
                                ft.Container(
                                    content=ft.Container(
                                        bgcolor=color,
                                        border_radius=Theme.RADIUS["sm"],
                                        height=8,
                                    ),
                                    width=f"{porcentaje}%",
                                    bgcolor=f"{color}22",
                                    border_radius=Theme.RADIUS["sm"],
                                    height=8,
                                    margin=ft.margin.only(top=Theme.SPACING["sm"])
                                ),
                            ], spacing=Theme.SPACING["xs"]),
                            padding=Theme.SPACING["lg"],
                            bgcolor=Theme.CARD_BG,
                            border_radius=Theme.RADIUS["md"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT)
                        )
                    )
                # Agregar tarjeta de TOTAL al final
                metodos_container.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=32, color=Theme.PRIMARY),
                            ], alignment=ft.MainAxisAlignment.CENTER, width=50),
                            ft.Column([
                                ft.Text("TOTAL GENERAL", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                ft.Text(f"{total_pagos} pagos totales", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                            ], spacing=4, expand=True),
                            ft.Column([
                                ft.Text(f"S/ {total_monto:,.2f}", size=Theme.FONT_SIZE["2xl"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY, text_align=ft.TextAlign.RIGHT),
                            ], horizontal_alignment=ft.CrossAxisAlignment.END),
                        ], spacing=Theme.SPACING["lg"]),
                        padding=Theme.SPACING["xl"],
                        bgcolor=f"{Theme.PRIMARY}15",
                        border_radius=Theme.RADIUS["lg"],
                        border=ft.border.all(2, Theme.PRIMARY)
                    )
                )
            else:
                metodos_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=48, color=Theme.TEXT_SECONDARY),
                            ft.Text(
                                "No hay pagos registrados en este período",
                                size=Theme.FONT_SIZE["md"],
                                color=Theme.TEXT_PRIMARY,
                                weight=Theme.FONT_WEIGHT["medium"],
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Los pagos aparecerán aquí cuando se registren membresías",
                                size=Theme.FONT_SIZE["sm"],
                                color=Theme.TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
                        padding=Theme.SPACING["2xl"],
                        alignment=ft.alignment.center
                    )
                )

            # Lista de pagos
            pagos_lista = reporte.get('pagos', [])
            pagos_container = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO, height=300)

            if pagos_lista:
                for pago in pagos_lista[:20]:  # Mostrar últimos 20
                    cliente_nombre = pago.get('nombre_cliente', 'Cliente desconocido')
                    membresia = pago.get('nombre_membresia', 'N/A')
                    monto = pago.get('monto', 0.0)
                    metodo = pago.get('metodo_pago', 'N/A')
                    fecha = pago.get('fecha_pago', '')

                    # Formatear fecha con conversión de timezone
                    try:
                        fecha_dt = parse_datetime_from_api(fecha)
                        if fecha_dt:
                            fecha_formateada = format_datetime_display(fecha_dt)
                        else:
                            fecha_formateada = fecha
                    except:
                        fecha_formateada = fecha

                    # Color e icono según método de pago
                    if "Yape" in metodo:
                        color_metodo = "#9C27B0"  # Morado para Yape
                    elif "Efectivo" in metodo:
                        color_metodo = Theme.SUCCESS  # Verde para Efectivo
                    else:
                        color_metodo = Theme.PRIMARY

                    icono_metodo = get_icono_metodo_pago(metodo)

                    pagos_container.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(cliente_nombre, size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                    ft.Text(membresia, size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                                ], spacing=2, expand=True),
                                ft.Column([
                                    ft.Text(f"S/ {monto:.2f}", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY, text_align=ft.TextAlign.RIGHT),
                                    ft.Row([
                                        ft.Icon(icono_metodo, size=14, color=color_metodo),
                                        ft.Text(metodo, size=Theme.FONT_SIZE["xs"], color=color_metodo, weight=Theme.FONT_WEIGHT["medium"]),
                                    ], spacing=4),
                                ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=2),
                                ft.Text(fecha_formateada, size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY, width=120),
                            ], spacing=Theme.SPACING["md"]),
                            padding=Theme.SPACING["md"],
                            bgcolor=Theme.CARD_BG,
                            border_radius=Theme.RADIUS["sm"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT)
                        )
                    )
            else:
                pagos_container.controls.append(
                    ft.Text("No hay pagos registrados", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY)
                )

            # Actualizar contenido
            content_pagos.content = ft.Column([
                # Filtros de período
                ft.Row([
                    create_outlined_button("Hoy", lambda _: cambiar_periodo("dia"), icon=ft.Icons.TODAY),
                    create_outlined_button("Esta Semana", lambda _: cambiar_periodo("semana"), icon=ft.Icons.DATE_RANGE),
                    create_outlined_button("Este Mes", lambda _: cambiar_periodo("mes"), icon=ft.Icons.CALENDAR_MONTH),
                    create_outlined_button("Este Año", lambda _: cambiar_periodo("anio"), icon=ft.Icons.CALENDAR_TODAY),
                ], spacing=Theme.SPACING["md"]),
                ft.Container(height=Theme.SPACING["lg"]),
                stats,
                ft.Container(height=Theme.SPACING["lg"]),
                create_card_container(
                    content=ft.Column([
                        ft.Text("Desglose por Método de Pago", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                        metodos_container,
                    ], spacing=Theme.SPACING["lg"]),
                    padding=Theme.SPACING["xl"]
                ),
                ft.Container(height=Theme.SPACING["lg"]),
                create_card_container(
                    content=ft.Column([
                        ft.Text("Últimos Pagos", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                        pagos_container,
                    ], spacing=Theme.SPACING["lg"]),
                    padding=Theme.SPACING["xl"]
                ),
            ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

            page.update()

        # Container principal para pagos
        content_pagos = ft.Container(expand=True)

        # Cargar datos iniciales
        cargar_reporte_pagos()

        return content_pagos

    # ==========================================
    # REPORTE DE CLIENTES
    # ==========================================
    def create_reporte_clientes():
        """Crear vista de reportes de clientes"""
        tipo_reporte = ["general"]  # general, nuevos, por_vencer, vencidas

        def cargar_reporte_clientes():
            """Cargar datos del reporte de clientes"""
            try:
                if tipo_reporte[0] == "general":
                    datos = api.get_reporte_clientes_general()
                    mostrar_reporte_general(datos)
                elif tipo_reporte[0] == "nuevos":
                    datos = api.get_reporte_clientes_nuevos()
                    mostrar_reporte_nuevos(datos)
                elif tipo_reporte[0] == "por_vencer":
                    datos = api.get_reporte_clientes_membresia_por_vencer(dias=7)
                    mostrar_reporte_por_vencer(datos)
                elif tipo_reporte[0] == "vencidas":
                    datos = api.get_reporte_clientes_membresia_vencida()
                    mostrar_reporte_vencidas(datos)
            except Exception as e:
                print(f"Error al cargar reporte de clientes: {e}")
                mostrar_error(page, f"Error al cargar reporte: {str(e)}")

        def cambiar_tipo_reporte(tipo):
            """Cambiar tipo de reporte"""
            tipo_reporte[0] = tipo
            cargar_reporte_clientes()

        def mostrar_reporte_general(datos):
            """Mostrar reporte general de clientes"""
            total_clientes = datos.get('total_clientes', 0)
            clientes_activos = datos.get('clientes_activos', 0)
            clientes_inactivos = datos.get('clientes_inactivos', 0)
            membresias_activas = datos.get('membresias_activas', 0)
            membresias_vencidas = datos.get('membresias_vencidas', 0)
            membresias_por_vencer = datos.get('membresias_por_vencer', 0)

            stats = ft.Column([
                ft.Row([
                    create_stat_card("Total Clientes", str(total_clientes), ft.Icons.PEOPLE, Theme.PRIMARY),
                    create_stat_card("Activos", str(clientes_activos), ft.Icons.CHECK_CIRCLE, Theme.SUCCESS),
                    create_stat_card("Inactivos", str(clientes_inactivos), ft.Icons.CANCEL, Theme.ERROR),
                ], spacing=Theme.SPACING["xl"], wrap=True),
                ft.Container(height=Theme.SPACING["lg"]),
                ft.Row([
                    create_stat_card("Membresías Activas", str(membresias_activas), ft.Icons.CARD_MEMBERSHIP, Theme.INFO),
                    create_stat_card("Por Vencer", str(membresias_por_vencer), ft.Icons.WARNING, Theme.WARNING),
                    create_stat_card("Vencidas", str(membresias_vencidas), ft.Icons.ERROR, Theme.ERROR),
                ], spacing=Theme.SPACING["xl"], wrap=True),
            ], spacing=0)

            content_clientes.content = ft.Column([
                ft.Row([
                    create_outlined_button("General", lambda _: cambiar_tipo_reporte("general"), icon=ft.Icons.DASHBOARD),
                    create_outlined_button("Nuevos", lambda _: cambiar_tipo_reporte("nuevos"), icon=ft.Icons.PERSON_ADD),
                    create_outlined_button("Por Vencer", lambda _: cambiar_tipo_reporte("por_vencer"), icon=ft.Icons.WARNING),
                    create_outlined_button("Vencidas", lambda _: cambiar_tipo_reporte("vencidas"), icon=ft.Icons.ERROR),
                ], spacing=Theme.SPACING["md"]),
                ft.Container(height=Theme.SPACING["lg"]),
                stats,
            ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

            page.update()

        def mostrar_reporte_nuevos(datos):
            """Mostrar reporte de clientes nuevos"""
            total_nuevos = datos.get('total_nuevos', 0)
            clientes = datos.get('clientes', [])

            lista_clientes = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO, height=400)

            for cliente in clientes:
                nombre = f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}"
                dni = cliente.get('dni', 'N/A')
                fecha_registro = cliente.get('fecha_registro', '')

                try:
                    fecha_dt = parse_datetime_from_api(fecha_registro)
                    if fecha_dt:
                        fecha_formateada = fecha_dt.strftime('%d/%m/%Y')
                    else:
                        fecha_formateada = fecha_registro
                except:
                    fecha_formateada = fecha_registro

                lista_clientes.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, size=24, color=Theme.PRIMARY),
                            ft.Column([
                                ft.Text(nombre, size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                ft.Text(f"DNI: {dni}", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ], spacing=2, expand=True),
                            ft.Text(fecha_formateada, size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        ], spacing=Theme.SPACING["md"]),
                        padding=Theme.SPACING["md"],
                        bgcolor=Theme.CARD_BG,
                        border_radius=Theme.RADIUS["sm"],
                        border=ft.border.all(1, Theme.BORDER_DEFAULT)
                    )
                )

            content_clientes.content = ft.Column([
                ft.Row([
                    create_outlined_button("General", lambda _: cambiar_tipo_reporte("general"), icon=ft.Icons.DASHBOARD),
                    create_outlined_button("Nuevos", lambda _: cambiar_tipo_reporte("nuevos"), icon=ft.Icons.PERSON_ADD),
                    create_outlined_button("Por Vencer", lambda _: cambiar_tipo_reporte("por_vencer"), icon=ft.Icons.WARNING),
                    create_outlined_button("Vencidas", lambda _: cambiar_tipo_reporte("vencidas"), icon=ft.Icons.ERROR),
                ], spacing=Theme.SPACING["md"]),
                ft.Container(height=Theme.SPACING["lg"]),
                create_stat_card("Clientes Nuevos", str(total_nuevos), ft.Icons.PERSON_ADD, Theme.SUCCESS),
                ft.Container(height=Theme.SPACING["lg"]),
                create_card_container(
                    content=ft.Column([
                        ft.Text("Lista de Clientes Nuevos", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                        lista_clientes,
                    ], spacing=Theme.SPACING["lg"]),
                    padding=Theme.SPACING["xl"]
                ),
            ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

            page.update()

        def mostrar_reporte_por_vencer(datos):
            """Mostrar reporte de membresías por vencer"""
            total = datos.get('total_clientes', 0)
            clientes = datos.get('clientes', [])

            lista_clientes = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO, height=400)

            for cliente in clientes:
                nombre = f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}"
                dni = cliente.get('dni', 'N/A')
                tipo_membresia = cliente.get('tipo_membresia', 'N/A')
                fecha_vencimiento = cliente.get('fecha_vencimiento', '')
                dias_restantes = cliente.get('dias_restantes', 0)

                try:
                    fecha_dt = parse_datetime_from_api(fecha_vencimiento)
                    if fecha_dt:
                        fecha_formateada = fecha_dt.strftime('%d/%m/%Y')
                    else:
                        fecha_formateada = fecha_vencimiento
                except:
                    fecha_formateada = fecha_vencimiento

                color_alerta = Theme.WARNING if dias_restantes <= 3 else Theme.INFO

                lista_clientes.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.WARNING, size=24, color=color_alerta),
                            ft.Column([
                                ft.Text(nombre, size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                ft.Text(f"DNI: {dni} | {tipo_membresia}", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ], spacing=2, expand=True),
                            ft.Container(
                                content=ft.Text(f"{dias_restantes} días", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_PRIMARY, weight=Theme.FONT_WEIGHT["bold"]),
                                bgcolor=color_alerta,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=Theme.RADIUS["sm"]
                            ),
                            ft.Text(fecha_formateada, size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        ], spacing=Theme.SPACING["md"]),
                        padding=Theme.SPACING["md"],
                        bgcolor=Theme.CARD_BG,
                        border_radius=Theme.RADIUS["sm"],
                        border=ft.border.all(1, color_alerta)
                    )
                )

            content_clientes.content = ft.Column([
                ft.Row([
                    create_outlined_button("General", lambda _: cambiar_tipo_reporte("general"), icon=ft.Icons.DASHBOARD),
                    create_outlined_button("Nuevos", lambda _: cambiar_tipo_reporte("nuevos"), icon=ft.Icons.PERSON_ADD),
                    create_outlined_button("Por Vencer", lambda _: cambiar_tipo_reporte("por_vencer"), icon=ft.Icons.WARNING),
                    create_outlined_button("Vencidas", lambda _: cambiar_tipo_reporte("vencidas"), icon=ft.Icons.ERROR),
                ], spacing=Theme.SPACING["md"]),
                ft.Container(height=Theme.SPACING["lg"]),
                create_stat_card("Membresías por Vencer", str(total), ft.Icons.WARNING, Theme.WARNING),
                ft.Container(height=Theme.SPACING["lg"]),
                create_card_container(
                    content=ft.Column([
                        ft.Text("Clientes con Membresía por Vencer", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                        lista_clientes,
                    ], spacing=Theme.SPACING["lg"]),
                    padding=Theme.SPACING["xl"]
                ),
            ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

            page.update()

        def mostrar_reporte_vencidas(datos):
            """Mostrar reporte de membresías vencidas"""
            total = datos.get('total_clientes', 0)
            clientes = datos.get('clientes', [])

            lista_clientes = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO, height=400)

            for cliente in clientes:
                nombre = f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}"
                dni = cliente.get('dni', 'N/A')
                tipo_membresia = cliente.get('tipo_membresia', 'N/A')
                fecha_vencimiento = cliente.get('fecha_vencimiento', '')
                dias_vencidos = cliente.get('dias_vencidos', 0)

                try:
                    fecha_dt = parse_datetime_from_api(fecha_vencimiento)
                    if fecha_dt:
                        fecha_formateada = fecha_dt.strftime('%d/%m/%Y')
                    else:
                        fecha_formateada = fecha_vencimiento
                except:
                    fecha_formateada = fecha_vencimiento

                lista_clientes.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ERROR, size=24, color=Theme.ERROR),
                            ft.Column([
                                ft.Text(nombre, size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                ft.Text(f"DNI: {dni} | {tipo_membresia}", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ], spacing=2, expand=True),
                            ft.Container(
                                content=ft.Text(f"Hace {dias_vencidos} días", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_PRIMARY, weight=Theme.FONT_WEIGHT["bold"]),
                                bgcolor=Theme.ERROR,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=Theme.RADIUS["sm"]
                            ),
                            ft.Text(fecha_formateada, size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        ], spacing=Theme.SPACING["md"]),
                        padding=Theme.SPACING["md"],
                        bgcolor=Theme.CARD_BG,
                        border_radius=Theme.RADIUS["sm"],
                        border=ft.border.all(1, Theme.ERROR)
                    )
                )

            content_clientes.content = ft.Column([
                ft.Row([
                    create_outlined_button("General", lambda _: cambiar_tipo_reporte("general"), icon=ft.Icons.DASHBOARD),
                    create_outlined_button("Nuevos", lambda _: cambiar_tipo_reporte("nuevos"), icon=ft.Icons.PERSON_ADD),
                    create_outlined_button("Por Vencer", lambda _: cambiar_tipo_reporte("por_vencer"), icon=ft.Icons.WARNING),
                    create_outlined_button("Vencidas", lambda _: cambiar_tipo_reporte("vencidas"), icon=ft.Icons.ERROR),
                ], spacing=Theme.SPACING["md"]),
                ft.Container(height=Theme.SPACING["lg"]),
                create_stat_card("Membresías Vencidas", str(total), ft.Icons.ERROR, Theme.ERROR),
                ft.Container(height=Theme.SPACING["lg"]),
                create_card_container(
                    content=ft.Column([
                        ft.Text("Clientes con Membresía Vencida", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                        ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                        lista_clientes,
                    ], spacing=Theme.SPACING["lg"]),
                    padding=Theme.SPACING["xl"]
                ),
            ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

            page.update()

        # Container principal para clientes
        content_clientes = ft.Container(expand=True)

        # Cargar datos iniciales
        cargar_reporte_clientes()

        return content_clientes

    # ==========================================
    # REPORTE DE ASISTENCIAS
    # ==========================================
    def create_reporte_asistencias():
        """Crear vista de reportes de asistencias"""

        def cargar_reporte_asistencias():
            """Cargar datos del reporte de asistencias"""
            try:
                datos = api.get_reporte_asistencias()

                total_asistencias = datos.get('total_asistencias', 0)
                promedio_diario = datos.get('promedio_diario', 0.0)
                asistencias_por_dia = datos.get('asistencias_por_dia', [])
                clientes_frecuentes = datos.get('clientes_frecuentes', [])

                # Estadísticas
                stats = ft.Row([
                    create_stat_card("Total Asistencias", str(total_asistencias), ft.Icons.FITNESS_CENTER, Theme.PRIMARY),
                    create_stat_card("Promedio Diario", f"{promedio_diario:.1f}", ft.Icons.TRENDING_UP, Theme.INFO),
                ], spacing=Theme.SPACING["xl"], wrap=True)

                # Asistencias por día
                dias_container = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO, height=200)

                for dia_data in asistencias_por_dia:
                    fecha = dia_data.get('fecha', '')
                    cantidad = dia_data.get('cantidad', 0)

                    try:
                        fecha_dt = parse_datetime_from_api(fecha)
                        if fecha_dt:
                            fecha_formateada = fecha_dt.strftime('%d/%m/%Y - %A')
                        else:
                            fecha_formateada = fecha
                    except:
                        fecha_formateada = fecha

                    # Calcular porcentaje para barra
                    max_cantidad = max(d.get('cantidad', 0) for d in asistencias_por_dia) if asistencias_por_dia else 1
                    porcentaje = (cantidad / max_cantidad * 100) if max_cantidad > 0 else 0

                    dias_container.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(fecha_formateada, size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_PRIMARY, expand=True),
                                    ft.Text(f"{cantidad} asistencias", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                                ]),
                                ft.Container(
                                    content=ft.Container(
                                        bgcolor=Theme.PRIMARY,
                                        border_radius=Theme.RADIUS["sm"],
                                        height=6,
                                    ),
                                    width=f"{porcentaje}%",
                                    bgcolor=f"{Theme.PRIMARY}22",
                                    border_radius=Theme.RADIUS["sm"],
                                    height=6,
                                    margin=ft.margin.only(top=Theme.SPACING["xs"])
                                ),
                            ], spacing=Theme.SPACING["xs"]),
                            padding=Theme.SPACING["md"],
                            bgcolor=Theme.CARD_BG,
                            border_radius=Theme.RADIUS["sm"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT)
                        )
                    )

                # Clientes más frecuentes
                frecuentes_container = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO, height=300)

                for idx, cliente_data in enumerate(clientes_frecuentes, 1):
                    nombre = cliente_data.get('nombre_cliente', 'Desconocido')
                    total = cliente_data.get('total_asistencias', 0)

                    color_medalla = Theme.PRIMARY if idx <= 3 else Theme.TEXT_SECONDARY

                    frecuentes_container.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Text(str(idx), size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                    bgcolor=color_medalla,
                                    border_radius=Theme.RADIUS["full"],
                                    width=32,
                                    height=32,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text(nombre, size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_PRIMARY, expand=True),
                                ft.Text(f"{total} visitas", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                            ], spacing=Theme.SPACING["md"]),
                            padding=Theme.SPACING["md"],
                            bgcolor=Theme.CARD_BG,
                            border_radius=Theme.RADIUS["sm"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT)
                        )
                    )

                content_asistencias.content = ft.Column([
                    stats,
                    ft.Container(height=Theme.SPACING["lg"]),
                    create_card_container(
                        content=ft.Column([
                            ft.Text("Asistencias por Día", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                            dias_container,
                        ], spacing=Theme.SPACING["lg"]),
                        padding=Theme.SPACING["xl"]
                    ),
                    ft.Container(height=Theme.SPACING["lg"]),
                    create_card_container(
                        content=ft.Column([
                            ft.Text("Clientes Más Frecuentes (Top 10)", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                            frecuentes_container,
                        ], spacing=Theme.SPACING["lg"]),
                        padding=Theme.SPACING["xl"]
                    ),
                ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

                page.update()

            except Exception as e:
                print(f"Error al cargar reporte de asistencias: {e}")
                mostrar_error(page, f"Error al cargar reporte: {str(e)}")

        # Container principal para asistencias
        content_asistencias = ft.Container(expand=True)

        # Cargar datos iniciales
        cargar_reporte_asistencias()

        return content_asistencias

    # ==========================================
    # TABS Y LAYOUT PRINCIPAL
    # ==========================================
    def cambiar_tab(e):
        """Cambiar entre tabs"""
        selected_tab[0] = e.control.selected_index

        if selected_tab[0] == 0:
            content_ref.current.content = create_reporte_pagos()
        elif selected_tab[0] == 1:
            content_ref.current.content = create_reporte_clientes()
        elif selected_tab[0] == 2:
            content_ref.current.content = create_reporte_asistencias()

        page.update()

    # Tabs
    tabs = ft.Tabs(
        selected_index=0,
        on_change=cambiar_tab,
        tabs=[
            ft.Tab(
                text="Reportes de Pagos",
                icon=ft.Icons.PAYMENT,
            ),
            ft.Tab(
                text="Reportes de Clientes",
                icon=ft.Icons.PEOPLE,
            ),
            ft.Tab(
                text="Reportes de Asistencias",
                icon=ft.Icons.FITNESS_CENTER,
            ),
        ],
        indicator_color=Theme.PRIMARY,
        label_color=Theme.PRIMARY,
        unselected_label_color=Theme.TEXT_SECONDARY,
    )

    # Contenedor principal de tabs
    tabs_container = create_card_container(
        content=tabs,
        padding=0
    )

    # Contenedor de contenido
    content_container = ft.Container(
        ref=content_ref,
        content=create_reporte_pagos(),  # Iniciar con reporte de pagos
        expand=True
    )

    # Layout completo
    content = ft.Column([
        tabs_container,
        ft.Container(height=Theme.SPACING["lg"]),
        content_container,
    ], spacing=0, expand=True)

    # Usar base_layout
    create_base_layout(
        page=page,
        role="admin",
        current_section=current_section,
        on_section_click=on_section_click,
        content=ft.Container(content=content, padding=Theme.SPACING["xl"]),
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )
