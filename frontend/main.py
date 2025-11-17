"""
BLESSED GYM - Sistema de Gestión Integral
Archivo principal CORREGIDO

Este archivo coordina la navegación entre las diferentes vistas
y gestiona el estado de la aplicación usando servicios.
"""

import flet as ft
from config.settings import (
    APP_TITLE, APP_WIDTH, APP_HEIGHT, BACKGROUND_DARK
)
from config.theme import BlessedTheme as Theme
from services.auth_service import AuthService
from services.api_service import APIService
from services.websocket_service import WebSocketService

# Vistas de autenticación
from ui.views.auth.role_selection import show_role_selection
from ui.views.auth.admin_login import show_admin_login
from ui.views.auth.client_login import show_client_login

# Vistas de administrador
from ui.views.admin.admin_dashboard import show_admin_dashboard
from ui.views.admin.clientes_view import show_clientes_view
from ui.views.admin.asistencia_view import show_asistencia_view
from ui.views.admin.admin_membresias_view import show_admin_membresias_view
from ui.views.admin.pos_view import show_pos_view
from ui.views.admin.productos_view import show_productos_view
from ui.views.admin.alertas_productos_view import show_alertas_productos_view
from ui.views.admin.reportes_view import show_reportes_view
from ui.views.admin.finanzas_view import show_finanzas_view

# Vistas de cliente
from ui.views.client.client_dashboard import show_client_dashboard
from ui.views.client.perfil_cliente_view import show_perfil_cliente_view
from ui.views.client.membresias_view import show_membresias_view
from ui.views.client.cliente_asistencias_view import show_cliente_asistencias_view

# Otras vistas
from ui.views.simple_message import show_simple_message


