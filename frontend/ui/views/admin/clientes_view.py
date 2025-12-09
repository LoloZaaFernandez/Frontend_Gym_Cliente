"""
Vista de Gestión de Clientes (CRUD completo) - Refactorizado con Sistema de Componentes
Incluye: Búsqueda por DNI, Tabla completa, Paginación
"""

import flet as ft
import re
import unicodedata
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button, create_status_badge, create_icon_button
from ui.components.molecules import create_card_container, create_confirmation_dialog, create_empty_state
from ui.utils.messages import mostrar_exito, mostrar_error
from ui.utils.datetime_utils import parse_datetime_from_api, format_datetime_display, format_date_display, get_now_local
from datetime import datetime


def show_clientes_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Mostrar vista de gestión de clientes con CRUD completo, búsqueda y tabla
    """
    page.title = "BLESSED GYM - Gestión de Clientes"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Estado de la vista
    clientes_list = []
    clientes_filtrados = []
    selected_cliente = None
    edit_mode = [False]

    # Caché para datos extendidos (evitar múltiples llamadas API)
    cache_membresia_info = {}
    cache_ultimo_checkin = {}

    # Paginación
    items_per_page = 10
    current_page = [0]

    # ==========================================
    # VALIDACIONES
    # ==========================================
    def validar_solo_numeros(e):
        if e.control.value:
            e.control.value = ''.join(filter(str.isdigit, e.control.value))
            e.control.update()

    def validar_solo_letras(e):
        if e.control.value:
            e.control.value = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', e.control.value)
            e.control.update()

    def validar_telefono(e):
        if e.control.value:
            # Solo permitir números y limitar a 9 dígitos
            e.control.value = ''.join(filter(str.isdigit, e.control.value))[:9]
            e.control.update()

    def validar_email(email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    # ==========================================
    # CAMPOS DEL FORMULARIO
    # ==========================================
    dni_field = ft.TextField(
        label="DNI *",
        hint_text="8 dígitos",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        max_length=8,
        counter_text="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=validar_solo_numeros,
        prefix_icon=ft.Icons.BADGE
    )

    nombre_field = ft.TextField(
        label="Nombre *",
        hint_text="Solo letras",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        on_change=validar_solo_letras,
        prefix_icon=ft.Icons.PERSON
    )

    apellidos_field = ft.TextField(
        label="Apellidos *",
        hint_text="Solo letras",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        on_change=validar_solo_letras,
        prefix_icon=ft.Icons.PERSON_OUTLINE
    )

    correo_field = ft.TextField(
        label="Correo *",
        hint_text="ejemplo@correo.com",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL
    )

    telefono_field = ft.TextField(
        label="Teléfono",
        hint_text="9 dígitos",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=9,
        counter_text="",
        on_change=validar_telefono,
        prefix_icon=ft.Icons.PHONE
    )

    estado_dropdown = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("Activo"),
            ft.dropdown.Option("Inactivo"),
        ],
        value="Activo",
        color=Theme.TEXT_PRIMARY,
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        visible=False
    )

    # Campos para nuevo registro con membresía
    membresia_dropdown = ft.Dropdown(
        label="Membresía *",
        hint_text="Selecciona una membresía",
        options=[],  # Se llenará dinámicamente
        color=Theme.TEXT_PRIMARY,
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        visible=True
    )

    metodo_pago_dropdown = ft.Dropdown(
        label="Método de Pago *",
        hint_text="Selecciona método de pago",
        options=[
            ft.dropdown.Option("Efectivo"),
            ft.dropdown.Option("Yape"),
           
        ],
        value="Efectivo",
        color=Theme.TEXT_PRIMARY,
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        visible=True
    )

    # Campo de búsqueda
    search_field = ft.TextField(
        hint_text="Buscar por DNI, nombre, apellidos o correo...",
        border_color=Theme.BORDER_DEFAULT,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.CARD_BG,
        color=Theme.TEXT_PRIMARY,
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=lambda e: filtrar_clientes(e.control.value),
        on_submit=lambda e: filtrar_clientes(e.control.value)  # Manejar Enter sin congelar
    )

    # Contenedor de la tabla
    tabla_container = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    # Texto de paginación
    pagination_text = ft.Text("", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY)

    # ==========================================
    # FUNCIONES DE DATOS EXTENDIDOS
    # ==========================================
    def get_cliente_membresia_info(cliente_id):
        """Obtener información de membresía del cliente con caché"""
        # Verificar si ya está en caché
        if cliente_id in cache_membresia_info:
            return cache_membresia_info[cliente_id]

        try:
            # Obtener información del cliente
            cliente_info = api.get_cliente_por_id(cliente_id)
            fecha_membresia = cliente_info.get('fecha_membresia')

            # Obtener el nombre del plan desde los pagos
            plan_nombre = "Sin membresía"
            try:
                pagos_membresia = api.get_pagos_membresia_cliente(cliente_id)
                if pagos_membresia and len(pagos_membresia) > 0:
                    # Ordenar por fecha de pago (más reciente primero)
                    pagos_ordenados = sorted(
                        pagos_membresia,
                        key=lambda x: x.get('fecha_pago', ''),
                        reverse=True
                    )
                    pago_reciente = pagos_ordenados[0]

                    # Buscar el nombre del plan en múltiples claves posibles
                    plan_nombre = (
                        pago_reciente.get('nombre_membresia') or
                        pago_reciente.get('membresia_nombre') or
                        pago_reciente.get('plan_nombre') or
                        pago_reciente.get('tipo_membresia') or
                        "Sin membresía"
                    )

                    # Si no se encontró, intentar desde el ID de la membresía
                    if plan_nombre == "Sin membresía":
                        membresia_id = pago_reciente.get('id_membresia') or pago_reciente.get('membresia_id')
                        if membresia_id:
                            todas_membresias = api.get_membresias()
                            for memb in todas_membresias:
                                if memb.get('id') == membresia_id:
                                    plan_nombre = memb.get('nombre_membresia', 'Sin membresía')
                                    break
            except Exception as e:
                print(f"Error obteniendo pagos de membresía para cliente {cliente_id}: {e}")

            # Calcular estatus basado en la fecha de vencimiento
            if fecha_membresia:
                try:
                    fecha_venc = parse_datetime_from_api(fecha_membresia)
                    if not fecha_venc:
                        raise ValueError("No se pudo parsear la fecha")
                    fecha_venc_solo_fecha = fecha_venc.date()
                    fecha_actual_solo_fecha = get_now_local().date()
                    dias_restantes = (fecha_venc_solo_fecha - fecha_actual_solo_fecha).days

                    if dias_restantes > 7:
                        estatus = "Activo"
                        estatus_tipo = "success"
                    elif dias_restantes > 0:
                        estatus = "Por vencer"
                        estatus_tipo = "warning"
                    elif dias_restantes == 0:
                        estatus = "Vence hoy"
                        estatus_tipo = "warning"
                    else:
                        estatus = "Inactivo"
                        estatus_tipo = "error"

                    resultado = {
                        'plan': plan_nombre,
                        'estatus': estatus,
                        'estatus_tipo': estatus_tipo,
                        'fecha_vencimiento': fecha_membresia,
                        'dias_restantes': dias_restantes
                    }
                    # Guardar en caché
                    cache_membresia_info[cliente_id] = resultado
                    return resultado
                except Exception as e:
                    print(f"Error procesando fecha de membresía: {e}")

            # Sin membresía
            resultado = {
                'plan': 'Sin membresía',
                'estatus': 'Inactivo',
                'estatus_tipo': 'error',
                'fecha_vencimiento': None,
                'dias_restantes': None
            }
            # Guardar en caché
            cache_membresia_info[cliente_id] = resultado
            return resultado

        except Exception as e:
            print(f"Error obteniendo membresía del cliente {cliente_id}: {e}")
            resultado = {
                'plan': 'Sin membresía',
                'estatus': 'Inactivo',
                'estatus_tipo': 'error',
                'fecha_vencimiento': None,
                'dias_restantes': None
            }
            # Guardar en caché
            cache_membresia_info[cliente_id] = resultado
            return resultado

    def get_ultimo_checkin(cliente_id):
        """Obtener último check-in del cliente con conversión correcta de timezone y caché"""
        # Verificar si ya está en caché
        if cliente_id in cache_ultimo_checkin:
            return cache_ultimo_checkin[cliente_id]

        resultado = "Sin registro"  # Valor por defecto

        try:
            asistencias = api.get_asistencias_cliente(cliente_id)

            if not asistencias or len(asistencias) == 0:
                cache_ultimo_checkin[cliente_id] = resultado
                return resultado

            # Ordenar por fecha_asistencia (campo que realmente existe en la API)
            asistencias_ordenadas = sorted(
                asistencias,
                key=lambda x: x.get('fecha_asistencia', ''),
                reverse=True
            )

            ultima = asistencias_ordenadas[0]

            # El API devuelve fecha_asistencia y hora_ingreso por separado
            fecha_asistencia = ultima.get('fecha_asistencia', '')
            hora_ingreso = ultima.get('hora_ingreso', '')

            if fecha_asistencia and hora_ingreso:
                try:
                    # Limpiar la hora si tiene microsegundos
                    hora_limpia = str(hora_ingreso).split('.')[0] if '.' in str(hora_ingreso) else str(hora_ingreso)

                    # Si la hora ya tiene formato ISO completo, usarla directamente
                    if 'T' in str(hora_ingreso):
                        datetime_str = hora_ingreso
                    else:
                        # Combinar fecha + hora en formato ISO
                        datetime_str = f"{fecha_asistencia}T{hora_limpia}"

                    # Parsear con conversión de UTC a hora local
                    dt = parse_datetime_from_api(datetime_str)
                    if dt:
                        resultado = format_datetime_display(dt)
                        cache_ultimo_checkin[cliente_id] = resultado
                        return resultado
                except Exception as e:
                    print(f"Error parseando último check-in: {e}")

            # Si solo tenemos fecha_asistencia
            if fecha_asistencia:
                try:
                    dt = parse_datetime_from_api(fecha_asistencia)
                    if dt:
                        resultado = dt.strftime('%d/%m/%Y')
                        cache_ultimo_checkin[cliente_id] = resultado
                        return resultado
                except:
                    pass
                resultado = fecha_asistencia
                cache_ultimo_checkin[cliente_id] = resultado
                return resultado

            cache_ultimo_checkin[cliente_id] = resultado
            return resultado

        except Exception as e:
            print(f"Error obteniendo asistencias del cliente {cliente_id}: {e}")
            import traceback
            traceback.print_exc()
            cache_ultimo_checkin[cliente_id] = resultado
            return resultado

    # ==========================================
    # FUNCIONES CRUD
    # ==========================================
    def load_membresias():
        """Cargar membresías disponibles en el dropdown"""
        try:
            membresias = api.get_membresias(estado="Activa")
            membresia_dropdown.options = [
                ft.dropdown.Option(
                    key=str(m['id']),
                    text=f"{m['nombre_membresia']} - {m['tipo_membresia']}"
                )
                for m in membresias
            ]
            if membresias:
                membresia_dropdown.value = str(membresias[0]['id'])
        except Exception as e:
            print(f"Error al cargar membresías: {e}")
            membresia_dropdown.options = []

    def normalizar_texto(texto):
        """
        Normaliza texto removiendo tildes y convirtiéndolo a minúsculas.
        Ejemplo: 'José' -> 'jose', 'María' -> 'maria'
        """
        if not texto:
            return ""
        # Convertir a minúsculas
        texto = texto.lower()
        # Normalizar caracteres Unicode (NFD descompone caracteres con tildes)
        texto_nfd = unicodedata.normalize('NFD', texto)
        # Filtrar los caracteres de marca (tildes, diéresis, etc.)
        texto_sin_tildes = ''.join(char for char in texto_nfd if unicodedata.category(char) != 'Mn')
        return texto_sin_tildes

    def load_clientes():
        nonlocal clientes_list, clientes_filtrados
        try:
            clientes_list = api.get_clientes()
            # Ordenar por ID descendente para mostrar los más recientes primero
            clientes_list.sort(key=lambda x: x.get('id', 0), reverse=True)
            clientes_filtrados = clientes_list.copy()
            current_page[0] = 0

            # Limpiar caché al recargar clientes para obtener datos actualizados
            cache_membresia_info.clear()
            cache_ultimo_checkin.clear()
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            clientes_list = []
            clientes_filtrados = []

        update_tabla()

    def filtrar_clientes(search_term):
        """
        Filtra clientes por DNI, nombre, apellidos o correo.
        La búsqueda es insensible a mayúsculas/minúsculas y tildes.
        """
        nonlocal clientes_filtrados
        search_term = search_term.strip()

        if not search_term:
            clientes_filtrados = clientes_list.copy()
        else:
            # Normalizar el término de búsqueda (quitar tildes y convertir a minúsculas)
            search_normalizado = normalizar_texto(search_term)

            clientes_filtrados = [
                c for c in clientes_list
                if (
                    # Búsqueda por DNI (sin normalización, solo números)
                    search_term in c.get('dni', '') or
                    # Búsqueda por nombre (con normalización)
                    search_normalizado in normalizar_texto(c.get('nombre', '')) or
                    # Búsqueda por apellidos (con normalización)
                    search_normalizado in normalizar_texto(c.get('apellidos', '')) or
                    # Búsqueda por correo (con normalización)
                    search_normalizado in normalizar_texto(c.get('correo', ''))
                )
            ]
            # Mantener el ordenamiento por ID descendente después del filtrado
            clientes_filtrados.sort(key=lambda x: x.get('id', 0), reverse=True)

        current_page[0] = 0
        update_tabla()

    def update_tabla():
        """Actualizar la tabla con paginación"""
        tabla_container.controls.clear()

        if not clientes_filtrados:
            tabla_container.controls.append(
                create_empty_state(
                    message="No hay clientes para mostrar",
                    icon=ft.Icons.PEOPLE_OUTLINE,
                    secondary_message="Intenta ajustar los filtros de búsqueda"
                )
            )
            pagination_text.value = "Mostrando 0 de 0 clientes"
            # Actualizar solo si los controles están en la página
            try:
                if tabla_container.page is not None:
                    tabla_container.update()
                if pagination_text.page is not None:
                    pagination_text.update()
            except Exception as e:
                # Si falla, intentar actualizar la página completa
                try:
                    page.update()
                except:
                    pass
            return

        # Calcular paginación
        total_items = len(clientes_filtrados)
        start_idx = current_page[0] * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        clientes_pagina = clientes_filtrados[start_idx:end_idx]

        # Encabezado de tabla
        header = ft.Container(
            content=ft.Row([
                ft.Container(ft.Text("Miembro", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=2),
                ft.Container(ft.Text("ID", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("DNI", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Teléfono", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Estatus", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Plan", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Vencimiento", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
                ft.Container(ft.Text("Último Check-in", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=2),
                ft.Container(ft.Text("Acciones", size=Theme.FONT_SIZE["sm"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY), expand=1),
            ], spacing=Theme.SPACING["sm"]),
            bgcolor=f"{Theme.PRIMARY}22",
            padding=Theme.SPACING["md"],
            border_radius=Theme.RADIUS["sm"]
        )
        tabla_container.controls.append(header)

        # Filas de datos
        for cliente in clientes_pagina:
            # Obtener información extendida
            membresia_info = get_cliente_membresia_info(cliente['id'])
            ultimo_checkin = get_ultimo_checkin(cliente['id'])

            # Formatear fecha de vencimiento con mejor presentación
            fecha_venc_str = "Sin membresía"
            fecha_venc_color = Theme.TEXT_SECONDARY
            if membresia_info['fecha_vencimiento']:
                dt = parse_datetime_from_api(membresia_info['fecha_vencimiento'])
                if dt:
                    fecha_venc_str = format_date_display(dt)

                    # Cambiar color según días restantes
                    dias_restantes = membresia_info.get('dias_restantes')
                    if dias_restantes is not None:
                        if dias_restantes > 7:
                            fecha_venc_color = Theme.SUCCESS
                        elif dias_restantes > 0:
                            fecha_venc_color = Theme.WARNING
                        else:
                            fecha_venc_color = Theme.ERROR
                else:
                    fecha_venc_str = "Fecha inválida"

            fila = ft.Container(
                content=ft.Row([
                    # Miembro
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                f"{cliente['nombre']} {cliente['apellidos']}",
                                size=Theme.FONT_SIZE["sm"],
                                weight=Theme.FONT_WEIGHT["semibold"],
                                color=Theme.TEXT_PRIMARY
                            ),
                            ft.Text(
                                cliente['correo'],
                                size=Theme.FONT_SIZE["xs"],
                                color=Theme.TEXT_SECONDARY
                            ),
                        ], spacing=2),
                        expand=2
                    ),
                    # ID
                    ft.Container(
                        ft.Text(str(cliente['id']), size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        expand=1
                    ),
                    # DNI
                    ft.Container(
                        ft.Text(cliente['dni'], size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_PRIMARY),
                        expand=1
                    ),
                    # Teléfono
                    ft.Container(
                        ft.Text(cliente.get('telefono') or 'Sin teléfono', size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        expand=1
                    ),
                    # Estatus Membresía
                    ft.Container(
                        create_status_badge(
                            membresia_info['estatus'],
                            status=membresia_info['estatus_tipo']
                        ),
                        expand=1
                    ),
                    # Plan
                    ft.Container(
                        ft.Text(
                            membresia_info['plan'],
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.TEXT_PRIMARY,
                            weight=Theme.FONT_WEIGHT["medium"]
                        ),
                        expand=1
                    ),
                    # Fecha Vencimiento
                    ft.Container(
                        ft.Text(
                            fecha_venc_str,
                            size=Theme.FONT_SIZE["sm"],
                            color=fecha_venc_color,
                            weight=Theme.FONT_WEIGHT["medium"]
                        ),
                        expand=1
                    ),
                    # Último Check-in
                    ft.Container(
                        ft.Text(
                            ultimo_checkin,
                            size=Theme.FONT_SIZE["sm"],
                            color=Theme.TEXT_SECONDARY
                        ),
                        expand=2
                    ),
                    # Acciones
                    ft.Container(
                        content=ft.Row([
                            create_icon_button(
                                ft.Icons.EDIT,
                                lambda _, c=cliente: edit_cliente(c),
                                tooltip="Editar cliente",
                                color=Theme.PRIMARY
                            ),
                            create_icon_button(
                                ft.Icons.DELETE,
                                lambda _, dni=cliente['dni']: confirm_delete_cliente_by_dni(dni),
                                tooltip="Eliminar cliente",
                                color=Theme.ERROR
                            ),
                        ], spacing=4),
                        expand=1
                    ),
                ], spacing=Theme.SPACING["sm"]),
                padding=Theme.SPACING["md"],
                border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
            )
            tabla_container.controls.append(fila)

        # Actualizar texto de paginación
        pagination_text.value = f"Mostrando {start_idx + 1} a {end_idx} de {total_items} clientes"

        # Actualizar solo si los controles están en la página
        try:
            if tabla_container.page is not None:
                tabla_container.update()
            if pagination_text.page is not None:
                pagination_text.update()
        except Exception as e:
            # Si falla, intentar actualizar la página completa
            try:
                page.update()
            except:
                pass

    def clear_form():
        nonlocal selected_cliente
        selected_cliente = None
        edit_mode[0] = False
        dni_field.value = ""
        nombre_field.value = ""
        apellidos_field.value = ""
        correo_field.value = ""
        telefono_field.value = ""
        dni_field.disabled = False
        dni_field.error_text = None
        nombre_field.error_text = None
        apellidos_field.error_text = None
        correo_field.error_text = None
        telefono_field.error_text = None
        membresia_dropdown.error_text = None
        metodo_pago_dropdown.error_text = None
        estado_dropdown.visible = False
        membresia_dropdown.visible = True
        metodo_pago_dropdown.visible = True
        update_view()

    def save_cliente(e):
        # Limpiar errores
        dni_field.error_text = None
        nombre_field.error_text = None
        apellidos_field.error_text = None
        correo_field.error_text = None
        telefono_field.error_text = None
        membresia_dropdown.error_text = None
        metodo_pago_dropdown.error_text = None

        # Validar campos básicos
        errores = []
        if not dni_field.value or len(dni_field.value) != 8:
            dni_field.error_text = "DNI inválido (8 dígitos)"
            errores.append("DNI")
        if not nombre_field.value:
            nombre_field.error_text = "Campo obligatorio"
            errores.append("Nombre")
        if not apellidos_field.value:
            apellidos_field.error_text = "Campo obligatorio"
            errores.append("Apellidos")
        if not correo_field.value or not validar_email(correo_field.value):
            correo_field.error_text = "Correo inválido"
            errores.append("Correo")
        if telefono_field.value and len(telefono_field.value) != 9:
            telefono_field.error_text = "Teléfono debe tener 9 dígitos"
            errores.append("Teléfono")

        # Validar campos de membresía solo para nuevo cliente
        if not selected_cliente:
            if not membresia_dropdown.value:
                membresia_dropdown.error_text = "Seleccione una membresía"
                errores.append("Membresía")
            if not metodo_pago_dropdown.value:
                metodo_pago_dropdown.error_text = "Seleccione método de pago"
                errores.append("Método de pago")

        if errores:
            mostrar_error(page, f"Complete correctamente: {', '.join(errores)}")
            page.update()
            return

        # Modo EDICIÓN
        if selected_cliente:
            cliente_data = {
                "dni": dni_field.value,
                "nombre": nombre_field.value,
                "apellidos": apellidos_field.value,
                "correo": correo_field.value,
                "telefono": telefono_field.value or None,
                "estado": estado_dropdown.value
            }
            try:
                cliente_encontrado = next((c for c in clientes_list if c['dni'] == selected_cliente['dni']), None)
                if cliente_encontrado:
                    api.update_cliente(cliente_encontrado['id'], cliente_data)
                    mostrar_exito(page, "Cliente actualizado correctamente")
                    clear_form()
                    load_clientes()
                else:
                    mostrar_error(page, "Cliente no encontrado")
            except Exception as e:
                mostrar_error(page, f"Error: {str(e)}")
            return

        # Modo NUEVO CLIENTE - Flujo con validación y modal
        def confirmar_y_registrar(e):
            """Función que se ejecuta cuando el usuario confirma en el modal"""
            try:
                # Preparar datos para el registro completo
                registro_data = {
                    "dni": dni_field.value,
                    "nombre": nombre_field.value,
                    "apellidos": apellidos_field.value,
                    "correo": correo_field.value,
                    "telefono": telefono_field.value or None,
                    "id_membresia": int(membresia_dropdown.value),
                    "metodo_pago": metodo_pago_dropdown.value,
                    "usuario_creacion": current_user.get("nombre", "admin")
                }

                # Registrar cliente completo con membresía
                resultado = api.registrar_cliente_completo(registro_data)
                mostrar_exito(page, resultado.get('mensaje', 'Cliente registrado correctamente'))
                clear_form()
                load_clientes()

            except Exception as error:
                mostrar_error(page, f"Error al registrar: {str(error)}")

        # Paso 1: Validar datos con el backend
        try:
            validacion_data = {
                "confirmar_registro": "preparar",
                "dni": dni_field.value,
                "nombre": nombre_field.value,
                "apellidos": apellidos_field.value,
                "correo": correo_field.value,
                "telefono": telefono_field.value or None,
                "id_membresia": int(membresia_dropdown.value),
                "metodo_pago": metodo_pago_dropdown.value
            }

            validacion = api.validar_cliente_registro(validacion_data)

            # Paso 2: Si la validación es exitosa, mostrar modal
            if validacion.get('validacion_exitosa'):
                from ui.components.molecules.dialogs import create_payment_confirmation_dialog

                dialog = create_payment_confirmation_dialog(
                    page=page,
                    resumen=validacion['resumen'],
                    mensaje=validacion['mensaje'],
                    on_confirm=confirmar_y_registrar,
                    on_cancel=lambda _: mostrar_error(page, "Vuelva a intentarlo")
                )
                page.open(dialog)
            else:
                mostrar_error(page, validacion.get('mensaje', 'Error en la validación'))

        except Exception as e:
            mostrar_error(page, f"Error en validación: {str(e)}")

    def edit_cliente(cliente):
        nonlocal selected_cliente
        selected_cliente = cliente
        edit_mode[0] = True
        dni_field.value = cliente['dni']
        nombre_field.value = cliente['nombre']
        apellidos_field.value = cliente['apellidos']
        correo_field.value = cliente['correo']
        telefono_field.value = cliente.get('telefono', '')
        estado_dropdown.value = cliente.get('estado', 'Activo')
        dni_field.disabled = True
        estado_dropdown.visible = True
        # Ocultar campos de membresía en modo edición
        membresia_dropdown.visible = False
        metodo_pago_dropdown.visible = False
        update_view()

    def confirm_delete_cliente_by_dni(dni):
        """Confirmar eliminación de cliente por DNI"""
        cliente = next((c for c in clientes_list if c['dni'] == dni), None)
        if not cliente:
            mostrar_error(page, "Cliente no encontrado")
            return

        dialog = create_confirmation_dialog(
            page,
            title="Eliminar Cliente",
            message=f"¿Estás seguro de eliminar a {cliente['nombre']} {cliente['apellidos']}?",
            on_confirm=lambda _: delete_cliente_by_dni(dni),
            warning_message="Esta acción no se puede deshacer",
            is_danger=True
        )
        page.open(dialog)

    def delete_cliente_by_dni(dni):
        """Eliminar cliente por DNI"""
        try:
            cliente = next((c for c in clientes_list if c['dni'] == dni), None)
            if cliente:
                api.delete_cliente(cliente['id'])
                mostrar_exito(page, "Cliente eliminado correctamente")
                load_clientes()
            else:
                mostrar_error(page, "Cliente no encontrado")
        except Exception as e:
            mostrar_error(page, f"Error al eliminar: {str(e)}")

    def cambiar_pagina(direccion):
        """Cambiar de página en la paginación"""
        total_pages = max(1, (len(clientes_filtrados) + items_per_page - 1) // items_per_page)

        if direccion == "prev" and current_page[0] > 0:
            current_page[0] -= 1
            update_tabla()
            # Reconstruir toda la vista para actualizar correctamente los botones de paginación
            update_view()
        elif direccion == "next" and current_page[0] < total_pages - 1:
            current_page[0] += 1
            update_tabla()
            # Reconstruir toda la vista para actualizar correctamente los botones de paginación
            update_view()

    # ==========================================
    # CONTENIDO COMPLETO
    # ==========================================
    def update_view():
        """Actualizar la vista completa"""
        page.clean()

        # Formulario
        form_fields_list = [dni_field, nombre_field, apellidos_field, correo_field, telefono_field]
        if estado_dropdown.visible:
            form_fields_list.append(estado_dropdown)
        if membresia_dropdown.visible:
            form_fields_list.append(membresia_dropdown)
        if metodo_pago_dropdown.visible:
            form_fields_list.append(metodo_pago_dropdown)

        form_title = "Editar Cliente" if edit_mode[0] else "Nuevo Cliente con Membresía"

        form_buttons = [create_outlined_button("Cancelar", lambda _: clear_form(), icon=ft.Icons.CLOSE)]
        if edit_mode[0]:
            form_buttons.append(create_primary_button("Actualizar", save_cliente, icon=ft.Icons.SAVE))
        else:
            form_buttons.append(create_primary_button("Crear", save_cliente, icon=ft.Icons.ADD))

        form_area = create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EDIT if edit_mode[0] else ft.Icons.ADD_CIRCLE,
                           size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text(form_title, size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ], spacing=Theme.SPACING["md"]),
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.ResponsiveRow(
                    [ft.Container(field, col={"sm": 12, "md": 6, "lg": 4}) for field in form_fields_list],
                    spacing=Theme.SPACING["md"]
                ),
                ft.Row(form_buttons, spacing=Theme.SPACING["md"], alignment=ft.MainAxisAlignment.END),
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        )

        # Área de búsqueda y tabla
        # Calcular paginación dinámicamente
        total_clientes = len(clientes_filtrados)
        total_pages = max(1, (total_clientes + items_per_page - 1) // items_per_page)
        current_page_display = current_page[0] + 1

        # Asegurar que current_page no exceda el total de páginas
        if current_page[0] >= total_pages and total_pages > 0:
            current_page[0] = total_pages - 1

        list_area = create_card_container(
            content=ft.Column([
                # Header con búsqueda
                ft.Row([
                    ft.Icon(ft.Icons.LIST, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text("Lista de Clientes", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ft.Container(expand=True),
                    # Mostrar total de clientes
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PEOPLE, size=16, color=Theme.PRIMARY),
                            ft.Text(
                                f"{total_clientes} clientes",
                                size=Theme.FONT_SIZE["sm"],
                                color=Theme.TEXT_SECONDARY,
                                weight=Theme.FONT_WEIGHT["medium"]
                            ),
                        ], spacing=4),
                        bgcolor=f"{Theme.PRIMARY}15",
                        padding=8,
                        border_radius=Theme.RADIUS["sm"]
                    ),
                ], spacing=Theme.SPACING["md"]),

                # Campo de búsqueda
                ft.Container(
                    content=search_field,
                    padding=ft.padding.only(bottom=Theme.SPACING["md"])
                ),

                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),

                # Tabla
                tabla_container,

                # Footer con paginación mejorada
                ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
                ft.Container(
                    content=ft.Row([
                        # Texto de resumen
                        ft.Container(
                            content=pagination_text,
                            expand=True
                        ),
                        # Controles de paginación
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

        # Layout completo
        content = ft.Column([
            form_area,
            ft.Container(height=Theme.SPACING["2xl"]),
            list_area,
        ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

        create_base_layout(
            page=page,
            role="admin",
            current_section="Clientes",
            on_section_click=on_section_click,
            content=content,
            user_info=user_info,
            on_logout=lambda _: on_section_click("logout")
        )

    # Inicializar
    load_membresias()
    load_clientes()
    update_view()
