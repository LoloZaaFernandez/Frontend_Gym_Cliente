"""
Componente MembershipCard - Tarjeta de Membresía PREMIUM
Adaptado del frontend admin para uso en tablets (cliente)

Tarjeta visual moderna para mostrar información de membresías
"""

import flet as ft
from datetime import datetime, timedelta
from config.theme import Theme


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
        "color": Theme.PRIMARY,
        "gradient_start": Theme.PRIMARY,
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


def create_membership_card(
    membresia: dict,
    precio_actual: float,
    on_select_click=None,
    is_selected: bool = False
) -> ft.Container:
    """
    Crear tarjeta de membresía para selección (registro)

    Args:
        membresia: Datos de la membresía (debe incluir tipo_membresia o nombre)
        precio_actual: Precio actual
        on_select_click: Callback para seleccionar la membresía
        is_selected: Si está seleccionada actualmente
    """
    # Intentar obtener el tipo de la membresía desde diferentes campos posibles
    tipo = membresia.get('tipo_membresia') or membresia.get('tipo') or 'Mensual'
    nombre = membresia.get('nombre_membresia') or membresia.get('nombre', 'Membresía')

    # Obtener estilo visual
    info = get_membership_style(tipo)

    # Calcular fecha de vencimiento
    fecha_vencimiento = calculate_expiration_date(tipo)

    # Construir contenido
    card_content = []

    # 🎨 HEADER CON GRADIENTE Y BADGE
    card_content.append(
        ft.Container(
            content=ft.Stack([
                # Fondo con color
                ft.Container(
                    bgcolor=info['color'],
                    border_radius=ft.border_radius.only(top_left=16, top_right=16),
                    height=100,
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
                    # Badge superior
                    ft.Container(
                        content=ft.Text(
                            info['badge'],
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF"
                        ),
                        bgcolor=f"{Theme.BACKGROUND_DARK}E6",
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
                    # Ícono central
                    ft.Container(
                        content=ft.Icon(
                            info['icono'],
                            size=32,
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

    # 💰 SECCIÓN DE PRECIO
    card_content.append(
        ft.Container(
            content=ft.Column([
                # Nombre de la membresía
                ft.Text(
                    nombre.upper(),
                    size=17,
                    weight=ft.FontWeight.W_800,
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                # Separador
                ft.Container(height=6),
                # Precio destacado
                ft.Row([
                    ft.Text(
                        "S/.",
                        size=18,
                        weight=ft.FontWeight.W_700,
                        color=info['color']
                    ),
                    ft.Text(
                        f"{precio_actual:.2f}",
                        size=38,
                        weight=ft.FontWeight.W_900,
                        color=info['color']
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                # Badge de duración
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=14, color=info['color']),
                        ft.Text(
                            info['duracion'],
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=Theme.TEXT_PRIMARY
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

    # 📋 BENEFICIOS
    card_content.append(
        ft.Container(
            content=ft.Column([
                # Beneficio 1
                ft.Row([
                    ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED, size=16, color=info['color']),
                    ft.Text("Acceso ilimitado al gimnasio", size=11, color=Theme.TEXT_PRIMARY,
                           weight=ft.FontWeight.W_500, expand=True)
                ], spacing=8),
                # Beneficio 2
                ft.Row([
                    ft.Icon(ft.Icons.GROUPS_ROUNDED, size=16, color=info['color']),
                    ft.Text("Todas las clases grupales", size=11, color=Theme.TEXT_PRIMARY,
                           weight=ft.FontWeight.W_500, expand=True)
                ], spacing=8),
                # Beneficio 3
                ft.Row([
                    ft.Icon(ft.Icons.SHOWER_ROUNDED, size=16, color=info['color']),
                    ft.Text("Uso de vestuarios y duchas", size=11, color=Theme.TEXT_PRIMARY,
                           weight=ft.FontWeight.W_500, expand=True)
                ], spacing=8),
                # Beneficio 4
                ft.Row([
                    ft.Icon(ft.Icons.SELF_IMPROVEMENT_ROUNDED, size=16, color=info['color']),
                    ft.Text("Asesoría personalizada", size=11, color=Theme.TEXT_PRIMARY,
                           weight=ft.FontWeight.W_500, expand=True)
                ], spacing=8),
            ], spacing=9),
            padding=ft.padding.symmetric(horizontal=16, vertical=14),
            bgcolor=f"{Theme.BACKGROUND_DARK}85",
            border_radius=10,
            margin=ft.margin.symmetric(horizontal=14),
            border=ft.border.all(1, f"{info['color']}18")
        )
    )

    # 📅 INFO ADICIONAL - FECHA DE VALIDEZ
    card_content.append(
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.EVENT_AVAILABLE_ROUNDED, size=17, color=Theme.TEXT_SECONDARY),
                ft.Text(
                    f"Válido hasta {fecha_vencimiento.strftime('%d/%m/%Y')}",
                    size=12,
                    color=Theme.TEXT_SECONDARY,
                    weight=ft.FontWeight.W_500
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=7),
            padding=ft.padding.symmetric(vertical=12)
        )
    )

    # Espaciador mínimo
    card_content.append(ft.Container(height=5))

    # 🎯 BOTÓN DE SELECCIÓN
    if is_selected:
        # Botón de seleccionado
        card_content.append(
            ft.Container(
                content=ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=20, color="#FFFFFF"),
                        ft.Text("SELECCIONADA", size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    bgcolor="#4CAF50",
                    padding=ft.padding.symmetric(horizontal=30, vertical=15),
                    border_radius=10,
                    height=48,
                    width=280
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=20, top=10, left=20, right=20)
            )
        )
    else:
        # Botón normal de selección
        card_content.append(
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.TOUCH_APP_ROUNDED, size=18, color="#FFFFFF"),
                        ft.Text("SELECCIONAR", size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    style=ft.ButtonStyle(
                        bgcolor=info['color'],
                        padding=ft.padding.symmetric(horizontal=30, vertical=15),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=5,
                        shadow_color=f"{info['color']}70"
                    ),
                    on_click=on_select_click,
                    height=48,
                    width=280
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=20, top=10, left=20, right=20)
            )
        )

    # Crear contenedor de tarjeta
    card = ft.Container(
        width=320,
        bgcolor=Theme.CARD_BG,
        border_radius=16,
        padding=0,
        border=ft.border.all(2, info['color'] if is_selected else "#2A2A2A"),
        shadow=ft.BoxShadow(
            spread_radius=0 if not is_selected else 2,
            blur_radius=20 if not is_selected else 28,
            color=f"{info['color']}30" if not is_selected else f"{info['color']}45",
            offset=ft.Offset(0, 8 if not is_selected else 12)
        ),
        animate=200,
        content=ft.Column(card_content, spacing=0, tight=True)
    )

    # 🎭 EFECTO HOVER - SUTIL Y PROFESIONAL
    def on_hover(e):
        if e.data == "true":
            card.scale = ft.Scale(1.02)
            card.shadow = ft.BoxShadow(
                spread_radius=2,
                blur_radius=28,
                color=f"{info['color']}45",
                offset=ft.Offset(0, 12)
            )
            if not is_selected:
                card.border = ft.border.all(2, info['color'])
        else:
            card.scale = ft.Scale(1.0)
            card.shadow = ft.BoxShadow(
                spread_radius=0 if not is_selected else 2,
                blur_radius=20 if not is_selected else 28,
                color=f"{info['color']}30" if not is_selected else f"{info['color']}45",
                offset=ft.Offset(0, 8 if not is_selected else 12)
            )
            if not is_selected:
                card.border = ft.border.all(2, "#2A2A2A")
        card.update()

    card.on_hover = on_hover

    return card