def main(page: ft.Page):
    """
    Función principal de la aplicación
    Configura la página y maneja la navegación entre vistas
    """
    # Configuración de la página
    page.title = APP_TITLE
    page.window.width = APP_WIDTH
    page.window.height = APP_HEIGHT
    page.window.resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BACKGROUND_DARK
    page.padding = 0

    # Inicializar servicios
    auth_service = AuthService()
    api_service = APIService()

    # ==========================================
    # VENTANA FLOTANTE PARA CONFIRMACIÓN DE REGISTROS
    # ==========================================
    # Variable para controlar visibilidad
    ventana_confirmacion_container = None

    def crear_ventana_confirmacion(datos: dict):
        """Crear y mostrar ventana flotante de confirmación"""
        nonlocal ventana_confirmacion_container

        print(f"🎯 [GLOBAL] Creando ventana para: {datos.get('nombre_completo')}")

        id_registro = datos.get("id_registro_pendiente")
        nombre_completo = datos.get("nombre_completo", "")
        monto = datos.get("monto", 0)
        metodo_pago = datos.get("metodo_pago", "")
        dni = datos.get("dni", "")
        nombre_membresia = datos.get("nombre_membresia", "")
        es_renovacion = datos.get("es_renovacion", False)

        def cerrar_ventana(e=None):
            print("🔴 Cerrando ventana")
            ventana_confirmacion_container.visible = False
            page.update()

        def confirmar_pago(e):
            try:
                print(f"✅ Confirmando registro {id_registro}...")
                resultado = api_service.confirmar_registro_pendiente(id_registro)
                print(f"✅ Resultado: {resultado}")

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"✅ Registro confirmado: {nombre_completo}"),
                    bgcolor=ft.Colors.GREEN
                )
                page.snack_bar.open = True
                cerrar_ventana()

            except Exception as error:
                print(f"❌ Error: {error}")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Error: {str(error)}"),
                    bgcolor=ft.Colors.RED
                )
                page.snack_bar.open = True
                page.update()

        def rechazar_pago(e):
            try:
                print(f"❌ Rechazando registro {id_registro}...")
                resultado = api_service.rechazar_registro_pendiente(id_registro)
                print(f"❌ Resultado: {resultado}")

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Registro rechazado: {nombre_completo}"),
                    bgcolor=ft.Colors.ORANGE
                )
                page.snack_bar.open = True
                cerrar_ventana()

            except Exception as error:
                print(f"❌ Error: {error}")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Error: {str(error)}"),
                    bgcolor=ft.Colors.RED
                )
                page.snack_bar.open = True
                page.update()

        # Crear ventana flotante con diseño BLESSED GYM
        ventana_confirmacion_container.content = ft.Container(
            content=ft.Column([
                # Header con gradiente naranja
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.NOTIFICATIONS_ACTIVE_ROUNDED,
                                color=ft.Colors.WHITE,
                                size=36
                            ),
                            bgcolor=Theme.WARNING,
                            border_radius=Theme.RADIUS["full"],
                            padding=12,
                        ),
                        ft.Column([
                            ft.Text(
                                "RENOVACIÓN PENDIENTE" if es_renovacion else "NUEVO REGISTRO PENDIENTE",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                "Confirma si el cliente realizó el pago de renovación" if es_renovacion else "Confirma si el cliente realizó el pago",
                                size=13,
                                color=ft.Colors.WHITE70,
                            ),
                        ], spacing=2, expand=True),
                    ], spacing=15),
                    bgcolor=Theme.PRIMARY,
                    padding=20,
                    border_radius=ft.border_radius.only(top_left=16, top_right=16),
                ),

                # Contenido principal
                ft.Container(
                    content=ft.Column([
                        # Pregunta principal
                        ft.Container(
                            content=ft.Text(
                                f"¿{nombre_completo} realizó el pago {'de renovación' if es_renovacion else ''}?",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=Theme.TEXT_PRIMARY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            padding=ft.padding.only(bottom=20),
                        ),

                        # Monto destacado
                        ft.Container(
                            content=ft.Column([
                                ft.Text("MONTO A PAGAR", size=12, color=Theme.TEXT_SECONDARY),
                                ft.Text(
                                    f"S/ {monto:.2f}",
                                    size=36,
                                    weight=ft.FontWeight.BOLD,
                                    color=Theme.SUCCESS,
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                            bgcolor=Theme.CARD_BG_LIGHT,
                            padding=20,
                            border_radius=Theme.RADIUS["xl"],
                            alignment=ft.alignment.center,
                        ),

                        ft.Container(height=20),

                        # Detalles
                        ft.Container(
                            content=ft.Column([
                                # DNI
                                ft.Row([
                                    ft.Icon(ft.Icons.BADGE_ROUNDED, color=Theme.PRIMARY, size=22),
                                    ft.Column([
                                        ft.Text("DNI", size=11, color=Theme.TEXT_SECONDARY),
                                        ft.Text(dni, size=15, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                                    ], spacing=2, expand=True),
                                ], spacing=12),

                                ft.Divider(color=Theme.BORDER_LIGHT, height=20),

                                # Membresía
                                ft.Row([
                                    ft.Icon(ft.Icons.CARD_MEMBERSHIP_ROUNDED, color=Theme.INFO, size=22),
                                    ft.Column([
                                        ft.Text("MEMBRESÍA", size=11, color=Theme.TEXT_SECONDARY),
                                        ft.Text(nombre_membresia, size=15, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                                    ], spacing=2, expand=True),
                                ], spacing=12),

                                ft.Divider(color=Theme.BORDER_LIGHT, height=20),

                                # Método de pago
                                ft.Row([
                                    ft.Icon(ft.Icons.PAYMENT_ROUNDED, color=Theme.WARNING, size=22),
                                    ft.Column([
                                        ft.Text("MÉTODO DE PAGO", size=11, color=Theme.TEXT_SECONDARY),
                                        ft.Text(metodo_pago, size=15, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                                    ], spacing=2, expand=True),
                                ], spacing=12),
                            ], spacing=0),
                            bgcolor=Theme.CARD_BG,
                            padding=20,
                            border_radius=Theme.RADIUS["lg"],
                            border=ft.border.all(1, Theme.BORDER_DEFAULT),
                        ),
                    ], spacing=0),
                    padding=25,
                    bgcolor=Theme.BACKGROUND_MEDIUM,
                ),

                # Footer con botones
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.CLOSE_ROUNDED, size=20),
                                    ft.Text("Rechazar", size=15, weight=ft.FontWeight.BOLD),
                                ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                                on_click=rechazar_pago,
                                bgcolor=Theme.ERROR,
                                color=ft.Colors.WHITE,
                                height=50,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["lg"]),
                                ),
                            ),
                            expand=1,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=20),
                                    ft.Text("Confirmar Pago", size=15, weight=ft.FontWeight.BOLD),
                                ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                                on_click=confirmar_pago,
                                bgcolor=Theme.SUCCESS,
                                color=ft.Colors.WHITE,
                                height=50,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS["lg"]),
                                ),
                            ),
                            expand=1,
                        ),
                    ], spacing=15),
                    padding=20,
                    bgcolor=Theme.CARD_BG_DARK,
                    border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16),
                ),
            ], spacing=0),
            bgcolor=Theme.BACKGROUND_MEDIUM,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=30,
                color=ft.Colors.BLACK54,
                offset=ft.Offset(0, 10),
            ),
            border=ft.border.all(2, Theme.BORDER_DEFAULT),
            width=520,
        )

        ventana_confirmacion_container.visible = True
        page.update()
        print(f"✅ [GLOBAL] Ventana mostrada y visible")

    # ==========================================
    # WEBSOCKET GLOBAL PARA NOTIFICACIONES
    # ==========================================
    def on_websocket_message(message: dict):
        """Handler para mensajes del WebSocket"""
        tipo = message.get("tipo")
        print(f"📩 [MAIN] WebSocket mensaje: {tipo}")

        if tipo == "registro_pendiente" or tipo == "renovacion_pendiente":
            datos = message.get("datos", {})
            # Publicar en pubsub para mostrar en el hilo principal
            page.pubsub.send_all(message)

    def on_pubsub_message(message):
        """Handler del pubsub (ejecuta en hilo principal)"""
        tipo = message.get("tipo")
        print(f"🎯 [PUBSUB] Tipo: {tipo}")
        if tipo == "registro_pendiente" or tipo == "renovacion_pendiente":
            datos = message.get("datos", {})
            es_renovacion = datos.get("es_renovacion", False)
            print(f"🎯 [PUBSUB] {'Renovación' if es_renovacion else 'Registro'} pendiente detectado")
            print(f"🎯 [PUBSUB] Llamando a crear_ventana_confirmacion...")
            crear_ventana_confirmacion(datos)

    # Suscribirse al pubsub
    page.pubsub.subscribe(on_pubsub_message)

    # Inicializar contenedor flotante en overlay (siempre presente pero invisible)
    ventana_confirmacion_container = ft.Container(
        content=ft.Container(),  # Vacío inicialmente
        visible=False,  # Oculto por defecto
        alignment=ft.alignment.center,
        expand=True,
    )
    page.overlay.append(ventana_confirmacion_container)
    print("✅ Ventana flotante agregada al overlay")

    # Inicializar WebSocket solo para admin
    ws_service = None
    def iniciar_websocket_si_es_admin():
        """Iniciar WebSocket cuando el usuario sea admin"""
        nonlocal ws_service
        if auth_service.get_current_role() == 'admin' and ws_service is None:
            ws_service = WebSocketService(on_message_callback=on_websocket_message)
            ws_service.connect()
            print("✅ WebSocket iniciado para admin")

    # --- FUNCIONES DE NAVEGACIÓN ---

    def navigate_to_role_selection(e=None):
        """Navegar a la pantalla de selección de rol"""
        auth_service.logout()
        show_role_selection(
            page,
            on_admin_click=navigate_to_admin_login,
            on_client_click=navigate_to_client_login
        )

    def navigate_to_admin_login():
        """Navegar al login de administrador"""
        show_admin_login(
            page,
            auth_service,
            on_success=navigate_to_admin_dashboard,
            on_back=navigate_to_role_selection
        )

    def navigate_to_client_login():
        """Navegar al login de cliente"""
        show_client_login(
            page,
            auth_service,
            on_success=navigate_to_client_dashboard,
            on_back=navigate_to_role_selection
        )

    def navigate_to_admin_dashboard():
        """Navegar al dashboard de administrador"""
        iniciar_websocket_si_es_admin()  # Iniciar WebSocket
        show_admin_dashboard(
            page,
            auth_service,
            on_logout=navigate_to_role_selection,
            on_section_click=navigate_to_section
        )

    def navigate_to_client_dashboard():
        """Navegar al dashboard de cliente"""
        show_client_dashboard(
            page,
            auth_service,
            on_logout=navigate_to_role_selection,
            on_section_click=navigate_to_section
        )

    def navigate_to_section(section_name: str):
        """
        Navegar a una sección específica

        Args:
            section_name: Nombre de la sección a mostrar
        """
        # Manejar logout (desde cualquier vista)
        if section_name == "logout":
            navigate_to_role_selection()
            return

        def go_back():
            if auth_service.get_current_role() == 'admin':
                navigate_to_admin_dashboard()
            else:
                navigate_to_client_dashboard()

        # Mapeo de secciones a vistas para Admin
        if auth_service.get_current_role() == 'admin':
            if section_name == "Dashboard":
                navigate_to_admin_dashboard()
            elif section_name == "Clientes":
                show_clientes_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "Membresias":
                show_admin_membresias_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "Asistencia":
                show_asistencia_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "POS":
                show_pos_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "Productos":
                show_productos_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "Alertas":
                show_alertas_productos_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "Reportes":
                show_reportes_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "Finanzas":
                show_finanzas_view(page, auth_service, navigate_to_section, section_name)
            else:
                show_simple_message(page, section_name, on_back=go_back)

        # Mapeo de secciones para Cliente
        else:
            if section_name == "Dashboard":
                navigate_to_client_dashboard()
            elif section_name == "Mi Perfil":
                show_perfil_cliente_view(
                    page,
                    auth_service,
                    navigate_to_section,
                    section_name,
                    on_navigate_membresias=lambda: navigate_to_section("Membresías")
                )
            elif section_name == "Membresías":
                show_membresias_view(page, auth_service, navigate_to_section, section_name)
            elif section_name == "Asistencias":
                show_cliente_asistencias_view(page, auth_service, navigate_to_section, section_name)
            else:
                show_simple_message(page, section_name, on_back=go_back)

    # --- INICIAR APLICACIÓN ---
    navigate_to_role_selection()


if __name__ == "__main__":
    ft.app(target=main)