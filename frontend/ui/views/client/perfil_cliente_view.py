"""
Vista de Perfil de Cliente - Refactorizado con Sistema de Componentes
ANTES: 255 líneas | DESPUÉS: ~180 líneas (29% menos código)
"""

import flet as ft
from datetime import datetime, timedelta
from config.theme import Theme
from config.settings import LOGO_PATH
from ui.layouts import create_base_layout
from ui.components.molecules import create_card_container
from services.api_service import APIService
from ui.utils.datetime_utils import parse_datetime_from_api, get_now_local


def show_perfil_cliente_view(page: ft.Page, auth_service, on_section_click, current_section, on_navigate_membresias=None):
    """
    Mostrar vista de perfil del cliente

    Mejoras:
    - 29% menos código (255 → ~180 líneas)
    - Uso de base_layout
    - Theme centralizado
    - Componentes reutilizables

    Args:
        on_navigate_membresias: Callback para ir a membresías
    """
    page.title = "BLESSED GYM - Mi Perfil"
    page.padding = 0
    page.spacing = 0

    cliente = auth_service.get_current_user()
    user_info = {"nombre": cliente.get("nombre", "Cliente"), "rol": "Cliente"}
    api = APIService()

    # Obtener datos reales del cliente desde la API
    def obtener_datos_cliente():
        """Obtener todos los datos del cliente desde la API"""
        try:
            cliente_id = cliente.get('id')

            # IMPORTANTE: Obtener datos actualizados del cliente desde la API
            # Esto asegura que tengamos la información más reciente de la membresía
            cliente_actualizado = api.get_cliente_por_id(cliente_id)
            if not cliente_actualizado:
                cliente_actualizado = cliente  # Fallback al cliente del auth

            # DEBUG: Mostrar TODOS los campos del cliente para ver qué está disponible
            print(f"\n{'='*60}")
            print(f"DEBUG PERFIL - CLIENTE ACTUALIZADO (ID: {cliente_id}):")
            print(f"{'='*60}")
            for key, value in cliente_actualizado.items():
                print(f"  {key}: {value}")
            print(f"{'='*60}\n")

            # Obtener estadísticas de asistencias
            stats_asistencias = api.get_estadisticas_cliente(cliente_id)

            # Obtener asistencias para calcular racha
            asistencias = api.get_asistencias_cliente(cliente_id)
            racha_dias = calcular_racha_dias(asistencias)

            # Obtener información de membresía desde pagos (método más confiable)
            pagos_membresia = api.get_pagos_membresia_cliente(cliente_id)
            membresia_info = obtener_info_membresia_desde_pagos(pagos_membresia, cliente_actualizado)

            # Formatear fecha de registro
            fecha_registro = cliente.get('fecha_registro', '')
            if fecha_registro:
                try:
                    fecha_obj = datetime.fromisoformat(fecha_registro.replace('Z', '+00:00'))
                    fecha_registro_formateada = fecha_obj.strftime('%d/%m/%Y')
                except:
                    fecha_registro_formateada = "No disponible"
            else:
                fecha_registro_formateada = "No disponible"

            # Formatear última asistencia
            ultima_asistencia = stats_asistencias.get('ultima_asistencia', '')
            if ultima_asistencia:
                try:
                    fecha_obj = datetime.fromisoformat(ultima_asistencia.replace('Z', '+00:00'))
                    ultima_asistencia_formateada = fecha_obj.strftime('%d/%m/%Y')
                except:
                    ultima_asistencia_formateada = "No disponible"
            else:
                ultima_asistencia_formateada = "Nunca"

            return {
                "fecha_registro": fecha_registro_formateada,
                "fecha_ultima_asistencia": ultima_asistencia_formateada,
                "total_asistencias": stats_asistencias.get('total_asistencias', 0),
                "racha_dias": racha_dias,
                "membresia_tipo": membresia_info.get('tipo', 'Sin membresía'),
                "membresia_vencimiento": membresia_info.get('vencimiento', 'N/A'),
                "membresia_estado": membresia_info.get('estado', 'Inactiva'),
                "cliente_actualizado": cliente_actualizado  # Retornar también el cliente actualizado
            }
        except Exception as e:
            print(f"Error al obtener datos del cliente: {e}")
            return {
                "fecha_registro": "No disponible",
                "fecha_ultima_asistencia": "No disponible",
                "total_asistencias": 0,
                "racha_dias": 0,
                "membresia_tipo": "Sin membresía",
                "membresia_vencimiento": "N/A",
                "membresia_estado": "Inactiva",
                "cliente_actualizado": cliente  # Fallback al cliente original
            }

    def calcular_racha_dias(asistencias):
        """Calcular racha de días consecutivos desde las asistencias"""
        if not asistencias:
            return 0

        try:
            # Ordenar asistencias por fecha (más reciente primero)
            asistencias_ordenadas = sorted(
                asistencias,
                key=lambda x: x.get('fecha_asistencia', ''),
                reverse=True
            )

            if not asistencias_ordenadas:
                return 0

            # Obtener fechas únicas (sin duplicados del mismo día)
            fechas = []
            for asistencia in asistencias_ordenadas:
                fecha_str = asistencia.get('fecha_asistencia', '')
                if fecha_str and fecha_str not in fechas:
                    fechas.append(fecha_str)

            if not fechas:
                return 0

            # Calcular racha (usando timezone local)
            racha = 1
            fecha_actual = get_now_local().date()

            # Verificar si la última asistencia fue hoy o ayer
            ultima_fecha = datetime.fromisoformat(fechas[0].replace('Z', '+00:00')).date()
            dias_diferencia = (fecha_actual - ultima_fecha).days

            if dias_diferencia > 1:
                return 0  # La racha se rompió

            # Contar días consecutivos
            for i in range(len(fechas) - 1):
                fecha1 = datetime.fromisoformat(fechas[i].replace('Z', '+00:00')).date()
                fecha2 = datetime.fromisoformat(fechas[i + 1].replace('Z', '+00:00')).date()

                diferencia = (fecha1 - fecha2).days

                if diferencia == 1:
                    racha += 1
                else:
                    break

            return racha
        except Exception as e:
            print(f"Error al calcular racha: {e}")
            return 0

    def obtener_info_membresia_desde_pagos(pagos, cliente_data):
        """
        Obtener información de membresía desde pagos de membresía
        Combina información de pagos con campos del cliente para mayor precisión
        """
        try:
            print(f"\n{'='*60}")
            print(f"DEBUG OBTENER_INFO_MEMBRESIA_DESDE_PAGOS:")
            print(f"  Total pagos recibidos: {len(pagos) if pagos else 0}")

            # OPCIÓN 1: Intentar obtener desde campos del cliente primero
            tipo_desde_cliente = (
                cliente_data.get('tipo_membresia') or
                cliente_data.get('plan_membresia') or
                cliente_data.get('membresia_tipo') or
                None
            )
            fecha_desde_cliente = (
                cliente_data.get('fecha_membresia') or
                cliente_data.get('fecha_vencimiento') or
                None
            )

            print(f"  Campos del cliente:")
            print(f"    tipo_membresia: '{tipo_desde_cliente}'")
            print(f"    fecha_membresia: '{fecha_desde_cliente}'")

            # OPCIÓN 2: Si los campos del cliente no están disponibles, usar pagos
            tipo_desde_pagos = None
            fecha_desde_pagos = None

            if pagos and len(pagos) > 0:
                # Obtener el pago más reciente
                pago_reciente = sorted(
                    pagos,
                    key=lambda x: x.get('fecha_pago', ''),
                    reverse=True
                )[0]

                print(f"\n  Pago más reciente:")
                for key, value in pago_reciente.items():
                    print(f"    {key}: {value}")

                tipo_desde_pagos = (
                    pago_reciente.get('tipo_membresia') or
                    pago_reciente.get('nombre_membresia') or
                    pago_reciente.get('plan') or
                    None
                )

                # Si no hay tipo pero hay id_membresia, buscar la membresía por ID
                if not tipo_desde_pagos and pago_reciente.get('id_membresia'):
                    id_membresia = pago_reciente.get('id_membresia')
                    print(f"    Buscando membresía con ID: {id_membresia}")

                    try:
                        # Obtener todas las membresías disponibles
                        todas_membresias = api.get_membresias()
                        print(f"    Total membresías disponibles: {len(todas_membresias)}")

                        # Buscar la membresía con el ID específico
                        for membresia in todas_membresias:
                            if membresia.get('id') == id_membresia:
                                tipo_desde_pagos = membresia.get('tipo_membresia') or membresia.get('nombre')
                                print(f"    ¡Membresía encontrada! Tipo: {tipo_desde_pagos}")
                                break
                    except Exception as e:
                        print(f"    Error al buscar membresía por ID: {e}")

                # Intentar obtener fecha_fin primero, luego calcular desde fecha_pago
                fecha_desde_pagos = pago_reciente.get('fecha_fin') or pago_reciente.get('fecha_vencimiento')

                if not fecha_desde_pagos and pago_reciente.get('fecha_pago'):
                    # Calcular vencimiento desde fecha_pago
                    try:
                        fecha_pago_str = pago_reciente.get('fecha_pago', '')
                        fecha_obj = datetime.fromisoformat(fecha_pago_str.replace('Z', '+00:00'))

                        # Calcular vencimiento según tipo
                        duracion_dias = 30  # Default mensual
                        if tipo_desde_pagos:
                            if 'Mensual' in tipo_desde_pagos:
                                duracion_dias = 30
                            elif 'Trimestral' in tipo_desde_pagos:
                                duracion_dias = 90
                            elif 'Semestral' in tipo_desde_pagos:
                                duracion_dias = 180
                            elif 'Anual' in tipo_desde_pagos or 'Año' in tipo_desde_pagos:
                                duracion_dias = 365

                        fecha_vencimiento = fecha_obj + timedelta(days=duracion_dias)
                        fecha_desde_pagos = fecha_vencimiento.isoformat()
                    except Exception as e:
                        print(f"    Error calculando fecha de vencimiento: {e}")

            print(f"\n  Desde pagos:")
            print(f"    tipo: '{tipo_desde_pagos}'")
            print(f"    fecha: '{fecha_desde_pagos}'")

            # DECISIÓN: Usar campos del cliente si existen, sino usar pagos
            tipo_membresia = tipo_desde_cliente or tipo_desde_pagos
            fecha_membresia = fecha_desde_cliente or fecha_desde_pagos

            print(f"\n  FINAL:")
            print(f"    tipo_membresia: '{tipo_membresia}'")
            print(f"    fecha_membresia: '{fecha_membresia}'")
            print(f"{'='*60}\n")

            # Si no hay tipo de membresía, el cliente no tiene membresía
            if not tipo_membresia or tipo_membresia == 'Sin membresía':
                return {
                    "tipo": "Sin membresía",
                    "vencimiento": "N/A",
                    "estado": "Inactiva"
                }

            # Si hay tipo pero no fecha de vencimiento
            if not fecha_membresia:
                return {
                    "tipo": tipo_membresia,
                    "vencimiento": "No disponible",
                    "estado": "Desconocida"
                }

            # Parsear fecha de vencimiento
            try:
                fecha_venc_dt = parse_datetime_from_api(fecha_membresia)

                if fecha_venc_dt:
                    vencimiento_formateado = fecha_venc_dt.strftime('%d/%m/%Y')

                    # Verificar si está activa (comparar con fecha actual local)
                    hoy = get_now_local()

                    # Comparar solo las fechas, sin la hora
                    estado = "Activa" if fecha_venc_dt.date() >= hoy.date() else "Vencida"

                    print(f"DEBUG Perfil: Estado calculado = {estado}")

                    return {
                        "tipo": tipo_membresia,
                        "vencimiento": vencimiento_formateado,
                        "estado": estado
                    }
                else:
                    # Si no se pudo parsear, intentar como formato simple
                    fecha_obj = datetime.fromisoformat(fecha_membresia.replace('Z', '+00:00'))
                    vencimiento_formateado = fecha_obj.strftime('%d/%m/%Y')

                    hoy = get_now_local()
                    estado = "Activa" if fecha_obj.date() >= hoy.date() else "Vencida"

                    return {
                        "tipo": tipo_membresia,
                        "vencimiento": vencimiento_formateado,
                        "estado": estado
                    }
            except Exception as e:
                print(f"Error parseando fecha de membresía: {e}")
                return {
                    "tipo": tipo_membresia,
                    "vencimiento": "Error en fecha",
                    "estado": "Desconocida"
                }

        except Exception as e:
            print(f"Error al obtener info de membresía desde cliente: {e}")
            return {
                "tipo": "Sin membresía",
                "vencimiento": "N/A",
                "estado": "Inactiva"
            }

    # Obtener datos reales del cliente
    datos_adicionales = obtener_datos_cliente()

    # Usar el cliente actualizado para mostrar información correcta
    cliente_display = datos_adicionales.get('cliente_actualizado', cliente)

    def crear_campo_info(label, valor, icon):
        """Crear campo de información"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20, color=Theme.PRIMARY),
                ft.Text(f"{label}:", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY, width=150),
                ft.Text(valor, size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_PRIMARY,
                       weight=Theme.FONT_WEIGHT["medium"]),
            ], spacing=Theme.SPACING["md"]),
            padding=Theme.SPACING["md"],
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["md"],
            border=ft.border.all(1, Theme.BORDER_DEFAULT)
        )

    def crear_stat_card(titulo, valor, icon, color):
        """Crear tarjeta de estadística"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(valor, size=Theme.FONT_SIZE["2xl"], weight=Theme.FONT_WEIGHT["bold"], color=color),
                ft.Text(titulo, size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_SECONDARY,
                       text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
            bgcolor=f"{color}11",
            border_radius=Theme.RADIUS["lg"],
            padding=Theme.SPACING["xl"],
            border=ft.border.all(1, color),
            width=200,
            height=150
        )

    def ir_a_membresias(e):
        """Navegar a la vista de membresías"""
        if on_navigate_membresias:
            on_navigate_membresias()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("⚠ Función de navegación no disponible"),
                                        bgcolor=Theme.WARNING)
            page.snack_bar.open = True
            page.update()

    # Foto de perfil y nombre
    profile_header = create_card_container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=Theme.PRIMARY),
                bgcolor=f"{Theme.PRIMARY}22",
                border_radius=Theme.RADIUS["full"],
                width=120,
                height=120,
                alignment=ft.alignment.center
            ),
            ft.Text(f"{cliente_display['nombre']} {cliente_display['apellidos']}", size=Theme.FONT_SIZE["xl"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY,
                   text_align=ft.TextAlign.CENTER),
            ft.Container(
                content=ft.Text("MIEMBRO ACTIVO", size=Theme.FONT_SIZE["xs"],
                               color=Theme.TEXT_PRIMARY, weight=Theme.FONT_WEIGHT["bold"]),
                bgcolor=Theme.PRIMARY,
                padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"], vertical=Theme.SPACING["xs"]),
                border_radius=Theme.RADIUS["lg"]
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
        padding=Theme.SPACING["2xl"]
    )

    # Información personal
    info_personal = create_card_container(
        content=ft.Column([
            ft.Text("Información Personal", size=Theme.FONT_SIZE["lg"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            crear_campo_info("DNI", cliente_display['dni'], ft.Icons.BADGE),
            crear_campo_info("Correo Electrónico", cliente_display['correo'], ft.Icons.EMAIL),
            crear_campo_info("Teléfono", cliente_display.get('telefono', 'No registrado'), ft.Icons.PHONE),
            crear_campo_info("Fecha de Registro", datos_adicionales['fecha_registro'], ft.Icons.CALENDAR_TODAY),
            crear_campo_info("Última Asistencia", datos_adicionales['fecha_ultima_asistencia'], ft.Icons.ACCESS_TIME),
        ], spacing=Theme.SPACING["lg"]),
        padding=Theme.SPACING["xl"]
    )

    # Estadísticas de actividad
    stats_actividad = create_card_container(
        content=ft.Column([
            ft.Text("Mi Actividad", size=Theme.FONT_SIZE["lg"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Row([
                crear_stat_card("Total Asistencias", str(datos_adicionales['total_asistencias']),
                              ft.Icons.FITNESS_CENTER, Theme.PRIMARY),
                crear_stat_card("Racha Actual", f"{datos_adicionales['racha_dias']} días",
                              ft.Icons.LOCAL_FIRE_DEPARTMENT, "#FF6F00"),
            ], spacing=Theme.SPACING["lg"], wrap=True),
        ], spacing=Theme.SPACING["lg"]),
        padding=Theme.SPACING["xl"]
    )

    # Información de membresía
    estado_color = Theme.PRIMARY if datos_adicionales['membresia_estado'] == "Activa" else Theme.ERROR

    # Formatear texto de membresía (evitar "Membresía Sin Membresía")
    tipo_membresia_display = datos_adicionales['membresia_tipo']
    if tipo_membresia_display and tipo_membresia_display.lower() in ["sin membresía", "sin membresia"]:
        texto_membresia = "Sin membresía activa"
    else:
        texto_membresia = f"Membresía {tipo_membresia_display}"

    info_membresia = create_card_container(
        content=ft.Column([
            ft.Text("Mi Membresía", size=Theme.FONT_SIZE["lg"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=50, color=Theme.PRIMARY),
                    ft.Column([
                        ft.Text(texto_membresia,
                               size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["bold"],
                               color=Theme.TEXT_PRIMARY),
                        ft.Text(f"Vence: {datos_adicionales['membresia_vencimiento']}",
                               size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
                        ft.Container(
                            content=ft.Text(datos_adicionales['membresia_estado'],
                                          size=Theme.FONT_SIZE["xs"], color=Theme.TEXT_PRIMARY,
                                          weight=Theme.FONT_WEIGHT["bold"]),
                            bgcolor=estado_color,
                            padding=ft.padding.symmetric(horizontal=Theme.SPACING["lg"],
                                                        vertical=Theme.SPACING["xs"]),
                            border_radius=Theme.RADIUS["sm"],
                            margin=ft.margin.only(top=Theme.SPACING["xs"])
                        ),
                    ], spacing=Theme.SPACING["xs"], expand=True),
                ], spacing=Theme.SPACING["xl"]),
                bgcolor=f"{Theme.PRIMARY}11",
                border_radius=Theme.RADIUS["lg"],
                padding=Theme.SPACING["xl"],
                border=ft.border.all(1, Theme.PRIMARY)
            ),
            ft.Container(height=Theme.SPACING["md"]),
            ft.ElevatedButton(
                "Renovar Membresía",
                icon=ft.Icons.AUTORENEW,
                bgcolor=Theme.PRIMARY,
                color=ft.Colors.BLACK,
                width=300,
                height=45,
                on_click=ir_a_membresias
            ),
        ], spacing=Theme.SPACING["lg"], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=Theme.SPACING["xl"]
    )

    # Layout con dos columnas
    content = ft.Row([
        ft.Column([profile_header, info_membresia], spacing=Theme.SPACING["xl"], expand=True),
        ft.Column([info_personal, stats_actividad], spacing=Theme.SPACING["xl"], expand=True),
    ], spacing=Theme.SPACING["xl"], expand=True)

    # Usar base_layout
    create_base_layout(
        page=page,
        role="cliente",
        current_section=current_section,
        on_section_click=on_section_click,
        content=ft.Container(content=content, padding=Theme.SPACING["xl"]),
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )