"""
Utilidades UI - Mensajes
Funciones para mostrar mensajes, notificaciones y snackbars
"""
import flet as ft
from config.theme import Theme


def mostrar_mensaje(page: ft.Page, mensaje: str, error=False, duration=3000):
    """
    Mostrar mensaje temporal (SnackBar)
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
    page.snack_bar = ft.SnackBar(
        content=ft.Text(
            mensaje,
            color=ft.Colors.WHITE,
            weight=Theme.FONT_WEIGHT["medium"]
        ),
        bgcolor=Theme.ERROR if error else Theme.SUCCESS,
        duration=duration,
        action="Cerrar",
        action_color=ft.Colors.WHITE,
    )
    page.snack_bar.open = True
    page.update()


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
    mostrar_mensaje(page, mensaje, error=False, duration=duration)


def mostrar_error(page: ft.Page, mensaje: str, duration=4000):
    """
    Mostrar mensaje de error (rojo)

    Args:
        page: Instancia de ft.Page
        mensaje: Texto del mensaje
        duration: Duración en milisegundos (default: 4s para errores)

    Ejemplo:
        >>> mostrar_error(page, "No se pudo conectar con el servidor")
    """
    mostrar_mensaje(page, mensaje, error=True, duration=duration)


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
