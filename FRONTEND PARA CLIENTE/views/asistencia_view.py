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

    def mostrar_mensaje(mensaje: str, tipo: str = "error"):
        """Mostrar mensaje (error, success, warning, info)"""
        mensaje_container.content = create_alert_card(mensaje, tipo)
        mensaje_container.update()

    def limpiar_mensaje():
        """Limpiar mensaje"""
        mensaje_container.content = None
        mensaje_container.update()

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

            # 2. Verificar que el cliente esté activo
            if cliente.get("estado", "") != "Activo":
                mostrar_mensaje(
                    f"El cliente {cliente.get('nombre', '')} {cliente.get('apellidos', '')} "
                    f"está en estado: {cliente.get('estado', 'Desconocido')}.\n"
                    "Por favor, contacta al personal del gimnasio.",
                    "error"
                )
                return

            # 3. Verificar si la membresía está por vencer o vencida
            alerta_membresia = api_service.verificar_membresia_por_vencer(cliente, dias_alerta=5)

            # Si la membresía está vencida, no permitir asistencia
            if alerta_membresia and alerta_membresia["tipo"] == "vencida":
                mostrar_mensaje(
                    f"{alerta_membresia['mensaje']}\n\n"
                    "No puedes registrar asistencia con membresía vencida. "
                    "Por favor, renueva tu membresía.",
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

        except Exception as e:
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
