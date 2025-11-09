"""
Componente MembershipCard - Tarjeta de Membresía PREMIUM
Sistema de Componentes Atómicos - Organism Level

Tarjeta visual moderna para mostrar información de membresías
Compatible con vistas de Cliente y Administrador
"""

import flet as ft
from datetime import datetime, timedelta
from config.theme import Theme
from config.settings import CARD_BG, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY_COLOR, BACKGROUND_DARK


# MAPEO DE COLORES Y ESTILOS POR TIPO
MEMBERSHIP_STYLES = {
    "Dia": {
        "color": Theme.PRIMARY,
        "gradient_start": Theme.PRIMARY,
        "gradient_end": "#FF8C61",
        "duracion": "1 día",
        "icono": ft.Icons.BOLT_ROUNDED,  # Rayo = Rápido/Día
        "badge": "DÍA"
    },
    "Mensual": {
        "color": "#FF6B35",
        "gradient_start": "#FF6B35",
        "gradient_end": "#FFA07A",
        "duracion": "30 días",
        "icono": ft.Icons.CALENDAR_MONTH_ROUNDED,  # Calendario mensual
        "badge": "MENSUAL"
    },
    "Trimestral": {
        "color": "#FFB84D",
        "gradient_start": "#FFB84D",
        "gradient_end": "#FFCC80",
        "duracion": "90 días",
        "icono": ft.Icons.MULTIPLE_STOP_ROUNDED,  # 3 paradas = 3 meses
        "badge": "TRIMESTRAL"
    },
    "Semestral": {
        "color": "#F4A261",
        "gradient_start": "#F4A261",
        "gradient_end": "#FFB88C",
        "duracion": "180 días",
        "icono": ft.Icons.TIMELINE_ROUNDED,  # Línea de tiempo = Largo plazo
        "badge": "SEMESTRAL"
    },
    "Anual": {
        "color": "#E76F51",
        "gradient_start": "#E76F51",
        "gradient_end": "#F4A261",
        "duracion": "365 días",
        "icono": ft.Icons.WORKSPACE_PREMIUM_ROUNDED,  # Premium = Mejor plan
        "badge": "ANUAL ⭐"
    }
}


def get_membership_style(tipo: str) -> dict:
    """Obtener estilo de membresía por tipo"""
    return MEMBERSHIP_STYLES.get(tipo, {
        "color": PRIMARY_COLOR,
        "gradient_start": PRIMARY_COLOR,
        "gradient_end": "#FF8C61",
        "duracion": "N/A",
        "icono": ft.Icons.CARD_MEMBERSHIP,
        "badge": "BÁSICO"
    })


def calculate_expiration_date(tipo: str) -> datetime:
    """Calcular fecha de vencimiento según tipo de membresía"""
    fecha = datetime.now()

    if tipo == "Dia":
        return fecha + timedelta(days=1)
    elif tipo == "Mensual":
        return fecha + timedelta(days=30)
    elif tipo == "Trimestral":
        return fecha + timedelta(days=90)
    elif tipo == "Semestral":
        return fecha + timedelta(days=180)
    elif tipo == "Anual":
        return fecha + timedelta(days=365)

    return fecha


