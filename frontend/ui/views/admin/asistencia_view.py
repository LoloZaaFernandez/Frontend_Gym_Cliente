"""
Vista de Control de Asistencia - Con tabla paginada y información completa
Incluye: Hora de registro, Nombre, Tipo de membresía, Método de pago
"""

import flet as ft
from datetime import datetime
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button, create_status_badge, create_icon_button
from ui.components.molecules import create_card_container, create_stat_card, create_empty_state
from ui.utils.messages import mostrar_exito, mostrar_error
from ui.utils.datetime_utils import parse_datetime_from_api, format_datetime_display, format_time_display


def show_asistencia_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Vista de control de asistencia con tabla paginada
    """
    page.title = "BLESSED GYM - Control de Asistencia"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Estado
    cliente_actual = [None]
    asistencias_list = []
    asistencias_filtradas = []
    stats_hoy = {"total_asistencias": 0}
    stats_mes = {"promedio_diario": 0}
    metodos_pago_cache = {}  # Cache para métodos de pago

    # Paginación
    items_per_page = 10
    current_page = [0]

    # ==========================================
    # COMPONENTES
    # ==========================================
    dni_search = ft.TextField(
        label="Ingrese DNI del cliente",
        hint_text="8 dígitos",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        max_length=8,
        counter_text="",
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.BADGE,
        width=300
    )

    cliente_info_content = ft.Column(spacing=Theme.SPACING["md"])
    cliente_info_container = ft.Container(
        content=cliente_info_content,
        visible=False,
        padding=Theme.SPACING["xl"],
        bgcolor=Theme.CARD_BG,
        border_radius=Theme.RADIUS["lg"],
        border=ft.border.all(1, Theme.PRIMARY),
    )

    search_field = ft.TextField(
        hint_text="Buscar asistencia...",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=lambda e: filtrar_asistencias(e.control.value)
    )

    tabla_container = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
    pagination_text = ft.Text("", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY)
    stat_total_hoy = ft.Ref[ft.Container]()
    stat_promedio_mes = ft.Ref[ft.Container]()
    contador_registros = ft.Ref[ft.Text]()

    # ==========================================
    # FUNCIONES DE DATOS
    # ==========================================
    def load_estadisticas():
        """Cargar estadísticas y asistencias"""
        nonlocal asistencias_list, asistencias_filtradas, stats_hoy, stats_mes, metodos_pago_cache

        try:
            # Cargar todas las asistencias de hoy
            asistencias_list = api.get_asistencias_hoy()
            asistencias_filtradas = asistencias_list.copy()
            stats_hoy["total_asistencias"] = len(asistencias_list)

            # Estadísticas del mes
            asistencias_mes = api.get_asistencias_mes()
            dias_transcurridos = datetime.now().day
            stats_mes["promedio_diario"] = round(len(asistencias_mes) / dias_transcurridos, 1) if dias_transcurridos > 0 else 0

            # Pre-cargar métodos de pago de todos los clientes con asistencias
            metodos_pago_cache.clear()
            clientes_ids = set(a.get('id_cliente') for a in asistencias_list if a.get('id_cliente'))

            for cliente_id in clientes_ids:
                try:
                    metodo = api.get_metodo_pago_cliente(cliente_id)
                    metodos_pago_cache[cliente_id] = metodo
                except:
                    metodos_pago_cache[cliente_id] = "Sin registro"

        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")
            asistencias_list = []
            asistencias_filtradas = []

        update_stats()
        update_tabla()

    def filtrar_asistencias(search_term):
        """Filtrar asistencias por término de búsqueda"""
        nonlocal asistencias_filtradas
        search_term = search_term.lower().strip()

        if not search_term:
            asistencias_filtradas = asistencias_list.copy()
        else:
            asistencias_filtradas = [
                a for a in asistencias_list
                if (search_term in a.get('nombre_cliente', '').lower() or
                    search_term in str(a.get('id_cliente', '')).lower() or
                    search_term in a.get('tipo_membresia', '').lower())
            ]

        current_page[0] = 0
        update_tabla()

    def update_stats():
        """Actualizar stats cards"""
        if stat_total_hoy.current:
            stat_total_hoy.current.content = create_stat_card(
                title="Asistencias Hoy",
                value=str(stats_hoy["total_asistencias"]),
                icon=ft.Icons.FITNESS_CENTER,
                color=Theme.PRIMARY
            ).content
            stat_total_hoy.current.update()

        if stat_promedio_mes.current:
            stat_promedio_mes.current.content = create_stat_card(
                title="Promedio Diario",
                value=str(stats_mes["promedio_diario"]),
                icon=ft.Icons.TRENDING_UP,
                color=Theme.INFO
            ).content
            stat_promedio_mes.current.update()

    def update_tabla():
        """Actualizar tabla de asistencias con paginación"""
        tabla_container.controls.clear()

        # Actualizar contador de registros
        if contador_registros.current:
            contador_registros.current.value = f"{len(asistencias_list)} registros"
            contador_registros.current.update()

        if not asistencias_filtradas:
            tabla_container.controls.append(
                create_empty_state(
                    message="No hay asistencias para mostrar",
                    icon=ft.Icons.FITNESS_CENTER,
                    secondary_message="Las asistencias registradas aparecerán aquí"
                )
            )
            pagination_text.value = "Mostrando 0 de 0 asistencias"
            page.update()
            return

        # Calcular paginación
        total_items = len(asistencias_filtradas)
        start_idx = current_page[0] * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        asistencias_pagina = asistencias_filtradas[start_idx:end_idx]

        # Encabezado de tabla
        header = ft.Container(
            content=ft.Row([
                ft.Container(ft.Text("Hora", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Fecha", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Cliente", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=2),
                ft.Container(ft.Text("Tipo de Membresía", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=2),
                ft.Container(ft.Text("Método de Pago", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Estado", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
            ], spacing=Theme.SPACING["sm"]),
            bgcolor=f"{Theme.PRIMARY}22",
            padding=Theme.SPACING["md"],
            border_radius=Theme.RADIUS["sm"]
        )
        tabla_container.controls.append(header)

        # Filas de datos
        for asistencia in asistencias_pagina:
            # Parsear fecha y hora con zona horaria correcta
            hora_str = "--:--"
            fecha_str = "--/--/----"

            # Intentar obtener hora_ingreso y fecha_asistencia
            hora_ingreso = asistencia.get('hora_ingreso')
            fecha_asistencia = asistencia.get('fecha_asistencia')

            if hora_ingreso:
                # Si hora_ingreso tiene formato completo ISO con fecha (YYYY-MM-DDTHH:MM:SS)
                if 'T' in str(hora_ingreso):
                    dt = parse_datetime_from_api(hora_ingreso)
                    if dt:
                        hora_str = format_time_display(dt)
                        fecha_str = dt.strftime("%d/%m/%Y")
                else:
                    # Es solo hora (HH:MM:SS.mmmmmm), combinar con fecha_asistencia
                    # IMPORTANTE: El backend envía hora en UTC, debemos convertir a Perú
                    if fecha_asistencia:
                        # Combinar fecha + hora para parsear correctamente
                        datetime_str = f"{fecha_asistencia}T{hora_ingreso}"
                        dt = parse_datetime_from_api(datetime_str)
                        if dt:
                            hora_str = format_time_display(dt)
                            fecha_str = dt.strftime("%d/%m/%Y")
                    else:
                        # Solo tenemos hora sin fecha, parsear solo la hora
                        dt = parse_datetime_from_api(hora_ingreso)
                        if dt:
                            hora_str = format_time_display(dt)

            # Si aún no tenemos fecha pero tenemos fecha_asistencia
            if fecha_asistencia and fecha_str == "--/--/----":
                try:
                    dt = datetime.strptime(fecha_asistencia, "%Y-%m-%d")
                    fecha_str = dt.strftime("%d/%m/%Y")
                except:
                    fecha_str = fecha_asistencia

            # Obtener método de pago del cache (pre-cargado en load_estadisticas)
            cliente_id = asistencia.get('id_cliente')
            metodo_pago = metodos_pago_cache.get(cliente_id, "Sin registro")

            # Nombre del cliente
            nombre_cliente = asistencia.get('nombre_cliente', 'N/A')

            # Tipo de membresía
            tipo_membresia = asistencia.get('tipo_membresia', 'Sin plan')

            # Estado
            estado = asistencia.get('estado', 'Activo')

            fila = ft.Container(
                content=ft.Row([
                    # Hora
                    ft.Container(
                        ft.Text(
                            hora_str,
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.PRIMARY,
                            weight=Theme.FONT_WEIGHT["bold"]
                        ),
                        expand=1
                    ),
                    # Fecha
                    ft.Container(
                        ft.Text(
                            fecha_str,
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.TEXT_SECONDARY
                        ),
                        expand=1
                    ),
                    # Cliente
                    ft.Container(
                        ft.Text(
                            nombre_cliente,
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.TEXT_PRIMARY,
                            weight=Theme.FONT_WEIGHT["medium"]
                        ),
                        expand=2
                    ),
                    # Tipo de Membresía
                    ft.Container(
                        ft.Container(
                            content=ft.Text(
                                tipo_membresia,
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_PRIMARY,
                                weight=Theme.FONT_WEIGHT["medium"]
                            ),
                            bgcolor=f"{Theme.PRIMARY}15",
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=Theme.RADIUS["sm"]
                        ),
                        expand=2
                    ),
                    # Método de Pago
                    ft.Container(
                        ft.Text(
                            metodo_pago,
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.TEXT_SECONDARY
                        ),
                        expand=1
                    ),
                    # Estado
                    ft.Container(
                        create_status_badge(
                            estado,
                            status="success" if estado == "Activo" else "error"
                        ),
                        expand=1
                    ),
                ], spacing=Theme.SPACING["sm"]),
                padding=Theme.SPACING["md"],
                border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
            )
            tabla_container.controls.append(fila)

        # Actualizar texto de paginación
        pagination_text.value = f"Mostrando {start_idx + 1} a {end_idx} de {total_items} asistencias"
        page.update()

    def cambiar_pagina(direccion):
        """Cambiar de página en la paginación"""
        total_pages = max(1, (len(asistencias_filtradas) + items_per_page - 1) // items_per_page)

        if direccion == "prev" and current_page[0] > 0:
            current_page[0] -= 1
            rebuild_view()
        elif direccion == "next" and current_page[0] < total_pages - 1:
            current_page[0] += 1
            rebuild_view()

    def rebuild_view():
        """Reconstruir toda la vista (necesario para actualizar paginación)"""
        page.clean()
        content = build_content()
        create_base_layout(
            page=page,
            role="admin",
            current_section="Asistencia",
            on_section_click=on_section_click,
            content=content,
            user_info=user_info,
            on_logout=lambda _: on_section_click("logout")
        )

    # ==========================================
    # FUNCIONES DE REGISTRO
    # ==========================================
    def on_dni_change(e):
        """Validar DNI y auto-buscar"""
        value = dni_search.value
        if value and not value.isdigit():
            dni_search.value = ''.join(filter(str.isdigit, value))
            dni_search.update()
            return
        if value and len(value) == 8:
            buscar_cliente()

    dni_search.on_change = on_dni_change
    dni_search.on_submit = lambda e: buscar_cliente()

    def buscar_cliente():
        """Buscar cliente por DNI"""
        nonlocal asistencias_list, asistencias_filtradas

        dni = dni_search.value
        if not dni or len(dni) != 8:
            mostrar_error(page, "Ingrese un DNI válido (8 dígitos)")
            return

        try:
            print(f"DEBUG: Buscando cliente con DNI: {dni}")
            cliente = api.get_cliente_by_dni(dni)

            if not cliente:
                print(f"DEBUG: Cliente no encontrado con DNI: {dni}")
                mostrar_error(page, f"❌ No se encontró cliente con DNI {dni}")
                cliente_info_container.visible = False
                cliente_actual[0] = None
                page.update()
                return

            print(f"DEBUG: Cliente encontrado: {cliente.get('nombre')} {cliente.get('apellidos')}")
            cliente_actual[0] = cliente

            # IMPORTANTE: Recargar asistencias de hoy ANTES de verificar duplicados
            # Esto asegura que tengamos los datos más recientes
            print(f"DEBUG: Recargando asistencias del día para verificar duplicados...")
            asistencias_list = api.get_asistencias_hoy()
            asistencias_filtradas = asistencias_list.copy()
            stats_hoy["total_asistencias"] = len(asistencias_list)
            print(f"DEBUG: Asistencias recargadas: {len(asistencias_list)} registros")

            # Actualizar tabla con nuevos datos
            update_stats()
            update_tabla()

            # Verificar si ya tiene asistencia hoy
            # IMPORTANTE: No necesitamos verificar la fecha porque get_asistencias_hoy()
            # ya retorna solo las asistencias del día de hoy (considerando zona horaria)
            ya_registro_hoy = False
            hora_registro = None

            print(f"DEBUG: Verificando asistencia para cliente ID '{cliente['id']}' (tipo: {type(cliente['id'])})")
            print(f"DEBUG: Total asistencias de HOY en lista: {len(asistencias_list)}")

            # Debug: mostrar todas las asistencias para ver cuáles hay
            for idx, asist in enumerate(asistencias_list):
                print(f"DEBUG: Asistencia {idx}: cliente_id={asist.get('id_cliente')} (tipo: {type(asist.get('id_cliente'))}), nombre={asist.get('nombre_cliente')}, fecha={asist.get('fecha_asistencia')}, hora={asist.get('hora_ingreso')}")

            # Buscar si el cliente ya tiene asistencia en la lista de hoy
            for idx, asist in enumerate(asistencias_list):
                # Comparar IDs convirtiendo ambos a string para evitar problemas de tipo
                id_asist = str(asist.get('id_cliente', ''))
                id_cliente = str(cliente.get('id', ''))

                print(f"DEBUG: Comparando asistencia {idx}: '{id_asist}' == '{id_cliente}' ? {id_asist == id_cliente}")

                if id_asist == id_cliente and id_asist != '':
                    # Si está en la lista de "asistencias de hoy", entonces ya registró
                    ya_registro_hoy = True
                    print(f"DEBUG: ¡Cliente YA registró asistencia hoy! (asistencia #{idx})")

                    # Obtener hora de registro
                    hora_ingreso = asist.get('hora_ingreso')
                    if hora_ingreso:
                        if 'T' in str(hora_ingreso):
                            dt = parse_datetime_from_api(hora_ingreso)
                            if dt:
                                hora_registro = format_time_display(dt)
                        else:
                            # Es solo hora (HH:MM:SS.mmmmmm)
                            hora_registro = str(hora_ingreso)[:8]  # HH:MM:SS

                    print(f"DEBUG: Hora de registro: {hora_registro}")
                    break

            print(f"DEBUG: ya_registro_hoy = {ya_registro_hoy}")

            # Verificar membresía activa
            fecha_membresia = cliente.get('fecha_membresia')
            tiene_membresia_activa = False

            if fecha_membresia:
                try:
                    fecha_venc = parse_datetime_from_api(fecha_membresia)
                    if fecha_venc:
                        dias_restantes = (fecha_venc.date() - datetime.now().date()).days
                        tiene_membresia_activa = dias_restantes >= 0
                except:
                    pass

            estado_membresia = "Activo" if tiene_membresia_activa else "Inactivo"
            status_badge = create_status_badge(
                estado_membresia,
                status="success" if tiene_membresia_activa else "error",
                icon=ft.Icons.CHECK_CIRCLE if tiene_membresia_activa else ft.Icons.CANCEL
            )

            # Construir información
            cliente_info_content.controls.clear()
            info_controls = [
                ft.Row([
                    ft.Icon(ft.Icons.PERSON, size=40, color=Theme.PRIMARY),
                    ft.Column([
                        ft.Text(
                            f"{cliente['nombre']} {cliente['apellidos']}",
                            size=Theme.FONT_SIZE["xl"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=Theme.TEXT_PRIMARY
                        ),
                        ft.Text(
                            f"DNI: {cliente['dni']}",
                            size=Theme.FONT_SIZE["md"],
                            color=Theme.TEXT_SECONDARY
                        ),
                    ], spacing=2, expand=True),
                    status_badge
                ]),
            ]

            if ya_registro_hoy:
                # Usar zona horaria de Perú para mostrar la fecha
                from datetime import timezone, timedelta
                peru_tz = timezone(timedelta(hours=-5))
                fecha_hoy_formateada = datetime.now(peru_tz).strftime("%d/%m/%Y")

                mensaje_ya_registrado = f"✓ Asistencia ya registrada hoy ({fecha_hoy_formateada})"
                if hora_registro:
                    mensaje_ya_registrado += f" a las {hora_registro}"

                info_controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color=Theme.WARNING, size=24),
                                ft.Text(
                                    mensaje_ya_registrado,
                                    size=Theme.FONT_SIZE["sm"],
                                    color=Theme.WARNING,
                                    weight=Theme.FONT_WEIGHT["bold"]
                                )
                            ], spacing=8),
                            ft.Text(
                                "Este cliente ya no puede registrar otra asistencia hoy",
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_SECONDARY,
                                italic=True
                            )
                        ], spacing=4),
                        bgcolor=f"{Theme.WARNING}20",
                        padding=Theme.SPACING["md"],
                        border_radius=Theme.RADIUS["md"],
                        border=ft.border.all(1, Theme.WARNING)
                    )
                )

            info_controls.extend([
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Row([
                    create_primary_button(
                        "Registrar Asistencia",
                        lambda _: registrar_asistencia(),
                        icon=ft.Icons.CHECK,
                        disabled=(not tiene_membresia_activa or ya_registro_hoy)
                    ),
                    create_outlined_button(
                        "Cancelar",
                        lambda _: cancelar_busqueda(),
                        icon=ft.Icons.CLOSE
                    )
                ], spacing=Theme.SPACING["md"])
            ])

            cliente_info_content.controls.extend(info_controls)
            cliente_info_container.visible = True

            if not tiene_membresia_activa:
                mostrar_error(page, "⚠️ El cliente no tiene una membresía activa")
            elif ya_registro_hoy:
                # Usar zona horaria de Perú para mostrar la fecha
                from datetime import timezone, timedelta
                peru_tz = timezone(timedelta(hours=-5))
                fecha_hoy_formateada = datetime.now(peru_tz).strftime("%d/%m/%Y")

                if hora_registro:
                    mostrar_error(page, f"⚠️ El cliente ya registró asistencia hoy ({fecha_hoy_formateada}) a las {hora_registro}")
                else:
                    mostrar_error(page, f"⚠️ El cliente ya registró asistencia hoy ({fecha_hoy_formateada})")

            page.update()

        except Exception as e:
            mostrar_error(page, f"Error al buscar cliente: {str(e)}")

    def registrar_asistencia():
        """Registrar asistencia del cliente actual"""
        if not cliente_actual[0]:
            mostrar_error(page, "No hay cliente seleccionado")
            return

        try:
            print(f"DEBUG: Registrando asistencia para DNI: {cliente_actual[0]['dni']}")

            # Registrar asistencia
            resultado = api.registrar_asistencia(cliente_actual[0]['dni'])
            print(f"DEBUG: Resultado del registro: {resultado}")

            # Mostrar mensaje de éxito con más detalle
            nombre_completo = f"{cliente_actual[0]['nombre']} {cliente_actual[0]['apellidos']}"
            mostrar_exito(page, f"✓ Asistencia registrada para {nombre_completo}")

            # Limpiar formulario
            cancelar_busqueda()

            # Recargar datos para mostrar la nueva asistencia
            load_estadisticas()

            print("DEBUG: Asistencia registrada exitosamente")

        except ValueError as e:
            error_msg = str(e)
            print(f"DEBUG: Error ValueError: {error_msg}")

            # Mensajes más amigables para el usuario
            if "ya registró asistencia" in error_msg.lower():
                mostrar_error(page, "Este cliente ya registró su asistencia hoy")
            elif "no tiene membresía activa" in error_msg.lower():
                mostrar_error(page, "El cliente no tiene una membresía activa")
            else:
                mostrar_error(page, f"Error: {error_msg}")

        except Exception as e:
            print(f"DEBUG: Error Exception: {type(e).__name__}: {str(e)}")
            mostrar_error(page, f"Error al registrar asistencia: {str(e)}")

    def cancelar_busqueda():
        """Cancelar búsqueda actual"""
        dni_search.value = ""
        cliente_actual[0] = None
        cliente_info_container.visible = False
        page.update()

    # ==========================================
    # CONTENIDO
    # ==========================================
    def build_content():
        # Calcular paginación
        total_asistencias_filtradas = len(asistencias_filtradas)
        total_asistencias_hoy = len(asistencias_list)  # Total real del día
        total_pages = max(1, (total_asistencias_filtradas + items_per_page - 1) // items_per_page)
        current_page_display = current_page[0] + 1

        if current_page[0] >= total_pages and total_pages > 0:
            current_page[0] = total_pages - 1

        # Stats
        stats_row = ft.Row([
            ft.Container(ref=stat_total_hoy, expand=True),
            ft.Container(ref=stat_promedio_mes, expand=True),
        ], spacing=Theme.SPACING["xl"])

        # Área de búsqueda para registro
        search_area = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SEARCH, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Registrar Asistencia", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ], spacing=Theme.SPACING["md"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Row([
                    dni_search,
                    create_primary_button("Buscar", lambda _: buscar_cliente(), icon=ft.Icons.SEARCH),
                ], spacing=Theme.SPACING["md"], alignment=ft.MainAxisAlignment.START),
                cliente_info_container,
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        # Tabla de asistencias
        tabla_area = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIST, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Asistencias de Hoy", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.FITNESS_CENTER, size=16, color=Theme.PRIMARY),
                            ft.Text(
                                f"{total_asistencias_hoy} registros",
                                size=Theme.FONT_SIZE["sm"],
                                color=Theme.TEXT_SECONDARY,
                                weight=Theme.FONT_WEIGHT["medium"],
                                ref=contador_registros
                            ),
                        ], spacing=4),
                        bgcolor=f"{Theme.PRIMARY}15",
                        padding=8,
                        border_radius=Theme.RADIUS["sm"]
                    ),
                ], spacing=Theme.SPACING["md"]),
                ft.Container(
                    content=search_field,
                    padding=ft.padding.only(bottom=Theme.SPACING["md"])
                ),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                tabla_container,
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=pagination_text,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS,
                                    icon_size=16,
                                    icon_color=Theme.PRIMARY if current_page[0] > 0 else Theme.TEXT_SECONDARY,
                                    tooltip="Página anterior",
                                    on_click=lambda _: cambiar_pagina("prev"),
                                    disabled=current_page[0] == 0
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"Página {current_page_display} de {total_pages}",
                                        size=Theme.FONT_SIZE["sm"],
                                        color=Theme.TEXT_PRIMARY,
                                        weight=Theme.FONT_WEIGHT["medium"]
                                    ),
                                    bgcolor=f"{Theme.PRIMARY}15",
                                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                    border_radius=Theme.RADIUS["sm"]
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_FORWARD_IOS,
                                    icon_size=16,
                                    icon_color=Theme.PRIMARY if current_page[0] < total_pages - 1 else Theme.TEXT_SECONDARY,
                                    tooltip="Página siguiente",
                                    on_click=lambda _: cambiar_pagina("next"),
                                    disabled=current_page[0] >= total_pages - 1
                                ),
                            ], spacing=8),
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.symmetric(vertical=8)
                ),
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        return ft.Column([
            stats_row,
            ft.Container(height=Theme.SPACING["xl"]),
            search_area,
            ft.Container(height=Theme.SPACING["xl"]),
            tabla_area,
        ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

    # ==========================================
    # CREAR LAYOUT
    # ==========================================
    content = build_content()

    create_base_layout(
        page=page,
        role="admin",
        current_section="Asistencia",
        on_section_click=on_section_click,
        content=content,
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )

    # Cargar datos iniciales
    load_estadisticas()
