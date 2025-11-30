"""
Vista de Registro de Nuevos Clientes - REDISEÑADA PARA TABLET
Flujo completo: datos personales → selección de membresía → confirmación → registro
"""
import flet as ft
import sys
import os

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme
from config.settings import USUARIO_SISTEMA, BACKGROUND_IMAGE
from components.buttons import create_large_button, create_back_button, create_success_button
from components.inputs import create_text_input, create_dni_input, create_phone_input, create_email_input
from components.cards import create_card_container, create_info_card, create_alert_card
from components.membership_card import create_membership_card
from services.api_service import APIService


def show_registro_view(page: ft.Page, api_service: APIService, on_back):
    """
    Mostrar vista de registro de nuevos clientes - RESPONSIVE

    Args:
        page: Instancia de la página
        api_service: Servicio API
        on_back: Función para volver a la pantalla inicial
    """

    # Obtener dimensiones de la página para cálculos responsive
    page_width = page.window.width or page.width or Theme.BASE_WIDTH
    page_height = page.window.height or page.height or Theme.BASE_HEIGHT

    # Estado del formulario
    form_data = {
        "dni": "",
        "nombre": "",
        "apellidos": "",
        "correo": "",
        "telefono": "",
        "id_membresia": None,
        "metodo_pago": "Efectivo"
    }

    opciones_membresias = []
    metodos_pago = []

    # Referencias a controles con dimensiones responsive
    dni_input = create_dni_input(page_width=page_width, page_height=page_height)
    nombre_input = create_text_input("Nombre", hint_text="Ej: Juan", icon=ft.Icons.PERSON, page_width=page_width, page_height=page_height)
    apellidos_input = create_text_input("Apellidos", hint_text="Ej: Pérez García", icon=ft.Icons.PERSON_OUTLINE, page_width=page_width, page_height=page_height)
    correo_input = create_email_input(page_width=page_width, page_height=page_height)
    telefono_input = create_phone_input(page_width=page_width, page_height=page_height)

    mensaje_error = ft.Container()
    btn_siguiente = create_success_button("Siguiente", None, icon=ft.Icons.ARROW_FORWARD, page_width=page_width, page_height=page_height)
    btn_registrar = create_success_button("Confirmar Registro", None, icon=ft.Icons.CHECK, page_width=page_width, page_height=page_height)

    # Contenedores de pasos
    paso1_container = ft.Container()
    paso2_container = ft.Container()
    paso3_container = ft.Container()

    paso_actual = ft.Ref[int]()
    paso_actual.current = 1

    def mostrar_error(mensaje: str):
        """Mostrar mensaje de error"""
        mensaje_error.content = create_alert_card(mensaje, "error", page_width=page_width)
        try:
            mensaje_error.update()
        except:
            # Si falla el update individual, actualizar toda la página
            page.update()

    def limpiar_error():
        """Limpiar mensaje de error"""
        mensaje_error.content = None
        try:
            mensaje_error.update()
        except:
            # Si falla el update individual, no hacer nada
            pass

    def validar_paso1() -> bool:
        """Validar datos del Paso 1"""
        limpiar_error()

        if not dni_input.value or len(dni_input.value) != 8:
            mostrar_error("El DNI debe tener 8 dígitos")
            return False

        if not nombre_input.value or len(nombre_input.value.strip()) < 2:
            mostrar_error("El nombre es requerido (mínimo 2 caracteres)")
            return False

        if not apellidos_input.value or len(apellidos_input.value.strip()) < 2:
            mostrar_error("Los apellidos son requeridos (mínimo 2 caracteres)")
            return False

        if not correo_input.value or "@" not in correo_input.value:
            mostrar_error("El correo electrónico no es válido")
            return False

        if not telefono_input.value or len(telefono_input.value) != 9:
            mostrar_error("El teléfono debe tener 9 dígitos")
            return False

        return True

    def cargar_opciones_registro():
        """Cargar opciones de membresías y métodos de pago"""
        nonlocal opciones_membresias, metodos_pago

        try:
            print("Cargando opciones de registro...")
            opciones = api_service.get_opciones_registro()
            print(f"Opciones recibidas: {opciones}")

            # Limpiar y actualizar las listas (no reasignar)
            opciones_membresias.clear()
            # El backend devuelve "membresias_disponibles" no "membresias"
            membresias_raw = opciones.get("membresias_disponibles", opciones.get("membresias", []))

            # Normalizar los datos del backend al formato esperado
            for memb in membresias_raw:
                membresia_normalizada = {
                    "id": memb.get("id"),
                    "nombre": memb.get("nombre_membresia", memb.get("nombre", "")),
                    "precio": memb.get("precio_actual", memb.get("precio", 0)),
                    "duracion_dias": memb.get("duracion_dias", 30),
                    "tipo_membresia": memb.get("tipo_membresia", "")
                }
                opciones_membresias.append(membresia_normalizada)

            # Solo permitir Yape y Efectivo (ambos requieren confirmación del admin)
            metodos_pago.clear()
            metodos_disponibles = opciones.get("metodos_pago", ["Efectivo", "Yape"])
            # Filtrar solo Yape y Efectivo
            metodos_permitidos = [m for m in metodos_disponibles if m in ["Yape", "Efectivo"]]
            if not metodos_permitidos:
                metodos_permitidos = ["Efectivo", "Yape"]
            metodos_pago.extend(metodos_permitidos)

            print(f"Membresias cargadas: {len(opciones_membresias)}")
            print(f"Metodos de pago: {metodos_pago}")

            if not opciones_membresias:
                mostrar_error("No se pudieron cargar las opciones de membresía. Verifica que el backend esté funcionando.")
                return False

            return True

        except Exception as e:
            print(f"ERROR - Error al cargar opciones: {e}")
            import traceback
            traceback.print_exc()
            mostrar_error(f"Error al cargar opciones: {str(e)}\n\nVerifica que el backend esté en ejecución.")
            return False

    def verificar_dni_disponible() -> bool:
        """Verificar que el DNI no esté registrado"""
        try:
            resultado = api_service.verificar_dni(dni_input.value)

            if not resultado.get("disponible", False):
                mostrar_error(
                    f"El DNI {dni_input.value} ya está registrado. "
                    "Si eres tú, ve a la opción de Asistencia."
                )
                return False

            return True

        except Exception as e:
            mostrar_error(f"Error al verificar DNI: {str(e)}")
            return False

    def ir_a_paso2(e):
        """Avanzar al Paso 2: Selección de membresía"""
        print("Iniciando paso 2...")

        print("Paso 1: Validando datos...")
        if not validar_paso1():
            print("ERROR - Validacion del paso 1 fallo")
            return

        print("Paso 2: Verificando DNI disponible...")
        # Verificar DNI disponible
        if not verificar_dni_disponible():
            print("ERROR - DNI no disponible")
            return

        print("Paso 3: Guardando datos del formulario...")
        # Guardar datos del paso 1
        form_data["dni"] = dni_input.value
        form_data["nombre"] = nombre_input.value.strip()
        form_data["apellidos"] = apellidos_input.value.strip()
        form_data["correo"] = correo_input.value.strip()
        form_data["telefono"] = telefono_input.value

        print("Paso 4: Cargando opciones de registro...")
        # Cargar opciones
        if not cargar_opciones_registro():
            print("ERROR - Error al cargar opciones de registro")
            return

        print("Paso 5: Cambiando a paso 2...")
        # Mostrar paso 2
        paso_actual.current = 2
        print(f"OK - paso_actual.current = {paso_actual.current}")

        print("Paso 6: Actualizando vista...")
        actualizar_vista()
        print("OK - Paso 2 deberia estar visible ahora!")

    def seleccionar_membresia(membresia_id: int):
        """Seleccionar una membresía"""
        form_data["id_membresia"] = membresia_id
        # Solo actualizar el contenedor del paso 2 sin refrescar toda la vista
        paso2_container.content = build_paso2()
        paso2_container.update()

    def seleccionar_metodo_pago(metodo: str):
        """Seleccionar método de pago"""
        form_data["metodo_pago"] = metodo
        # Solo actualizar el contenedor del paso 2 sin refrescar toda la vista
        paso2_container.content = build_paso2()
        paso2_container.update()

    def ir_a_paso3(e):
        """Avanzar al Paso 3: Confirmación"""
        if not form_data["id_membresia"]:
            mostrar_error("Debes seleccionar una membresía")
            return

        if not form_data["metodo_pago"]:
            mostrar_error("Debes seleccionar un método de pago")
            return

        paso_actual.current = 3
        actualizar_vista()

    def volver_paso1(e):
        """Volver al Paso 1"""
        paso_actual.current = 1
        limpiar_error()
        actualizar_vista()

    def volver_paso2(e):
        """Volver al Paso 2"""
        paso_actual.current = 2
        limpiar_error()
        actualizar_vista()

    def confirmar_registro(e):
        """Realizar el registro final"""
        try:
            limpiar_error()

            print("🎯 Iniciando registro del cliente...")

            # Llamar al API
            resultado = api_service.registrar_cliente_con_validacion(
                dni=form_data["dni"],
                nombre=form_data["nombre"],
                apellidos=form_data["apellidos"],
                correo=form_data["correo"],
                telefono=form_data["telefono"],
                id_membresia=form_data["id_membresia"],
                metodo_pago=form_data["metodo_pago"],
                usuario_creacion=USUARIO_SISTEMA
            )

            print(f"Resultado del registro: {resultado}")

            if resultado.get("registro_creado", False):
                print("OK - Registro pendiente creado exitosamente")
                print(f"ID Registro Pendiente: {resultado.get('id_registro_pendiente')}")
                print(f"⚠️ PAGO CON {form_data['metodo_pago'].upper()} - Requiere confirmación del admin")
                print("📡 El backend ya envió la notificación WebSocket al admin")

                # Mostrar pantalla de éxito
                mostrar_registro_exitoso(resultado)
            else:
                mostrar_error(resultado.get("mensaje", "Error al registrar cliente"))

        except Exception as e:
            print(f"ERROR - Error al registrar: {e}")
            import traceback
            traceback.print_exc()
            mostrar_error(f"Error al registrar: {str(e)}")

    def mostrar_registro_exitoso(resultado):
        """Mostrar pantalla de registro exitoso"""
        # Obtener datos del resumen (nueva estructura de respuesta)
        resumen = resultado.get("resumen", {})
        metodo_pago = form_data.get("metodo_pago", "Efectivo")
        id_registro_pendiente = resultado.get("id_registro_pendiente")

        # DEBUG: Imprimir lo que viene del backend
        print(f"🔍 DEBUG - Resultado completo: {resultado}")
        print(f"🔍 DEBUG - Resumen: {resumen}")
        print(f"🔍 DEBUG - ID Registro Pendiente: {id_registro_pendiente}")

        # Obtener datos del resumen
        nombre_completo = resumen.get("nombre_completo", f"{form_data['nombre']} {form_data['apellidos']}")
        dni = resumen.get("dni", form_data["dni"])
        nombre_membresia = resumen.get("nombre_membresia", "Membresía")
        tipo_membresia = resumen.get("tipo_membresia", "")
        monto = resumen.get("monto", 0.0)

        print(f"🔍 DEBUG - Nombre de membresía final: {nombre_membresia}")

        contenido_exito = ft.Column([
            # Ícono de pendiente grande y moderno
            ft.Container(
                content=ft.Icon(
                    ft.Icons.SCHEDULE_ROUNDED,
                    size=Theme.ICON_SIZE["2xl"],
                    color=Theme.WARNING
                ),
                width=Theme.ICON_SIZE["3xl"],
                height=Theme.ICON_SIZE["3xl"],
                bgcolor="#1A1A1A",
                border_radius=60,
                border=ft.border.all(4, Theme.WARNING),
                alignment=ft.alignment.center,
                shadow=Theme.get_shadow("lg"),
            ),

            ft.Container(height=Theme.SPACING["lg"]),

            # Título
            ft.Text(
                "¡REGISTRO PENDIENTE!",
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

            # Información del cliente con diseño mejorado
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Información de Registro",
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

            # Alerta de confirmación pendiente (PARA AMBOS: Yape y Efectivo)
            create_alert_card(
                f"PAGO CON {metodo_pago.upper()} - CONFIRMACION PENDIENTE\n\n"
                "El personal del gimnasio ha sido notificado. "
                "Por favor, espera la confirmacion del pago por parte del administrador.",
                "warning",
                page_width=page_width
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            # Botón volver mejorado
            ft.Container(
                content=create_large_button(
                    "Finalizar",
                    lambda e: on_back(),
                    icon=ft.Icons.HOME_ROUNDED,
                    bgcolor=Theme.PRIMARY,
                    page_width=page_width,
                    page_height=page_height
                ),
                width=280,
            )

        ],
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

    def build_paso1():
        """Construir vista del Paso 1: Datos personales"""
        return ft.Column([
            ft.Text(
                "Registro de Nuevo Cliente",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.PRIMARY
            ),
            ft.Text(
                "Paso 1: Datos Personales",
                size=Theme.FONT_SIZE["2xl"],
                color=Theme.TEXT_SECONDARY
            ),

            ft.Container(height=Theme.SPACING["xl"]),

            dni_input,
            nombre_input,
            apellidos_input,
            correo_input,
            telefono_input,

            ft.Container(height=Theme.SPACING["2xl"]),

            mensaje_error,

            ft.Row([
                create_back_button(lambda e: on_back(), page_width=page_width, page_height=page_height),
                btn_siguiente,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=500)

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

    def build_paso2():
        """Construir vista del Paso 2: Selección de membresía"""
        print(f"Construyendo paso 2...")
        print(f"Membresias disponibles: {len(opciones_membresias)}")
        print(f"Datos: {opciones_membresias}")

        # Cards de membresías
        membresias_cards = []

        if not opciones_membresias:
            # Mostrar mensaje si no hay membresías
            membresias_cards.append(
                create_alert_card(
                    "No hay membresías disponibles. Por favor, contacta al administrador.",
                    "error",
                    page_width=page_width
                )
            )
        else:
            for memb in opciones_membresias:
                seleccionada = form_data["id_membresia"] == memb["id"]

                # Usar tarjeta premium del frontend admin
                card = create_membership_card(
                    membresia=memb,
                    precio_actual=memb['precio'],
                    on_select_click=lambda e, mid=memb["id"]: seleccionar_membresia(mid),
                    is_selected=seleccionada,
                    page_width=page_width
                )
                membresias_cards.append(card)

        # Botones de método de pago (estilo formulario con grises)
        metodos_buttons = []
        for metodo in metodos_pago:
            seleccionado = form_data["metodo_pago"] == metodo

            # Ícono según método
            icono = ft.Icons.PAYMENT if metodo == "Yape" else ft.Icons.MONEY

            # Colores grises del formulario (como los inputs)
            border_color = Theme.PRIMARY if seleccionado else Theme.BORDER_DEFAULT
            bg_color = Theme.CARD_BG  # Mismo fondo que los inputs

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
                on_click=lambda e, m=metodo: seleccionar_metodo_pago(m)
            )
            metodos_buttons.append(btn)

        return ft.Column([
            ft.Text(
                "Paso 2: Selecciona tu Membresía",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.PRIMARY
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            ft.Text("Membresías Disponibles:", size=Theme.FONT_SIZE["2xl"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ft.Container(height=Theme.SPACING["lg"]),

            # Tarjetas con wrap para adaptarse a múltiples membresías
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

            mensaje_error,

            ft.Row([
                create_back_button(volver_paso1, "Volver", page_width=page_width, page_height=page_height),
                create_success_button("Continuar", ir_a_paso3, icon=ft.Icons.ARROW_FORWARD, page_width=page_width, page_height=page_height),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=600)

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

    def build_paso3():
        """Construir vista del Paso 3: Confirmación"""
        # Obtener membresía seleccionada
        membresia_sel = next((m for m in opciones_membresias if m["id"] == form_data["id_membresia"]), {})

        # Layout en dos columnas para mejor organización
        columna_izquierda = ft.Column([
            # Datos Personales
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON_ROUNDED, color=Theme.PRIMARY, size=24),
                        ft.Text("Datos Personales", size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["md"]),

                    ft.Text(f"DNI: {form_data['dni']}",
                           size=Theme.FONT_SIZE["md"],
                           color=Theme.TEXT_SECONDARY),
                    ft.Text(f"{form_data['nombre']} {form_data['apellidos']}",
                           size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["semibold"],
                           color=Theme.TEXT_PRIMARY),
                    ft.Text(form_data['correo'],
                           size=Theme.FONT_SIZE["md"],
                           color=Theme.TEXT_SECONDARY),
                    ft.Text(form_data['telefono'],
                           size=Theme.FONT_SIZE["md"],
                           color=Theme.TEXT_SECONDARY),
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

                    ft.Text(form_data['metodo_pago'],
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
                        ft.Text("Membresía", size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ], spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["lg"]),

                    ft.Text(membresia_sel.get('nombre') or membresia_sel.get('nombre_membresia', 'Membresía'),
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

        # Construir elementos de la vista
        elementos_paso3 = [
            ft.Text(
                "Confirmar Registro",
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
        if form_data['metodo_pago'] == "Yape":
            import os
            qr_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "QR_YAPE.jpg")

            # Verificar si existe el QR
            if os.path.exists(qr_path):
                elementos_paso3.extend([
                    # Título simple y limpio
                    ft.Row([
                        ft.Icon(ft.Icons.QR_CODE_2_ROUNDED, color=Theme.PRIMARY, size=28),
                        ft.Text("Escanea para pagar con Yape",
                               size=Theme.FONT_SIZE["xl"],
                               weight=Theme.FONT_WEIGHT["bold"],
                               color=Theme.TEXT_PRIMARY),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),

                    ft.Container(height=Theme.SPACING["lg"]),

                    # QR Code minimalista y limpio
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

                    # Monto simple
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
                elementos_paso3.extend([
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

        # Agregar mensaje de error y botones
        elementos_paso3.extend([
            mensaje_error,
            ft.Row([
                create_back_button(volver_paso2, "Volver", page_width=page_width, page_height=page_height),
                btn_registrar,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=600)
        ])

        return ft.Column(elementos_paso3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

    def actualizar_vista():
        """Actualizar la vista según el paso actual"""
        print(f"actualizar_vista() llamada. Paso actual: {paso_actual.current}")

        # Verificar si existe el background
        background_existe = os.path.exists(BACKGROUND_IMAGE)

        if paso_actual.current == 1:
            print("Renderizando PASO 1")
            btn_siguiente.on_click = ir_a_paso2
            paso1_container.content = build_paso1()

            contenido_paso = ft.Column(
                [paso1_container],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            if background_existe:
                main_container = ft.Stack([
                    ft.Image(
                        src=BACKGROUND_IMAGE,
                        fit=ft.ImageFit.COVER,
                        width=float('inf'),
                        height=float('inf'),
                    ),
                    ft.Container(bgcolor=Theme.OVERLAY_DARK, expand=True),
                    ft.Container(content=contenido_paso, padding=Theme.SPACING["4xl"], expand=True, alignment=ft.alignment.center),
                ], expand=True)
            else:
                main_container = ft.Container(
                    content=contenido_paso,
                    padding=Theme.SPACING["4xl"],
                    bgcolor=Theme.BACKGROUND_DARK,
                    expand=True,
                    alignment=ft.alignment.center
                )

            page.controls.clear()
            page.add(main_container)

        elif paso_actual.current == 2:
            print("Renderizando PASO 2")
            paso2_container.content = build_paso2()

            contenido_paso = ft.Column(
                [paso2_container],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            if background_existe:
                main_container = ft.Stack([
                    ft.Image(
                        src=BACKGROUND_IMAGE,
                        fit=ft.ImageFit.COVER,
                        width=float('inf'),
                        height=float('inf'),
                    ),
                    ft.Container(bgcolor=Theme.OVERLAY_DARK, expand=True),
                    ft.Container(content=contenido_paso, padding=Theme.SPACING["4xl"], expand=True, alignment=ft.alignment.center),
                ], expand=True)
            else:
                main_container = ft.Container(
                    content=contenido_paso,
                    padding=Theme.SPACING["4xl"],
                    bgcolor=Theme.BACKGROUND_DARK,
                    expand=True,
                    alignment=ft.alignment.center
                )

            page.controls.clear()
            page.add(main_container)
            print("Paso 2 agregado a la pagina")

        elif paso_actual.current == 3:
            print("Renderizando PASO 3")
            btn_registrar.on_click = confirmar_registro
            paso3_container.content = build_paso3()

            contenido_paso = ft.Column(
                [paso3_container],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            if background_existe:
                main_container = ft.Stack([
                    ft.Image(
                        src=BACKGROUND_IMAGE,
                        fit=ft.ImageFit.COVER,
                        width=float('inf'),
                        height=float('inf'),
                    ),
                    ft.Container(bgcolor=Theme.OVERLAY_DARK, expand=True),
                    ft.Container(content=contenido_paso, padding=Theme.SPACING["4xl"], expand=True, alignment=ft.alignment.center),
                ], expand=True)
            else:
                main_container = ft.Container(
                    content=contenido_paso,
                    padding=Theme.SPACING["4xl"],
                    bgcolor=Theme.BACKGROUND_DARK,
                    expand=True,
                    alignment=ft.alignment.center
                )

            page.controls.clear()
            page.add(main_container)

        print("Llamando a page.update()...")
        page.update()
        print("page.update() completado")

    # Mostrar paso 1 inicialmente
    actualizar_vista()
