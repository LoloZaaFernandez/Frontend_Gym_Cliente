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
from services.auth_service import AuthService

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
from ui.views.admin.reportes_view import show_reportes_view

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

    # Inicializar servicio de autenticación
    auth_service = AuthService()

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
            elif section_name == "Reportes":
                show_reportes_view(page, auth_service, navigate_to_section, section_name)
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