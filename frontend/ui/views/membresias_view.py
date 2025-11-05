"""
Vista de Membresías para Clientes - Conectada con Backend
"""

import flet as ft
from datetime import datetime, timedelta
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_membresias_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de membresías disponibles

    Args:
        page: Página de Flet
        auth_service: Servicio de autenticación
        on_back: Callback para volver atrás
    """
    page.clean()
    page.title = "BLESSED GYM - Membresías"

    api = APIService()
    cliente = auth_service.get_current_user()
    cliente_id = cliente['id']

    # Mapeo de tipos de membresía a información visual
    membresia_info = {
        "Dia": {
            "precio": 15.00,
            "duracion": "1 día",
            "color": "#FF9800",
            "beneficios": [
                "Acceso completo al gimnasio",
                "Vestuarios y duchas",
                "Válido por 24 horas"
            ]
        },
        "Mensual": {
            "precio": 150.00,
            "duracion": "30 días",
            "color": PRIMARY_COLOR,
            "beneficios": [
                "Acceso completo al gimnasio",
                "Clases grupales ilimitadas",
                "Asesoría básica",
                "Vestuarios y duchas"
            ]
        },
        "Trimestral": {
            "precio": 400.00,
            "precio_mes": 133.33,
            "duracion": "90 días",
            "color": "#4CAF50",
            "ahorro": "11%",
            "beneficios": [
                "Todo del plan mensual",
                "1 evaluación física gratis",
                "Plan nutricional básico",
                "Descuento 10% en productos"
            ]
        },
        "Semestral": {
            "precio": 750.00,
            "precio_mes": 125.00,
            "duracion": "180 días",
            "color": "#2196F3",
            "ahorro": "17%",
            "beneficios": [
                "Todo del plan trimestral",
                "2 sesiones con entrenador personal",
                "Evaluaciones físicas mensuales",
                "Descuento 15% en productos"
            ]
        },
        "Anual": {
            "precio": 1500.00,
            "precio_mes": 125.00,
            "duracion": "365 días",
            "color": "#9C27B0",
            "ahorro": "17%",
            "beneficios": [
                "Todo del plan semestral",
                "Entrenador personal 2 sesiones/mes",
                "Evaluaciones físicas mensuales",
                "Plan nutricional personalizado",
                "Descuento 15% en productos",
                "Invitaciones a eventos exclusivos"
            ]
        }
    }

    # Contenedores
    membresias_container = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Información de membresía actual del cliente
    membresia_actual_container = ft.Container()

    def cargar_membresia_actual():
        """Cargar información de la membresía actual del cliente"""
        membresia_actual_container.content = None

        # Obtener información del cliente actualizada
        try:
            cliente_info = api.get_cliente_por_id(cliente_id)
            fecha_membresia = cliente_info.get('fecha_membresia')

            if fecha_membresia:
                try:
                    fecha_venc = datetime.fromisoformat(fecha_membresia)
                    fecha_actual = datetime.now()
                    dias_restantes = (fecha_venc - fecha_actual).days

                    if dias_restantes > 0:
                        # Membresía activa
                        membresia_actual_container.content = ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=30, color="#4CAF50"),
                                    ft.Text(
                                        "Membresía Activa",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=TEXT_PRIMARY
                                    ),
                                ], spacing=10),
                                ft.Divider(height=1, color="#333333"),
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Vence el:", size=12, color=TEXT_SECONDARY),
                                        ft.Text(
                                            fecha_venc.strftime("%d/%m/%Y"),
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=TEXT_PRIMARY
                                        ),
                                    ]),
                                    ft.Container(width=20),
                                    ft.Column([
                                        ft.Text("Días restantes:", size=12, color=TEXT_SECONDARY),
                                        ft.Text(
                                            str(dias_restantes),
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color="#4CAF50"
                                        ),
                                    ]),
                                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                            ], spacing=15),
                            bgcolor=CARD_BG,
                            border_radius=12,
                            padding=20,
                            border=ft.border.all(2, "#4CAF50"),
                            margin=ft.margin.only(bottom=20)
                        )
                    else:
                        # Membresía vencida
                        membresia_actual_container.content = ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.ERROR, size=30, color="#ef5350"),
                                    ft.Text(
                                        "Membresía Vencida",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=TEXT_PRIMARY
                                    ),
                                ], spacing=10),
                                ft.Text(
                                    "Tu membresía ha vencido. Renueva para seguir disfrutando del gimnasio.",
                                    size=14,
                                    color=TEXT_SECONDARY
                                ),
                            ], spacing=10),
                            bgcolor=CARD_BG,
                            border_radius=12,
                            padding=20,
                            border=ft.border.all(2, "#ef5350"),
                            margin=ft.margin.only(bottom=20)
                        )
                except:
                    pass
            else:
                # Sin membresía
                membresia_actual_container.content = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.INFO, size=30, color="#FF9800"),
                            ft.Text(
                                "Sin Membresía",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY
                            ),
                        ], spacing=10),
                        ft.Text(
                            "Adquiere una membresía para acceder al gimnasio.",
                            size=14,
                            color=TEXT_SECONDARY
                        ),
                    ], spacing=10),
                    bgcolor=CARD_BG,
                    border_radius=12,
                    padding=20,
                    border=ft.border.all(2, "#FF9800"),
                    margin=ft.margin.only(bottom=20)
                )
        except Exception as e:
            print(f"Error al cargar membresía actual: {e}")

        page.update()

    def cargar_membresias():
        """Cargar membresías disponibles desde el backend"""
        membresias_container.controls.clear()

        try:
            membresias = api.get_membresias(estado="Activa")

            if not membresias:
                membresias_container.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "No hay membresías disponibles",
                            color=TEXT_SECONDARY,
                            size=16
                        ),
                        padding=40
                    )
                )
            else:
                for membresia in membresias:
                    tipo = membresia['tipo_membresia']
                    info = membresia_info.get(tipo, {})

                    if info:
                        membresias_container.controls.append(
                            crear_plan_card(membresia, info)
                        )

        except Exception as e:
            print(f"Error al cargar membresías: {e}")
            mostrar_mensaje("Error al cargar membresías", error=True)

        page.update()

    def crear_plan_card(membresia, info):
        """Crear tarjeta de plan de membresía"""
        tipo = membresia['tipo_membresia']
        nombre = membresia['nombre_membresia']

        beneficios_list = ft.Column(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=info['color']),
                    ft.Text(beneficio, size=12, color=TEXT_SECONDARY, expand=True)
                ], spacing=8)
                for beneficio in info['beneficios']
            ],
            spacing=8
        )

        # Badge de ahorro si aplica
        badge_ahorro = None
        if info.get('ahorro'):
            badge_ahorro = ft.Container(
                content=ft.Text(
                    f"Ahorra {info['ahorro']}",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                bgcolor=info['color'],
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
                margin=ft.margin.only(bottom=10)
            )

        # Construir contenido de la tarjeta
        card_content = []

        if badge_ahorro:
            card_content.append(badge_ahorro)

        card_content.append(
            ft.Text(
                nombre,
                size=18,
                weight=ft.FontWeight.BOLD,
                color=info['color'],
                text_align=ft.TextAlign.CENTER
            )
        )

        # Precio mensual si aplica
        precio_mes_text = None
        if info.get('precio_mes'):
            precio_mes_text = ft.Text(
                f"S/. {info['precio_mes']:.2f}/mes",
                size=13,
                color=TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER
            )

        card_content.extend([
            ft.Text(
                f"S/. {info['precio']:.2f}",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER
            ),
        ])

        if precio_mes_text:
            card_content.append(precio_mes_text)

        card_content.extend([
            ft.Text(
                info['duracion'],
                size=14,
                color=TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Divider(height=1, color="#333333"),
            beneficios_list,
            ft.Container(height=10),
            ft.ElevatedButton(
                "Adquirir Plan",
                icon=ft.Icons.SHOPPING_CART,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=info['color'],
                ),
                width=220,
                height=45,
                on_click=lambda _, m=membresia, i=info: confirmar_compra(m, i)
            ),
        ])

        # Destacar si es trimestral (más popular)
        destacado = tipo == "Trimestral"
        border_width = 2 if destacado else 1
        border_color = info['color'] if destacado else "#333333"

        return ft.Container(
            content=ft.Column(
                controls=card_content,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=CARD_BG,
            border_radius=12,
            padding=25,
            border=ft.border.all(border_width, border_color),
            shadow=ft.BoxShadow(
                spread_radius=2 if destacado else 0,
                blur_radius=15 if destacado else 10,
                color=f"{info['color']}44" if destacado else ft.Colors.BLACK26,
                offset=ft.Offset(0, 4)
            ),
            width=280
        )

    def confirmar_compra(membresia, info):
        """Confirmar compra de membresía"""
        def close_dialog(e):
            dialog.open = False
            page.update()

        def compra_confirmada(e):
            dialog.open = False
            page.update()

            # Realizar compra a través del backend
            try:
                resultado = api.comprar_membresia(
                    cliente_id=cliente_id,
                    membresia_id=membresia['id'],
                    monto=info['precio'],
                    metodo_pago="Efectivo"
                )

                # Mostrar mensaje de éxito
                mostrar_mensaje(
                    f"✅ ¡Membresía {membresia['nombre_membresia']} adquirida exitosamente!",
                    error=False
                )

                # Recargar información de membresía actual
                cargar_membresia_actual()

            except ValueError as e:
                error_msg = str(e)
                if "Cliente no encontrado" in error_msg:
                    mostrar_mensaje("❌ Error: Cliente no encontrado", error=True)
                elif "Membresía no encontrada" in error_msg:
                    mostrar_mensaje("❌ Error: Membresía no disponible", error=True)
                else:
                    mostrar_mensaje(f"❌ Error al comprar membresía: {error_msg}", error=True)
            except Exception as e:
                mostrar_mensaje(f"❌ Error inesperado: {str(e)}", error=True)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Confirmar Compra - {membresia['nombre_membresia']}", color=TEXT_PRIMARY),
            content=ft.Column([
                ft.Text(
                    f"Precio: S/. {info['precio']:.2f}",
                    size=16,
                    color=TEXT_SECONDARY
                ),
                ft.Text(
                    f"Duración: {info['duracion']}",
                    size=14,
                    color=TEXT_SECONDARY
                ),
                ft.Container(height=10),
                ft.Text(
                    "¿Deseas adquirir esta membresía?",
                    size=14,
                    color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD
                ),
            ], tight=True, spacing=8),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.ElevatedButton(
                    "Confirmar",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=info['color']
                    ),
                    on_click=compra_confirmada
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def mostrar_mensaje(mensaje, error=False):
        """Mostrar mensaje temporal"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#ef5350" if error else "#4CAF50",
            duration=3000
        )
        page.snack_bar.open = True
        page.update()

    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=PRIMARY_COLOR,
                        on_click=lambda _: on_back(),
                        icon_size=24
                    ),
                    ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=32, color=PRIMARY_COLOR),
                    ft.Text("Membresías Disponibles", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ], spacing=10),
                ft.ElevatedButton(
                    "Actualizar",
                    icon=ft.Icons.REFRESH,
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        bgcolor=ft.Colors.TRANSPARENT,
                        side=ft.border.all(1, PRIMARY_COLOR)
                    ),
                    on_click=lambda _: (cargar_membresia_actual(), cargar_membresias()),
                    height=40
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Layout principal
    main_content = ft.Column(
        controls=[
            header,
            ft.Container(
                content=ft.Column([
                    membresia_actual_container,
                    ft.Text(
                        "Planes Disponibles",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY
                    ),
                    membresias_container,
                ], spacing=15),
                padding=20
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    page.add(
        ft.Container(
            content=main_content,
            bgcolor=BACKGROUND_DARK,
            expand=True
        )
    )

    # Cargar datos iniciales
    cargar_membresia_actual()
    cargar_membresias()
