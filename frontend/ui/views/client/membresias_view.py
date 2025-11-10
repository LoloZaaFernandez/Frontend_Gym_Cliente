"""
Vista de Membresías para Clientes - Refactorizado con Sistema de Componentes
REFACTOR: Uso de MembershipCard y MembershipStatusCard unificados
"""

import flet as ft
from datetime import datetime
from config.theme import Theme
from config.settings import CARD_BG, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY_COLOR, BACKGROUND_DARK
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.organisms import MembershipCard, MembershipStatusCard


def show_membresias_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Mostrar vista de membresías disponibles - CON COMPONENTES UNIFICADOS

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_section_click: Callback para cambiar sección
        current_section: Sección actual
    """
    page.clean()
    page.title = "BLESSED FIT CLUB - Membresías"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    cliente = auth_service.get_current_user()
    cliente_id = cliente['id']

    # Contenedores
    membresias_container = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Información de membresía actual del cliente
    membresia_actual_container = ft.Container()

    # Variable de control para evitar cargas concurrentes
    cargando_membresias = {"estado": False}

    def cargar_membresia_actual():
        """Cargar información de la membresía actual del cliente"""
        membresia_actual_container.content = None

        try:
            # Obtener cliente actualizado desde el backend
            cliente_info = api.get_cliente_por_id(cliente_id)
            fecha_membresia = cliente_info.get('fecha_membresia')

            if fecha_membresia:
                try:
                    fecha_venc = datetime.fromisoformat(fecha_membresia)
                    # Comparar solo fechas (sin hora) para que venza al final del día
                    fecha_venc_solo_fecha = fecha_venc.date()
                    fecha_actual_solo_fecha = datetime.now().date()
                    dias_restantes = (fecha_venc_solo_fecha - fecha_actual_solo_fecha).days

                    if dias_restantes >= 0:
                        # Membresía activa - Usar componente MembershipStatusCard
                        membresia_actual_container.content = MembershipStatusCard.create_active(
                            fecha_vencimiento=fecha_venc,
                            dias_restantes=dias_restantes,
                            on_renew_click=lambda e: cargar_membresias()
                        )
                    else:
                        # Membresía vencida
                        membresia_actual_container.content = MembershipStatusCard.create_status(
                            titulo="MEMBRESÍA VENCIDA",
                            subtitulo="Tu membresía ha expirado",
                            accion="Renueva para continuar",
                            color="#ef5350",
                            on_action_click=lambda e: cargar_membresias()
                        )
                except Exception as e:
                    print(f"Error al procesar fecha: {e}")
                    membresia_actual_container.content = MembershipStatusCard.create_status(
                        titulo="ERROR",
                        subtitulo="Error al cargar información",
                        accion="Intenta actualizar",
                        color="#757575",
                        on_action_click=lambda e: cargar_membresia_actual()
                    )
            else:
                # Sin membresía
                membresia_actual_container.content = MembershipStatusCard.create_status(
                    titulo="SIN MEMBRESÍA",
                    subtitulo="No tienes membresía activa",
                    accion="Adquiere una membresía",
                    color="#FF9800",
                    on_action_click=lambda e: cargar_membresias()
                )
        except Exception as e:
            print(f"Error al cargar membresía actual: {e}")
            membresia_actual_container.content = MembershipStatusCard.create_status(
                titulo="ERROR",
                subtitulo="Error al conectar",
                accion="Revisa tu conexión",
                color="#757575",
                on_action_click=lambda e: cargar_membresia_actual()
            )

        page.update()

    def cargar_membresias():
        """Cargar membresías ACTIVAS con diseño unificado"""
        print("\n" + "="*60)
        print("🔄 INICIANDO CARGA DE MEMBRESÍAS...")
        print("="*60)

        # 🔒 EVITAR CARGAS CONCURRENTES
        if cargando_membresias["estado"]:
            print("⚠️ Ya hay una carga en progreso, ignorando...")
            return

        cargando_membresias["estado"] = True

        try:
            print("✅ Limpiando contenedor...")
            membresias_container.controls.clear()
            page.update()

            print("📡 Consultando API...")
            # Obtener membresías ACTIVAS
            membresias = api.get_membresias(estado="Activa")

            print(f"🔍 Se encontraron {len(membresias)} membresías activas")

            if not membresias:
                membresias_container.controls.append(
                    ft.Container(
                        width=350,
                        height=200,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        padding=20,
                        content=ft.Column([
                            ft.Icon(ft.Icons.INBOX, size=50, color=ft.Colors.GREY_400),
                            ft.Text("No hay membresías disponibles",
                                   size=14, color=ft.Colors.GREY_600),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15,
                           alignment=ft.MainAxisAlignment.CENTER),
                        alignment=ft.alignment.center
                    )
                )
            else:
                # Procesar cada membresía
                tarjetas_agregadas = 0
                print(f"\n🔧 Procesando {len(membresias)} membresías...")

                for idx, membresia in enumerate(membresias, 1):
                    try:
                        print(f"\n  [{idx}] Procesando: {membresia.get('nombre_membresia', 'Sin nombre')}")

                        precio_data = api.get_precio_membresia(membresia['id'])

                        if precio_data and 'precio_actual' in precio_data:
                            precio_actual = float(precio_data['precio_actual'])
                            print(f"      Precio: S/. {precio_actual:.2f}")

                            if precio_actual > 0:
                                print(f"      ✅ Creando tarjeta con componente unificado...")
                                # Usar componente unificado MembershipCard
                                card = MembershipCard.create(
                                    membresia=membresia,
                                    precio_actual=precio_actual,
                                    mode="client",
                                    on_buy_click=lambda e, m=membresia, p=precio_actual: confirmar_compra(m, p)
                                )
                                membresias_container.controls.append(card)
                                tarjetas_agregadas += 1
                                print(f"      ✅ Tarjeta agregada exitosamente")
                            else:
                                print(f"      ⚠️ Precio = 0, omitiendo...")
                        else:
                            print(f"      ⚠️ Sin precio_actual en datos")
                    except Exception as e:
                        print(f"      ❌ Error al procesar membresía: {e}")
                        import traceback
                        traceback.print_exc()
                        continue

                print(f"\n✅ Total de tarjetas agregadas: {tarjetas_agregadas}")

        except Exception as e:
            print(f"\n❌ ERROR GENERAL al cargar membresías: {e}")
            import traceback
            traceback.print_exc()
            mostrar_mensaje("Error al cargar membresías", error=True)
        finally:
            # 🔓 LIBERAR BLOQUEO SIEMPRE
            cargando_membresias["estado"] = False
            print("\n🔓 Bloqueo liberado")

        # Actualizar página al final
        print("🔄 Actualizando página...")
        page.update()
        print("="*60)
        print("✅ CARGA DE MEMBRESÍAS COMPLETADA")
        print("="*60 + "\n")

    def confirmar_compra(membresia, precio_actual):
        """Confirmar compra de membresía"""
        metodo_pago = ft.Dropdown(
            label="Método de Pago",
            options=[
                ft.dropdown.Option("Efectivo"),
                ft.dropdown.Option("Yape"),
            ],
            value="Efectivo",
            width=300
        )

        def procesar_compra(e):
            if not metodo_pago.value:
                mostrar_mensaje("Selecciona método de pago", error=True)
                return

            page.close(dialog)

            try:
                resultado = api.comprar_membresia(
                    cliente_id=cliente_id,
                    membresia_id=membresia['id'],
                    monto=precio_actual,
                    metodo_pago=metodo_pago.value
                )

                mostrar_mensaje(f"✅ ¡Membresía adquirida! S/. {precio_actual:.2f}")
                cargar_membresia_actual()

            except Exception as e:
                mostrar_mensaje(f"❌ Error: {str(e)}", error=True)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Comprar - {membresia['nombre_membresia']}"),
            content=ft.Column([
                ft.Text(f"Precio: S/. {precio_actual:.2f}", size=16, weight=ft.FontWeight.BOLD),
                metodo_pago,
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
                ft.ElevatedButton("Confirmar Compra", on_click=procesar_compra),
            ],
        )

        page.open(dialog)

    def mostrar_mensaje(mensaje, error=False):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#ef5350" if error else "#4CAF50",
        )
        page.snack_bar.open = True
        page.update()

    # Info de usuario para el layout
    user_info = {"nombre": cliente.get("nombre", "Cliente"), "rol": "Cliente"}

    # Botón de actualizar
    refresh_button = ft.ElevatedButton(
        "Actualizar",
        icon=ft.Icons.REFRESH,
        on_click=lambda _: (cargar_membresia_actual(), cargar_membresias()),
        height=40
    )

    # Contenido principal
    content = ft.Column([
        ft.Row([
            ft.Text("Mi Estado de Membresía", size=Theme.FONT_SIZE["xl"],
                   weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
            ft.Container(expand=True),
            refresh_button,
        ]),
        ft.Container(height=Theme.SPACING["xl"]),
        ft.Container(
            content=membresia_actual_container,
            alignment=ft.alignment.center
        ),
        ft.Container(height=Theme.SPACING["2xl"]),
        ft.Text("Planes Disponibles", size=Theme.FONT_SIZE["lg"],
               weight=Theme.FONT_WEIGHT["bold"], color=Theme.TEXT_PRIMARY),
        ft.Container(height=Theme.SPACING["md"]),
        membresias_container,
    ], scroll=ft.ScrollMode.AUTO, spacing=0)

    # Usar base_layout para sidebar consistente
    create_base_layout(
        page=page,
        role="cliente",
        current_section=current_section,
        on_section_click=on_section_click,
        content=ft.Container(content=content, padding=Theme.SPACING["xl"]),
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )

    # Cargar datos iniciales
    cargar_membresia_actual()
    cargar_membresias()
