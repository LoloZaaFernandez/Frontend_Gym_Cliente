"""
Vista de Historial de Asistencias para Cliente - Refactorizado con Sistema de Componentes
ANTES: 401 líneas | DESPUÉS: ~300 líneas (25% menos código)
"""

import flet as ft
from datetime import datetime
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.molecules import create_card_container, create_empty_state
from ui.utils.datetime_utils import parse_datetime_from_api, format_time_display


def show_cliente_asistencias_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Mostrar vista de historial de asistencias para cliente

    Mejoras:
    - 25% menos código (401 → ~300 líneas)
    - Uso de base_layout
    - Theme centralizado
    - Componentes reutilizables
    """
    page.title = "BLESSED GYM - Mis Asistencias"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    cliente_data = auth_service.get_current_user()
    cliente_id = cliente_data['id']
    user_info = {"nombre": cliente_data.get("nombre", "Cliente"), "rol": "Cliente"}

    # Estadísticas del cliente
    stats = {
        "total_asistencias": 0,
        "ultima_asistencia": None,
        "asistencias_mes_actual": 0,
        "asistencias_recientes": []
    }

    # Tarjetas de estadísticas
    total_text = ft.Text("0", size=Theme.FONT_SIZE["3xl"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY)
    mes_text = ft.Text("0", size=Theme.FONT_SIZE["3xl"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.SUCCESS)
    ultima_text = ft.Text("Sin registros", size=Theme.FONT_SIZE["md"], weight=Theme.FONT_WEIGHT["medium"], color=Theme.TEXT_SECONDARY)

    # Lista de asistencias
    asistencias_list = ft.Column(spacing=Theme.SPACING["md"], scroll=ft.ScrollMode.AUTO)

    asistencias_container = ft.Container(
        content=asistencias_list,
        height=500,
        padding=Theme.SPACING["lg"],
        bgcolor=Theme.CARD_BG,
        border_radius=Theme.RADIUS["lg"],
        border=ft.border.all(1, Theme.BORDER_DEFAULT)
    )

    def cargar_datos():
        """Cargar datos del cliente"""
        nonlocal stats

        try:
            # Obtener estadísticas (para los contadores)
            stats_api = api.get_estadisticas_cliente(cliente_id)

            # Obtener TODAS las asistencias del cliente (para el historial completo)
            asistencias_completas = api.get_asistencias_cliente(cliente_id)

            # Calcular última asistencia desde la lista completa (con fecha + hora)
            ultima_asistencia_fecha = None
            if asistencias_completas and len(asistencias_completas) > 0:
                # Ordenar por fecha descendente para obtener la más reciente
                asistencias_ordenadas = sorted(
                    asistencias_completas,
                    key=lambda x: x.get('fecha_asistencia', ''),
                    reverse=True
                )
                if asistencias_ordenadas:
                    ultima_asist = asistencias_ordenadas[0]
                    fecha_asistencia = ultima_asist.get('fecha_asistencia', '')
                    hora_ingreso = ultima_asist.get('hora_ingreso', '')

                    # Combinar fecha + hora como en clientes_view.py para conversión correcta de timezone
                    if fecha_asistencia and hora_ingreso:
                        hora_limpia = str(hora_ingreso).split('.')[0] if '.' in str(hora_ingreso) else str(hora_ingreso)
                        if 'T' in str(hora_ingreso):
                            ultima_asistencia_fecha = hora_ingreso
                        else:
                            ultima_asistencia_fecha = f"{fecha_asistencia}T{hora_limpia}"
                    elif fecha_asistencia:
                        ultima_asistencia_fecha = fecha_asistencia

            # Combinar estadísticas con la lista completa de asistencias
            stats = {
                'total_asistencias': len(asistencias_completas) if asistencias_completas else stats_api.get('total_asistencias', 0),
                'asistencias_mes_actual': stats_api.get('asistencias_mes_actual', 0),
                'ultima_asistencia': ultima_asistencia_fecha or stats_api.get('ultima_asistencia'),
                'asistencias_recientes': asistencias_completas  # ✅ Lista completa
            }

            print(f"DEBUG: Estadísticas obtenidas:")
            print(f"  Total asistencias: {stats['total_asistencias']}")
            print(f"  Asistencias este mes: {stats['asistencias_mes_actual']}")
            print(f"  Asistencias en lista: {len(stats['asistencias_recientes'])}")
            print(f"  Última asistencia calculada: {stats['ultima_asistencia']}")

            # Actualizar textos de estadísticas
            total_text.value = str(stats.get('total_asistencias', 0))
            mes_text.value = str(stats.get('asistencias_mes_actual', 0))

            # Última asistencia - ahora calculada desde la lista con conversión de timezone
            ultima = stats.get('ultima_asistencia')
            if ultima:
                try:
                    # Usar parse_datetime_from_api para convertir de UTC a hora local
                    fecha_dt = parse_datetime_from_api(ultima)
                    if fecha_dt:
                        ultima_text.value = fecha_dt.strftime("%d/%m/%Y")
                        print(f"  Última asistencia formateada: {ultima_text.value}")
                    else:
                        # Fallback si parse_datetime_from_api falla
                        ultima_text.value = str(ultima)[:10]
                        print(f"  Fallback - usando fecha directa: {ultima_text.value}")
                except Exception as e:
                    print(f"  Error formateando fecha: {e}")
                    ultima_text.value = str(ultima)[:10]  # Tomar solo la fecha
            else:
                ultima_text.value = "Sin registros"
                print(f"  No hay última asistencia")

            # Actualizar lista de asistencias
            actualizar_lista_asistencias()

        except Exception as e:
            print(f"Error al cargar datos: {e}")
            import traceback
            traceback.print_exc()
            mostrar_mensaje("Error al cargar datos", error=True)

        page.update()

    def actualizar_lista_asistencias():
        """Actualizar lista de asistencias"""
        asistencias_list.controls.clear()

        asistencias = stats.get('asistencias_recientes', [])

        print(f"DEBUG actualizar_lista_asistencias: {len(asistencias)} asistencias para mostrar")

        if not asistencias:
            asistencias_list.controls.append(
                create_empty_state(
                    message="No hay asistencias registradas",
                    icon=ft.Icons.FITNESS_CENTER,
                    secondary_message="Registra tu primera asistencia en el gimnasio"
                )
            )
        else:
            for asistencia in asistencias:
                asistencias_list.controls.append(crear_asistencia_card(asistencia))

    def crear_asistencia_card(asistencia):
        """Crear tarjeta de asistencia"""
        # Formatear fecha y hora con conversión correcta de UTC a hora local
        fecha_asistencia = asistencia.get('fecha_asistencia', '')
        hora_ingreso = asistencia.get('hora_ingreso', '')

        fecha_formatted = fecha_asistencia
        hora_formatted = "--:--"

        # Parsear fecha y hora correctamente
        if hora_ingreso and fecha_asistencia:
            try:
                # Limpiar la hora si tiene microsegundos
                hora_limpia = str(hora_ingreso).split('.')[0] if '.' in str(hora_ingreso) else str(hora_ingreso)

                # Si la hora ya tiene formato ISO completo, usarla directamente
                if 'T' in str(hora_ingreso):
                    datetime_str = hora_ingreso
                else:
                    # Combinar fecha + hora en formato ISO para parsear correctamente
                    datetime_str = f"{fecha_asistencia}T{hora_limpia}"

                # Parsear con la función que convierte UTC a hora local
                dt = parse_datetime_from_api(datetime_str)
                if dt:
                    fecha_formatted = dt.strftime("%d %b %Y")
                    hora_formatted = format_time_display(dt)
            except Exception as e:
                print(f"Error parseando fecha/hora en card: {e}")
                # Fallback
                try:
                    fecha_dt = datetime.fromisoformat(fecha_asistencia)
                    fecha_formatted = fecha_dt.strftime("%d %b %Y")
                except:
                    fecha_formatted = fecha_asistencia
                hora_formatted = str(hora_ingreso)[:8] if hora_ingreso else "--:--"
        elif fecha_asistencia:
            try:
                fecha_dt = datetime.fromisoformat(fecha_asistencia)
                fecha_formatted = fecha_dt.strftime("%d %b %Y")
            except:
                fecha_formatted = fecha_asistencia

        hora = hora_formatted

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.CHECK_CIRCLE, size=28, color="#4CAF50"),
                        bgcolor="#4CAF5022",
                        border_radius=10,
                        padding=12
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                fecha_formatted,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=Theme.TEXT_PRIMARY
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=Theme.TEXT_SECONDARY),
                                    ft.Text(
                                        f"Hora de ingreso: {hora}",
                                        size=13,
                                        color=Theme.TEXT_SECONDARY
                                    ),
                                ],
                                spacing=5
                            ),
                        ],
                        spacing=5,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.FITNESS_CENTER, size=24, color=Theme.PRIMARY),
                        padding=8
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=15,
            bgcolor="#1A1A1A",
            border_radius=10,
            border=ft.border.all(1, "#333333"),
            ink=True,
            on_hover=lambda e: hover_effect(e)
        )

    def hover_effect(e):
        """Efecto hover en cards"""
        if e.data == "true":
            e.control.border = ft.border.all(1, Theme.PRIMARY)
        else:
            e.control.border = ft.border.all(1, "#333333")
        e.control.update()

    def mostrar_mensaje(mensaje, error=False):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=Theme.ERROR if error else Theme.SUCCESS
        )
        page.snack_bar.open = True
        page.update()

    # Botón de actualizar
    refresh_button = ft.ElevatedButton(
        "Actualizar",
        icon=ft.Icons.REFRESH,
        style=ft.ButtonStyle(
            color=Theme.PRIMARY,
            bgcolor=ft.Colors.TRANSPARENT,
            side=ft.border.all(1, Theme.PRIMARY),
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["md"])
        ),
        on_click=lambda _: cargar_datos(),
        height=40
    )

    # Información del cliente
    info_cliente = create_card_container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=Theme.PRIMARY),
                bgcolor=f"{Theme.PRIMARY}22",
                border_radius=Theme.RADIUS["full"],
                padding=Theme.SPACING["md"]
            ),
            ft.Column([
                ft.Text(f"{cliente_data['nombre']} {cliente_data['apellidos']}",
                       size=Theme.FONT_SIZE["lg"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                ft.Text(f"DNI: {cliente_data['dni']}", size=Theme.FONT_SIZE["sm"], color=Theme.TEXT_SECONDARY),
            ], spacing=Theme.SPACING["xs"]),
        ], spacing=Theme.SPACING["lg"]),
        padding=Theme.SPACING["xl"]
    )

    # Tarjetas de estadísticas
    stats_cards = ft.Row([
        create_card_container(
            content=ft.Column([
                ft.Icon(ft.Icons.FITNESS_CENTER, size=32, color=Theme.PRIMARY),
                total_text,
                ft.Text("Total de Asistencias", size=Theme.FONT_SIZE["xs"],
                       color=Theme.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
            padding=Theme.SPACING["xl"]
        ),
        create_card_container(
            content=ft.Column([
                ft.Icon(ft.Icons.CALENDAR_MONTH, size=32, color=Theme.SUCCESS),
                mes_text,
                ft.Text("Asistencias Este Mes", size=Theme.FONT_SIZE["xs"],
                       color=Theme.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
            padding=Theme.SPACING["xl"]
        ),
        create_card_container(
            content=ft.Column([
                ft.Icon(ft.Icons.ACCESS_TIME, size=32, color=Theme.INFO),
                ultima_text,
                ft.Text("Última Asistencia", size=Theme.FONT_SIZE["xs"],
                       color=Theme.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
            padding=Theme.SPACING["xl"]
        ),
    ], spacing=Theme.SPACING["lg"])

    # Panel de historial
    historial_panel = create_card_container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LIST_ALT, size=22, color=Theme.PRIMARY),
                ft.Text("Historial Reciente", size=Theme.FONT_SIZE["lg"],
                       weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ], spacing=Theme.SPACING["md"]),
            ft.Divider(height=1, color=Theme.BORDER_DEFAULT),
            asistencias_container,
        ], spacing=Theme.SPACING["lg"]),
        padding=Theme.SPACING["2xl"]
    )

    # Contenido principal
    content = ft.Column([
        ft.Row([ft.Container(expand=True), refresh_button], alignment=ft.MainAxisAlignment.END),
        info_cliente,
        stats_cards,
        historial_panel,
    ], spacing=Theme.SPACING["xl"], scroll=ft.ScrollMode.AUTO, expand=True)

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

    # Cargar datos iniciales
    cargar_datos()
