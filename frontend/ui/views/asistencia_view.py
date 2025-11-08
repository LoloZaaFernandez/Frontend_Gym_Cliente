"""
Vista de Control de Asistencia - CORREGIDA
Conectada con API con validaciones completas
"""

import flet as ft
from datetime import datetime
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_asistencia_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de control de asistencia - CORREGIDA
    """
    page.clean()
    page.title = "BLESSED GYM - Control de Asistencia"

    api = APIService()

    # Variables para estadísticas
    stats_hoy = {"total_asistencias": 0, "asistencias": []}
    stats_mes = {"total_asistencias": 0, "promedio_diario": 0}

    # Variables de estado para búsqueda
    is_searching = False

    # Campo de búsqueda con validación
    def on_dni_change(e):
        """Validar DNI mientras se escribe"""
        value = dni_search.value
        if value and not value.isdigit():
            dni_search.value = ''.join(filter(str.isdigit, value))
            dni_search.update()
            return
        # Auto-buscar cuando se completen 8 dígitos
        if value and len(value) == 8:
            buscar_cliente()

    dni_search = ft.TextField(
        label="Ingrese DNI del cliente",
        hint_text="8 dígitos",
        border_color="#333333",
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_BG,
        color=TEXT_PRIMARY,
        width=350,
        max_length=8,
        counter_text="",
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: buscar_cliente(),
        on_change=on_dni_change,
        prefix_icon=ft.Icons.BADGE
    )

    search_button = ft.ElevatedButton(
        "Buscar Cliente",
        icon=ft.Icons.SEARCH,
        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=PRIMARY_COLOR),
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
                    content=ft.Text("No hay asistencias registradas hoy", color=TEXT_SECONDARY, size=14),
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
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.CHECK_CIRCLE, size=24, color="#4CAF50"),
                    bgcolor="#4CAF5022",
                    border_radius=8,
                    padding=8
                ),
                ft.Column([
                    ft.Text(asistencia.get('nombre_cliente', 'N/A'), size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                    ft.Text(f"Hora: {hora} | {asistencia.get('tipo_membresia', 'Sin tipo')}", size=12, color=TEXT_SECONDARY),
                ], spacing=2, expand=True),
                ft.Container(
                    content=ft.Icon(ft.Icons.FITNESS_CENTER, size=20, color=PRIMARY_COLOR),
                    padding=5
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=12,
            bgcolor="#1A1A1A",
            border_radius=8,
            border=ft.border.all(1, "#333333")
        )

    def buscar_cliente():
        """ CORREGIDO: Buscar cliente con todas las validaciones"""
        nonlocal cliente_actual, is_searching

        if is_searching:
            return

        dni = dni_search.value.strip()

        # Validar formato de DNI
        if not dni:
            mostrar_mensaje("Por favor ingrese un DNI", error=True)
            return

        if not dni.isdigit() or len(dni) != 8:
            mostrar_mensaje("El DNI debe tener exactamente 8 dígitos", error=True)
            return

        # Mostrar estado de carga
        is_searching = True
        search_button.text = "Buscando..."
        search_button.disabled = True
        dni_search.disabled = True
        page.update()

        try:
            #  Buscar cliente en el backend
            cliente = api.get_cliente_por_dni(dni)

            if not cliente:
                mostrar_mensaje(f"❌ Cliente con DNI {dni} no encontrado", error=True)
                cliente_info_container.visible = False
            else:
                #  Cliente encontrado - mostrar info con validaciones
                cliente_actual = cliente
                mostrar_info_cliente(cliente)

        except Exception as e:
            error_msg = str(e)
            if "Connection" in error_msg:
                mostrar_mensaje("❌ Error de conexión. Verifique que el backend esté corriendo.", error=True)
            else:
                mostrar_mensaje(f"❌ Error: {error_msg}", error=True)
            cliente_info_container.visible = False

        finally:
            is_searching = False
            search_button.text = "Buscar Cliente"
            search_button.disabled = False
            dni_search.disabled = False
            page.update()

    def mostrar_info_cliente(cliente):
        """ CORREGIDO: Mostrar información del cliente con validaciones completas"""
        cliente_info_content.controls.clear()

        #  1. VALIDAR ESTADO DEL CLIENTE
        estado_cliente = cliente.get('estado', 'Desconocido')
        
        estado_config = {
            "Activo": {
                "color": "#4CAF50",
                "icono": ft.Icons.CHECK_CIRCLE,
                "texto": "Cliente Activo"
            },
            "Inactivo": {
                "color": "#ef5350",
                "icono": ft.Icons.CANCEL,
                "texto": "Cliente Inactivo"
            },
            "Congelado": {
                "color": "#FF9800",
                "icono": ft.Icons.AC_UNIT,
                "texto": "Membresía Congelada"
            }
        }

        config_estado = estado_config.get(estado_cliente, estado_config["Inactivo"])

        # 2. VALIDAR MEMBRESÍA
        tiene_membresia = cliente.get('fecha_membresia') is not None
        membresia_vigente = False
        dias_restantes = 0

        if tiene_membresia:
            try:
                fecha_venc = datetime.fromisoformat(cliente['fecha_membresia'])
                fecha_actual = datetime.now()
                dias_restantes = (fecha_venc - fecha_actual).days
                membresia_vigente = dias_restantes >= 0
            except:
                membresia_vigente = False

        # 3. VERIFICAR SI YA REGISTRÓ ASISTENCIA HOY
        ya_registro_hoy = False
        hora_registro = None
        
        try:
            # Obtener asistencias del cliente hoy
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            asistencias_hoy_cliente = api.get_asistencias(
                fecha_inicio=fecha_hoy,
                fecha_fin=fecha_hoy,
                cliente_id=cliente['id']
            )
            
            if asistencias_hoy_cliente and len(asistencias_hoy_cliente) > 0:
                ya_registro_hoy = True
                hora_registro = asistencias_hoy_cliente[0].get('hora_ingreso', '')[:8]
        except Exception as e:
            print(f"Error al verificar asistencia: {e}")

        # 4. DETERMINAR SI PUEDE REGISTRAR ASISTENCIA
        puede_registrar = (
            estado_cliente == "Activo" and 
            tiene_membresia and 
            membresia_vigente and 
            not ya_registro_hoy
        )

        # 5. CREAR BADGES DE ESTADO
        # Badge de estado del cliente
        badge_estado_cliente = ft.Container(
            content=ft.Row([
                ft.Icon(config_estado['icono'], size=16, color=ft.Colors.WHITE),
                ft.Text(config_estado['texto'], size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ], spacing=5),
            bgcolor=config_estado['color'],
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=20,
        )

        # Badge de membresía
        if not tiene_membresia:
            badge_membresia = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.WARNING, size=16, color=ft.Colors.WHITE),
                    ft.Text("Sin Membresía", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                ], spacing=5),
                bgcolor="#FF9800",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
            )
        elif not membresia_vigente:
            badge_membresia = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, size=16, color=ft.Colors.WHITE),
                    ft.Text("Membresía Vencida", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                ], spacing=5),
                bgcolor="#ef5350",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
            )
        else:
            badge_membresia = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=ft.Colors.WHITE),
                    ft.Text(f"Membresía Activa ({dias_restantes} días)", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                ], spacing=5),
                bgcolor="#4CAF50",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
            )

        # Badge si ya registró hoy
        badge_registro_hoy = None
        if ya_registro_hoy:
            badge_registro_hoy = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, size=16, color=ft.Colors.WHITE),
                    ft.Text(f"Ya registró hoy a las {hora_registro}", size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                ], spacing=5),
                bgcolor="#2196F3",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
            )

        # 6. OBTENER ESTADÍSTICAS DEL CLIENTE
        try:
            stats_cliente = api.get_estadisticas_cliente(cliente['id'])
        except:
            stats_cliente = {
                "total_asistencias": 0,
                "asistencias_mes_actual": 0
            }

        # 7. CONSTRUIR CONTENIDO DE LA TARJETA
        contenido = [
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, size=50, color=PRIMARY_COLOR),
                    bgcolor=f"{PRIMARY_COLOR}22",
                    border_radius=25,
                    padding=10
                ),
                ft.Column([
                    ft.Text(
                        f"{cliente['nombre']} {cliente['apellidos']}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY
                    ),
                    ft.Text(f"DNI: {cliente['dni']}", size=14, color=TEXT_SECONDARY),
                    ft.Text(
                        f"Asistencias este mes: {stats_cliente.get('asistencias_mes_actual', 0)}",
                        size=13,
                        color=PRIMARY_COLOR,
                        weight=ft.FontWeight.BOLD
                    ),
                ], spacing=3, expand=True),
            ], spacing=15),
            ft.Container(height=10),
            # Badges de estado
            ft.Row([badge_estado_cliente, badge_membresia], spacing=10, wrap=True),
        ]

        # Agregar badge de registro hoy si aplica
        if badge_registro_hoy:
            contenido.append(ft.Container(height=5))
            contenido.append(badge_registro_hoy)

        contenido.append(ft.Divider(height=1, color="#333333"))

        # 8. BOTONES DE ACCIÓN
        botones = []

        if puede_registrar:
            # Puede registrar asistencia
            botones.append(
                ft.ElevatedButton(
                    "✓ REGISTRAR ASISTENCIA",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor="#4CAF50"),
                    on_click=lambda _: registrar_asistencia(),
                    height=50,
                    expand=True
                )
            )
        else:
            # ❌ NO puede registrar - Mostrar razón
            if estado_cliente != "Activo":
                razon = f"Cliente {estado_cliente.lower()}"
            elif not tiene_membresia:
                razon = "Sin membresía"
            elif not membresia_vigente:
                razon = "Membresía vencida"
            elif ya_registro_hoy:
                razon = "Ya registró hoy"
            else:
                razon = "No puede registrar"

            botones.append(
                ft.ElevatedButton(
                    f" {razon}",
                    icon=ft.Icons.BLOCK,
                    style=ft.ButtonStyle(color="#999999", bgcolor="#333333"),
                    disabled=True,
                    height=50,
                    expand=True
                )
            )

        botones.append(
            ft.OutlinedButton(
                "Cancelar",
                style=ft.ButtonStyle(color=TEXT_SECONDARY, side=ft.border.all(1, "#333333")),
                on_click=lambda _: limpiar_busqueda(),
                height=50
            )
        )

        contenido.append(ft.Row(botones, spacing=10))

        cliente_info_content.controls.extend(contenido)
        cliente_info_container.visible = True
        page.update()

    def registrar_asistencia():
        """ CORREGIDO: Registrar asistencia con validaciones"""
        if not cliente_actual:
            mostrar_mensaje("No hay cliente seleccionado", error=True)
            return

        try:
            # Registrar asistencia
            result = api.registrar_asistencia(cliente_actual['dni'])

            # Mensaje de éxito
            hora = result.get('hora_ingreso', '')[:8]
            fecha = result.get('fecha_asistencia', '')
            
            mostrar_mensaje(
                f"✓ Asistencia registrada: {cliente_actual['nombre']} {cliente_actual['apellidos']} - {hora}",
                error=False
            )

            # Limpiar y recargar
            limpiar_busqueda()
            cargar_estadisticas()

        except ValueError as e:
            error_msg = str(e)
            
            # Detectar error de asistencia duplicada
            if "ya registró asistencia" in error_msg.lower():
                mostrar_mensaje(f"⚠ {error_msg}", error=True)
            elif "Membresía vencida" in error_msg:
                mostrar_mensaje("❌ Membresía vencida. El cliente debe renovar.", error=True)
            elif "sin membresía" in error_msg.lower():
                mostrar_mensaje("❌ Cliente sin membresía activa.", error=True)
            elif "Cliente inactivo" in error_msg:
                mostrar_mensaje("❌ Cliente inactivo. No puede registrar asistencia.", error=True)
            else:
                mostrar_mensaje(f"❌ Error: {error_msg}", error=True)
                
        except Exception as e:
            mostrar_mensaje(f"❌ Error inesperado: {str(e)}", error=True)

    def limpiar_busqueda():
        """Limpiar búsqueda"""
        nonlocal cliente_actual
        cliente_actual = None
        dni_search.value = ""
        cliente_info_container.visible = False
        dni_search.focus()
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
        content=ft.Row([
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=PRIMARY_COLOR, on_click=lambda _: on_back(), icon_size=24),
                ft.Icon(ft.Icons.DIRECTIONS_RUN, size=32, color=PRIMARY_COLOR),
                ft.Text("Control de Asistencia", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ], spacing=10),
            ft.ElevatedButton(
                "Actualizar",
                icon=ft.Icons.REFRESH,
                style=ft.ButtonStyle(color=PRIMARY_COLOR, bgcolor=ft.Colors.TRANSPARENT, side=ft.border.all(1, PRIMARY_COLOR)),
                on_click=lambda _: cargar_estadisticas(),
                height=40
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Tarjetas de estadísticas
    stats_cards = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.TODAY, size=30, color=PRIMARY_COLOR),
                total_hoy_text,
                ft.Text("Asistencias Hoy", size=14, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=CARD_BG,
            padding=20,
            border_radius=12,
            border=ft.border.all(1, "#333333"),
            expand=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.TRENDING_UP, size=30, color="#2196F3"),
                promedio_text,
                ft.Text("Promedio Diario", size=14, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=CARD_BG,
            padding=20,
            border_radius=12,
            border=ft.border.all(1, "#333333"),
            expand=True
        ),
    ], spacing=15)

    # Panel de registro
    registro_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PERSON_SEARCH, size=24, color=PRIMARY_COLOR),
                ft.Text("Registrar Nueva Asistencia", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ], spacing=10),
            ft.Divider(height=1, color="#333333"),
            ft.Row([dni_search, search_button], spacing=10, wrap=True),
            ft.Row([
                ft.TextButton(
                    "Limpiar",
                    icon=ft.Icons.CLEAR,
                    style=ft.ButtonStyle(color=TEXT_SECONDARY),
                    on_click=lambda _: limpiar_busqueda()
                ),
            ]),
            cliente_info_container,
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333")
    )

    # Panel de asistencias del día
    asistencias_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.HISTORY, size=20, color=PRIMARY_COLOR),
                ft.Text("Asistencias de Hoy", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ], spacing=10),
            asistencias_container,
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        border=ft.border.all(1, "#333333")
    )

    # Layout principal
    main_content = ft.Column([
        header,
        ft.Container(content=stats_cards, padding=ft.padding.symmetric(horizontal=10)),
        ft.Row([
            ft.Container(content=registro_panel, expand=2),
            ft.Container(content=asistencias_panel, expand=3),
        ], spacing=15, alignment=ft.MainAxisAlignment.START)
    ], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

    page.add(ft.Container(content=main_content, bgcolor=BACKGROUND_DARK, expand=True, padding=10))

    # Cargar datos iniciales
    cargar_estadisticas()