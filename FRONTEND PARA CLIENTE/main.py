"""
BLESSED GYM - Frontend para Cliente (Tablet)
Aplicación para registro de nuevos clientes y asistencias

Flujo:
1. Pantalla Inicial: Registrarse / Asistencia
2. Registro: Datos personales → Selección membresía → Confirmación → Registro
3. Asistencia: DNI → Verificación → Registro de asistencia + Alerta membresía
"""

import flet as ft
import sys
import os

# Agregar paths para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from config.theme import Theme
from config.settings import APP_TITLE, APP_WIDTH, APP_HEIGHT, API_BASE_URL, API_TIMEOUT
from services.api_service import APIService
from views.pantalla_inicial import show_pantalla_inicial
from views.registro_view import show_registro_view
from views.asistencia_view import show_asistencia_view


def main(page: ft.Page):
    """
    Función principal de la aplicación

    Args:
        page: Página principal de Flet
    """

    # ==================== CONFIGURACIÓN DE LA PÁGINA ====================

    page.title = APP_TITLE
    page.window.width = APP_WIDTH
    page.window.height = APP_HEIGHT
    page.window.resizable = True
    page.padding = 0
    page.spacing = 0
    page.bgcolor = Theme.BACKGROUND_DARK

    # Prevenir que se cierre accidentalmente en modo fullscreen
    page.window.prevent_close = False

    # ==================== SERVICIOS ====================

    api_service = APIService(base_url=API_BASE_URL, timeout=API_TIMEOUT)

    # ==================== NAVEGACIÓN ====================

    def navegar_a_pantalla_inicial():
        """Navegar a la pantalla inicial"""
        show_pantalla_inicial(page, on_navigate=navegar_desde_inicial)

    def navegar_desde_inicial(destino: str):
        """
        Navegar desde la pantalla inicial

        Args:
            destino: "registro" o "asistencia"
        """
        if destino == "registro":
            show_registro_view(page, api_service, on_back=navegar_a_pantalla_inicial)
        elif destino == "asistencia":
            show_asistencia_view(page, api_service, on_back=navegar_a_pantalla_inicial)

    # ==================== INICIALIZACIÓN ====================

    def verificar_conexion_backend():
        """Verificar conexión con el backend al inicio"""
        try:
            if api_service.health_check():
                print("✅ Conexión con el backend establecida")
                return True
            else:
                print("⚠️ No se pudo conectar con el backend")
                mostrar_error_conexion()
                return False
        except Exception as e:
            print(f"❌ Error al verificar conexión con backend: {e}")
            mostrar_error_conexion()
            return False

    def mostrar_error_conexion():
        """Mostrar pantalla de error de conexión"""
        from components.cards import create_alert_card
        from components.buttons import create_large_button

        contenido_error = ft.Column([
            ft.Icon(
                ft.Icons.CLOUD_OFF,
                size=Theme.ICON_SIZE["2xl"] * 2,
                color=Theme.ERROR
            ),
            ft.Container(height=Theme.SPACING["xl"]),
            ft.Text(
                "Error de Conexión",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.ERROR,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=Theme.SPACING["lg"]),
            create_alert_card(
                f"No se pudo conectar con el servidor.\n\n"
                f"URL del servidor: {API_BASE_URL}\n\n"
                f"Por favor, verifica que el backend esté en ejecución.",
                "error"
            ),
            ft.Container(height=Theme.SPACING["2xl"]),
            create_large_button(
                "Reintentar",
                lambda e: iniciar_aplicacion(),
                icon=ft.Icons.REFRESH,
                bgcolor=Theme.INFO
            )
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

        page.controls.clear()
        page.add(ft.Container(
            content=contenido_error,
            padding=Theme.SPACING["5xl"],
            bgcolor=Theme.BACKGROUND_DARK,
            expand=True,
            alignment=ft.alignment.center
        ))
        page.update()

    def iniciar_aplicacion():
        """Iniciar la aplicación"""
        # Verificar conexión con backend
        if verificar_conexion_backend():
            # Mostrar pantalla inicial
            navegar_a_pantalla_inicial()
        # Si falla, mostrar_error_conexion() ya se encarga de mostrar el error

    # ==================== INICIO ====================

    # Iniciar la aplicación
    iniciar_aplicacion()


# ==================== PUNTO DE ENTRADA ====================

if __name__ == "__main__":
    print("=" * 60)
    print("BLESSED GYM - Frontend Cliente (Tablet)")
    print("=" * 60)
    print(f"Backend API: {API_BASE_URL}")
    print("Iniciando aplicación...")
    print("=" * 60)

    # Ejecutar aplicación Flet
    ft.app(target=main)
