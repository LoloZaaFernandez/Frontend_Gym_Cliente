"""
Vista de Registro de Nuevos Clientes
Flujo completo: datos personales → selección de membresía → confirmación → registro
"""
import flet as ft
import sys
import os

# Agregar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.theme import Theme
from config.settings import USUARIO_SISTEMA, API_BASE_URL
from components.buttons import create_large_button, create_back_button, create_success_button
from components.inputs import create_text_input, create_dni_input, create_phone_input, create_email_input
from components.cards import create_card_container, create_info_card, create_alert_card
from components.membership_card import create_membership_card
from services.api_service import APIService
from services.websocket_service import enviar_notificacion_async


def show_registro_view(page: ft.Page, api_service: APIService, on_back):
    """
    Mostrar vista de registro de nuevos clientes

    Args:
        page: Instancia de la página
        api_service: Servicio API
        on_back: Función para volver a la pantalla inicial
    """

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

    # Referencias a controles
    dni_input = create_dni_input()
    nombre_input = create_text_input("Nombre", hint_text="Ej: Juan", icon=ft.Icons.PERSON)
    apellidos_input = create_text_input("Apellidos", hint_text="Ej: Pérez García", icon=ft.Icons.PERSON_OUTLINE)
    correo_input = create_email_input()
    telefono_input = create_phone_input()

    mensaje_error = ft.Container()
    btn_siguiente = create_success_button("Siguiente", None, icon=ft.Icons.ARROW_FORWARD)
    btn_registrar = create_success_button("Confirmar Registro", None, icon=ft.Icons.CHECK)

    # Contenedores de pasos
    paso1_container = ft.Container()
    paso2_container = ft.Container()
    paso3_container = ft.Container()

    paso_actual = ft.Ref[int]()
    paso_actual.current = 1

    def mostrar_error(mensaje: str):
        """Mostrar mensaje de error"""
        mensaje_error.content = create_alert_card(mensaje, "error")
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
            print("🔄 Cargando opciones de registro...")
            opciones = api_service.get_opciones_registro()
            print(f"📦 Opciones recibidas: {opciones}")

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

            print(f"✅ Membresías cargadas: {len(opciones_membresias)}")
            print(f"✅ Métodos de pago: {metodos_pago}")

            if not opciones_membresias:
                mostrar_error("No se pudieron cargar las opciones de membresía. Verifica que el backend esté funcionando.")
                return False

            return True

        except Exception as e:
            print(f"❌ Error al cargar opciones: {e}")
            import traceback
            traceback.print_exc()
            mostrar_error(f"Error al cargar opciones: {str(e)}\n\nVerifica que el backend esté en ejecución.")
            return False

    def verificar_dni_disponible() -> bool:
        """Verificar que el DNI no esté registrado"""
        try:
            resultado = api_service.verificar_dni(dni_input.value)

            if resultado.get("existe", False):
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
        print("🚀 Iniciando paso 2...")

        print("✅ Paso 1: Validando datos...")
        if not validar_paso1():
            print("❌ Validación del paso 1 falló")
            return

        print("✅ Paso 2: Verificando DNI disponible...")
        # Verificar DNI disponible
        if not verificar_dni_disponible():
            print("❌ DNI no disponible")
            return

        print("✅ Paso 3: Guardando datos del formulario...")
        # Guardar datos del paso 1
        form_data["dni"] = dni_input.value
        form_data["nombre"] = nombre_input.value.strip()
        form_data["apellidos"] = apellidos_input.value.strip()
        form_data["correo"] = correo_input.value.strip()
        form_data["telefono"] = telefono_input.value

        print("✅ Paso 4: Cargando opciones de registro...")
        # Cargar opciones
        if not cargar_opciones_registro():
            print("❌ Error al cargar opciones de registro")
            return

        print("✅ Paso 5: Cambiando a paso 2...")
        # Mostrar paso 2
        paso_actual.current = 2
        print(f"✅ paso_actual.current = {paso_actual.current}")

        print("✅ Paso 6: Actualizando vista...")
        actualizar_vista()
        print("✅ ¡Paso 2 debería estar visible ahora!")

    def seleccionar_membresia(membresia_id: int):
        """Seleccionar una membresía"""
        form_data["id_membresia"] = membresia_id
        actualizar_vista()

    def seleccionar_metodo_pago(metodo: str):
        """Seleccionar método de pago"""
        form_data["metodo_pago"] = metodo
        actualizar_vista()

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

            print(f"📥 Resultado del registro: {resultado}")

            if resultado.get("registrado", False):
                print("✅ Cliente registrado exitosamente")

                # Enviar notificación WebSocket al admin (en segundo plano)
                try:
                    cliente = resultado.get("cliente", {})
                    membresia_info = resultado.get("membresia", {})
                    pago_info = resultado.get("pago", {})
                    metodo_pago = form_data["metodo_pago"]

                    # Obtener datos de la membresía seleccionada
                    membresia_seleccionada = next(
                        (m for m in opciones_membresias if m["id"] == form_data["id_membresia"]),
                        {}
                    )

                    print(f"📡 Intentando enviar notificación WebSocket al admin...")
                    print(f"   Cliente: {cliente.get('nombre', '')} {cliente.get('apellidos', '')}")
                    print(f"   Método de pago: {metodo_pago}")

                    # Construir URL del WebSocket
                    ws_url = API_BASE_URL.replace("http://", "ws://").replace("https://", "wss://")
                    ws_url = f"{ws_url}/ws/notificaciones"

                    # Enviar notificación en segundo plano (no bloquear UI)
                    enviar_notificacion_async(
                        cliente=cliente,
                        membresia=membresia_seleccionada or membresia_info,
                        metodo_pago=metodo_pago,
                        pago=pago_info,
                        ws_url=ws_url
                    )

                    print(f"⚠️ PAGO CON {metodo_pago.upper()} - Requiere confirmación del admin")
                    print("   (Se envió notificación. Verifica arriba si fue exitosa o si websocket-client no está instalado)")

                except Exception as ws_error:
                    print(f"⚠️ Error al enviar notificación WebSocket (no crítico): {ws_error}")
                    print(f"   El registro se completó correctamente, solo falló la notificación al admin.")
                    # No detener el flujo si falla la notificación

                # Mostrar pantalla de éxito
                mostrar_registro_exitoso(resultado)
            else:
                mostrar_error(resultado.get("mensaje", "Error al registrar cliente"))

        except Exception as e:
            print(f"❌ Error al registrar: {e}")
            import traceback
            traceback.print_exc()
            mostrar_error(f"Error al registrar: {str(e)}")

    def mostrar_registro_exitoso(resultado):
        """Mostrar pantalla de registro exitoso"""
        cliente = resultado.get("cliente", {})
        pago_info = resultado.get("pago", {})
        metodo_pago = form_data.get("metodo_pago", "Efectivo")

        contenido_exito = ft.Column([
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
                "¡Registro Exitoso!",
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
                    ft.Text("Información de Registro", size=Theme.FONT_SIZE["xl"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
                    ft.Divider(color=Theme.BORDER_DEFAULT),
                    ft.Text(f"DNI: {cliente.get('dni', '')}", size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Membresía: {resultado.get('membresia', {}).get('nombre', '')}", size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Válida hasta: {cliente.get('fecha_membresia', '')}", size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Método de pago: {metodo_pago}", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                ], spacing=Theme.SPACING["sm"]),
                width=500
            ),

            # Alerta de confirmación pendiente (PARA AMBOS: Yape y Efectivo)
            create_alert_card(
                f"⚠️ PAGO CON {metodo_pago.upper()} - CONFIRMACIÓN PENDIENTE\n\n"
                "El personal del gimnasio ha sido notificado. "
                "Por favor, espera la confirmación del pago por parte del administrador.",
                "warning"
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Botón volver
            create_large_button(
                "Finalizar",
                lambda e: on_back(),
                icon=ft.Icons.HOME,
                bgcolor=Theme.SUCCESS
            )

        ],
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
                create_back_button(lambda e: on_back()),
                btn_siguiente,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=500)

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

    def build_paso2():
        """Construir vista del Paso 2: Selección de membresía"""
        print(f"🏗️ Construyendo paso 2...")
        print(f"📋 Membresías disponibles: {len(opciones_membresias)}")
        print(f"📋 Datos: {opciones_membresias}")

        # Cards de membresías
        membresias_cards = []

        if not opciones_membresias:
            # Mostrar mensaje si no hay membresías
            membresias_cards.append(
                create_alert_card(
                    "No hay membresías disponibles. Por favor, contacta al administrador.",
                    "error"
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
                    is_selected=seleccionada
                )
                membresias_cards.append(card)

        # Botones de método de pago (más grandes y visibles)
        metodos_buttons = []
        for metodo in metodos_pago:
            seleccionado = form_data["metodo_pago"] == metodo

            # Ícono según método
            icono = ft.Icons.PAYMENT if metodo == "Yape" else ft.Icons.MONEY

            btn = ft.Container(
                content=ft.Column([
                    ft.Icon(
                        icono,
                        size=48,
                        color=ft.Colors.WHITE if seleccionado else Theme.PRIMARY
                    ),
                    ft.Text(
                        metodo,
                        size=Theme.FONT_SIZE["2xl"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=ft.Colors.WHITE if seleccionado else Theme.TEXT_PRIMARY
                    ),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE,
                        size=24,
                        color="#4CAF50",
                        visible=seleccionado
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),
                bgcolor=Theme.PRIMARY if seleccionado else Theme.CARD_BG,
                border=ft.border.all(3 if seleccionado else 2, Theme.PRIMARY),
                border_radius=Theme.RADIUS["xl"],
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
                create_back_button(volver_paso1, "Volver"),
                create_success_button("Continuar", ir_a_paso3, icon=ft.Icons.ARROW_FORWARD),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=600)

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

    def build_paso3():
        """Construir vista del Paso 3: Confirmación"""
        # Obtener membresía seleccionada
        membresia_sel = next((m for m in opciones_membresias if m["id"] == form_data["id_membresia"]), {})

        # Construir elementos de la vista
        elementos_paso3 = [
            ft.Text(
                "Paso 3: Confirmar Registro",
                size=Theme.FONT_SIZE["4xl"],
                weight=Theme.FONT_WEIGHT["bold"],
                color=Theme.PRIMARY
            ),

            ft.Container(height=Theme.SPACING["2xl"]),

            # Resumen completo
            create_card_container(
                content=ft.Column([
                    ft.Text("Resumen de Registro", size=Theme.FONT_SIZE["2xl"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),
                    ft.Divider(color=Theme.BORDER_DEFAULT, thickness=2),

                    ft.Text("Datos Personales:", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"DNI: {form_data['dni']}", size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Nombre: {form_data['nombre']} {form_data['apellidos']}", size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Correo: {form_data['correo']}", size=Theme.FONT_SIZE["lg"]),
                    ft.Text(f"Teléfono: {form_data['telefono']}", size=Theme.FONT_SIZE["lg"]),

                    ft.Divider(color=Theme.BORDER_DEFAULT),

                    ft.Text("Membresía:", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_SECONDARY),
                    ft.Text(f"{membresia_sel.get('nombre', '')} - S/ {membresia_sel.get('precio', 0):.2f}",
                           size=Theme.FONT_SIZE["2xl"], weight=Theme.FONT_WEIGHT["bold"], color=Theme.SUCCESS),

                    ft.Divider(color=Theme.BORDER_DEFAULT),

                    ft.Text("Método de Pago:", size=Theme.FONT_SIZE["lg"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_SECONDARY),
                    ft.Text(form_data['metodo_pago'], size=Theme.FONT_SIZE["xl"],
                           weight=Theme.FONT_WEIGHT["bold"], color=Theme.PRIMARY),

                ], spacing=Theme.SPACING["sm"]),
                width=600
            ),

            ft.Container(height=Theme.SPACING["2xl"]),
        ]

        # Si el método de pago es Yape, mostrar QR
        if form_data['metodo_pago'] == "Yape":
            import os
            qr_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "QR_YAPE.jpg")

            # Verificar si existe el QR
            if os.path.exists(qr_path):
                elementos_paso3.extend([
                    create_alert_card(
                        "💳 PAGO CON YAPE\n\nEscanea el siguiente código QR con tu app de Yape:",
                        "info"
                    ),
                    ft.Container(height=Theme.SPACING["md"]),
                    ft.Container(
                        content=ft.Image(
                            src=qr_path,
                            width=300,
                            height=300,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        bgcolor=Theme.CARD_BG,
                        border_radius=Theme.RADIUS["xl"],
                        padding=Theme.SPACING["xl"],
                        border=ft.border.all(2, Theme.PRIMARY),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=Theme.SPACING["md"]),
                    create_alert_card(
                        f"Monto a pagar: S/ {membresia_sel.get('precio', 0):.2f}\n\nDespués de realizar el pago, haz clic en 'Confirmar Registro'",
                        "warning"
                    ),
                    ft.Container(height=Theme.SPACING["xl"]),
                ])
            else:
                elementos_paso3.extend([
                    create_alert_card(
                        "⚠️ QR de Yape no disponible\n\nPor favor, realiza el pago directamente con el personal del gimnasio.",
                        "warning"
                    ),
                    ft.Container(height=Theme.SPACING["xl"]),
                ])

        # Agregar mensaje de error y botones
        elementos_paso3.extend([
            mensaje_error,
            ft.Row([
                create_back_button(volver_paso2, "Volver"),
                btn_registrar,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=600)
        ])

        return ft.Column(elementos_paso3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"])

    def actualizar_vista():
        """Actualizar la vista según el paso actual"""
        print(f"📺 actualizar_vista() llamada. Paso actual: {paso_actual.current}")

        if paso_actual.current == 1:
            print("📺 Renderizando PASO 1")
            btn_siguiente.on_click = ir_a_paso2
            paso1_container.content = build_paso1()
            page.controls.clear()
            page.add(ft.Container(
                content=ft.Column(
                    [paso1_container],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["5xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.top_center
            ))

        elif paso_actual.current == 2:
            print("📺 Renderizando PASO 2")
            paso2_container.content = build_paso2()
            page.controls.clear()
            # Agregar scroll para que se vean los métodos de pago y botones
            page.add(ft.Container(
                content=ft.Column(
                    [paso2_container],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["5xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.top_center
            ))
            print("📺 Paso 2 agregado a la página")

        elif paso_actual.current == 3:
            print("📺 Renderizando PASO 3")
            btn_registrar.on_click = confirmar_registro
            paso3_container.content = build_paso3()
            page.controls.clear()
            page.add(ft.Container(
                content=ft.Column(
                    [paso3_container],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=Theme.SPACING["5xl"],
                bgcolor=Theme.BACKGROUND_DARK,
                expand=True,
                alignment=ft.alignment.top_center
            ))

        print("📺 Llamando a page.update()...")
        page.update()
        print("📺 page.update() completado")

    # Mostrar paso 1 inicialmente
    actualizar_vista()
