"""
Vista de dashboard para administradores - DISEÑO PROFESIONAL OPTIMIZADO
Dashboard intuitivo, ordenado y visualmente coherente
"""

import flet as ft
from datetime import datetime, date
from config.theme import Theme
from ui.layouts import create_dashboard_layout, create_activity_widget
from ui.components.molecules import create_card_container
from ui.components.atoms import create_primary_button
from services.api_service import APIService
from ui.utils.datetime_utils import get_now_local, parse_datetime_from_api, format_time_display


def show_admin_dashboard(page: ft.Page, auth_service, on_logout, on_section_click):
    """
    Dashboard de administrador con diseño profesional y estructura clara

    ESTRUCTURA:
    ┌──────────────────────────────────────────────────────────┐
    │  ┌─────────────────┬─────────┬─────────┬─────────┐      │
    │  │  INGRESOS HOY   │ CLIENTE │ ACTIVOS │   HOY   │      │
    │  │   (DESTACADO)   │         │         │         │      │
    │  └─────────────────┴─────────┴─────────┴─────────┘      │
    │  ┌──────────────────────────┬────────────────────┐      │
    │  │  ACTIVIDAD RECIENTE      │  ACCIONES RÁPIDAS  │      │
    │  │                          │  MÉTRICAS          │      │
    │  └──────────────────────────┴────────────────────┘      │
    └──────────────────────────────────────────────────────────┘
    """
    # Configuración de página
    page.title = "BLESSED GYM - Dashboard Administrador"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    # Obtener usuario actual
    current_user = auth_service.get_current_user()
    user_info = {
        "nombre": current_user.get("nombre", "Admin"),
        "rol": "Administrador"
    }

    # Inicializar API Service
    api = APIService()

    # ==========================================
    # PALETA DE COLORES CON ALTO CONTRASTE
    # ==========================================
    COLORS = {
        "primary": "#FF6B35",      # Naranja BLESSED vibrante
        "purple": "#B794F6",       # Púrpura brillante
        "green": "#48D597",        # Verde esmeralda vivo
        "blue": "#4FC3F7",         # Azul cyan brillante
        "yellow": "#FFD93D",       # Amarillo dorado
    }

    # ==========================================
    # CARGAR DATOS REALES DEL BACKEND
    # ==========================================
    def cargar_estadisticas():
        """Cargar estadísticas reales del backend"""
        try:
            # Obtener datos de clientes
            reporte_clientes = api.get_reporte_clientes_general()
            total_clientes = reporte_clientes.get('total_clientes', 0)
            clientes_activos = reporte_clientes.get('clientes_activos', 0)

            # Calcular porcentaje de clientes activos
            if total_clientes > 0:
                porcentaje_activos = round((clientes_activos / total_clientes) * 100, 1)
            else:
                porcentaje_activos = 0

            # Obtener asistencias de hoy
            stats_asistencias = api.get_estadisticas_asistencias_hoy()
            asistencias_hoy = stats_asistencias.get('total_asistencias', 0)

            # Obtener ventas de hoy usando el endpoint correcto (con timezone local)
            fecha_hoy = get_now_local().strftime('%Y-%m-%d')
            ventas_hoy = api.get_ventas(fecha_desde=fecha_hoy, fecha_hasta=fecha_hoy)
            total_ventas = len(ventas_hoy) if ventas_hoy else 0
            # Calcular ingresos sumando los totales de las ventas
            ingresos_hoy = sum(venta.get('total', 0) for venta in ventas_hoy) if ventas_hoy else 0

            return {
                'total_clientes': total_clientes,
                'clientes_activos': clientes_activos,
                'porcentaje_activos': porcentaje_activos,
                'asistencias_hoy': asistencias_hoy,
                'total_ventas': total_ventas,
                'ingresos_hoy': ingresos_hoy
            }
        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")
            return {
                'total_clientes': 0,
                'clientes_activos': 0,
                'porcentaje_activos': 0,
                'asistencias_hoy': 0,
                'total_ventas': 0,
                'ingresos_hoy': 0
            }

    # Cargar estadísticas
    stats = cargar_estadisticas()

    # ==========================================
    # CARD PRINCIPAL: INGRESOS HOY (DESTACADO)
    # ==========================================
    def crear_card_ingresos():
        """Card principal de ingresos con diseño destacado y simétrico"""
        return create_card_container(
            content=ft.Column([
                # Ícono
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                        size=40,
                        color=ft.Colors.WHITE
                    ),
                    bgcolor=COLORS["primary"],
                    border_radius=Theme.RADIUS["lg"],
                    padding=Theme.SPACING["md"],
                    width=68,
                    height=68,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=Theme.SPACING["lg"]),
                # Título
                ft.Text(
                    "INGRESOS DE HOY",
                    size=Theme.FONT_SIZE["sm"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                # Valor
                ft.Text(
                    f"S/. {stats['ingresos_hoy']:.2f}",
                    size=Theme.FONT_SIZE["5xl"],
                    weight=Theme.FONT_WEIGHT["black"],
                    color=COLORS["primary"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                # Subtexto
                ft.Text(
                    f"{stats['total_ventas']} ventas",
                    size=Theme.FONT_SIZE["xs"],
                    color=COLORS["primary"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=Theme.SPACING["xl"],
            shadow="md",
            bgcolor=Theme.CARD_BG_LIGHT,
            expand=1,
        )

    # ==========================================
    # CARDS SECUNDARIAS: CLIENTES, ACTIVOS, HOY (SIMÉTRICAS)
    # ==========================================
    def crear_mini_stat_card(titulo, valor, icono, color, subtitulo=None):
        """Crear mini card de estadística simétrica con ingresos"""
        return create_card_container(
            content=ft.Column([
                # Ícono (mismo tamaño que ingresos)
                ft.Container(
                    content=ft.Icon(icono, size=32, color=ft.Colors.WHITE),
                    bgcolor=color,
                    border_radius=Theme.RADIUS["lg"],
                    padding=Theme.SPACING["md"],
                    width=68,
                    height=68,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=Theme.SPACING["lg"]),
                # Título
                ft.Text(
                    titulo,
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_SECONDARY,
                    weight=Theme.FONT_WEIGHT["bold"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                # Valor
                ft.Text(
                    str(valor),
                    size=Theme.FONT_SIZE["5xl"],
                    weight=Theme.FONT_WEIGHT["black"],
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                # Subtítulo
                ft.Text(
                    subtitulo if subtitulo else "",
                    size=Theme.FONT_SIZE["xs"],
                    color=color,
                    weight=Theme.FONT_WEIGHT["bold"],
                    text_align=ft.TextAlign.CENTER,
                    visible=subtitulo is not None,
                ) if subtitulo else ft.Container(height=16),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=Theme.SPACING["xl"],
            shadow="md",
            expand=1,
        )

    # ==========================================
    # BARRA DE ACCIONES RÁPIDAS - FLOTANTE Y HERMOSA
    # ==========================================
    def crear_barra_acciones_rapidas():
        """Crear barra horizontal de acciones rápidas con diseño flotante"""
        def crear_boton_accion_flotante(texto, icono, color, color_gradient, on_click):
            """Crear botón de acción flotante con gradiente y efectos"""

            # Contenedor del botón con hover effect
            boton = ft.Container(
                content=ft.Column([
                    # Ícono con fondo redondeado
                    ft.Container(
                        content=ft.Icon(
                            icono,
                            size=22,
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=color,
                        border_radius=Theme.RADIUS["full"],  # Completamente redondo
                        padding=Theme.SPACING["sm"],
                        width=48,
                        height=48,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=15,
                            color=f"{color}40",
                            offset=ft.Offset(0, 6),
                        ),
                    ),
                    ft.Container(height=Theme.SPACING["xs"]),
                    # Texto
                    ft.Text(
                        texto,
                        size=Theme.FONT_SIZE["xs"],
                        color=Theme.TEXT_PRIMARY,
                        weight=Theme.FONT_WEIGHT["semibold"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=Theme.SPACING["md"],
                border_radius=Theme.RADIUS["2xl"],  # Bordes muy redondeados
                bgcolor=Theme.CARD_BG_LIGHT,
                border=ft.border.all(1, f"{color}30"),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color=ft.Colors.BLACK38,
                    offset=ft.Offset(0, 3),
                ),
                ink=True,
                on_click=on_click,
                animate_scale=ft.Animation(200, "easeOut"),
                animate_opacity=200,
                expand=1,
            )

            # Agregar efecto hover
            def on_hover(e):
                if e.data == "true":
                    boton.scale = 1.03
                    boton.shadow = ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=20,
                        color=f"{color}50",
                        offset=ft.Offset(0, 8),
                    )
                else:
                    boton.scale = 1.0
                    boton.shadow = ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.Colors.BLACK38,
                        offset=ft.Offset(0, 3),
                    )
                boton.update()

            boton.on_hover = on_hover
            return boton

        # Contenedor invisible/transparente
        return ft.Container(
            content=ft.Row([
                crear_boton_accion_flotante(
                    "Nueva Venta",
                    ft.Icons.POINT_OF_SALE_ROUNDED,
                    COLORS["primary"],
                    [COLORS["primary"], "#FF8C61"],
                    lambda e: on_section_click("POS")
                ),
                crear_boton_accion_flotante(
                    "Registrar Asistencia",
                    ft.Icons.LOGIN_ROUNDED,
                    COLORS["blue"],
                    [COLORS["blue"], "#7DD3FC"],
                    lambda e: on_section_click("Asistencia")
                ),
                crear_boton_accion_flotante(
                    "Agregar Cliente",
                    ft.Icons.PERSON_ADD_ROUNDED,
                    COLORS["green"],
                    [COLORS["green"], "#86EFAC"],
                    lambda e: on_section_click("Clientes")
                ),
                crear_boton_accion_flotante(
                    "Ver Reportes",
                    ft.Icons.BAR_CHART_ROUNDED,
                    COLORS["purple"],
                    [COLORS["purple"], "#DDD6FE"],
                    lambda e: on_section_click("Reportes")
                ),
            ], spacing=Theme.SPACING["2xl"]),
            padding=0,
            bgcolor="transparent",  # Fondo transparente/invisible
        )

    # ==========================================
    # CONTENIDO PRINCIPAL: STATS + ACCIONES
    # ==========================================
    def crear_contenido_principal():
        """Crear contenido principal con estructura clara"""
        return ft.Column([
            # CONTENEDOR 1: ESTADÍSTICAS (4 CARDS)
            create_card_container(
                content=ft.Row([
                    # Card de Ingresos (más ancha)
                    crear_card_ingresos(),

                    # Mini Stats
                    crear_mini_stat_card(
                        "TOTAL CLIENTES",
                        stats['total_clientes'],
                        ft.Icons.GROUPS_3_ROUNDED,
                        COLORS["purple"],
                    ),
                    crear_mini_stat_card(
                        "CLIENTES ACTIVOS",
                        stats['clientes_activos'],
                        ft.Icons.VERIFIED_USER_ROUNDED,
                        COLORS["green"],
                        subtitulo=f"{stats['porcentaje_activos']}%"
                    ),
                    crear_mini_stat_card(
                        "ASISTENCIAS HOY",
                        stats['asistencias_hoy'],
                        ft.Icons.FITNESS_CENTER_ROUNDED,
                        COLORS["blue"],
                    ),
                ], spacing=Theme.SPACING["xl"]),
                padding=Theme.SPACING["xl"],
                shadow="xl",
                bgcolor=Theme.CARD_BG_DARK,
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # CONTENEDOR 2: BARRA DE ACCIONES RÁPIDAS (HORIZONTAL)
            crear_barra_acciones_rapidas(),

        ], spacing=0)

    # ==========================================
    # ACTIVIDAD RECIENTE - FEED COMPLETO Y ORDENADO
    # ==========================================
    def cargar_actividades_recientes():
        """
        Cargar actividades recientes del backend con feed mixto ordenado cronológicamente

        Muestra:
        1. Ventas (compras de productos/servicios)
        2. Asistencias (check-ins al gimnasio)
        3. Nuevos clientes registrados
        4. Renovaciones de membresías

        Todo ordenado por hora (más reciente primero)
        """
        actividades = []

        try:
            fecha_hoy = get_now_local().strftime('%Y-%m-%d')

            # ==========================================
            # 1. OBTENER VENTAS DEL DÍA
            # ==========================================
            try:
                ventas = api.get_ventas(fecha_desde=fecha_hoy, fecha_hasta=fecha_hoy)
                if ventas:
                    for venta in ventas:
                        try:
                            fecha_str = venta.get('fecha', '')
                            if fecha_str:
                                fecha_dt = parse_datetime_from_api(fecha_str)
                                hora = format_time_display(fecha_dt) if fecha_dt else "N/A"
                                # Timestamp para ordenar
                                timestamp = fecha_dt if fecha_dt else get_now_local()
                            else:
                                hora = "N/A"
                                timestamp = get_now_local()
                        except:
                            hora = "N/A"
                            timestamp = get_now_local()

                        cliente_nombre = venta.get('cliente_nombre', 'Sin cliente')
                        total = venta.get('total', 0)

                        actividades.append({
                            "titulo": cliente_nombre,
                            "descripcion": f"Venta • S/. {total:.2f}",
                            "icono": ft.Icons.SHOPPING_CART_ROUNDED,
                            "hora": hora,
                            "color": COLORS["primary"],
                            "tipo": "venta",
                            "timestamp": timestamp
                        })
            except Exception as e:
                print(f"Error al cargar ventas: {e}")

            # ==========================================
            # 2. OBTENER ASISTENCIAS DEL DÍA
            # ==========================================
            try:
                stats_asistencias = api.get_estadisticas_asistencias_hoy()
                asistencias_lista = stats_asistencias.get('asistencias', [])

                for asistencia in asistencias_lista:
                    try:
                        hora_str = asistencia.get('hora_entrada', '')
                        if hora_str and ':' in hora_str:
                            hora = hora_str[:5]  # HH:MM
                            # Crear timestamp para hoy con esa hora
                            hora_parts = hora.split(':')
                            now = get_now_local()
                            timestamp = now.replace(
                                hour=int(hora_parts[0]),
                                minute=int(hora_parts[1]),
                                second=0
                            )
                        else:
                            hora = hora_str or "N/A"
                            timestamp = get_now_local()
                    except:
                        hora = "N/A"
                        timestamp = get_now_local()

                    cliente_nombre = asistencia.get('cliente_nombre', 'Cliente')

                    actividades.append({
                        "titulo": cliente_nombre,
                        "descripcion": "Check-in al gimnasio",
                        "icono": ft.Icons.LOGIN_ROUNDED,
                        "hora": hora,
                        "color": COLORS["blue"],
                        "tipo": "asistencia",
                        "timestamp": timestamp
                    })
            except Exception as e:
                print(f"Error al cargar asistencias: {e}")

            # ==========================================
            # 3. OBTENER NUEVOS CLIENTES DEL DÍA
            # ==========================================
            try:
                # Obtener todos los clientes y filtrar los de hoy
                reporte_clientes = api.get_reporte_clientes_general()
                clientes_nuevos_hoy = reporte_clientes.get('clientes_nuevos_hoy', 0)

                # Si hay clientes nuevos, agregar una entrada genérica
                # (El backend debería tener un endpoint específico para esto)
                if clientes_nuevos_hoy > 0:
                    actividades.append({
                        "titulo": f"{clientes_nuevos_hoy} nuevo{'s' if clientes_nuevos_hoy > 1 else ''} cliente{'s' if clientes_nuevos_hoy > 1 else ''}",
                        "descripcion": "Registrado en el sistema",
                        "icono": ft.Icons.PERSON_ADD_ROUNDED,
                        "hora": "Hoy",
                        "color": COLORS["green"],
                        "tipo": "nuevo_cliente",
                        "timestamp": get_now_local()
                    })
            except Exception as e:
                print(f"Error al cargar nuevos clientes: {e}")

            # ==========================================
            # 4. ORDENAR POR TIMESTAMP (MÁS RECIENTE PRIMERO)
            # ==========================================
            actividades_ordenadas = sorted(
                actividades,
                key=lambda x: x.get('timestamp', get_now_local()),
                reverse=True
            )

            # ==========================================
            # 5. LIMITAR A LAS 10 MÁS RECIENTES
            # ==========================================
            actividades_finales = actividades_ordenadas[:10]

            # Si no hay actividades, mostrar mensaje
            if len(actividades_finales) == 0:
                return [{
                    "titulo": "Sin actividad reciente",
                    "descripcion": "Aún no hay registros hoy",
                    "icono": ft.Icons.INBOX_ROUNDED,
                    "hora": "--:--",
                    "color": Theme.TEXT_DISABLED,
                    "tipo": "empty",
                    "timestamp": get_now_local()
                }]

            return actividades_finales

        except Exception as e:
            print(f"Error general al cargar actividades: {e}")
            return [{
                "titulo": "Error al cargar actividades",
                "descripcion": "Intenta recargar la página",
                "icono": ft.Icons.ERROR_OUTLINE_ROUNDED,
                "hora": "--:--",
                "color": Theme.ERROR,
                "tipo": "error",
                "timestamp": get_now_local()
            }]

    # Cargar actividades
    actividades_data = cargar_actividades_recientes()

    # Crear items de actividad con diseño minimalista
    activity_items = []
    for act in actividades_data:
        item = ft.Container(
            content=ft.Row([
                # Ícono circular
                ft.Container(
                    content=ft.Icon(
                        act["icono"],
                        size=20,
                        color=ft.Colors.WHITE
                    ),
                    bgcolor=act["color"],
                    border_radius=Theme.RADIUS["full"],
                    width=44,
                    height=44,
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=Theme.SPACING["md"]),
                # Información
                ft.Column([
                    ft.Text(
                        act["titulo"],
                        size=Theme.FONT_SIZE["md"],
                        color=Theme.TEXT_PRIMARY,
                        weight=Theme.FONT_WEIGHT["semibold"],
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        act["descripcion"],
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.TEXT_SECONDARY,
                    ),
                ], spacing=4, expand=True),
                # Hora
                ft.Text(
                    act["hora"],
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_MUTED,
                    weight=Theme.FONT_WEIGHT["medium"],
                ),
            ], spacing=0),
            padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"], vertical=Theme.SPACING["md"]),
            border=ft.border.only(bottom=ft.BorderSide(1, Theme.BORDER_DEFAULT)),
        )
        activity_items.append(item)

    # Widget de actividad
    activity_widget = create_activity_widget(
        title="Actividad Reciente",
        items=activity_items,
        icon=ft.Icons.HISTORY_ROUNDED
    )

    # ==========================================
    # WIDGET: MÉTRICAS VISUALES (COMPACTO)
    # ==========================================
    def crear_widget_metricas():
        """Widget de métricas con progress bars - versión compacta"""
        return create_card_container(
            content=ft.Column([
                # Header compacto
                ft.Row([
                    ft.Icon(ft.Icons.SPEED_ROUNDED, size=20, color=COLORS["primary"]),
                    ft.Text(
                        "Métricas del Día",
                        size=Theme.FONT_SIZE["md"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                ], spacing=Theme.SPACING["xs"]),

                ft.Container(height=Theme.SPACING["xl"]),

                # Métrica 1: Asistencias
                ft.Column([
                    ft.Row([
                        ft.Text("Asistencias", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                        ft.Container(expand=True),
                        ft.Text(
                            str(stats['asistencias_hoy']),
                            size=Theme.FONT_SIZE["lg"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=COLORS["blue"]
                        ),
                    ]),
                    ft.Container(height=8),
                    ft.ProgressBar(
                        value=min(1.0, stats['asistencias_hoy'] / 50) if stats['asistencias_hoy'] > 0 else 0,
                        color=COLORS["blue"],
                        bgcolor=f"{COLORS['blue']}25",
                        height=6,
                        border_radius=Theme.RADIUS["full"],
                    ),
                ], spacing=0),

                ft.Container(height=Theme.SPACING["lg"]),

                # Métrica 2: Ventas
                ft.Column([
                    ft.Row([
                        ft.Text("Ventas", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                        ft.Container(expand=True),
                        ft.Text(
                            str(stats['total_ventas']),
                            size=Theme.FONT_SIZE["lg"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=COLORS["primary"]
                        ),
                    ]),
                    ft.Container(height=8),
                    ft.ProgressBar(
                        value=min(1.0, stats['total_ventas'] / 30) if stats['total_ventas'] > 0 else 0,
                        color=COLORS["primary"],
                        bgcolor=f"{COLORS['primary']}25",
                        height=6,
                        border_radius=Theme.RADIUS["full"],
                    ),
                ], spacing=0),

                ft.Container(height=Theme.SPACING["lg"]),

                # Métrica 3: Tasa de Actividad
                ft.Column([
                    ft.Row([
                        ft.Text("Tasa Activa", size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY),
                        ft.Container(expand=True),
                        ft.Text(
                            f"{stats['porcentaje_activos']}%",
                            size=Theme.FONT_SIZE["lg"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=COLORS["green"]
                        ),
                    ]),
                    ft.Container(height=8),
                    ft.ProgressBar(
                        value=stats['porcentaje_activos'] / 100 if stats['porcentaje_activos'] > 0 else 0,
                        color=COLORS["green"],
                        bgcolor=f"{COLORS['green']}25",
                        height=6,
                        border_radius=Theme.RADIUS["full"],
                    ),
                ], spacing=0),
            ], spacing=0),
            padding=Theme.SPACING["lg"],
            shadow="md"
        )

    metricas_widget = crear_widget_metricas()


    # ==========================================
    # ESTRUCTURA FINAL DEL DASHBOARD
    # ==========================================
    create_dashboard_layout(
        page=page,
        role="admin",
        current_section="Dashboard",
        on_section_click=on_section_click,
        user_info=user_info,
        on_logout=on_logout,
        stats_cards=[],  # Sin stats cards, todo en main_content
        main_content=crear_contenido_principal(),
        activity_feed=activity_widget,
        widgets=[metricas_widget]  # Solo métricas en el lateral
    )

    page.update()


# ==========================================
# DOCUMENTACIÓN DEL DISEÑO OPTIMIZADO
# ==========================================
"""
✨ ESTRUCTURA VISUAL OPTIMIZADA:

┌────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ┌─────────────┬──────────┬──────────┬──────────┐             │
│  │  INGRESOS   │ CLIENTES │ ACTIVOS  │   HOY    │             │
│  │    HOY      │    👥    │    ✓     │    💪    │             │
│  │  💰 Grande  │    40    │    32    │    12    │             │
│  │  S/. XXX.XX │          │   84%    │          │             │
│  │  X ventas   │          │          │          │             │
│  └─────────────┴──────────┴──────────┴──────────┘             │
│                                                                  │
│  ┌──────────────────────────┬──────────────────────┐           │
│  │  ACTIVIDAD RECIENTE      │  ACCIONES RÁPIDAS    │           │
│  │                          │  🛒 Nueva Venta      │           │
│  │  🛒 Juan - S/50          │  🏃 Asistencia       │           │
│  │  🏃 María - Check        │  👤 Cliente          │           │
│  │  🛒 Pedro - S/30         │  📊 Reportes         │           │
│  │  🏃 Ana - Check          │                      │           │
│  │                          │  MÉTRICAS DEL DÍA    │           │
│  │                          │  • Asistencias       │           │
│  │                          │  • Ventas            │           │
│  │                          │  • Tasa Activa       │           │
│  └──────────────────────────┴──────────────────────┘           │
│                                                                  │
└────────────────────────────────────────────────────────────────┘

🎨 MEJORAS IMPLEMENTADAS:

1. FILA ÚNICA DE STATS
   ✓ Ingresos + 3 mini cards en la misma fila
   ✓ Ingresos ocupa más espacio (expand=1)
   ✓ Mini cards compactas pero legibles
   ✓ Todo alineado horizontalmente

2. ACCIONES RÁPIDAS MEJORADAS
   ✓ Botones con iconos circulares de colores
   ✓ Cada acción tiene su color distintivo:
     • Nueva Venta → Naranja
     • Asistencia → Azul
     • Cliente → Verde
     • Reportes → Púrpura
   ✓ Diseño coherente con el resto del dashboard
   ✓ Icono ⚡ (rayo) para el título

3. ORDEN DE WIDGETS
   ✓ Acciones Rápidas primero (más importante)
   ✓ Métricas después (información secundaria)

4. HEGEMONÍA VISUAL
   ✓ Mismo estilo de iconos circulares
   ✓ Paleta de colores consistente
   ✓ Espaciado uniforme
   ✓ Bordes y sombras coherentes
   ✓ Tipografía balanceada

💡 LAYOUT FINAL:
- Fila 1: Ingresos (grande) + 3 mini stats
- Fila 2: Actividad (2/3) + Acciones/Métricas (1/3)
- Todo ordenado, limpio y coherente
"""
