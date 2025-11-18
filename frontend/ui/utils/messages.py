"""
Utilidades UI - Mensajes
Funciones para mostrar mensajes, notificaciones y snackbars
"""
import flet as ft
from config.theme import Theme


def mostrar_mensaje(page: ft.Page, mensaje: str, error=False, duration=3000):
    """
    Mostrar mensaje temporal usando overlay flotante
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
        print(f"DEBUG MESSAGES: Creando notificación flotante con mensaje: '{mensaje}'")

        import threading
        import time

        # Contenedor para la notificación
        def cerrar_notificacion():
            try:
                for control in page.overlay[:]:
                    if hasattr(control, '_es_notificacion_temporal'):
                        control.visible = False
                        page.overlay.remove(control)
                page.update()
                print("DEBUG MESSAGES: Notificación cerrada")
            except Exception as e:
                print(f"Error al cerrar notificación: {e}")

        # Crear notificación flotante en la parte superior derecha
        notificacion = ft.Container(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.ERROR_ROUNDED if error else ft.Icons.CHECK_CIRCLE_ROUNDED,
                        color=ft.Colors.WHITE,
                        size=28
                    ),
                    ft.Text(
                        mensaje,
                        color=ft.Colors.WHITE,
                        weight=Theme.FONT_WEIGHT["bold"],
                        size=16,
                        max_lines=3,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.WHITE,
                        icon_size=20,
                        on_click=lambda _: cerrar_notificacion(),
                        tooltip="Cerrar"
                    )
                ], spacing=12, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=Theme.ERROR if error else Theme.SUCCESS,
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                border_radius=Theme.RADIUS["lg"],
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=20,
                    color=ft.Colors.BLACK54,
                    offset=ft.Offset(0, 4),
                ),
                border=ft.border.all(2, ft.Colors.WHITE24),
                width=500,
            ),
            right=20,
            top=20,
            animate_opacity=300,
        )

        # Marcar como notificación temporal
        notificacion._es_notificacion_temporal = True

        # Remover notificaciones anteriores
        for control in page.overlay[:]:
            if hasattr(control, '_es_notificacion_temporal'):
                page.overlay.remove(control)

        # Agregar al overlay
        page.overlay.append(notificacion)
        print("DEBUG MESSAGES: Notificación agregada al overlay")

        page.update()
        print("DEBUG MESSAGES: Page actualizado - Notificación VISIBLE en esquina superior derecha")

        # Auto-cerrar después de duration
        def auto_cerrar():
            time.sleep(duration / 1000)
            cerrar_notificacion()

        threading.Thread(target=auto_cerrar, daemon=True).start()

    except Exception as e:
        print(f"DEBUG MESSAGES: ERROR CRITICO en mostrar_mensaje: {e}")
        import traceback
        traceback.print_exc()



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
