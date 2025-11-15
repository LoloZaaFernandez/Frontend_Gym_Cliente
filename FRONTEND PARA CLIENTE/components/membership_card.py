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
        "gradient_end": "#B8FF66",
        "duracion": "1 día",
        "icono": ft.Icons.BOLT_ROUNDED,  # Rayo = Rápido/Día
        "badge": "DÍA"
    },
    "Mensual": {
        "color": "#9FFF33",
        "gradient_start": "#9FFF33",
        "gradient_end": "#B8FF66",
        "duracion": "30 días",
        "icono": ft.Icons.CALENDAR_MONTH_ROUNDED,  # Calendario mensual
        "badge": "MENSUAL"
    },
    "Trimestral": {
        "color": "#8EE622",
        "gradient_start": "#8EE622",
        "gradient_end": "#A8FF55",
        "duracion": "90 días",
        "icono": ft.Icons.MULTIPLE_STOP_ROUNDED,  # 3 paradas = 3 meses
        "badge": "TRIMESTRAL"
    },
    "Semestral": {
        "color": "#7ACC00",
        "gradient_start": "#7ACC00",
        "gradient_end": "#9FFF33",
        "duracion": "180 días",
        "icono": ft.Icons.TIMELINE_ROUNDED,  # Línea de tiempo = Largo plazo
        "badge": "SEMESTRAL"
    },
    "Anual": {
        "color": "#6BB300",
        "gradient_start": "#6BB300",
        "gradient_end": "#8EE622",
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
        "gradient_end": "#B8FF66",
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
    Crear tarjeta de membresía MINIMAL para selección (registro)

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

    # Color para la tarjeta seleccionada (verde SUCCESS)
    select_color = Theme.SUCCESS if is_selected else Theme.PRIMARY

    # Construir contenido MINIMAL
    card_content = []

    # 🎨 HEADER MINIMAL - Solo badge tipo
    card_content.append(
        ft.Container(
            content=ft.Text(
                info['badge'],
                size=11,
                weight=ft.FontWeight.BOLD,
                color=select_color,
                text_align=ft.TextAlign.CENTER
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            margin=ft.margin.only(top=20, bottom=10),
            alignment=ft.alignment.center,
        )
    )

    # 💰 SECCIÓN DE PRECIO - DESTACADO Y LIMPIO
    card_content.append(
        ft.Container(
            content=ft.Column([
                # Nombre de la membresía
                ft.Text(
                    nombre.upper(),
                    size=20,
                    weight=ft.FontWeight.W_900,
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),

                ft.Container(height=16),

                # Precio destacado - MÁS GRANDE
                ft.Row([
                    ft.Text(
                        "S/",
                        size=22,
                        weight=ft.FontWeight.W_700,
                        color=select_color
                    ),
                    ft.Text(
                        f"{precio_actual:.2f}",
                        size=56,
                        weight=ft.FontWeight.W_900,
                        color=select_color
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),

                ft.Container(height=12),

                # Duración - SIMPLE
                ft.Row([
                    ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=16, color=Theme.TEXT_SECONDARY),
                    ft.Text(
                        info['duracion'],
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=Theme.TEXT_SECONDARY
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.symmetric(vertical=20, horizontal=20)
        )
    )

    # 📅 FECHA DE VALIDEZ - CENTRADA
    card_content.append(
        ft.Container(
            content=ft.Row([
                ft.Text(
                    "Válido hasta  ",
                    size=12,
                    color=Theme.TEXT_SECONDARY,
                    weight=ft.FontWeight.W_500
                ),
                ft.Text(
                    fecha_vencimiento.strftime('%d/%m/%Y'),
                    size=13,
                    color=Theme.TEXT_PRIMARY,
                    weight=ft.FontWeight.W_700
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.symmetric(vertical=14),
            alignment=ft.alignment.center
        )
    )

    # Espaciador
    card_content.append(ft.Container(height=10))

    # 🎯 BOTÓN DE SELECCIÓN - MINIMAL CON BLANCO
    if is_selected:
        # Botón de seleccionado - Verde Success
        card_content.append(
            ft.Container(
                content=ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=20, color="#0A0A0A"),
                        ft.Text("SELECCIONADA", size=14, weight=ft.FontWeight.BOLD, color="#0A0A0A")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    bgcolor=Theme.SUCCESS,
                    padding=ft.padding.symmetric(horizontal=32, vertical=16),
                    border_radius=12,
                    height=52,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=24, left=20, right=20)
            )
        )
    else:
        # Botón normal de selección - BLANCO para contraste
        card_content.append(
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Text("SELECCIONAR", size=14, weight=ft.FontWeight.BOLD, color="#0A0A0A"),
                    style=ft.ButtonStyle(
                        bgcolor="#FFFFFF",  # Blanco para contraste
                        padding=ft.padding.symmetric(horizontal=32, vertical=16),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation=0,
                    ),
                    on_click=on_select_click,
                    height=52,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=24, left=20, right=20)
            )
        )

    # Crear contenedor de tarjeta MINIMAL
    card = ft.Container(
        width=280,
        bgcolor="rgba(26, 26, 26, 0.8)",  # Más transparente para que no se pierda
        border_radius=20,
        padding=0,
        border=ft.border.all(2, select_color if is_selected else "rgba(255, 255, 255, 0.15)"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=24,
            color="rgba(0, 0, 0, 0.5)",
            offset=ft.Offset(0, 8)
        ),
        animate=200,
        content=ft.Column(card_content, spacing=0, tight=True)
    )

    # 🎭 EFECTO HOVER - MINIMAL
    def on_hover(e):
        if e.data == "true":
            card.scale = ft.Scale(1.03)
            card.border = ft.border.all(2, select_color)
            card.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=30,
                color=f"{select_color}60",
                offset=ft.Offset(0, 10)
            )
        else:
            card.scale = ft.Scale(1.0)
            card.border = ft.border.all(2, select_color if is_selected else "rgba(255, 255, 255, 0.15)")
            card.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=24,
                color="rgba(0, 0, 0, 0.5)",
                offset=ft.Offset(0, 8)
            )
        card.update()

    card.on_hover = on_hover
    card.animate_scale = 200

    return card
