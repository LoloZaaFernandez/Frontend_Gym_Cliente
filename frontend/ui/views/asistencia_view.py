"""
Vista de Control de Asistencia mejorada - Conectada con API
"""

import flet as ft
from datetime import datetime
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_asistencia_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de control de asistencia mejorada

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Control de Asistencia"

    api = APIService()

    # Variables para estadísticas
    stats_hoy = {"total_asistencias": 0, "asistencias": []}
    stats_mes = {"total_asistencias": 0, "clientes_activos": 0, "promedio_diario": 0}

    # Campo de búsqueda
    dni_search = ft.TextField(
        label="Ingrese DNI del cliente",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=350,
        autofocus=True,
        on_submit=lambda e: buscar_cliente(),
        prefix_icon=ft.Icons.BADGE
    )

    search_button = ft.ElevatedButton(
        "Buscar Cliente",
        icon=ft.Icons.SEARCH,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=PRIMARY_COLOR,
        ),
        on_click=lambda _: buscar_cliente(),
        height=50
    )

    # Información del cliente encontrado
    cliente_actual = None
    cliente_info_content = ft.Column(spacing=10)

    cliente_info_container = ft.Container(
        content=cliente_info_content,
        visible=False,
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, PRIMARY_COLOR),
        margin=ft.margin.only(top=10, bottom=10)
    )

    # Estadísticas en tarjetas
    total_hoy_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR)
    clientes_activos_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color="#4CAF50")
    promedio_text = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color="#2196F3")

    # Historial de asistencias de hoy
    asistencias_hoy_list = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

    asistencias_container = ft.Container(
        content=asistencias_hoy_list,
        height=400,
        padding=15,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333")
    )

    def cargar_estadisticas():
        """Cargar estadísticas del día y mes"""
        nonlocal stats_hoy, stats_mes

        try:
            # Estadísticas del día
            stats_hoy = api.get_estadisticas_asistencias_hoy()
            total_hoy_text.value = str(stats_hoy.get('total_asistencias', 0))

            # Estadísticas del mes
            stats_mes = api.get_estadisticas_asistencias_mes()
            clientes_activos_text.value = str(stats_mes.get('clientes_activos', 0))
            promedio_text.value = str(stats_mes.get('promedio_diario', 0))

            # Actualizar lista de asistencias
            actualizar_lista_asistencias()

        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")

        page.update()

    def actualizar_lista_asistencias():
        """Actualizar lista de asistencias del día"""
        asistencias_hoy_list.controls.clear()

        asistencias = stats_hoy.get('asistencias', [])

        if not asistencias:
            asistencias_hoy_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay asistencias registradas hoy",
                        color=TEXT_SECONDARY,
                        size=14
                    ),
                    padding=20,
                    alignment=ft.alignment.center
                )
            )
        else:
            for asistencia in asistencias:
                asistencias_hoy_list.controls.append(crear_asistencia_card(asistencia))

    def crear_asistencia_card(asistencia):
        """Crear tarjeta de asistencia"""
        hora = asistencia.get('hora_ingreso', '')[:8]  # Solo HH:MM:SS

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.CHECK_CIRCLE, size=24, color="#4CAF50"),
                        bgcolor="#4CAF5022",
                        border_radius=8,
                        padding=8
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                asistencia.get('nombre_cliente', 'N/A'),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY
                            ),
                            ft.Text(
                                f"Hora: {hora} | {asistencia.get('tipo_membresia', 'Sin tipo')}",
                                size=12,
                                color=TEXT_SECONDARY
                            ),
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.FITNESS_CENTER, size=20, color=PRIMARY_COLOR),
                        padding=5
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=12,
            bgcolor="#1A1A1A",
            border_radius=8,
            border=ft.border.all(1, "#333333")
        )

    def buscar_cliente():
        """Buscar cliente por DNI"""
        nonlocal cliente_actual

        dni = dni_search.value.strip()

        if not dni:
            mostrar_mensaje("Por favor ingrese un DNI", error=True)
            return

        try:
            cliente = api.get_cliente_por_dni(dni)

            if not cliente:
                mostrar_mensaje("Cliente no encontrado", error=True)
                cliente_info_container.visible = False
                page.update()
                return

            if cliente.get('estado') != 'Activo':
                mostrar_mensaje("Cliente inactivo. No puede registrar asistencia.", error=True)
                cliente_info_container.visible = False
                page.update()
                return

            # Cliente encontrado
            cliente_actual = cliente
            mostrar_info_cliente(cliente)

        except Exception as e:
            mostrar_mensaje(f"Error al buscar cliente: {str(e)}", error=True)
            cliente_info_container.visible = False
            page.update()

    def mostrar_info_cliente(cliente):
        """Mostrar información del cliente encontrado"""
        cliente_info_content.controls.clear()

        # Obtener estadísticas del cliente
        try:
            stats_cliente = api.get_estadisticas_cliente(cliente['id'])
        except:
            stats_cliente = {
                "total_asistencias": 0,
                "ultima_asistencia": "Sin registros",
                "asistencias_mes_actual": 0
            }

        # Verificar estado de la membresía
        tiene_membresia = cliente.get('fecha_membresia') is not None
        membresia_vencida = False

        if tiene_membresia:
            try:
                from datetime import datetime
                fecha_venc = datetime.fromisoformat(cliente['fecha_membresia'])
                membresia_vencida = fecha_venc < datetime.now()
            except:
                membresia_vencida = True

        # Determinar mensaje de estado de membresía
        if not tiene_membresia:
            membresia_status = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.WARNING, size=20, color="#FF9800"),
                        ft.Text("Sin membresía activa", size=13, color="#FF9800", weight=ft.FontWeight.BOLD)
                    ],
                    spacing=5
                ),
                bgcolor="#FF980022",
                padding=8,
                border_radius=6,
                margin=ft.margin.only(top=5)
            )
        elif membresia_vencida:
            membresia_status = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ERROR, size=20, color="#ef5350"),
                        ft.Text("Membresía vencida", size=13, color="#ef5350", weight=ft.FontWeight.BOLD)
                    ],
                    spacing=5
                ),
                bgcolor="#ef535022",
                padding=8,
                border_radius=6,
                margin=ft.margin.only(top=5)
            )
        else:
            membresia_status = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color="#4CAF50"),
                        ft.Text("Membresía activa", size=13, color="#4CAF50", weight=ft.FontWeight.BOLD)
                    ],
                    spacing=5
                ),
                bgcolor="#4CAF5022",
                padding=8,
                border_radius=6,
                margin=ft.margin.only(top=5)
            )

        # Determinar qué botones mostrar
        puede_registrar = tiene_membresia and not membresia_vencida

        botones = []
        if puede_registrar:
            botones.append(
                ft.ElevatedButton(
                    "✓ REGISTRAR ASISTENCIA",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor="#4CAF50",
                    ),
                    on_click=lambda _: registrar_asistencia(),
                    height=50,
                    expand=True
                )
            )
        else:
            # Botón deshabilitado si no puede registrar
            botones.append(
                ft.ElevatedButton(
                    "⚠ No puede registrar asistencia",
                    icon=ft.Icons.BLOCK,
                    style=ft.ButtonStyle(
                        color="#999999",
                        bgcolor="#333333",
                    ),
                    disabled=True,
                    height=50,
                    expand=True
                )
            )

        botones.append(
            ft.OutlinedButton(
                "Cancelar",
                style=ft.ButtonStyle(
                    color=TEXT_SECONDARY,
                    side=ft.border.all(1, "#333333")
                ),
                on_click=lambda _: limpiar_busqueda(),
                height=50
            )
        )

        cliente_info_content.controls.extend([
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, size=50, color=PRIMARY_COLOR),
                        bgcolor=f"{PRIMARY_COLOR}22",
                        border_radius=25,
                        padding=10
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"{cliente['nombre']} {cliente['apellidos']}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY
                            ),
                            ft.Text(
                                f"DNI: {cliente['dni']}",
                                size=14,
                                color=TEXT_SECONDARY
                            ),
                            ft.Text(
                                f"Asistencias este mes: {stats_cliente.get('asistencias_mes_actual', 0)}",
                                size=13,
                                color=PRIMARY_COLOR,
                                weight=ft.FontWeight.BOLD
                            ),
                            membresia_status
                        ],
                        spacing=3,
                        expand=True
                    ),
                ],
                spacing=15
            ),
            ft.Divider(height=1, color="#333333"),
            ft.Row(
                controls=botones,
                spacing=10
            )
        ])

        cliente_info_container.visible = True
        page.update()

    def registrar_asistencia():
        """Registrar asistencia del cliente actual"""
        if not cliente_actual:
            mostrar_mensaje("No hay cliente seleccionado", error=True)
            return

        try:
            result = api.registrar_asistencia(cliente_actual['dni'])

            # Mostrar mensaje de éxito
            hora = result.get('hora_ingreso', '')[:8]
            mostrar_mensaje(
                f"✓ Asistencia registrada: {cliente_actual['nombre']} {cliente_actual['apellidos']} - {hora}",
                error=False
            )

            # Limpiar búsqueda y recargar estadísticas
            limpiar_busqueda()
            cargar_estadisticas()

        except ValueError as e:
            # Errores de validación del backend
            error_msg = str(e)
            if "Membresía vencida" in error_msg:
                mostrar_mensaje("❌ Membresía vencida. El cliente debe renovar su membresía.", error=True)
            elif "sin membresía" in error_msg.lower():
                mostrar_mensaje("❌ Cliente sin membresía activa. Debe adquirir una membresía.", error=True)
            elif "Cliente inactivo" in error_msg:
                mostrar_mensaje("❌ Cliente inactivo. No puede registrar asistencia.", error=True)
            elif "Cliente no encontrado" in error_msg:
                mostrar_mensaje("❌ Cliente no encontrado en el sistema.", error=True)
            else:
                mostrar_mensaje(f"❌ Error: {error_msg}", error=True)
        except ConnectionError as e:
            mostrar_mensaje("❌ Error de conexión con el servidor. Verifique que el backend esté corriendo.", error=True)
        except Exception as e:
            mostrar_mensaje(f"❌ Error inesperado: {str(e)}", error=True)

    def limpiar_busqueda():
        """Limpiar búsqueda y ocultar info del cliente"""
        nonlocal cliente_actual
        cliente_actual = None
        dni_search.value = ""
        cliente_info_container.visible = False
        page.update()

    def mostrar_mensaje(mensaje, error=False):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#ef5350" if error else "#4CAF50"
        )
        page.snack_bar.open = True
        page.update()

    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=PRIMARY_COLOR,
                        on_click=lambda _: on_back(),
                        icon_size=24
                    ),
                    ft.Icon(ft.Icons.DIRECTIONS_RUN, size=32, color=PRIMARY_COLOR),
                    ft.Text("Control de Asistencia", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ], spacing=10),
                ft.ElevatedButton(
                    "Actualizar",
                    icon=ft.Icons.REFRESH,
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        bgcolor=ft.Colors.TRANSPARENT,
                        side=ft.border.all(1, PRIMARY_COLOR)
                    ),
                    on_click=lambda _: cargar_estadisticas(),
                    height=40
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Tarjetas de estadísticas
    stats_cards = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.TODAY, size=30, color=PRIMARY_COLOR),
                        total_hoy_text,
                        ft.Text("Asistencias Hoy", size=14, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                bgcolor=CARD_BG,
                padding=20,
                border_radius=12,
                border=ft.border.all(1, "#333333"),
                expand=True
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.PEOPLE, size=30, color="#4CAF50"),
                        clientes_activos_text,
                        ft.Text("Clientes Activos Mes", size=14, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                bgcolor=CARD_BG,
                padding=20,
                border_radius=12,
                border=ft.border.all(1, "#333333"),
                expand=True
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.TRENDING_UP, size=30, color="#2196F3"),
                        promedio_text,
                        ft.Text("Promedio Diario", size=14, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                bgcolor=CARD_BG,
                padding=20,
                border_radius=12,
                border=ft.border.all(1, "#333333"),
                expand=True
            ),
        ],
        spacing=15
    )

    # Panel de registro
    registro_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Registrar Nueva Asistencia",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY
                ),
                ft.Row(
                    controls=[dni_search, search_button],
                    spacing=10
                ),
                cliente_info_container,
            ],
            spacing=15
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333")
    )

    # Panel de asistencias del día
    asistencias_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.HISTORY, size=20, color=PRIMARY_COLOR),
                        ft.Text(
                            "Asistencias de Hoy",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY
                        ),
                    ],
                    spacing=10
                ),
                asistencias_container,
            ],
            spacing=15
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333")
    )

    # Layout principal
    main_content = ft.Column(
        controls=[
            header,
            ft.Container(
                content=stats_cards,
                padding=ft.padding.symmetric(horizontal=10)
            ),
            ft.Row(
                controls=[
                    ft.Container(content=registro_panel, expand=2),
                    ft.Container(content=asistencias_panel, expand=3),
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.START
            )
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    page.add(
        ft.Container(
            content=main_content,
            bgcolor=BACKGROUND_DARK,
            expand=True,
            padding=10
        )
    )

    # Cargar datos iniciales
    cargar_estadisticas()
