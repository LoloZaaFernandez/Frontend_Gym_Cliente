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
    """Vista de reportes y estadísticas con diseño UX/UI profesional"""
    page.title = "BLESSED GYM - Reportes"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # ==========================================
    # PALETA DE COLORES MINIMALISTA Y COHESIVA
    # ==========================================
    COLORS_REPORTES = {
        # Color principal BLESSED
        "primary": "#FF6B35",            # Naranja BLESSED
        "primary_light": "#FF8A5C",      # Naranja claro
        "primary_glow": "#FF6B3540",     # Glow/sombra

        # Métodos de pago - Colores distintivos
        "yape": "#9C27B0",               # Púrpura para Yape
        "efectivo": "#00E676",           # Verde para Efectivo
        "tarjeta": "#2196F3",            # Azul para tarjeta
        "transferencia": "#FF9800",      # Naranja para transferencia
    }

    # Referencias para actualizar contenido
    content_ref = ft.Ref[ft.Container]()
    selected_tab = [0]  # 0: Pagos, 1: Clientes, 2: Asistencias

    # ==========================================
    # REPORTE DE PAGOS
    # ==========================================
    def create_reporte_pagos(periodo_inicial="dia"):
        """Crear vista de reportes de pagos"""
        periodo_seleccionado = [periodo_inicial]  # dia, semana, mes, anio
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

        def get_color_metodo_pago(metodo):
            """Obtener color específico según método de pago"""
            metodo_lower = metodo.lower() if metodo else ""

            if "yape" in metodo_lower:
                return COLORS_REPORTES["yape"]  # Púrpura para Yape
            elif "efectivo" in metodo_lower:
                return COLORS_REPORTES["efectivo"]  # Verde para Efectivo
            elif "tarjeta" in metodo_lower or "visa" in metodo_lower or "mastercard" in metodo_lower:
                return COLORS_REPORTES["tarjeta"]  # Azul para tarjeta
            elif "transferencia" in metodo_lower:
                return COLORS_REPORTES["transferencia"]  # Naranja para transferencia
            else:
                return COLORS_REPORTES["primary"]  # Naranja BLESSED genérico

        def actualizar_vista_pagos():
            """Actualizar la vista con los datos del reporte"""
            reporte = datos_reporte[0]

            print(f"DEBUG VISTA PAGOS: Actualizando vista con reporte: {reporte}")

            # Estadísticas principales
            total_pagos = reporte.get('total_pagos', 0)
            total_monto = reporte.get('monto_total', 0.0)  # CORREGIDO: era 'total_monto'

            # Contar clientes únicos desde detalle_pagos
            detalle_pagos = reporte.get('detalle_pagos', [])
            clientes_unicos = set()
            for pago in detalle_pagos:
                id_cliente = pago.get('id_cliente')
                if id_cliente:
                    clientes_unicos.add(id_cliente)
            total_clientes = len(clientes_unicos)

            print(f"DEBUG VISTA PAGOS: total_pagos={total_pagos}, total_monto={total_monto}, total_clientes={total_clientes}")

            # Desglose por método de pago - CONVERTIR DE DICT A LISTA
            metodos_pago_dict = reporte.get('metodos_pago', {})
            desglose_metodo = []
            for metodo, datos in metodos_pago_dict.items():
                desglose_metodo.append({
                    'metodo_pago': metodo,
                    'cantidad': datos.get('cantidad', 0),
                    'monto_total': datos.get('monto', 0.0)
                })
            print(f"DEBUG VISTA PAGOS: desglose_metodo={desglose_metodo}")

            # Stats cards minimalistas - UN SOLO COLOR para cohesión
            stats = ft.Row([
                # Total Pagos
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.RECEIPT_ROUNDED, size=32, color=ft.Colors.WHITE),
                            bgcolor=COLORS_REPORTES["primary"],
                            border_radius=Theme.RADIUS["lg"],
                            padding=Theme.SPACING["md"],
                            width=64,
                            height=64,
                        ),
                        ft.Container(width=Theme.SPACING["md"]),
                        ft.Column([
                            ft.Text("Total Pagos", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ft.Text(str(total_pagos), size=Theme.FONT_SIZE["3xl"], color=Theme.TEXT_PRIMARY, weight=Theme.FONT_WEIGHT["bold"]),
                        ], spacing=4, expand=True),
                    ]),
                    padding=Theme.SPACING["lg"],
                    bgcolor=Theme.CARD_BG,
                    border_radius=Theme.RADIUS["lg"],
                    border=ft.border.all(1, Theme.BORDER_DEFAULT),
                    expand=1,
                ),
                # Total Recaudado - MÁS PROMINENTE
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.ATTACH_MONEY_ROUNDED, size=40, color=ft.Colors.WHITE),
                            bgcolor=COLORS_REPORTES["primary"],
                            border_radius=Theme.RADIUS["lg"],
                            padding=Theme.SPACING["lg"],
                            width=72,
                            height=72,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=20,
                                color=COLORS_REPORTES["primary_glow"],
                                offset=ft.Offset(0, 4),
                            ),
                        ),
                        ft.Container(width=Theme.SPACING["lg"]),
                        ft.Column([
                            ft.Text("Total Recaudado", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY, weight=Theme.FONT_WEIGHT["medium"]),
                            ft.Text(f"S/ {total_monto:,.2f}", size=Theme.FONT_SIZE["4xl"], color=COLORS_REPORTES["primary"], weight=Theme.FONT_WEIGHT["extrabold"]),
                        ], spacing=4, expand=True),
                    ]),
                    padding=Theme.SPACING["xl"],
                    bgcolor=f"{COLORS_REPORTES['primary']}10",
                    border_radius=Theme.RADIUS["lg"],
                    border=ft.border.all(2, COLORS_REPORTES["primary"]),
                    expand=1,
                ),
                # Clientes
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.GROUPS_ROUNDED, size=32, color=ft.Colors.WHITE),
                            bgcolor=COLORS_REPORTES["primary"],
                            border_radius=Theme.RADIUS["lg"],
                            padding=Theme.SPACING["md"],
                            width=64,
                            height=64,
                        ),
                        ft.Container(width=Theme.SPACING["md"]),
                        ft.Column([
                            ft.Text("Clientes", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                            ft.Text(str(total_clientes), size=Theme.FONT_SIZE["3xl"], color=Theme.TEXT_PRIMARY, weight=Theme.FONT_WEIGHT["bold"]),
                        ], spacing=4, expand=True),
                    ]),
                    padding=Theme.SPACING["lg"],
                    bgcolor=Theme.CARD_BG,
                    border_radius=Theme.RADIUS["lg"],
                    border=ft.border.all(1, Theme.BORDER_DEFAULT),
                    expand=1,
                ),
            ], spacing=Theme.SPACING["md"])

            # Desglose por método de pago
            metodos_container = ft.Column(spacing=Theme.SPACING["md"])

            if desglose_metodo:
                for metodo_data in desglose_metodo:
                    metodo = metodo_data.get('metodo_pago', 'Desconocido')
                    cantidad = metodo_data.get('cantidad', 0)
                    monto = metodo_data.get('monto_total', 0.0)
                    porcentaje = (cantidad / total_pagos * 100) if total_pagos > 0 else 0

                    # Obtener icono y color específicos
                    icono = get_icono_metodo_pago(metodo)
                    color = get_color_metodo_pago(metodo)

                    metodos_container.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(icono, size=24, color=ft.Colors.WHITE),
                                    bgcolor=color,
                                    border_radius=Theme.RADIUS["md"],
                                    padding=10,
                                    width=48,
                                    height=48,
                                ),
                                ft.Container(width=Theme.SPACING["md"]),
                                ft.Column([
                                    ft.Text(metodo, size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                    ft.Text(f"{cantidad} pagos · {porcentaje:.0f}%", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                                ], spacing=2, expand=True),
                                ft.Text(f"S/ {monto:,.2f}", size=Theme.FONT_SIZE["xl"], weight=Theme.FONT_WEIGHT["bold"], color=color),
                            ]),
                            padding=Theme.SPACING["lg"],
                            bgcolor=Theme.CARD_BG,
                            border_radius=Theme.RADIUS["md"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT),
                        )
                    )
                # TOTAL simplificado
                metodos_container.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=28, color=ft.Colors.WHITE),
                                bgcolor=COLORS_REPORTES["primary"],
                                border_radius=Theme.RADIUS["lg"],
                                padding=Theme.SPACING["md"],
                                width=56,
                                height=56,
                            ),
                            ft.Container(width=Theme.SPACING["lg"]),
                            ft.Column([
                                ft.Text("TOTAL GENERAL", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                ft.Text(f"{total_pagos} pagos", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                            ], spacing=2, expand=True),
                            ft.Text(f"S/ {total_monto:,.2f}", size=Theme.FONT_SIZE["3xl"], weight=Theme.FONT_WEIGHT["extrabold"], color=COLORS_REPORTES["primary"]),
                        ]),
                        padding=Theme.SPACING["xl"],
                        bgcolor=f"{COLORS_REPORTES['primary']}15",
                        border_radius=Theme.RADIUS["lg"],
                        border=ft.border.all(2, COLORS_REPORTES["primary"]),
                    )
                )
            else:
                metodos_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.RECEIPT_LONG_ROUNDED, size=64, color=ft.Colors.WHITE),
                                bgcolor=f"{COLORS_REPORTES['primary']}30",
                                border_radius=Theme.RADIUS["2xl"],
                                padding=Theme.SPACING["2xl"],
                                width=120,
                                height=120,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(height=Theme.SPACING["lg"]),
                            ft.Text(
                                "No hay pagos registrados en este período",
                                size=Theme.FONT_SIZE["xl"],
                                color=Theme.TEXT_PRIMARY,
                                weight=Theme.FONT_WEIGHT["bold"],
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=Theme.SPACING["xs"]),
                            ft.Text(
                                "Los pagos aparecerán aquí cuando se registren membresías.\nRevisa otro período o registra una nueva membresía.",
                                size=Theme.FONT_SIZE["sm"],
                                color=Theme.TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        padding=Theme.SPACING["2xl"] * 2,
                        alignment=ft.alignment.center,
                        bgcolor=f"{COLORS_REPORTES['primary']}08",
                        border_radius=Theme.RADIUS["2xl"],
                        border=ft.border.all(1.5, f"{COLORS_REPORTES['primary']}20"),
                    )
                )

            # Lista de pagos - CORREGIDO: era 'pagos', ahora es 'detalle_pagos'
            pagos_lista = reporte.get('detalle_pagos', [])
            pagos_container = ft.Column(spacing=Theme.SPACING["sm"])

            if pagos_lista:
                for pago in pagos_lista[:10]:  # Mostrar últimos 10 para evitar lista infinita
                    # CORREGIDO: construir nombre del cliente desde 'nombre' y 'apellidos'
                    nombre = pago.get('nombre', '')
                    apellidos = pago.get('apellidos', '')
                    cliente_nombre = f"{nombre} {apellidos}".strip() if nombre or apellidos else 'Cliente desconocido'

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
                    color_metodo = get_color_metodo_pago(metodo)
                    icono_metodo = get_icono_metodo_pago(metodo)

                    pagos_container.controls.append(
                        ft.Container(
                            content=ft.Row([
                                # Barra de color lateral
                                ft.Container(
                                    bgcolor=color_metodo,
                                    width=4,
                                    border_radius=Theme.RADIUS["sm"],
                                ),
                                ft.Container(width=Theme.SPACING["md"]),
                                ft.Column([
                                    ft.Text(cliente_nombre, size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["semibold"], color=Theme.TEXT_PRIMARY),
                                    ft.Row([
                                        ft.Icon(icono_metodo, size=12, color=color_metodo),
                                        ft.Text(f"{membresia} · {metodo}", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                                    ], spacing=4),
                                ], spacing=2, expand=True),
                                ft.Column([
                                    ft.Text(f"S/ {monto:.2f}", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"], color=color_metodo, text_align=ft.TextAlign.RIGHT),
                                    ft.Text(fecha_formateada, size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY, text_align=ft.TextAlign.RIGHT),
                                ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=2),
                            ]),
                            padding=Theme.SPACING["md"],
                            bgcolor=Theme.CARD_BG,
                            border_radius=Theme.RADIUS["sm"],
                            border=ft.border.all(1, f"{color_metodo}30"),
                        )
                    )
            else:
                pagos_container.controls.append(
                    ft.Text("No hay pagos registrados", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY)
                )

            # Actualizar contenido - Diseño minimalista y cohesivo
            content_pagos.content = ft.Column([
                stats,
                ft.Container(height=Theme.SPACING["xl"]),
                # Desglose por método
                ft.Container(
                    content=ft.Column([
                        ft.Text("Desglose por Método", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                        ft.Container(height=Theme.SPACING["md"]),
                        metodos_container,
                    ]),
                    padding=Theme.SPACING["lg"],
                    bgcolor=Theme.CARD_BG,
                    border_radius=Theme.RADIUS["lg"],
                    border=ft.border.all(1, Theme.BORDER_DEFAULT),
                ),
                ft.Container(height=Theme.SPACING["lg"]),
                # Últimos pagos
                ft.Container(
                    content=ft.Column([
                        ft.Text("Últimos 10 Pagos", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                        ft.Container(height=Theme.SPACING["md"]),
                        pagos_container,
                    ]),
                    padding=Theme.SPACING["lg"],
                    bgcolor=Theme.CARD_BG,
                    border_radius=Theme.RADIUS["lg"],
                    border=ft.border.all(1, Theme.BORDER_DEFAULT),
                ),
            ], spacing=0)

            page.update()

        # Container principal para pagos
        content_pagos = ft.Container(expand=True)

        # Cargar datos iniciales
        cargar_reporte_pagos()

        return content_pagos

    # ==========================================
    # REPORTE DE CLIENTES
    # ==========================================
    def create_reporte_clientes(tipo_inicial="general"):
        """Crear vista de reportes de clientes"""
        tipo_reporte = [tipo_inicial]  # general, nuevos, por_vencer, vencidas

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
            total_nuevos = datos.get('total', 0)  # CORREGIDO: era 'total_nuevos', ahora es 'total'
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
            total = datos.get('total', 0)  # CORREGIDO: era 'total_clientes', ahora es 'total'
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
            total = datos.get('total', 0)  # CORREGIDO: era 'total_clientes', ahora es 'total'
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

                # DEBUG: Imprimir datos recibidos
                print(f"DEBUG ASISTENCIAS: Datos recibidos de la API: {datos}")

                total_asistencias = datos.get('total_asistencias', 0)
                # CORREGIDO: La API no retorna promedio_diario, lo calculamos manualmente
                asistencias_por_dia = datos.get('asistencias_por_dia', [])
                promedio_diario = total_asistencias / len(asistencias_por_dia) if len(asistencias_por_dia) > 0 else 0.0
                # CORREGIDO: El campo correcto es 'clientes_mas_frecuentes', no 'clientes_frecuentes'
                clientes_frecuentes = datos.get('clientes_mas_frecuentes', [])

                # DEBUG: Imprimir datos procesados
                print(f"DEBUG ASISTENCIAS: total_asistencias={total_asistencias}")
                print(f"DEBUG ASISTENCIAS: asistencias_por_dia={asistencias_por_dia}")
                print(f"DEBUG ASISTENCIAS: clientes_frecuentes={clientes_frecuentes}")
                print(f"DEBUG ASISTENCIAS: promedio_diario={promedio_diario}")

                # Estadísticas
                stats = ft.Row([
                    create_stat_card("Total Asistencias", str(total_asistencias), ft.Icons.FITNESS_CENTER, Theme.PRIMARY),
                    create_stat_card("Promedio Diario", f"{promedio_diario:.1f}", ft.Icons.TRENDING_UP, Theme.INFO),
                ], spacing=Theme.SPACING["xl"], wrap=True)

                # Asistencias por día
                dias_container = ft.Column(spacing=Theme.SPACING["sm"], scroll=ft.ScrollMode.AUTO, height=200)

                if not asistencias_por_dia:
                    dias_container.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=32, color=Theme.TEXT_SECONDARY),
                                ft.Text("No hay registros de asistencias", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                            padding=Theme.SPACING["xl"],
                            alignment=ft.alignment.center
                        )
                    )

                for dia_data in asistencias_por_dia:
                    fecha = dia_data.get('fecha', '')
                    # CORREGIDO: El campo correcto es 'total', no 'cantidad'
                    cantidad = dia_data.get('total', 0)

                    # Convertir fecha a formato legible en español
                    try:
                        # La fecha viene como string 'YYYY-MM-DD'
                        from datetime import datetime
                        if fecha:
                            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                            # Diccionario de días en español
                            dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                            dia_nombre = dias_semana[fecha_obj.weekday()]
                            fecha_formateada = f"{fecha_obj.strftime('%d/%m/%Y')} - {dia_nombre}"
                        else:
                            fecha_formateada = fecha
                    except Exception as e:
                        print(f"Error al formatear fecha: {e}")
                        fecha_formateada = fecha

                    # Calcular porcentaje para barra
                    # CORREGIDO: El campo correcto es 'total', no 'cantidad'
                    max_cantidad = max(d.get('total', 0) for d in asistencias_por_dia) if asistencias_por_dia else 1
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

                if not clientes_frecuentes:
                    frecuentes_container.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=32, color=Theme.TEXT_SECONDARY),
                                ft.Text("No hay clientes frecuentes registrados", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                            padding=Theme.SPACING["xl"],
                            alignment=ft.alignment.center
                        )
                    )

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
    # REPORTE FINANCIERO
    # ==========================================
    def create_reporte_financiero(tipo="diario"):
        """Crear vista de reporte financiero"""

        def cargar_reporte_financiero():
            """Cargar datos del reporte financiero"""
            try:
                if tipo == "diario":
                    datos = api.get_reporte_financiero_diario()
                elif tipo == "mensual":
                    datos = api.get_reporte_financiero_mensual()
                elif tipo == "anual":
                    datos = api.get_reporte_financiero_anual()
                else:
                    datos = {}

                # Datos principales - CORREGIDO: convertir todos a float
                fecha = datos.get('fecha', 'N/A')
                ingresos_membresias = float(datos.get('ingresos_membresias', 0.0)) if datos.get('ingresos_membresias') else 0.0
                ingresos_productos = float(datos.get('ingresos_productos', 0.0)) if datos.get('ingresos_productos') else 0.0
                ganancia_productos = float(datos.get('ganancia_productos', 0.0)) if datos.get('ganancia_productos') else 0.0
                total_ingresos = float(datos.get('total_ingresos', 0.0)) if datos.get('total_ingresos') else 0.0
                total_egresos = float(datos.get('total_egresos', 0.0)) if datos.get('total_egresos') else 0.0
                ganancia_neta = float(datos.get('ganancia_neta', 0.0)) if datos.get('ganancia_neta') else 0.0
                margen_neto = float(datos.get('margen_neto', 0.0)) if datos.get('margen_neto') else 0.0

                # Estadísticas principales
                stats = ft.Column([
                    ft.Row([
                        create_stat_card("Total Ingresos", f"S/ {total_ingresos:,.2f}", ft.Icons.ATTACH_MONEY, Theme.SUCCESS),
                        create_stat_card("Total Egresos", f"S/ {total_egresos:,.2f}", ft.Icons.MONEY_OFF, Theme.ERROR),
                        create_stat_card("Ganancia Neta", f"S/ {ganancia_neta:,.2f}", ft.Icons.TRENDING_UP, Theme.PRIMARY),
                    ], spacing=Theme.SPACING["xl"], wrap=True),
                    ft.Container(height=Theme.SPACING["md"]),
                    ft.Row([
                        create_stat_card("Ingresos Membresías", f"S/ {ingresos_membresias:,.2f}", ft.Icons.CARD_MEMBERSHIP, Theme.INFO),
                        create_stat_card("Ingresos Productos", f"S/ {ingresos_productos:,.2f}", ft.Icons.SHOPPING_CART, Theme.INFO),
                        create_stat_card("Margen Neto", f"{margen_neto:.2f}%", ft.Icons.PERCENT, Theme.WARNING),
                    ], spacing=Theme.SPACING["xl"], wrap=True),
                ], spacing=0)

                # Título del período
                if tipo == "diario":
                    titulo_periodo = f"Reporte Financiero del Día - {fecha}"
                elif tipo == "mensual":
                    titulo_periodo = f"Reporte Financiero Mensual"
                else:
                    titulo_periodo = f"Reporte Financiero Anual"

                content_financiero.content = ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ASSESSMENT, size=28, color=Theme.WARNING),
                            ft.Text(titulo_periodo, size=Theme.FONT_SIZE["xl"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                        ], spacing=12),
                        padding=Theme.SPACING["md"],
                        bgcolor=f"{Theme.WARNING}15",
                        border_radius=Theme.RADIUS["md"]
                    ),
                    ft.Container(height=Theme.SPACING["lg"]),
                    stats,
                ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

                page.update()

            except Exception as e:
                print(f"Error al cargar reporte financiero: {e}")
                import traceback
                traceback.print_exc()
                mostrar_error(page, f"Error al cargar reporte: {str(e)}")

        # Container principal para financiero
        content_financiero = ft.Container(expand=True)

        # Cargar datos iniciales
        cargar_reporte_financiero()

        return content_financiero

    # ==========================================
    # REPORTE DE EGRESOS POR CATEGORÍA
    # ==========================================
    def create_reporte_egresos_categoria():
        """Crear vista de reporte de egresos por categoría"""

        def cargar_reporte_egresos():
            """Cargar datos del reporte de egresos"""
            try:
                datos = api.get_reporte_egresos_por_categoria()

                # CORREGIDO: convertir a int y float desde el inicio
                total_egresos = int(datos.get('total_egresos', 0)) if datos.get('total_egresos') else 0
                total_monto = float(datos.get('total_monto', 0.0)) if datos.get('total_monto') else 0.0
                egresos_por_categoria = datos.get('egresos_por_categoria', [])

                # Estadísticas principales
                stats = ft.Row([
                    create_stat_card("Total Egresos", str(total_egresos), ft.Icons.RECEIPT_LONG, Theme.ERROR),
                    create_stat_card("Monto Total", f"S/ {total_monto:,.2f}", ft.Icons.MONEY_OFF, Theme.WARNING),
                ], spacing=Theme.SPACING["xl"], wrap=True)

                # Egresos por categoría
                categorias_container = ft.Column(spacing=Theme.SPACING["md"])

                if egresos_por_categoria:
                    for cat_data in egresos_por_categoria:
                        categoria = cat_data.get('categoria', 'Sin categoría')
                        cantidad = int(cat_data.get('cantidad', 0)) if cat_data.get('cantidad') else 0
                        monto = float(cat_data.get('total', 0.0)) if cat_data.get('total') else 0.0  # CORREGIDO: convertir a float
                        porcentaje = (monto / total_monto * 100) if total_monto > 0 else 0

                        categorias_container.controls.append(
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Column([
                                            ft.Icon(ft.Icons.CATEGORY, size=32, color=Theme.ERROR),
                                        ], alignment=ft.MainAxisAlignment.CENTER, width=50),
                                        ft.Column([
                                            ft.Text(categoria, size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                                            ft.Text(f"{cantidad} egresos ({porcentaje:.1f}%)", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                                        ], spacing=4, expand=True),
                                        ft.Column([
                                            ft.Text(f"S/ {monto:,.2f}", size=Theme.FONT_SIZE["xl"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.ERROR, text_align=ft.TextAlign.RIGHT),
                                        ], horizontal_alignment=ft.CrossAxisAlignment.END),
                                    ], spacing=Theme.SPACING["lg"]),
                                    # Barra de progreso
                                    ft.Container(
                                        content=ft.Container(
                                            bgcolor=Theme.ERROR,
                                            border_radius=Theme.RADIUS["sm"],
                                            height=8,
                                        ),
                                        width=f"{porcentaje}%",
                                        bgcolor=f"{Theme.ERROR}22",
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
                else:
                    categorias_container.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=48, color=Theme.TEXT_SECONDARY),
                                ft.Text("No hay egresos registrados", size=Theme.FONT_SIZE["md"], color=Theme.TEXT_PRIMARY),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
                            padding=Theme.SPACING["2xl"]
                        )
                    )

                content_egresos.content = ft.Column([
                    stats,
                    ft.Container(height=Theme.SPACING["lg"]),
                    create_card_container(
                        content=ft.Column([
                            ft.Text("Egresos por Categoría", size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.ERROR),
                            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                            categorias_container,
                        ], spacing=Theme.SPACING["lg"]),
                        padding=Theme.SPACING["xl"]
                    ),
                ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

                page.update()

            except Exception as e:
                print(f"Error al cargar reporte de egresos: {e}")
                import traceback
                traceback.print_exc()
                mostrar_error(page, f"Error al cargar reporte: {str(e)}")

        # Container principal para egresos
        content_egresos = ft.Container(expand=True)

        # Cargar datos iniciales
        cargar_reporte_egresos()

        return content_egresos

    # ==========================================
    # FUNCIONES AUXILIARES PARA INICIALIZAR REPORTES
    # ==========================================
    def create_reporte_pagos_con_periodo(periodo):
        """Crear reporte de pagos con un período específico"""
        return create_reporte_pagos(periodo_inicial=periodo)

    def create_reporte_clientes_con_tipo(tipo):
        """Crear reporte de clientes con un tipo específico"""
        # Mapear nombres de tipo para que coincidan con los esperados
        tipo_mapeado = tipo
        if tipo == "vencidas":
            tipo_mapeado = "vencidas"
        elif tipo == "por_vencer":
            tipo_mapeado = "por_vencer"
        return create_reporte_clientes(tipo_inicial=tipo_mapeado)

    # ==========================================
    # NAVEGACIÓN CON MENÚ HORIZONTAL SUPERIOR
    # ==========================================
    seccion_actual = ["pagos"]  # Sección actual: pagos, clientes, asistencias, financiero
    subseccion_actual = ["dia"]  # Subsección actual depende de la sección

    # Referencias para los botones del menú
    botones_seccion_refs = {}  # Referencias a botones de sección (PAGOS, CLIENTES, etc)
    botones_subseccion_refs = {}  # Referencias a botones de subsección (Hoy, Semana, etc)

    def actualizar_botones_seccion():
        """Actualizar botones de sección principal (PAGOS, CLIENTES, ASISTENCIAS, FINANCIERO)"""
        for seccion, boton_ref in botones_seccion_refs.items():
            if boton_ref.current:
                es_activo = seccion_actual[0] == seccion
                boton_ref.current.bgcolor = f"{COLORS_REPORTES['primary']}20" if es_activo else "transparent"
                boton_ref.current.border = ft.border.all(2 if es_activo else 1, COLORS_REPORTES["primary"] if es_activo else Theme.BORDER_DEFAULT)

                # Actualizar texto
                texto = boton_ref.current.content
                texto.weight = Theme.FONT_WEIGHT["bold"] if es_activo else Theme.FONT_WEIGHT["medium"]
                texto.color = COLORS_REPORTES["primary"] if es_activo else Theme.TEXT_PRIMARY

                boton_ref.current.update()

    def actualizar_botones_subseccion():
        """Actualizar botones de subsección (Hoy, Semana, General, etc)"""
        for subseccion, boton_ref in botones_subseccion_refs.items():
            if boton_ref.current:
                es_activo = subseccion_actual[0] == subseccion
                boton_ref.current.bgcolor = COLORS_REPORTES["primary"] if es_activo else Theme.CARD_BG
                boton_ref.current.border = ft.border.all(1, COLORS_REPORTES["primary"] if es_activo else Theme.BORDER_DEFAULT)

                # Actualizar ícono y texto
                icono = boton_ref.current.content.controls[0]
                texto = boton_ref.current.content.controls[2]

                icono.color = ft.Colors.WHITE if es_activo else COLORS_REPORTES["primary"]
                texto.color = ft.Colors.WHITE if es_activo else Theme.TEXT_PRIMARY
                texto.weight = Theme.FONT_WEIGHT["semibold"] if es_activo else Theme.FONT_WEIGHT["medium"]

                boton_ref.current.update()

    def cambiar_seccion(seccion):
        """Cambiar la sección principal"""
        seccion_actual[0] = seccion

        # Establecer subsección por defecto según sección
        if seccion == "pagos":
            subseccion_actual[0] = "dia"
            content_ref.current.content = create_reporte_pagos_con_periodo("dia")
        elif seccion == "clientes":
            subseccion_actual[0] = "general"
            content_ref.current.content = create_reporte_clientes_con_tipo("general")
        elif seccion == "asistencias":
            subseccion_actual[0] = "general"
            content_ref.current.content = create_reporte_asistencias()
        elif seccion == "financiero":
            subseccion_actual[0] = "diario"
            content_ref.current.content = create_reporte_financiero(tipo="diario")

        # Actualizar botones y contenido
        actualizar_botones_seccion()
        actualizar_botones_subseccion()
        content_ref.current.update()
        page.update()

    def cambiar_subseccion(subseccion):
        """Cambiar la subsección dentro de la sección actual"""
        subseccion_actual[0] = subseccion

        # Cargar contenido según sección y subsección
        if seccion_actual[0] == "pagos":
            content_ref.current.content = create_reporte_pagos_con_periodo(subseccion)
        elif seccion_actual[0] == "clientes":
            content_ref.current.content = create_reporte_clientes_con_tipo(subseccion)
        elif seccion_actual[0] == "financiero":
            if subseccion == "egresos":
                content_ref.current.content = create_reporte_egresos_categoria()
            else:
                content_ref.current.content = create_reporte_financiero(tipo=subseccion)

        # Actualizar botones y contenido
        actualizar_botones_subseccion()
        content_ref.current.update()
        page.update()

    # ==========================================
    # MENÚ HORIZONTAL SUPERIOR MINIMALISTA
    # ==========================================
    def crear_boton_seccion(texto, seccion):
        """Crear botón de sección principal"""
        boton_ref = ft.Ref[ft.Container]()
        botones_seccion_refs[seccion] = boton_ref
        es_activo = seccion_actual[0] == seccion

        return ft.Container(
            ref=boton_ref,
            content=ft.Text(
                texto,
                size=Theme.FONT_SIZE["md"],
                weight=Theme.FONT_WEIGHT["bold"] if es_activo else Theme.FONT_WEIGHT["medium"],
                color=COLORS_REPORTES["primary"] if es_activo else Theme.TEXT_PRIMARY,
            ),
            padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"], vertical=Theme.SPACING["md"]),
            bgcolor=f"{COLORS_REPORTES['primary']}20" if es_activo else "transparent",
            border_radius=Theme.RADIUS["md"],
            border=ft.border.all(2 if es_activo else 1, COLORS_REPORTES["primary"] if es_activo else Theme.BORDER_DEFAULT),
            on_click=lambda _: cambiar_seccion(seccion),
            ink=True,
        )

    def crear_boton_subseccion(texto, icono, subseccion):
        """Crear botón de subsección"""
        boton_ref = ft.Ref[ft.Container]()
        botones_subseccion_refs[subseccion] = boton_ref
        es_activo = subseccion_actual[0] == subseccion

        return ft.Container(
            ref=boton_ref,
            content=ft.Row([
                ft.Icon(icono, size=16, color=ft.Colors.WHITE if es_activo else COLORS_REPORTES["primary"]),
                ft.Container(width=Theme.SPACING["xs"]),
                ft.Text(
                    texto,
                    size=Theme.FONT_SIZE["sm"],
                    weight=Theme.FONT_WEIGHT["semibold"] if es_activo else Theme.FONT_WEIGHT["medium"],
                    color=ft.Colors.WHITE if es_activo else Theme.TEXT_PRIMARY,
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=Theme.SPACING["md"], vertical=Theme.SPACING["sm"]),
            bgcolor=COLORS_REPORTES["primary"] if es_activo else Theme.CARD_BG,
            border_radius=Theme.RADIUS["md"],
            border=ft.border.all(1, COLORS_REPORTES["primary"] if es_activo else Theme.BORDER_DEFAULT),
            on_click=lambda _: cambiar_subseccion(subseccion),
            ink=True,
        )

    # Menú superior horizontal
    menu_horizontal = ft.Column([
        # Fila 1: Secciones principales (PAGOS, CLIENTES, ASISTENCIAS, FINANCIERO)
        ft.Row([
            crear_boton_seccion("PAGOS", "pagos"),
            crear_boton_seccion("CLIENTES", "clientes"),
            crear_boton_seccion("ASISTENCIAS", "asistencias"),
            crear_boton_seccion("FINANCIERO", "financiero"),
        ], spacing=Theme.SPACING["sm"]),

        ft.Container(height=Theme.SPACING["md"]),

        # Fila 2: Subsecciones (cambian según la sección activa)
        ft.Container(
            ref=ft.Ref[ft.Container](),
            content=ft.Row([
                # Por defecto: subsecciones de PAGOS
                crear_boton_subseccion("Hoy", ft.Icons.TODAY_ROUNDED, "dia"),
                crear_boton_subseccion("Semana", ft.Icons.DATE_RANGE_ROUNDED, "semana"),
                crear_boton_subseccion("Mes", ft.Icons.CALENDAR_MONTH_ROUNDED, "mes"),
                crear_boton_subseccion("Año", ft.Icons.CALENDAR_TODAY_ROUNDED, "anio"),
            ], spacing=Theme.SPACING["sm"]),
        ),
    ], spacing=0)

    # Contenedor de contenido
    content_container = ft.Container(
        ref=content_ref,
        content=create_reporte_pagos(),  # Iniciar con reporte de pagos
        expand=True
    )

    # Layout completo - Menú horizontal arriba + contenido abajo
    content = ft.Column([
        # Menú horizontal minimalista
        ft.Container(
            content=menu_horizontal,
            padding=Theme.SPACING["lg"],
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["lg"],
            border=ft.border.all(1, Theme.BORDER_DEFAULT),
        ),
        ft.Container(height=Theme.SPACING["lg"]),
        # Contenido del reporte
        content_container,
    ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

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
