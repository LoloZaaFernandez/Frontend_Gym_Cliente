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
    # MAPEO DE COLORES E ICONOS POR TIPO (visual, no datos)
    tipo_visual = {
        "Dia": {"color": "#FF9800", "icono": ft.Icons.TODAY},
        "Mensual": {"color": PRIMARY_COLOR, "icono": ft.Icons.CALENDAR_MONTH},
        "Trimestral": {"color": "#4CAF50", "icono": ft.Icons.CALENDAR_TODAY},
        "Semestral": {"color": "#2196F3", "icono": ft.Icons.DATE_RANGE},
        "Anual": {"color": "#9C27B0", "icono": ft.Icons.CALENDAR_VIEW_MONTH}
    }
    
    #  DURACIONES PARA CÁLCULO (días)
    duraciones_dias = {
        "Dia": 1,
        "Mensual": 30,
        "Trimestral": 90,
        "Semestral": 180,
        "Anual": 365
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
                        # Obtener el último pago para saber qué tipo de membresía tiene
                        try:
                            pagos = api.get_pagos_membresia_cliente(cliente_id)
                            if pagos:
                                ultimo_pago = pagos[0]  # El más reciente
                                membresia_tipo = "Activa"
                                
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
                            membresia_tipo = "Activa"

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
            # Mostrar mensaje de error
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
        """Cargar membresías disponibles desde el backend"""
        membresias_container.controls.clear()

        try:
            # Obtener solo membresías ACTIVAS desde el backend
            membresias = api.get_membresias(estado="Activa")

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
                for membresia in membresias:
                    # Obtener precio real desde el backend
                    try:
                        precio_data = api.get_precio_membresia(membresia['id'])
                        precio_actual = float(precio_data['precio_actual']) if precio_data else 0.0
                    except Exception as e:
                        print(f"Error al obtener precio de {membresia['nombre_membresia']}: {e}")
                        precio_actual = 0.0

                    # Si el precio es 0, no mostrar esta membresía
                    if precio_actual <= 0:
                        continue

                    # Crear tarjeta con datos reales
                    membresias_container.controls.append(
                        crear_plan_card(membresia, precio_actual)
                    )

        except Exception as e:
            print(f"Error al cargar membresías: {e}")
            mostrar_mensaje("Error al cargar membresías", error=True)
            membresias_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR, size=60, color="#ef5350"),
                        ft.Text("Error al conectar con el servidor", color=TEXT_SECONDARY, size=14),
                        ft.Text("Verifica tu conexión e intenta nuevamente", color="#666666", size=12),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )

        page.update()

    def crear_plan_card(membresia, precio_actual):
        """Crear tarjeta de plan de membresía con datos del backend"""
        tipo = membresia['tipo_membresia']
        nombre = membresia['nombre_membresia']
        
        # Obtener info visual del tipo
        visual = tipo_visual.get(tipo, {"color": PRIMARY_COLOR, "icono": ft.Icons.CARD_MEMBERSHIP})
        
        # Calcular duración en días
        duracion_dias = duraciones_dias.get(tipo, 30)
        duracion_text = f"{duracion_dias} día{'s' if duracion_dias != 1 else ''}"
        
        # Calcular precio mensual si aplica
        precio_mes = None
        if tipo in ["Trimestral", "Semestral", "Anual"]:
            meses = {"Trimestral": 3, "Semestral": 6, "Anual": 12}[tipo]
            precio_mes = precio_actual / meses
            precio_mes_text = ft.Text(
                f"S/. {precio_mes:.2f}/mes",
                size=13,
                color=TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER
            )
        else:
            precio_mes_text = None
        
        # Calcular ahorro si aplica
        badge_ahorro = None
        if tipo in ["Trimestral", "Semestral", "Anual"]:
            # Obtener precio mensual para calcular ahorro
            try:
                membresias_todas = api.get_membresias(estado="Activa")
                precio_mensual = None
                for m in membresias_todas:
                    if m['tipo_membresia'] == "Mensual":
                        precio_data = api.get_precio_membresia(m['id'])
                        precio_mensual = float(precio_data['precio_actual']) if precio_data else None
                        break
                
                if precio_mensual and precio_mes:
                    ahorro_porcentaje = ((precio_mensual - precio_mes) / precio_mensual) * 100
                    if ahorro_porcentaje > 0:
                        badge_ahorro = ft.Container(
                            content=ft.Text(
                                f"Ahorra {ahorro_porcentaje:.0f}%",
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                            bgcolor=visual['color'],
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=20,
                            margin=ft.margin.only(bottom=10)
                        )
            except:
                pass
        
        # Generar lista de beneficios genérica basada en el tipo
        beneficios = [
            "Acceso completo al gimnasio",
            "Vestuarios y duchas"
        ]
        
        if tipo == "Mensual":
            beneficios.extend([
                "Clases grupales ilimitadas",
                "Asesoría básica"
            ])
        elif tipo == "Trimestral":
            beneficios.extend([
                "Clases grupales ilimitadas",
                "1 evaluación física gratis",
                "Plan nutricional básico",
                "Descuento 10% en productos"
            ])
        elif tipo in ["Semestral", "Anual"]:
            beneficios.extend([
                "Clases grupales ilimitadas",
                "Evaluaciones físicas mensuales",
                "Plan nutricional personalizado",
                "Descuento 15% en productos",
                "Invitaciones a eventos exclusivos"
            ])
        
        beneficios_list = ft.Column(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=visual['color']),
                    ft.Text(beneficio, size=12, color=TEXT_SECONDARY, expand=True)
                ], spacing=8)
                for beneficio in beneficios
            ],
            spacing=8
        )
        
        # Construir contenido de la tarjeta
        card_content = []
        
        if badge_ahorro:
            card_content.append(badge_ahorro)
        
        card_content.extend([
            ft.Container(
                content=ft.Icon(visual['icono'], size=16, color=ft.Colors.WHITE),
                bgcolor=visual['color'],
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
                margin=ft.margin.only(bottom=10)
            ),
            ft.Text(
                nombre,
                size=18,
                weight=ft.FontWeight.BOLD,
                color=visual['color'],
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                f"S/. {precio_actual:.2f}",
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
                duracion_text,
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
                    bgcolor=visual['color'],
                ),
                width=220,
                height=45,
                on_click=lambda e, m=membresia, p=precio_actual: confirmar_compra(m, p, visual)
            ),
        ])
        
        # Destacar trimestral si existe
        destacado = tipo == "Trimestral"
        border_width = 2 if destacado else 1
        border_color = visual['color'] if destacado else "#333333"
        
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
                color=f"{visual['color']}44" if destacado else ft.Colors.BLACK26,
                offset=ft.Offset(0, 4)
            ),
            width=280
        )
    def confirmar_compra(membresia, precio_actual, visual):
        """Confirmar compra de membresía con selección de método de pago"""

        # Dropdown para seleccionar método de pago
        metodo_pago = ft.Dropdown(
            label="Método de Pago",
            options=[
                ft.dropdown.Option("Efectivo", "💵 Efectivo"),
                ft.dropdown.Option("Transferencia", "🏦 Transferencia"),
                ft.dropdown.Option("Yape", "📱 Yape"),
                
            ],
            value="Efectivo",  # Por defecto Efectivo
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

            # Realizar compra a través del backend
            try:
                resultado = api.comprar_membresia(
                    cliente_id=cliente_id,
                    membresia_id=membresia['id'],
                    monto=precio_actual,  # Usar precio_actual en lugar de info['precio']
                    metodo_pago=metodo_pago.value
                )

                # Mostrar mensaje de éxito con método de pago
                mostrar_mensaje(
                    f" ¡Membresía adquirida! Pago: {metodo_pago.value} - S/. {precio_actual:.2f}",
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
                    mostrar_mensaje(f"❌ Error: {error_msg}", error=True)
            except Exception as e:
                mostrar_mensaje(f"❌ Error inesperado: {str(e)}", error=True)
        # Calcular duración
        tipo = membresia['tipo_membresia']
        duracion_text = f"{duraciones_dias.get(tipo, 30)} días"
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.SHOPPING_CART, color=visual['color']),  
                ft.Text(f"Comprar - {membresia['nombre_membresia']}", color=TEXT_PRIMARY)
            ], spacing=10),
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CALENDAR_MONTH, size=20, color=visual['color']),  
                            ft.Text(f"Duración: {duracion_text}", size=14, color=TEXT_SECONDARY),
                        ], spacing=5),
                        ft.Container(height=5),
                        ft.Row([
                            ft.Icon(ft.Icons.ATTACH_MONEY, size=20, color=visual['color']),  
                            ft.Text(f"Precio: S/. {precio_actual:.2f}", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),  
                        ], spacing=5),
                    ]),
                    padding=15,
                    bgcolor="#1A1A1A",
                    border_radius=8,
                    border=ft.border.all(1, "#333333")
                ),
                ft.Container(height=10),
                ft.Text("Selecciona el método de pago:", size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD),
                metodo_pago,
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color="#2196F3"),
                        ft.Text(
                            "Tu membresía se activará inmediatamente",
                            size=12,
                            color=TEXT_SECONDARY,
                            italic=True
                        ),
                    ], spacing=5),
                    margin=ft.margin.only(top=10)
                )
            ], tight=True, spacing=10, width=350),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.ElevatedButton(
                    "Confirmar Compra",
                    icon=ft.Icons.CHECK_CIRCLE,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=visual['color']  
                    ),
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
