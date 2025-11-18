"""
Utilidades UI - Mensajes
Funciones para mostrar mensajes, notificaciones y snackbars
"""
import flet as ft
from config.theme import Theme


def mostrar_mensaje(page: ft.Page, mensaje: str, error=False, duration=3000):
    """
    Mostrar mensaje temporal (Banner)
    Esta función reemplaza todas las instancias de mostrar_mensaje() en las vistas

    Args:
        page: Instancia de ft.Page
        mensaje: Texto del mensaje
        error: Si es un mensaje de error (rojo) o éxito (verde)
        duration: Duración en milisegundos (default: 3000ms / 3s)

    Ejemplo:
        >>> mostrar_mensaje(page, "Cliente guardado correctamente")
        >>> mostrar_mensaje(page, "Error al guardar", error=True)
    """
    try:
        print(f"DEBUG MESSAGES: Creando Banner con mensaje: '{mensaje}'")

        # Cerrar banner anterior si existe
        if hasattr(page, 'banner') and page.banner:
            page.banner.open = False

        # Crear nuevo banner
        page.banner = ft.Banner(
            bgcolor=Theme.ERROR if error else Theme.SUCCESS,
            leading=ft.Icon(
                ft.Icons.ERROR_OUTLINE if error else ft.Icons.CHECK_CIRCLE_OUTLINE,
                color=ft.Colors.WHITE,
                size=30
            ),
            content=ft.Text(
                mensaje,
                color=ft.Colors.WHITE,
                weight=Theme.FONT_WEIGHT["bold"],
                size=16
            ),
            actions=[
                ft.TextButton("CERRAR", on_click=lambda _: cerrar_banner(page), style=ft.ButtonStyle(color=ft.Colors.WHITE))
            ],
        )

        print("DEBUG MESSAGES: Banner creado, abriendo...")
        page.banner.open = True

        # Auto-cerrar después de duration
        import threading
        def auto_cerrar():
            import time
            time.sleep(duration / 1000)
            try:
                if page.banner and page.banner.open:
                    page.banner.open = False
                    page.update()
            except:
                pass

        threading.Thread(target=auto_cerrar, daemon=True).start()

        print("DEBUG MESSAGES: Actualizando page...")
        page.update()
        print("DEBUG MESSAGES: Page actualizado exitosamente - Banner visible en la parte superior")
    except Exception as e:
        print(f"DEBUG MESSAGES: ERROR CRITICO en mostrar_mensaje: {e}")
        import traceback
        traceback.print_exc()

def cerrar_banner(page: ft.Page):
    """Cerrar el banner actual"""
    try:
        if page.banner:
            page.banner.open = False
            page.update()
    except:
        pass


def mostrar_exito(page: ft.Page, mensaje: str, duration=3000):
    """
    Mostrar mensaje de éxito (verde)

    Args:
        page: Instancia de ft.Page
        mensaje: Texto del mensaje
        duration: Duración en milisegundos

    Ejemplo:
        >>> mostrar_exito(page, "Operación completada exitosamente")
    """
    try:
        print(f"DEBUG MESSAGES: Mostrando exito: {mensaje}")
        mostrar_mensaje(page, mensaje, error=False, duration=duration)
        print("DEBUG MESSAGES: Mensaje de exito mostrado correctamente")
    except Exception as e:
        print(f"DEBUG MESSAGES: ERROR al mostrar mensaje: {e}")
        import traceback
        traceback.print_exc()


def mostrar_error(page: ft.Page, mensaje: str, duration=8000):
    """
    Mostrar mensaje de error (rojo)

    Args:
        page: Instancia de ft.Page
        mensaje: Texto del mensaje
        duration: Duración en milisegundos (default: 4s para errores)

    Ejemplo:
        >>> mostrar_error(page, "No se pudo conectar con el servidor")
    """
    try:
        print(f"DEBUG MESSAGES: Mostrando error: {mensaje}")
        mostrar_mensaje(page, mensaje, error=True, duration=duration)
        print("DEBUG MESSAGES: Mensaje de error mostrado correctamente")
    except Exception as e:
        print(f"DEBUG MESSAGES: ERROR al mostrar mensaje: {e}")
        import traceback
        traceback.print_exc()


def mostrar_advertencia(page: ft.Page, mensaje: str, duration=3500):
    """
    Mostrar mensaje de advertencia (naranja)

    Args:
        page: Instancia de ft.Page
        mensaje: Texto del mensaje
        duration: Duración en milisegundos

    Ejemplo:
        >>> mostrar_advertencia(page, "La membresía vence pronto")
    """
    page.snack_bar = ft.SnackBar(
        content=ft.Text(
            mensaje,
            color=ft.Colors.WHITE,
            weight=Theme.FONT_WEIGHT["medium"]
        ),
        bgcolor=Theme.WARNING,
        duration=duration,
        action="Cerrar",
        action_color=ft.Colors.WHITE,
    )
    page.snack_bar.open = True
    page.update()


def mostrar_info(page: ft.Page, mensaje: str, duration=3000):
    """
    Mostrar mensaje informativo (azul)

    Args:
        page: Instancia de ft.Page
        mensaje: Texto del mensaje
        duration: Duración en milisegundos

    Ejemplo:
        >>> mostrar_info(page, "Nuevo cliente registrado")
    """
    page.snack_bar = ft.SnackBar(
        content=ft.Text(
            mensaje,
            color=ft.Colors.WHITE,
            weight=Theme.FONT_WEIGHT["medium"]
        ),
        bgcolor=Theme.INFO,
        duration=duration,
        action="Cerrar",
        action_color=ft.Colors.WHITE,
    )
    page.snack_bar.open = True
    page.update()


def mostrar_loading(page: ft.Page, mensaje="Cargando..."):
    """
    Mostrar indicador de carga (sin auto-cerrar)

    Args:
        page: Instancia de ft.Page
        mensaje: Texto del mensaje

    Nota: Debes cerrar manualmente con page.snack_bar.open = False

    Ejemplo:
        >>> mostrar_loading(page, "Guardando datos...")
        >>> # ... hacer operación ...
        >>> page.snack_bar.open = False
        >>> page.update()
    """
    page.snack_bar = ft.SnackBar(
        content=ft.Row([
            ft.ProgressRing(width=20, height=20, stroke_width=2, color=ft.Colors.WHITE),
            ft.Text(
                mensaje,
                color=ft.Colors.WHITE,
                weight=Theme.FONT_WEIGHT["medium"]
            ),
        ], spacing=Theme.SPACING["md"]),
        bgcolor=Theme.PRIMARY,
        duration=60000,  # 60 segundos (debe cerrarse manualmente)
    )
    page.snack_bar.open = True
    page.update()
