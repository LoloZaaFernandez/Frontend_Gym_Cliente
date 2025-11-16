"""
Vista de Asistencia para Clientes Registrados - REDISEÑADA PARA TABLET
Flujo: ingresar DNI → verificar cliente → registrar asistencia → alerta si membresía por vencer
"""
import flet as ft
import sys
import os

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme
from config.settings import USUARIO_SISTEMA, BACKGROUND_IMAGE
from components.buttons import create_large_button, create_back_button, create_success_button
from components.inputs import create_dni_input
from components.cards import create_card_container, create_alert_card
from components.membership_card import create_membership_card
from services.api_service import APIService
from utils.datetime_utils import parse_datetime_from_api, format_date_display, format_time_display


def show_asistencia_view(page: ft.Page, api_service: APIService, on_back):
    """
    Mostrar vista de registro de asistencia

    Args:
        page: Instancia de la página
        api_service: Servicio API
        on_back: Función para volver a la pantalla inicial
    """

    # Controles
    dni_input = create_dni_input()
    mensaje_container = ft.Container()
    btn_registrar = create_success_button("Registrar Asistencia", None, icon=ft.Icons.CHECK_CIRCLE)

    # Estado para renovación de membresía
    cliente_actual = {}  # Guardar datos del cliente para renovación
    opciones_membresias = []
    metodos_pago = []
    renovacion_data = {
        "id_membresia": None,
        "metodo_pago": "Efectivo"
    }

    def mostrar_mensaje(mensaje: str, tipo: str = "error"):
        """Mostrar mensaje (error, success, warning, info)"""
        mensaje_container.content = create_alert_card(mensaje, tipo)
        try:
            mensaje_container.update()
        except:
            # Si el contenedor no está en la página, usar page.update()
            try:
                page.update()
            except:
                pass

    def limpiar_mensaje():
        """Limpiar mensaje"""
        mensaje_container.content = None
        try:
            mensaje_container.update()
        except:
            # Si el contenedor no está en la página, ignorar
            pass

    def validar_dni() -> bool:
        """Validar que el DNI esté completo"""
        if not dni_input.value or len(dni_input.value) != 8:
            mostrar_mensaje("El DNI debe tener 8 dígitos", "error")
            return False
        return True

    def registrar_asistencia_cliente(e):
        """Registrar asistencia del cliente"""
        limpiar_mensaje()

        if not validar_dni():
            return

        try:
            # 1. Verificar que el cliente existe y obtener sus datos
            cliente = api_service.get_cliente_por_dni(dni_input.value)

            if not cliente:
                mostrar_mensaje(
                    f"No se encontró ningún cliente con DNI {dni_input.value}.\n"
                    "Si eres nuevo, regresa y selecciona 'Registrarse'.",
                    "error"
                )
                return

            # 2. Verificar si la membresía está por vencer o vencida (ANTES de verificar estado)
            alerta_membresia = api_service.verificar_membresia_por_vencer(cliente, dias_alerta=5)

            print(f"🔍 DEBUG - Cliente: {cliente.get('nombre')} {cliente.get('apellidos')}")
            print(f"🔍 DEBUG - Estado: {cliente.get('estado')}")
            print(f"🔍 DEBUG - Fecha membresía: {cliente.get('fecha_membresia')}")
            print(f"🔍 DEBUG - Alerta membresía: {alerta_membresia}")

            # Si la membresía está vencida, mostrar pantalla de renovación
            if alerta_membresia and alerta_membresia["tipo"] == "vencida":
                print("⚠️ Membresía vencida detectada - Mostrando pantalla de renovación")
                # Guardar datos del cliente
                cliente_actual.update(cliente)
                # Mostrar pantalla de membresía vencida con opción de renovar
                mostrar_membresia_vencida(cliente, alerta_membresia)
                return

            # 3. Verificar que el cliente esté activo (solo si NO tiene membresía vencida)
            if cliente.get("estado", "") != "Activo":
                mostrar_mensaje(
                    f"El cliente {cliente.get('nombre', '')} {cliente.get('apellidos', '')} "
                    f"está en estado: {cliente.get('estado', 'Desconocido')}.\n"
                    "Por favor, contacta al personal del gimnasio.",
                    "error"
                )
                return

            # 4. Registrar la asistencia
            resultado = api_service.registrar_asistencia(
                dni=dni_input.value,
                usuario_creacion=USUARIO_SISTEMA
            )

            # 5. Mostrar pantalla de éxito
            mostrar_asistencia_exitosa(cliente, resultado, alerta_membresia)

        except ValueError as e:
            # Capturar error específico de membresía vencida del backend
            error_msg = str(e).lower()
            print(f"🔍 DEBUG - Error capturado: {error_msg}")

            if "membresia vencida" in error_msg or "membresía vencida" in error_msg or "vencida" in error_msg:
                print("⚠️ Error de membresía vencida del backend - Mostrando pantalla de renovación")
                # Obtener datos del cliente nuevamente
                cliente = api_service.get_cliente_por_dni(dni_input.value)
                if cliente:
                    cliente_actual.update(cliente)
                    alerta_membresia = {
                        "tipo": "vencida",
                        "mensaje": "Tu membresía ha vencido. Por favor, renuévala para continuar."
                    }
                    mostrar_membresia_vencida(cliente, alerta_membresia)
                else:
                    mostrar_mensaje(f"Error: {str(e)}", "error")
            else:
                mostrar_mensaje(f"Error al registrar asistencia: {str(e)}", "error")

        except Exception as e:
            print(f"🔍 DEBUG - Excepción general: {type(e).__name__}: {str(e)}")
            mostrar_mensaje(f"Error al registrar asistencia: {str(e)}", "error")

    def mostrar_asistencia_exitosa(cliente, resultado_asistencia, alerta_membresia):
        """Mostrar pantalla de asistencia registrada exitosamente"""

        # DEBUG: Imprimir lo que viene del backend
        print(f"🔍 DEBUG ASISTENCIA - Cliente: {cliente}")
        print(f"🔍 DEBUG ASISTENCIA - Resultado asistencia: {resultado_asistencia}")
        print(f"🔍 DEBUG ASISTENCIA - fecha_membresia raw: {cliente.get('fecha_membresia', '')}")
        print(f"🔍 DEBUG ASISTENCIA - fecha_asistencia raw: {resultado_asistencia.get('fecha_asistencia', '')}")

        # Procesar fecha de membresía usando utilidades
        fecha_membresia_dt = parse_datetime_from_api(cliente.get('fecha_membresia', ''))
        fecha_membresia = format_date_display(fecha_membresia_dt) if fecha_membresia_dt else "Sin fecha"

        # Procesar fecha y hora de asistencia usando utilidades
        fecha_asistencia_raw = resultado_asistencia.get('fecha_asistencia', '')
        fecha_asistencia_dt = parse_datetime_from_api(fecha_asistencia_raw)

        # Si viene solo fecha (sin 'T'), la hora será 00:00, así que usamos hora actual
        if fecha_asistencia_dt and 'T' not in str(fecha_asistencia_raw):
            # Reemplazar la hora 00:00 por la hora actual
            from utils.datetime_utils import get_now_local
            ahora = get_now_local()
            fecha_asistencia_dt = fecha_asistencia_dt.replace(
                hour=ahora.hour,
                minute=ahora.minute,
                second=ahora.second
            )

        fecha_asistencia = format_date_display(fecha_asistencia_dt) if fecha_asistencia_dt else "Sin fecha"
        hora_asistencia = format_time_display(fecha_asistencia_dt) if fecha_asistencia_dt else "--:--"

        print(f"🔍 DEBUG ASISTENCIA - fecha_membresia formateada: {fecha_membresia}")
        print(f"🔍 DEBUG ASISTENCIA - fecha_asistencia formateada: {fecha_asistencia}")
        print(f"🔍 DEBUG ASISTENCIA - hora_asistencia formateada: {hora_asistencia}")

        # Layout minimal en dos columnas
        columna_izquierda = ft.Column([
            # Info del cliente
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON_ROUNDED, color=Theme.SUCCESS, size=24),
                        ft.Text("Cliente", size=Theme.FONT_SIZE["lg"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["md"]),

                    ft.Text(f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}",
                           size=Theme.FONT_SIZE["xl"],
                           weight=Theme.FONT_WEIGHT["bold"],
                           color=Theme.TEXT_PRIMARY),
                    ft.Text(f"DNI: {cliente.get('dni', '')}",
                           size=Theme.FONT_SIZE["md"],
                           color=Theme.TEXT_SECONDARY),
                ], spacing=Theme.SPACING["xs"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["lg"],
                border=ft.border.all(1, Theme.BORDER_LIGHT),
                shadow=Theme.get_shadow("md"),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            # Membresía
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CARD_MEMBERSHIP_ROUNDED, color=Theme.SUCCESS, size=24),
                        ft.Text("Membresía", size=Theme.FONT_SIZE["lg"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["sm"]),

                    ft.Text("Válida hasta",
                           size=Theme.FONT_SIZE["sm"],
                           color=Theme.TEXT_SECONDARY),
                    ft.Text(fecha_membresia,
                           size=Theme.FONT_SIZE["2xl"],
                           weight=Theme.FONT_WEIGHT["bold"],
                           color=Theme.SUCCESS),
                ], spacing=Theme.SPACING["xs"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["lg"],
                border=ft.border.all(1, Theme.BORDER_LIGHT),
                shadow=Theme.get_shadow("md"),
            ),
        ], spacing=0)

        columna_derecha = ft.Column([
            # Fecha y hora
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.EVENT_AVAILABLE_ROUNDED, color=Theme.PRIMARY, size=24),
                        ft.Text("Registro", size=Theme.FONT_SIZE["lg"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["md"]),

                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED, color=Theme.PRIMARY, size=20),
                        ft.Text(fecha_asistencia,
                               size=Theme.FONT_SIZE["lg"],
                               color=Theme.TEXT_SECONDARY),
                    ], spacing=Theme.SPACING["xs"]),

                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, color=Theme.PRIMARY, size=20),
                        ft.Text(hora_asistencia,
                               size=Theme.FONT_SIZE["2xl"],
                               weight=Theme.FONT_WEIGHT["bold"],
                               color=Theme.PRIMARY),
                    ], spacing=Theme.SPACING["xs"]),
                ], spacing=Theme.SPACING["sm"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["lg"],
                border=ft.border.all(1, Theme.BORDER_LIGHT),
                shadow=Theme.get_shadow("md"),
            ),
        ], spacing=0)

        controles_exito = [
            # Ícono de éxito simple
            ft.Icon(
                ft.Icons.CHECK_CIRCLE_ROUNDED,
                size=64,
                color=Theme.SUCCESS
            ),

            ft.Container(height=Theme.SPACING["md"]),

            # Título
            ft.Text(
                "Asistencia Registrada",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["extrabold"],
                color=Theme.SUCCESS,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Layout dos columnas
            ft.Row([
                ft.Container(content=columna_izquierda, width=360),
                ft.Container(content=columna_derecha, width=360),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["2xl"]),
        ]

        # Agregar alerta de membresía por vencer (si aplica)
        if alerta_membresia:
            controles_exito.append(ft.Container(height=Theme.SPACING["xl"]))
            controles_exito.append(
                create_alert_card(
                    alerta_membresia["mensaje"],
                    "warning"
                )
            )

        controles_exito.extend([
            ft.Container(height=Theme.SPACING["xl"]),

            # Botón volver mejorado
            ft.Container(
                content=create_large_button(
                    "Finalizar",
                    lambda e: volver_a_inicio(),
                    icon=ft.Icons.HOME_ROUNDED,
                    bgcolor=Theme.SUCCESS
                ),
                width=280,
            )
        ])

        contenido_exito = ft.Column(
            controles_exito,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=Theme.SPACING["md"]
        )

        # Layout con background
        background_existe = os.path.exists(BACKGROUND_IMAGE)

        if background_existe:
            main_container = ft.Stack([
                ft.Image(
                    src=BACKGROUND_IMAGE,
                    fit=ft.ImageFit.COVER,
                    width=float('inf'),
                    height=float('inf'),
                ),
                ft.Container(
                    bgcolor=Theme.OVERLAY_DARK,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [contenido_exito],
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=Theme.SPACING["3xl"],
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ], expand=True)
        else:
            main_container = ft.Container(
                content=ft.Column(
                    [contenido_exito],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["3xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.center
            )

        page.controls.clear()
        page.add(main_container)
        page.update()

    # ==================== FUNCIONES PARA RENOVACIÓN DE MEMBRESÍA ====================

    def cargar_opciones_renovacion():
        """Cargar opciones de membresías y métodos de pago para renovación"""
        try:
            print("Cargando opciones de renovación...")
            opciones = api_service.get_opciones_registro()
            print(f"Opciones recibidas: {opciones}")

            # Limpiar y actualizar las listas
            opciones_membresias.clear()
            membresias_raw = opciones.get("membresias_disponibles", opciones.get("membresias", []))

            # Normalizar los datos del backend
            for memb in membresias_raw:
                membresia_normalizada = {
                    "id": memb.get("id"),
                    "nombre": memb.get("nombre_membresia", memb.get("nombre", "")),
                    "precio": memb.get("precio_actual", memb.get("precio", 0)),
                    "duracion_dias": memb.get("duracion_dias", 30),
                    "tipo_membresia": memb.get("tipo_membresia", "")
                }
                opciones_membresias.append(membresia_normalizada)

            # Solo permitir Yape y Efectivo
            metodos_pago.clear()
            metodos_disponibles = opciones.get("metodos_pago", ["Efectivo", "Yape"])
            metodos_permitidos = [m for m in metodos_disponibles if m in ["Yape", "Efectivo"]]
            if not metodos_permitidos:
                metodos_permitidos = ["Efectivo", "Yape"]
            metodos_pago.extend(metodos_permitidos)

            print(f"Membresias cargadas: {len(opciones_membresias)}")
            print(f"Metodos de pago: {metodos_pago}")

            if not opciones_membresias:
                mostrar_mensaje("No se pudieron cargar las opciones de membresía.", "error")
                return False

            return True

        except Exception as e:
            print(f"ERROR - Error al cargar opciones de renovación: {e}")
            import traceback
            traceback.print_exc()
            mostrar_mensaje(f"Error al cargar opciones: {str(e)}", "error")
            return False

    def mostrar_membresia_vencida(cliente, alerta_membresia):
        """Mostrar pantalla cuando la membresía está vencida con opción de renovar"""

        nombre_completo = f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}"
        dni = cliente.get('dni', '')

        # Procesar fecha de membresía
        fecha_membresia_dt = parse_datetime_from_api(cliente.get('fecha_membresia', ''))
        fecha_membresia = format_date_display(fecha_membresia_dt) if fecha_membresia_dt else "Sin fecha"

        contenido_vencida = ft.Column([
            # Ícono de alerta
            ft.Container(
                content=ft.Icon(
                    ft.Icons.ERROR_OUTLINE_ROUNDED,
                    size=Theme.ICON_SIZE["2xl"],
                    color=Theme.ERROR
                ),
                width=120,
                height=120,
                bgcolor="rgba(244, 67, 54, 0.1)",
                border_radius=60,
                border=ft.border.all(4, Theme.ERROR),
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=25,
                    color="rgba(244, 67, 54, 0.3)",
                    offset=ft.Offset(0, 0),
                ),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            # Título
            ft.Text(
                "MEMBRESÍA VENCIDA",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["extrabold"],
                color=Theme.ERROR,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Text(
                f"Hola, {nombre_completo}",
                size=Theme.FONT_SIZE["xl"],
                weight=Theme.FONT_WEIGHT["medium"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Info del cliente y membresía vencida
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.BADGE_ROUNDED, color=Theme.PRIMARY, size=28),
                        ft.Text(f"DNI: {dni}", size=Theme.FONT_SIZE["lg"]),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["md"]),

                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED, color=Theme.ERROR, size=28),
                        ft.Text(
                            f"Membresía vencida el: {fecha_membresia}",
                            size=Theme.FONT_SIZE["lg"],
                            color=Theme.ERROR,
                            weight=Theme.FONT_WEIGHT["semibold"]
                        ),
                    ], spacing=Theme.SPACING["sm"]),
                ], spacing=Theme.SPACING["sm"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["xl"],
                border=ft.border.all(2, Theme.ERROR),
                shadow=Theme.get_shadow("lg"),
                width=600,
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Alerta
            create_alert_card(
                "No puedes registrar asistencia con membresía vencida.\n"
                "Por favor, renueva tu membresía para continuar.",
                "error"
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Botones
            ft.Row([
                create_back_button(lambda e: volver_a_inicio(), "Volver"),
                create_large_button(
                    "Renovar Membresía",
                    lambda e: iniciar_renovacion(),
                    icon=ft.Icons.AUTORENEW_ROUNDED,
                    bgcolor=Theme.SUCCESS
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["xl"])

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

        # Layout con background
        background_existe = os.path.exists(BACKGROUND_IMAGE)

        if background_existe:
            main_container = ft.Stack([
                ft.Image(
                    src=BACKGROUND_IMAGE,
                    fit=ft.ImageFit.COVER,
                    width=float('inf'),
                    height=float('inf'),
                ),
                ft.Container(bgcolor=Theme.OVERLAY_DARK, expand=True),
                ft.Container(
                    content=ft.Column(
                        [contenido_vencida],
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=Theme.SPACING["3xl"],
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ], expand=True)
        else:
            main_container = ft.Container(
                content=ft.Column(
                    [contenido_vencida],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["3xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.center
            )

        page.controls.clear()
        page.add(main_container)
        page.update()

    def iniciar_renovacion():
        """Iniciar el proceso de renovación"""
        # Cargar opciones
        if not cargar_opciones_renovacion():
            return

        # Mostrar pantalla de selección de membresía
        mostrar_seleccion_membresia()

    def seleccionar_membresia_renovacion(membresia_id: int):
        """Seleccionar una membresía para renovación"""
        renovacion_data["id_membresia"] = membresia_id
        mostrar_seleccion_membresia()  # Re-renderizar para mostrar selección

    def seleccionar_metodo_pago_renovacion(metodo: str):
        """Seleccionar método de pago para renovación"""
        renovacion_data["metodo_pago"] = metodo
        mostrar_seleccion_membresia()  # Re-renderizar para mostrar selección

    def mostrar_seleccion_membresia():
        """Mostrar pantalla de selección de membresía y método de pago"""

        # Cards de membresías
        membresias_cards = []

        if not opciones_membresias:
            membresias_cards.append(
                create_alert_card(
                    "No hay membresías disponibles. Por favor, contacta al administrador.",
                    "error"
                )
            )
        else:
            for memb in opciones_membresias:
                seleccionada = renovacion_data["id_membresia"] == memb["id"]
                card = create_membership_card(
                    membresia=memb,
                    precio_actual=memb['precio'],
                    on_select_click=lambda e, mid=memb["id"]: seleccionar_membresia_renovacion(mid),
                    is_selected=seleccionada
                )
                membresias_cards.append(card)

        # Botones de método de pago
        metodos_buttons = []
        for metodo in metodos_pago:
            seleccionado = renovacion_data["metodo_pago"] == metodo
            icono = ft.Icons.PAYMENT if metodo == "Yape" else ft.Icons.MONEY
            border_color = Theme.PRIMARY if seleccionado else Theme.BORDER_DEFAULT
            bg_color = Theme.CARD_BG

            btn = ft.Container(
                content=ft.Column([
                    ft.Icon(
                        icono,
                        size=48,
                        color=Theme.PRIMARY if seleccionado else Theme.TEXT_SECONDARY
                    ),
                    ft.Text(
                        metodo,
                        size=Theme.FONT_SIZE["2xl"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY if seleccionado else Theme.TEXT_SECONDARY
                    ),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE_ROUNDED,
                        size=24,
                        color=Theme.PRIMARY,
                        visible=seleccionado
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),
                bgcolor=bg_color,
                border=ft.border.all(2 if not seleccionado else 3, border_color),
                border_radius=Theme.RADIUS["lg"],
                padding=Theme.SPACING["2xl"],
                width=200,
                animate=200,
                on_click=lambda e, m=metodo: seleccionar_metodo_pago_renovacion(m)
            )
            metodos_buttons.append(btn)

        contenido_seleccion = ft.Column([
            ft.Text(
                "Renovar Membresía",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.PRIMARY
            ),

            ft.Text(
                f"Cliente: {cliente_actual.get('nombre', '')} {cliente_actual.get('apellidos', '')}",
                size=Theme.FONT_SIZE["lg"],
                color=Theme.TEXT_SECONDARY
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            ft.Text("Selecciona tu Membresía:", size=Theme.FONT_SIZE["2xl"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ft.Container(height=Theme.SPACING["lg"]),

            ft.Row(
                membresias_cards,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                run_spacing=20,
                wrap=True
            ),

            ft.Container(height=Theme.SPACING["3xl"]),

            ft.Text("Método de Pago:", size=Theme.FONT_SIZE["2xl"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ft.Container(height=Theme.SPACING["lg"]),
            ft.Row(metodos_buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["2xl"], wrap=True),

            ft.Container(height=Theme.SPACING["2xl"]),

            mensaje_container,

            ft.Row([
                create_back_button(lambda e: volver_a_inicio(), "Cancelar"),
                create_success_button("Continuar", lambda e: ir_a_confirmacion_renovacion(), icon=ft.Icons.ARROW_FORWARD),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=600)

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

        # Layout con background
        background_existe = os.path.exists(BACKGROUND_IMAGE)

        if background_existe:
            main_container = ft.Stack([
                ft.Image(
                    src=BACKGROUND_IMAGE,
                    fit=ft.ImageFit.COVER,
                    width=float('inf'),
                    height=float('inf'),
                ),
                ft.Container(bgcolor=Theme.OVERLAY_DARK, expand=True),
                ft.Container(
                    content=ft.Column(
                        [contenido_seleccion],
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=Theme.SPACING["4xl"],
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ], expand=True)
        else:
            main_container = ft.Container(
                content=ft.Column(
                    [contenido_seleccion],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["4xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.center
            )

        page.controls.clear()
        page.add(main_container)
        page.update()

    def ir_a_confirmacion_renovacion():
        """Ir a la pantalla de confirmación de renovación"""
        if not renovacion_data["id_membresia"]:
            mostrar_mensaje("Debes seleccionar una membresía", "error")
            return

        if not renovacion_data["metodo_pago"]:
            mostrar_mensaje("Debes seleccionar un método de pago", "error")
            return

        mostrar_confirmacion_renovacion()

    def mostrar_confirmacion_renovacion():
        """Mostrar pantalla de confirmación de renovación"""

        # Obtener membresía seleccionada
        membresia_sel = next((m for m in opciones_membresias if m["id"] == renovacion_data["id_membresia"]), {})
        metodo_pago = renovacion_data["metodo_pago"]

        # Info del cliente
        nombre_completo = f"{cliente_actual.get('nombre', '')} {cliente_actual.get('apellidos', '')}"
        dni = cliente_actual.get('dni', '')

        # Layout en dos columnas
        columna_izquierda = ft.Column([
            # Datos Personales
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON_ROUNDED, color=Theme.PRIMARY, size=24),
                        ft.Text("Datos del Cliente", size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["md"]),

                    ft.Text(f"DNI: {dni}",
                           size=Theme.FONT_SIZE["md"],
                           color=Theme.TEXT_SECONDARY),
                    ft.Text(nombre_completo,
                           size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["semibold"],
                           color=Theme.TEXT_PRIMARY),
                ], spacing=Theme.SPACING["xs"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["xl"],
                border=ft.border.all(1, Theme.BORDER_LIGHT),
                shadow=Theme.get_shadow("md"),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            # Método de Pago
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PAYMENT_ROUNDED, color=Theme.PRIMARY, size=24),
                        ft.Text("Método de Pago", size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["sm"]),

                    ft.Text(metodo_pago,
                           size=Theme.FONT_SIZE["2xl"],
                           weight=Theme.FONT_WEIGHT["bold"],
                           color=Theme.PRIMARY),
                ], spacing=Theme.SPACING["xs"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["xl"],
                border=ft.border.all(1, Theme.BORDER_LIGHT),
                shadow=Theme.get_shadow("md"),
            ),
        ], spacing=0)

        columna_derecha = ft.Column([
            # Membresía
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CARD_MEMBERSHIP_ROUNDED, color=Theme.SUCCESS, size=24),
                        ft.Text("Nueva Membresía", size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["lg"]),

                    ft.Text(membresia_sel.get('nombre', 'Membresía'),
                           size=Theme.FONT_SIZE["2xl"],
                           weight=Theme.FONT_WEIGHT["bold"],
                           color=Theme.SUCCESS),

                    ft.Container(height=Theme.SPACING["sm"]),

                    ft.Row([
                        ft.Text("S/", size=Theme.FONT_SIZE["2xl"], color=Theme.PRIMARY),
                        ft.Text(f"{membresia_sel.get('precio', 0):.2f}",
                               size=Theme.FONT_SIZE["5xl"],
                               weight=Theme.FONT_WEIGHT["extrabold"],
                               color=Theme.PRIMARY),
                    ], spacing=Theme.SPACING["xs"], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Container(height=Theme.SPACING["sm"]),

                    ft.Text(f"Duración: {membresia_sel.get('duracion_dias', 30)} días",
                           size=Theme.FONT_SIZE["md"],
                           color=Theme.TEXT_SECONDARY,
                           text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=Theme.SPACING["2xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["xl"],
                border=ft.border.all(2, Theme.SUCCESS),
                shadow=Theme.get_shadow("lg"),
            ),
        ], spacing=0)

        elementos_confirmacion = [
            ft.Text(
                "Confirmar Renovación",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["extrabold"],
                color=Theme.PRIMARY
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Layout dos columnas
            ft.Row([
                ft.Container(content=columna_izquierda, width=380),
                ft.Container(content=columna_derecha, width=380),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["2xl"]),

            ft.Container(height=Theme.SPACING["2xl"]),
        ]

        # Si el método de pago es Yape, mostrar QR
        if metodo_pago == "Yape":
            qr_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "QR_YAPE.jpg")

            if os.path.exists(qr_path):
                elementos_confirmacion.extend([
                    ft.Row([
                        ft.Icon(ft.Icons.QR_CODE_2_ROUNDED, color=Theme.PRIMARY, size=28),
                        ft.Text("Escanea para pagar con Yape",
                               size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"],
                               color=Theme.TEXT_PRIMARY),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["lg"]),

                    ft.Row([
                        ft.Container(
                            content=ft.Image(
                                src=qr_path,
                                width=280,
                                height=280,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            bgcolor="#FFFFFF",
                            border_radius=Theme.RADIUS["lg"],
                            padding=Theme.SPACING["lg"],
                            alignment=ft.alignment.center,
                            shadow=Theme.get_shadow("lg"),
                            width=320,
                            height=320,
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Container(height=Theme.SPACING["lg"]),

                    ft.Row([
                        ft.Text("Monto:",
                               size=Theme.FONT_SIZE["lg"],
                               color=Theme.TEXT_SECONDARY),
                        ft.Text(f"S/ {membresia_sel.get('precio', 0):.2f}",
                               size=Theme.FONT_SIZE["3xl"],
                               weight=Theme.FONT_WEIGHT["extrabold"],
                               color=Theme.PRIMARY),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["xl"]),
                ])
            else:
                elementos_confirmacion.extend([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.WARNING_ROUNDED, color=Theme.WARNING, size=36),
                            ft.Container(height=Theme.SPACING["sm"]),
                            ft.Text("QR de Yape no disponible",
                                   size=Theme.FONT_SIZE["lg"],
                                   weight=Theme.FONT_WEIGHT["semibold"],
                                   color=Theme.TEXT_PRIMARY,
                                   text_align=ft.TextAlign.CENTER),
                            ft.Container(height=Theme.SPACING["xs"]),
                            ft.Text("Realiza el pago con el personal",
                                   size=Theme.FONT_SIZE["md"],
                                   color=Theme.TEXT_SECONDARY,
                                   text_align=ft.TextAlign.CENTER),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        padding=Theme.SPACING["xl"],
                        bgcolor=Theme.CARD_BG,
                        border_radius=Theme.RADIUS["lg"],
                        border=ft.border.all(1, Theme.BORDER_LIGHT),
                    ),
                    ft.Container(height=Theme.SPACING["xl"]),
                ])

        elementos_confirmacion.extend([
            mensaje_container,
            ft.Row([
                create_back_button(lambda e: mostrar_seleccion_membresia(), "Volver"),
                create_success_button("Confirmar Renovación", lambda e: confirmar_renovacion(), icon=ft.Icons.CHECK),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=600)
        ])

        contenido_confirmacion = ft.Column(
            elementos_confirmacion,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=Theme.SPACING["md"]
        )

        # Layout con background
        background_existe = os.path.exists(BACKGROUND_IMAGE)

        if background_existe:
            main_container = ft.Stack([
                ft.Image(
                    src=BACKGROUND_IMAGE,
                    fit=ft.ImageFit.COVER,
                    width=float('inf'),
                    height=float('inf'),
                ),
                ft.Container(bgcolor=Theme.OVERLAY_DARK, expand=True),
                ft.Container(
                    content=ft.Column(
                        [contenido_confirmacion],
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=Theme.SPACING["4xl"],
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ], expand=True)
        else:
            main_container = ft.Container(
                content=ft.Column(
                    [contenido_confirmacion],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["4xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.center
            )

        page.controls.clear()
        page.add(main_container)
        page.update()

    def confirmar_renovacion():
        """Confirmar y registrar la renovación de membresía"""
        try:
            limpiar_mensaje()

            print("🎯 Iniciando renovación de membresía...")

            # Llamar al API para renovar (usar el mismo endpoint que registro)
            resultado = api_service.renovar_membresia_cliente(
                dni=cliente_actual.get('dni'),
                id_membresia=renovacion_data["id_membresia"],
                metodo_pago=renovacion_data["metodo_pago"],
                usuario_creacion=USUARIO_SISTEMA
            )

            print(f"Resultado de la renovación: {resultado}")

            if resultado.get("renovacion_creada", False) or resultado.get("registro_creado", False):
                print("OK - Renovación pendiente creada exitosamente")
                mostrar_renovacion_exitosa(resultado)
            else:
                mostrar_mensaje(resultado.get("mensaje", "Error al renovar membresía"), "error")

        except Exception as e:
            print(f"ERROR - Error al renovar: {e}")
            import traceback
            traceback.print_exc()
            mostrar_mensaje(f"Error al renovar membresía: {str(e)}", "error")

    def mostrar_renovacion_exitosa(resultado):
        """Mostrar pantalla de renovación exitosa"""

        resumen = resultado.get("resumen", {})
        metodo_pago = renovacion_data.get("metodo_pago", "Efectivo")

        nombre_completo = resumen.get("nombre_completo", f"{cliente_actual.get('nombre', '')} {cliente_actual.get('apellidos', '')}")
        dni = resumen.get("dni", cliente_actual.get('dni', ''))
        nombre_membresia = resumen.get("nombre_membresia", "Membresía")
        monto = resumen.get("monto", 0.0)

        contenido_exito = ft.Column([
            # Ícono de pendiente
            ft.Container(
                content=ft.Icon(
                    ft.Icons.SCHEDULE_ROUNDED,
                    size=Theme.ICON_SIZE["2xl"],
                    color=Theme.WARNING
                ),
                width=120,
                height=120,
                bgcolor="#1A1A1A",
                border_radius=60,
                border=ft.border.all(4, Theme.WARNING),
                alignment=ft.alignment.center,
                shadow=Theme.get_shadow("lg"),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            ft.Text(
                "¡RENOVACIÓN PENDIENTE!",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["extrabold"],
                color=Theme.WARNING,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Text(
                f"Hola, {nombre_completo}",
                size=Theme.FONT_SIZE["xl"],
                weight=Theme.FONT_WEIGHT["medium"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Información de la renovación
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Información de Renovación",
                        size=Theme.FONT_SIZE["xl"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.PRIMARY,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=Theme.SPACING["md"]),
                    ft.Row([
                        ft.Icon(ft.Icons.BADGE_ROUNDED, color=Theme.PRIMARY, size=28),
                        ft.Text(f"DNI: {dni}", size=Theme.FONT_SIZE["lg"]),
                    ], spacing=Theme.SPACING["sm"]),
                    ft.Row([
                        ft.Icon(ft.Icons.CARD_MEMBERSHIP_ROUNDED, color=Theme.WARNING, size=28),
                        ft.Text(f"Membresía: {nombre_membresia}",
                               size=Theme.FONT_SIZE["lg"]),
                    ], spacing=Theme.SPACING["sm"]),
                    ft.Row([
                        ft.Icon(ft.Icons.ATTACH_MONEY_ROUNDED, color=Theme.WARNING, size=28),
                        ft.Text(f"Monto: S/ {monto:.2f}",
                               size=Theme.FONT_SIZE["lg"],
                               weight=Theme.FONT_WEIGHT["semibold"],
                               color=Theme.WARNING),
                    ], spacing=Theme.SPACING["sm"]),
                    ft.Divider(color=Theme.BORDER_LIGHT, height=15),
                    ft.Row([
                        ft.Icon(ft.Icons.PAYMENT_ROUNDED, color=Theme.PRIMARY, size=28),
                        ft.Text(f"Método de pago: {metodo_pago}",
                               size=Theme.FONT_SIZE["lg"],
                               weight=Theme.FONT_WEIGHT["bold"],
                               color=Theme.PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),
                ], spacing=Theme.SPACING["md"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["xl"],
                border=ft.border.all(2, Theme.BORDER_LIGHT),
                shadow=Theme.get_shadow("lg"),
                width=600,
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Alerta de confirmación pendiente
            create_alert_card(
                f"PAGO CON {metodo_pago.upper()} - CONFIRMACIÓN PENDIENTE\n\n"
                "El personal del gimnasio ha sido notificado. "
                "Por favor, espera la confirmación del pago por parte del administrador.",
                "warning"
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Botón volver
            ft.Container(
                content=create_large_button(
                    "Finalizar",
                    lambda e: volver_a_inicio(),
                    icon=ft.Icons.HOME_ROUNDED,
                    bgcolor=Theme.PRIMARY
                ),
                width=280,
            )

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

        # Layout con background
        background_existe = os.path.exists(BACKGROUND_IMAGE)

        if background_existe:
            main_container = ft.Stack([
                ft.Image(
                    src=BACKGROUND_IMAGE,
                    fit=ft.ImageFit.COVER,
                    width=float('inf'),
                    height=float('inf'),
                ),
                ft.Container(bgcolor=Theme.OVERLAY_DARK, expand=True),
                ft.Container(
                    content=ft.Column(
                        [contenido_exito],
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=Theme.SPACING["3xl"],
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ], expand=True)
        else:
            main_container = ft.Container(
                content=ft.Column(
                    [contenido_exito],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["3xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.center
            )

        page.controls.clear()
        page.add(main_container)
        page.update()

    # ==================== FIN FUNCIONES RENOVACIÓN ====================

    def volver_a_inicio():
        """Volver a la pantalla inicial"""
        on_back()

    def on_dni_submit(e):
        """Manejar submit del campo DNI (Enter)"""
        registrar_asistencia_cliente(e)

    # Configurar eventos
    btn_registrar.on_click = registrar_asistencia_cliente
    dni_input.on_submit = on_dni_submit

    # ==================== VISTA PRINCIPAL DE ASISTENCIA ====================

    # Header moderno con icono glow
    header = ft.Container(
        content=ft.Column([
            # Icono con efecto glow
            ft.Container(
                content=ft.Icon(
                    ft.Icons.HOW_TO_REG_ROUNDED,
                    size=64,
                    color=Theme.SUCCESS
                ),
                width=120,
                height=120,
                bgcolor="rgba(76, 175, 80, 0.1)",
                border_radius=60,
                border=ft.border.all(3, Theme.SUCCESS),
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=25,
                    color="rgba(76, 175, 80, 0.3)",
                    offset=ft.Offset(0, 0),
                ),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            ft.Text(
                "Registro de Asistencia",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["extrabold"],
                color=Theme.PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Container(height=Theme.SPACING["sm"]),

            ft.Text(
                "Ingresa tu DNI para registrar tu asistencia",
                size=Theme.FONT_SIZE["lg"],
                color=Theme.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
                weight=Theme.FONT_WEIGHT["medium"],
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        margin=ft.margin.only(bottom=Theme.SPACING["2xl"]),
    )

    # Card principal con formulario
    card_formulario = ft.Container(
        content=ft.Column([
            # Instrucciones minimal
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, color=Theme.PRIMARY, size=24),
                        ft.Text(
                            "¿Cómo registrar tu asistencia?",
                            size=Theme.FONT_SIZE["lg"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=Theme.TEXT_PRIMARY
                        )
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["md"]),

                    ft.Text("1. Ingresa tu DNI (8 dígitos)", size=Theme.FONT_SIZE["md"], color=Theme.TEXT_SECONDARY),
                    ft.Text("2. Presiona 'Registrar Asistencia'", size=Theme.FONT_SIZE["md"], color=Theme.TEXT_SECONDARY),
                    ft.Text("3. ¡Listo! Tu asistencia quedará registrada", size=Theme.FONT_SIZE["md"], color=Theme.TEXT_SECONDARY),
                ], spacing=Theme.SPACING["sm"]),
                padding=Theme.SPACING["xl"],
                bgcolor=Theme.CARD_BG,
                border_radius=Theme.RADIUS["lg"],
                border=ft.border.all(1, Theme.BORDER_LIGHT),
                shadow=Theme.get_shadow("sm"),
            ),

            ft.Container(height=Theme.SPACING["3xl"]),

            # Input DNI
            dni_input,

            ft.Container(height=Theme.SPACING["xl"]),

            # Mensajes
            mensaje_container,

            ft.Container(height=Theme.SPACING["xl"]),

            # Botones
            ft.Row([
                create_back_button(lambda e: on_back()),
                btn_registrar,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True)

        ], spacing=0),
        width=700,
        padding=Theme.SPACING["3xl"],
        bgcolor=Theme.CARD_BG,
        border_radius=Theme.RADIUS["2xl"],
        border=ft.border.all(1, Theme.BORDER_LIGHT),
        shadow=Theme.get_shadow("xl"),
    )

    # Contenido principal
    contenido_principal = ft.Column([
        header,
        card_formulario,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Layout con background
    background_existe = os.path.exists(BACKGROUND_IMAGE)

    if background_existe:
        main_container = ft.Stack([
            ft.Image(
                src=BACKGROUND_IMAGE,
                fit=ft.ImageFit.COVER,
                width=float('inf'),
                height=float('inf'),
            ),
            ft.Container(
                bgcolor=Theme.OVERLAY_DARK,
                expand=True,
            ),
            ft.Container(
                content=contenido_principal,
                padding=Theme.SPACING["4xl"],
                expand=True,
                alignment=ft.alignment.center
            ),
        ], expand=True)
    else:
        main_container = ft.Container(
            content=contenido_principal,
            padding=Theme.SPACING["4xl"],
            bgcolor=Theme.BACKGROUND_DARK,
            expand=True,
            alignment=ft.alignment.center
        )

    # Limpiar y mostrar
    page.controls.clear()
    page.add(main_container)
    page.update()

    # Enfocar el campo DNI automáticamente
    dni_input.focus()