class MembershipCard:
    """
    Tarjeta de Membresía Premium - Diseño Unificado

    Características:
    - Diseño moderno con gradientes y sombras
    - Efectos hover interactivos
    - Soporte para modo cliente y administrador
    - Información visual clara y atractiva
    """

    @staticmethod
    def create(
        membresia: dict,
        precio_actual: float,
        mode: str = "client",  # "client" o "admin"
        on_buy_click=None,
        on_edit_click=None,
        on_price_click=None,
        on_status_click=None
    ) -> ft.Container:
        """
        Crear tarjeta de membresía

        Args:
            membresia: Datos de la membresía
            precio_actual: Precio actual
            mode: Modo de visualización ("client" o "admin")
            on_buy_click: Callback para botón comprar (modo cliente)
            on_edit_click: Callback para botón editar (modo admin)
            on_price_click: Callback para botón precio (modo admin)
            on_status_click: Callback para cambiar estado (modo admin)
        """
        tipo = membresia.get('tipo_membresia', 'Mensual')
        nombre = membresia.get('nombre_membresia', 'Membresía')
        estado = membresia.get('estado', 'Activa')

        # Obtener estilo visual
        info = get_membership_style(tipo)

        # Calcular fecha de vencimiento
        fecha_vencimiento = calculate_expiration_date(tipo)

        # Indicador de estado (solo para admin)
        estado_color = "#4CAF50" if estado == "Activa" else "#ef5350"

        # Construir contenido según modo
        card_content = []

        # 🎨 HEADER CON GRADIENTE Y BADGE - COMPACTO Y PROPORCIONAL
        card_content.append(
            ft.Container(
                content=ft.Stack([
                    # Fondo con color y gradiente visual
                    ft.Container(
                        bgcolor=info['color'],
                        border_radius=ft.border_radius.only(top_left=16, top_right=16),
                        height=100,  # Más compacto
                    ),
                    # Overlay sutil para profundidad
                    ft.Container(
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=["#00000000", "#00000015"]
                        ),
                        border_radius=ft.border_radius.only(top_left=16, top_right=16),
                        height=100,
                    ),
                    # Contenido del header
                    ft.Column([
                        # Badge superior equilibrado
                        ft.Container(
                            content=ft.Text(
                                info['badge'],
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF"
                            ),
                            bgcolor=f"{BACKGROUND_DARK}E6",
                            padding=ft.padding.symmetric(horizontal=12, vertical=5),
                            border_radius=18,
                            margin=ft.margin.only(top=10, left=10),
                            alignment=ft.alignment.top_left,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=6,
                                color="#00000030",
                                offset=ft.Offset(0, 2)
                            )
                        ),
                        # Ícono central más pequeño y proporcional
                        ft.Container(
                            content=ft.Icon(
                                info['icono'],
                                size=32,  # Más pequeño para mejor proporción
                                color="#FFFFFF"
                            ),
                            margin=ft.margin.only(top=12),
                            alignment=ft.alignment.center
                        )
                    ], spacing=0)
                ], clip_behavior=ft.ClipBehavior.HARD_EDGE),
                border_radius=ft.border_radius.only(top_left=16, top_right=16),
            )
        )

        # 💰 SECCIÓN DE PRECIO - JERARQUÍA EQUILIBRADA
        card_content.append(
            ft.Container(
                content=ft.Column([
                    # Nombre de la membresía con buena legibilidad
                    ft.Text(
                        nombre.upper(),
                        size=17,  # Balanceado
                        weight=ft.FontWeight.W_800,
                        color=TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    # Separador sutil
                    ft.Container(height=6),
                    # Precio destacado proporcionado
                    ft.Row([
                        ft.Text(
                            "S/.",
                            size=18,
                            weight=ft.FontWeight.W_700,
                            color=info['color']
                        ),
                        ft.Text(
                            f"{precio_actual:.2f}",
                            size=38,  # Tamaño balanceado
                            weight=ft.FontWeight.W_900,
                            color=info['color']
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    # Badge de duración compacto
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=14, color=info['color']),
                            ft.Text(
                                info['duracion'],
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=TEXT_PRIMARY
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                        bgcolor=f"{info['color']}15",
                        padding=ft.padding.symmetric(horizontal=14, vertical=6),
                        border_radius=8,
                        margin=ft.margin.only(top=6),
                        border=ft.border.all(1, f"{info['color']}35")
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                padding=ft.padding.symmetric(vertical=18, horizontal=14)
            )
        )

        # 📋 BENEFICIOS (solo en modo cliente) - COMPACTOS
        if mode == "client":
            card_content.append(
                ft.Container(
                    content=ft.Column([
                        # Beneficio 1
                        ft.Row([
                            ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED, size=16, color=info['color']),
                            ft.Text("Acceso ilimitado al gimnasio", size=11, color=TEXT_PRIMARY,
                                   weight=ft.FontWeight.W_500, expand=True)
                        ], spacing=8),
                        # Beneficio 2
                        ft.Row([
                            ft.Icon(ft.Icons.GROUPS_ROUNDED, size=16, color=info['color']),
                            ft.Text("Todas las clases grupales", size=11, color=TEXT_PRIMARY,
                                   weight=ft.FontWeight.W_500, expand=True)
                        ], spacing=8),
                        # Beneficio 3
                        ft.Row([
                            ft.Icon(ft.Icons.SHOWER_ROUNDED, size=16, color=info['color']),
                            ft.Text("Uso de vestuarios y duchas", size=11, color=TEXT_PRIMARY,
                                   weight=ft.FontWeight.W_500, expand=True)
                        ], spacing=8),
                        # Beneficio 4
                        ft.Row([
                            ft.Icon(ft.Icons.SELF_IMPROVEMENT_ROUNDED, size=16, color=info['color']),
                            ft.Text("Asesoría personalizada", size=11, color=TEXT_PRIMARY,
                                   weight=ft.FontWeight.W_500, expand=True)
                        ], spacing=8),
                    ], spacing=9),
                    padding=ft.padding.symmetric(horizontal=16, vertical=14),
                    bgcolor=f"{BACKGROUND_DARK}85",
                    border_radius=10,
                    margin=ft.margin.symmetric(horizontal=14),
                    border=ft.border.all(1, f"{info['color']}18")
                )
            )

        # 📊 ESTADO (solo en modo admin) - DISEÑO MEJORADO
        if mode == "admin":
            card_content.append(
                ft.Container(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE_ROUNDED if estado == "Activa" else ft.Icons.CANCEL_ROUNDED,
                                size=18,
                                color=estado_color
                            ),
                            ft.Text(f"{estado}", size=14, color=estado_color, weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        bgcolor=f"{estado_color}15",
                        padding=ft.padding.symmetric(horizontal=16, vertical=10),
                        border_radius=10,
                        border=ft.border.all(1, f"{estado_color}40")
                    ),
                    margin=ft.margin.only(top=8, bottom=8, left=16, right=16)
                )
            )

        # 📅 INFO ADICIONAL - FECHA DE VALIDEZ
        card_content.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EVENT_AVAILABLE_ROUNDED, size=17, color=TEXT_SECONDARY),
                    ft.Text(
                        f"Válido hasta {fecha_vencimiento.strftime('%d/%m/%Y')}",
                        size=12,
                        color=TEXT_SECONDARY,
                        weight=ft.FontWeight.W_500
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=7),
                padding=ft.padding.symmetric(vertical=12)
            )
        )

        # Espaciador mínimo (sin expand para evitar que los botones se corten)
        card_content.append(ft.Container(height=5))

        # 🎯 BOTONES DE ACCIÓN - COMPACTOS Y SIEMPRE VISIBLES
        if mode == "client":
            # Botón de compra para cliente
            card_content.append(
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SHOPPING_CART_ROUNDED, size=18, color="#FFFFFF"),
                            ft.Text("COMPRAR AHORA", size=13, weight=ft.FontWeight.BOLD,
                                   color="#FFFFFF")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        style=ft.ButtonStyle(
                            bgcolor=info['color'],
                            padding=ft.padding.symmetric(horizontal=30, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=5,
                            shadow_color=f"{info['color']}70"
                        ),
                        on_click=on_buy_click,
                        height=48,
                        width=280
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=20, top=10, left=20, right=20)
                )
            )
        else:
            # Botones de administración - Compactos y visibles
            card_content.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "Editar",
                                icon=ft.Icons.EDIT_ROUNDED,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=PRIMARY_COLOR,
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=on_edit_click,
                                expand=True,
                                height=40
                            ),
                            ft.ElevatedButton(
                                "Precio",
                                icon=ft.Icons.PAYMENTS_ROUNDED,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor="#4CAF50",
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=on_price_click,
                                expand=True,
                                height=40
                            ),
                        ], spacing=8),
                        ft.ElevatedButton(
                            "Desactivar" if estado == "Activa" else "Activar",
                            icon=ft.Icons.TOGGLE_OFF_ROUNDED if estado == "Activa" else ft.Icons.TOGGLE_ON_ROUNDED,
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor="#ef5350" if estado == "Activa" else "#4CAF50",
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=on_status_click,
                            width=280,
                            height=40
                        ),
                    ], spacing=8, tight=True),
                    padding=ft.padding.only(top=10, bottom=20, left=20, right=20)
                )
            )

        # Crear contenedor de tarjeta con dimensiones balanceadas
        card = ft.Container(
            width=320,  # Tamaño óptimo
            # Sin altura fija para que se ajuste al contenido y los botones se vean completos
            bgcolor=CARD_BG,
            border_radius=16,  # Balance entre suave y definido
            padding=0,
            border=ft.border.all(2, "#2A2A2A"),  # Border sutil
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=f"{info['color']}30",
                offset=ft.Offset(0, 8)
            ),
            animate=200,
            content=ft.Column(card_content, spacing=0, tight=True)
        )

        # 🎭 EFECTO HOVER - SUTIL Y PROFESIONAL
        def on_hover(e):
            if e.data == "true":
                card.scale = ft.Scale(1.02)  # Sutil
                card.shadow = ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=28,
                    color=f"{info['color']}45",
                    offset=ft.Offset(0, 12)
                )
                card.border = ft.border.all(2, info['color'])
            else:
                card.scale = ft.Scale(1.0)
                card.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=20,
                    color=f"{info['color']}30",
                    offset=ft.Offset(0, 8)
                )
                card.border = ft.border.all(2, "#2A2A2A")
            card.update()

        card.on_hover = on_hover

        return card


