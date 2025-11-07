"""
Vista de Membresías para Clientes - CORREGIDA
Muestra membresías activas desde el backend y permite comprarlas
"""

import flet as ft
from datetime import datetime, timedelta
from config.settings import PRIMARY_COLOR, TEXT_SECONDARY, CARD_BG, TEXT_PRIMARY, BACKGROUND_DARK
from services.api_service import APIService


def show_membresias_view(page: ft.Page, auth_service, on_back):
    """
    Mostrar vista de membresías disponibles - CORREGIDA

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
    
    # MAPEO DE COLORES E ICONOS POR TIPO
    tipo_visual = {
        "Dia": {"color": "#FF9800", "duracion": "1 día", "icono": ft.Icons.TODAY},
        "Mensual": {"color": PRIMARY_COLOR, "duracion": "30 días", "icono": ft.Icons.CALENDAR_MONTH},
        "Trimestral": {"color": "#4CAF50", "duracion": "90 días", "icono": ft.Icons.CALENDAR_TODAY},
        "Semestral": {"color": "#2196F3", "duracion": "180 días", "icono": ft.Icons.DATE_RANGE},
        "Anual": {"color": "#9C27B0", "duracion": "365 días", "icono": ft.Icons.CALENDAR_VIEW_MONTH}
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

        try:
            # Obtener cliente actualizado desde el backend
            cliente_info = api.get_cliente_por_id(cliente_id)
            fecha_membresia = cliente_info.get('fecha_membresia')

            if fecha_membresia:
                try:
                    fecha_venc = datetime.fromisoformat(fecha_membresia)
                    fecha_actual = datetime.now()
                    dias_restantes = (fecha_venc - fecha_actual).days

                    if dias_restantes > 0:
                        # Membresía activa
                        membresia_tipo = "Activa"
                        
                        # Obtener el último pago para saber qué tipo de membresía tiene
                        try:
                            pagos = api.get_pagos_membresia_cliente(cliente_id)
                            if pagos:
                                ultimo_pago = pagos[0]
                                
                                # Obtener info de la membresía
                                try:
                                    membresias = api.get_membresias()
                                    for m in membresias:
                                        if m['id'] == ultimo_pago.get('id_membresia'):
                                            membresia_tipo = m.get('nombre_membresia', 'Activa')
                                            break
                                except:
                                    pass
                        except:
                            pass

                        membresia_actual_container.content = ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=30, color="#4CAF50"),
                                    ft.Text(
                                        f"Membresía {membresia_tipo}",
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
                except Exception as e:
                    print(f"Error al procesar fecha: {e}")
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
            membresia_actual_container.content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, size=30, color="#ef5350"),
                    ft.Text("Error al cargar información de membresía", color=TEXT_SECONDARY, size=14),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                bgcolor=CARD_BG,
                border_radius=12,
                padding=20,
                border=ft.border.all(2, "#ef5350"),
                margin=ft.margin.only(bottom=20)
            )

        page.update()

    def cargar_membresias():
        """✅ CORREGIDO: Cargar membresías ACTIVAS con precios"""
        membresias_container.controls.clear()

        try:
            # ✅ IMPORTANTE: Solo obtener membresías ACTIVAS
            membresias = api.get_membresias(estado="Activa")
            
            print(f"🔍 DEBUG: Se encontraron {len(membresias)} membresías activas")  # Para depuración

            if not membresias:
                membresias_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INBOX, size=80, color="#333333"),
                            ft.Text("No hay membresías disponibles", color=TEXT_SECONDARY, size=16),
                            ft.Text("Contacta al administrador", color="#666666", size=14),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        padding=40,
                        alignment=ft.alignment.center
                    )
                )
            else:
                # ✅ Procesar cada membresía
                for membresia in membresias:
                    # ✅ Obtener precio real desde el backend
                    try:
                        precio_data = api.get_precio_membresia(membresia['id'])
                        if precio_data and 'precio_actual' in precio_data:
                            precio_actual = float(precio_data['precio_actual'])
                            
                            # Solo mostrar si tiene precio válido
                            if precio_actual > 0:
                                print(f"✅ Membresía: {membresia['nombre_membresia']} - S/. {precio_actual:.2f}")
                                membresias_container.controls.append(
                                    crear_plan_card(membresia, precio_actual)
                                )
                            else:
                                print(f"⚠️ Membresía sin precio: {membresia['nombre_membresia']}")
                        else:
                            print(f"⚠️ No se pudo obtener precio de: {membresia['nombre_membresia']}")
                    except Exception as e:
                        print(f"❌ Error al obtener precio de {membresia['nombre_membresia']}: {e}")
                        continue

        except Exception as e:
            print(f"❌ Error al cargar membresías: {e}")
            mostrar_mensaje("Error al cargar membresías desde el servidor", error=True)
            membresias_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR, size=60, color="#ef5350"),
                        ft.Text("Error al conectar con el servidor", color=TEXT_SECONDARY, size=14),
                        ft.Text(str(e), color="#666666", size=12),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )

        page.update()

    def crear_plan_card(membresia, precio_actual):
        """Crear tarjeta visual de membresía"""
        tipo = membresia['tipo_membresia']
        nombre = membresia['nombre_membresia']
        info = tipo_visual.get(tipo, {"color": PRIMARY_COLOR, "duracion": "N/A", "icono": ft.Icons.CARD_MEMBERSHIP})

        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(info['icono'], size=16, color=ft.Colors.WHITE),
                        ft.Text(tipo, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ], spacing=5),
                    bgcolor=info['color'],
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=20,
                    margin=ft.margin.only(bottom=10)
                ),
                ft.Text(nombre, size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                ft.Text(f"S/. {precio_actual:.2f}", size=32, weight=ft.FontWeight.BOLD, color=info['color'], text_align=ft.TextAlign.CENTER),
                ft.Text(info['duracion'], size=14, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                ft.Divider(height=1, color="#333333"),
                ft.ElevatedButton(
                    "Adquirir Plan",
                    icon=ft.Icons.SHOPPING_CART,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=info['color']),
                    width=220,
                    height=45,
                    on_click=lambda e, m=membresia, p=precio_actual: confirmar_compra(m, p, info)
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            bgcolor=CARD_BG,
            border_radius=12,
            padding=25,
            border=ft.border.all(2 if tipo == "Trimestral" else 1, info['color'] if tipo == "Trimestral" else "#333333"),
            width=280
        )

    def confirmar_compra(membresia, precio_actual, visual):
        """Confirmar compra de membresía"""
        metodo_pago = ft.Dropdown(
            label="Método de Pago",
            options=[
                ft.dropdown.Option("Efectivo"),
                ft.dropdown.Option("Transferencia"),
                ft.dropdown.Option("Yape"),
                ft.dropdown.Option("Plin"),
            ],
            value="Efectivo",
            color=TEXT_PRIMARY,
            border_color="#333333",
            focused_border_color=visual['color'],
            width=300
        )

        def close_dialog(e):
            page.close(dialog)

        def procesar_compra(e):
            if not metodo_pago.value:
                mostrar_mensaje("⚠ Por favor selecciona un método de pago", error=True)
                return

            page.close(dialog)

            try:
                # ✅ Realizar compra
                resultado = api.comprar_membresia(
                    cliente_id=cliente_id,
                    membresia_id=membresia['id'],
                    monto=precio_actual,
                    metodo_pago=metodo_pago.value
                )

                mostrar_mensaje(f"✅ ¡Membresía adquirida! Pago: {metodo_pago.value} - S/. {precio_actual:.2f}", error=False)
                
                # ✅ Recargar información
                cargar_membresia_actual()

            except ValueError as e:
                mostrar_mensaje(f"❌ Error: {str(e)}", error=True)
            except Exception as e:
                mostrar_mensaje(f"❌ Error inesperado: {str(e)}", error=True)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.SHOPPING_CART, color=visual['color']),
                ft.Text(f"Comprar - {membresia['nombre_membresia']}", color=TEXT_PRIMARY)
            ], spacing=10),
            content=ft.Column([
                ft.Text(f"Precio: S/. {precio_actual:.2f}", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                metodo_pago,
            ], tight=True, spacing=15, width=350),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.ElevatedButton(
                    "Confirmar Compra",
                    icon=ft.Icons.CHECK_CIRCLE,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=visual['color']),
                    on_click=procesar_compra
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)

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
        content=ft.Row([
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=PRIMARY_COLOR, on_click=lambda _: on_back(), icon_size=24),
                ft.Icon(ft.Icons.CARD_MEMBERSHIP, size=32, color=PRIMARY_COLOR),
                ft.Text("Membresías Disponibles", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ], spacing=10),
            ft.ElevatedButton(
                "Actualizar",
                icon=ft.Icons.REFRESH,
                style=ft.ButtonStyle(color=PRIMARY_COLOR, bgcolor=ft.Colors.TRANSPARENT, side=ft.border.all(1, PRIMARY_COLOR)),
                on_click=lambda _: (cargar_membresia_actual(), cargar_membresias()),
                height=40
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=20,
        bgcolor=CARD_BG,
        border_radius=12,
        margin=10,
        border=ft.border.all(1, "#333333")
    )

    # Layout principal
    main_content = ft.Column([
        header,
        ft.Container(
            content=ft.Column([
                membresia_actual_container,
                ft.Text("Planes Disponibles", size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                membresias_container,
            ], spacing=15),
            padding=20
        ),
    ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    page.add(ft.Container(content=main_content, bgcolor=BACKGROUND_DARK, expand=True))

    # ✅ Cargar datos al iniciar
    cargar_membresia_actual()
    cargar_membresias()