"""
Vista de Asistencia para Clientes Registrados
Flujo: ingresar DNI → verificar cliente → registrar asistencia → alerta si membresía por vencer
"""
import flet as ft
import sys
import os

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme
from config.settings import USUARIO_SISTEMA
from components.buttons import create_large_button, create_back_button, create_success_button
from components.inputs import create_dni_input
from components.cards import create_card_container, create_alert_card
from services.api_service import APIService


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

        controles_exito = [
            # Ícono de éxito
            ft.Container(
                content=ft.Icon(
                    ft.Icons.CHECK_CIRCLE,
                    size=Theme.ICON_SIZE["2xl"] * 2,
                    color=Theme.SUCCESS
                ),
                alignment=ft.alignment.center,
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Título
            ft.Text(
                "¡Asistencia Registrada!",
                size=Theme.FONT_SIZE["5xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.SUCCESS,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Text(
                f"Bienvenido, {cliente.get('nombre', '')} {cliente.get('apellidos', '')}",
                size=Theme.FONT_SIZE["2xl"],
                color=Theme.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Información del cliente
            create_card_container(
                content=ft.Column([
                    ft.Text("Información de Asistencia", size=Theme.FONT_SIZE["xl"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ft.Divider(color=Theme.BORDER_DEFAULT),
                    ft.Text(f"DNI: {cliente.get('dni', '')}", size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Fecha: {resultado_asistencia.get('fecha_asistencia', '')[:10]}",
                           size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Hora: {resultado_asistencia.get('fecha_asistencia', '')[11:19]}",
                           size=Theme.FONT_SIZE["lg"]),
                    ft.Divider(color=Theme.BORDER_DEFAULT),
                    ft.Text(f"Membresía válida hasta: {cliente.get('fecha_membresia', '')}",
                           size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["semibold"],
                           color=Theme.INFO),
                ], spacing=Theme.SPACING["sm"]),
                width=500
            ),
        ]

        # Agregar alerta de membresía por vencer (si aplica)
        if alerta_membresia:
            controles_exito.append(ft.Container(height=Theme.SPACING["lg"]))
            controles_exito.append(
                create_alert_card(
                    alerta_membresia["mensaje"],
                    "warning"
                )
            )

        controles_exito.extend([
            ft.Container(height=Theme.SPACING["2xl"]),

            # Botón volver
            create_large_button(
                "Finalizar",
                lambda e: volver_a_inicio(),
                icon=ft.Icons.HOME,
                bgcolor=Theme.SUCCESS
            )
        ])

        contenido_exito = ft.Column(
            controles_exito,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=Theme.SPACING["md"]
        )

        page.controls.clear()
        page.add(ft.Container(
            content=contenido_exito,
            padding=Theme.SPACING["5xl"],
            bgcolor=Theme.BACKGROUND_DARK,
            expand=True,
            alignment=ft.alignment.center
        ))
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

    # Vista principal de asistencia
    contenido_principal = ft.Column([
        ft.Text(
            "Registro de Asistencia",
            size=Theme.FONT_SIZE["4xl"],
            weight=Theme.FONT_WEIGHT["bold"],
            color=Theme.PRIMARY
        ),
        ft.Text(
            "Ingresa tu DNI para registrar tu asistencia",
            size=Theme.FONT_SIZE["2xl"],
            color=Theme.TEXT_SECONDARY
        ),

        ft.Container(height=Theme.SPACING["3xl"]),

        # Card con instrucciones
        create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO, color=Theme.INFO, size=Theme.ICON_SIZE["lg"]),
                    ft.Text(
                        "Instrucciones:",
                        size=Theme.FONT_SIZE["xl"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    )
                ], spacing=Theme.SPACING["md"]),
                ft.Divider(color=Theme.BORDER_DEFAULT),
                ft.Text("1. Ingresa tu DNI (8 dígitos)", size=Theme.FONT_SIZE["lg"]),
                ft.Text("2. Presiona 'Registrar Asistencia'", size=Theme.FONT_SIZE["lg"]),
                ft.Text("3. ¡Listo! Tu asistencia quedará registrada", size=Theme.FONT_SIZE["lg"]),
            ], spacing=Theme.SPACING["sm"]),
            width=600,
            bgcolor=Theme.CARD_BG_LIGHT
        ),

        ft.Container(height=Theme.SPACING["2xl"]),

        # Input DNI
        dni_input,

        ft.Container(height=Theme.SPACING["2xl"]),

        # Mensajes
        mensaje_container,

        ft.Container(height=Theme.SPACING["xl"]),

        # Botones
        ft.Row([
            create_back_button(lambda e: on_back()),
            btn_registrar,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=600)

    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

    # Limpiar y mostrar
    page.controls.clear()
    page.add(ft.Container(
        content=contenido_principal,
        padding=Theme.SPACING["5xl"],
        bgcolor=Theme.BACKGROUND_DARK,
        expand=True,
        alignment=ft.alignment.top_center
    ))
    page.update()

    # Enfocar el campo DNI automáticamente
    dni_input.focus()