class MembershipStatusCard:
    """
    Tarjeta de Estado de Membresía

    Muestra el estado actual de la membresía del cliente con diseño premium
    """

    @staticmethod
    def create_active(
        fecha_vencimiento: datetime,
        dias_restantes: int,
        on_renew_click=None
    ) -> ft.Container:
        """Crear tarjeta de membresía activa"""

        # Determinar color según días restantes
        estado_color = PRIMARY_COLOR if dias_restantes > 7 else "#FF9800" if dias_restantes > 0 else "#EF5350"

        return ft.Container(
            width=380,
            bgcolor=CARD_BG,
            border_radius=16,
            padding=0,
            border=ft.border.all(2, estado_color),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=25,
                color=f"{estado_color}40",
                offset=ft.Offset(0, 8)
            ),
            content=ft.Column([
                # Header premium
                ft.Container(
                    content=ft.Stack([
                        # Fondo
                        ft.Container(
                            bgcolor=estado_color,
                            border_radius=ft.border_radius.only(top_left=16, top_right=16),
                            height=120,
                        ),
                        # Contenido
                        ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.WORKSPACE_PREMIUM_ROUNDED, size=32, color="#FFFFFF"),
                                ft.Text(
                                    "MI MEMBRESÍA",
                                    size=20,
                                    weight=ft.FontWeight.W_900,
                                    color="#FFFFFF"
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                            ft.Container(
                                content=ft.Text(
                                    "ACTIVA" if dias_restantes > 0 else "VENCE HOY",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color="#FFFFFF"
                                ),
                                bgcolor=f"{BACKGROUND_DARK}E6",
                                padding=ft.padding.symmetric(horizontal=20, vertical=8),
                                border_radius=25,
                                margin=ft.margin.only(top=12),
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=8,
                                    color="#00000040",
                                    offset=ft.Offset(0, 2)
                                )
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                           alignment=ft.MainAxisAlignment.CENTER,
                           spacing=0)
                    ]),
                    border_radius=ft.border_radius.only(top_left=16, top_right=16),
                ),

                # Información detallada
                ft.Container(
                    content=ft.Column([
                        # Fecha de vencimiento
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CALENDAR_MONTH, size=22, color=estado_color),
                                ft.Column([
                                    ft.Text("VENCIMIENTO", size=10, color=TEXT_SECONDARY),
                                    ft.Text(
                                        fecha_vencimiento.strftime("%d/%m/%Y"),
                                        size=16,
                                        color=TEXT_PRIMARY,
                                        weight=ft.FontWeight.BOLD
                                    )
                                ], spacing=2)
                            ], spacing=12),
                            bgcolor=f"{BACKGROUND_DARK}60",
                            padding=15,
                            border_radius=10
                        ),

                        # Días restantes
                        ft.Container(
                            content=ft.Column([
                                ft.Text("TIEMPO RESTANTE", size=10, color=TEXT_SECONDARY,
                                       text_align=ft.TextAlign.CENTER),
                                ft.Row([
                                    ft.Icon(
                                        ft.Icons.TIMER if dias_restantes > 0 else ft.Icons.WARNING_AMBER_ROUNDED,
                                        size=32,
                                        color=estado_color
                                    ),
                                    ft.Text(
                                        f"{dias_restantes}" if dias_restantes > 0 else "0",
                                        size=36,
                                        color=estado_color,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        "días" if dias_restantes != 1 else "día",
                                        size=16,
                                        color=TEXT_SECONDARY,
                                        weight=ft.FontWeight.W_500
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                            bgcolor=f"{estado_color}10",
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, f"{estado_color}30")
                        ),
                    ], spacing=12),
                    padding=20
                ),

                # Botón de renovar
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.AUTORENEW, size=22, color="#FFFFFF"),
                            ft.Text("RENOVAR MEMBRESÍA", size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        style=ft.ButtonStyle(
                            bgcolor=PRIMARY_COLOR,
                            padding=ft.padding.symmetric(horizontal=30, vertical=18),
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation=4
                        ),
                        on_click=on_renew_click,
                        height=55,
                        width=340
                    ),
                    padding=ft.padding.only(bottom=20, left=20, right=20, top=5)
                )
            ], spacing=0)
        )

    @staticmethod
    def create_status(
        titulo: str,
        subtitulo: str,
        accion: str,
        color: str,
        on_action_click=None
    ) -> ft.Container:
        """Crear tarjeta de estado genérica (sin membresía, vencida, error)"""

        # Determinar ícono según el estado - ICONOS MEJORADOS
        icono = ft.Icons.ERROR_OUTLINE_ROUNDED
        if "VENCIDA" in titulo:
            icono = ft.Icons.CANCEL_ROUNDED
        elif "SIN" in titulo:
            icono = ft.Icons.CARD_MEMBERSHIP_OUTLINED
        elif "ERROR" in titulo:
            icono = ft.Icons.WARNING_ROUNDED

        return ft.Container(
            width=380,
            bgcolor=CARD_BG,
            border_radius=16,
            padding=0,
            border=ft.border.all(2, color),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=25,
                color=f"{color}40",
                offset=ft.Offset(0, 8)
            ),
            content=ft.Column([
                # Header mejorado
                ft.Container(
                    content=ft.Column([
                        ft.Icon(icono, size=60, color=color),  # Ícono más grande
                        ft.Text(
                            titulo,
                            size=20,
                            weight=ft.FontWeight.W_900,
                            color=TEXT_PRIMARY,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=18),
                    padding=35,
                    bgcolor=f"{color}12"
                ),

                # Contenido
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            subtitulo,
                            size=14,
                            color=TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_500
                        ),
                        ft.Container(height=5),
                        ft.Text(
                            "¡No te pierdas los beneficios de entrenar!",
                            size=12,
                            color=TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                            italic=True
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20
                ),

                # Botón de acción
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SHOPPING_CART_ROUNDED, size=20, color="#FFFFFF"),
                            ft.Text(accion, size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        style=ft.ButtonStyle(
                            bgcolor=color,
                            padding=ft.padding.symmetric(horizontal=30, vertical=18),
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation=4
                        ),
                        on_click=on_action_click,
                        height=55,
                        width=340
                    ),
                    padding=ft.padding.only(bottom=20, left=20, right=20)
                )
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
