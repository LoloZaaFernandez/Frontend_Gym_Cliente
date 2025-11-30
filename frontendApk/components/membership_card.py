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
        # Vence al final del mismo día (23:59:59)
        return fecha.replace(hour=23, minute=59, second=59, microsecond=999999)
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
    is_selected: bool = False,
    page_width: float = None
) -> ft.Container:
    """
    Crear tarjeta de membresía MINIMAL para selección (registro) - RESPONSIVE

    Args:
        membresia: Datos de la membresía (debe incluir tipo_membresia o nombre)
        precio_actual: Precio actual
        on_select_click: Callback para seleccionar la membresía
        is_selected: Si está seleccionada actualmente
        page_width: Ancho de la página para cálculo responsive
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

    # Calcular dimensiones y tamaños responsive
    card_width = 280
    badge_size = 11
    nombre_size = 20
    precio_label_size = 22
    precio_size = 56
    duracion_icon_size = 16
    duracion_text_size = 14
    fecha_label_size = 12
    fecha_value_size = 13
    button_text_size = 14
    button_icon_size = 20
    button_height = 52
    padding_top = 20
    padding_bottom = 10
    padding_h_badge = 14
    padding_v_badge = 8
    padding_section = 20
    margin_bottom = 16
    spacing_precio = 6

    if page_width:
        # Escalar proporcionalmente basado en el ancho de la página
        scale = page_width / Theme.BASE_WIDTH
        # Limitar el factor de escala
        scale = max(0.75, min(1.25, scale))

        card_width = int(280 * scale)
        badge_size = int(11 * scale)
        nombre_size = int(20 * scale)
        precio_label_size = int(22 * scale)
        precio_size = int(56 * scale)
        duracion_icon_size = int(16 * scale)
        duracion_text_size = int(14 * scale)
        fecha_label_size = int(12 * scale)
        fecha_value_size = int(13 * scale)
        button_text_size = int(14 * scale)
        button_icon_size = int(20 * scale)
        button_height = int(52 * scale)
        padding_top = int(20 * scale)
        padding_bottom = int(10 * scale)
        padding_h_badge = int(14 * scale)
        padding_v_badge = int(8 * scale)
        padding_section = int(20 * scale)
        margin_bottom = int(16 * scale)
        spacing_precio = int(6 * scale)

    # Construir contenido MINIMAL
    card_content = []

    # 🎨 HEADER MINIMAL - Solo badge tipo
    card_content.append(
        ft.Container(
            content=ft.Text(
                info['badge'],
                size=badge_size,
                weight=ft.FontWeight.BOLD,
                color=select_color,
                text_align=ft.TextAlign.CENTER
            ),
            padding=ft.padding.symmetric(horizontal=padding_h_badge, vertical=padding_v_badge),
            margin=ft.margin.only(top=padding_top, bottom=padding_bottom),
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
                    size=nombre_size,
                    weight=ft.FontWeight.W_900,
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),

                ft.Container(height=margin_bottom),

                # Precio destacado - MÁS GRANDE
                ft.Row([
                    ft.Text(
                        "S/",
                        size=precio_label_size,
                        weight=ft.FontWeight.W_700,
                        color=select_color
                    ),
                    ft.Text(
                        f"{precio_actual:.2f}",
                        size=precio_size,
                        weight=ft.FontWeight.W_900,
                        color=select_color
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=spacing_precio),

                ft.Container(height=int(margin_bottom * 0.75)),

                # Duración - SIMPLE
                ft.Row([
                    ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=duracion_icon_size, color=Theme.TEXT_SECONDARY),
                    ft.Text(
                        info['duracion'],
                        size=duracion_text_size,
                        weight=ft.FontWeight.W_600,
                        color=Theme.TEXT_SECONDARY
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=spacing_precio),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.symmetric(vertical=padding_section, horizontal=padding_section)
        )
    )

    # 📅 FECHA DE VALIDEZ - CENTRADA
    card_content.append(
        ft.Container(
            content=ft.Row([
                ft.Text(
                    "Válido hasta  ",
                    size=fecha_label_size,
                    color=Theme.TEXT_SECONDARY,
                    weight=ft.FontWeight.W_500
                ),
                ft.Text(
                    fecha_vencimiento.strftime('%d/%m/%Y'),
                    size=fecha_value_size,
                    color=Theme.TEXT_PRIMARY,
                    weight=ft.FontWeight.W_700
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.symmetric(vertical=int(14 * (page_width / Theme.BASE_WIDTH) if page_width else 14)),
            alignment=ft.alignment.center
        )
    )

    # Espaciador
    espaciador_height = int(10 * (page_width / Theme.BASE_WIDTH)) if page_width else 10
    card_content.append(ft.Container(height=espaciador_height))

    # Padding de botones
    button_padding_h = int(32 * (page_width / Theme.BASE_WIDTH)) if page_width else 32
    button_padding_v = int(16 * (page_width / Theme.BASE_WIDTH)) if page_width else 16
    button_padding_outer = int(24 * (page_width / Theme.BASE_WIDTH)) if page_width else 24
    button_padding_side = int(20 * (page_width / Theme.BASE_WIDTH)) if page_width else 20
    button_spacing = int(10 * (page_width / Theme.BASE_WIDTH)) if page_width else 10
    border_radius_btn = int(12 * (page_width / Theme.BASE_WIDTH)) if page_width else 12

    # 🎯 BOTÓN DE SELECCIÓN - MINIMAL CON BLANCO
    if is_selected:
        # Botón de seleccionado - Verde Success
        card_content.append(
            ft.Container(
                content=ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=button_icon_size, color="#0A0A0A"),
                        ft.Text("SELECCIONADA", size=button_text_size, weight=ft.FontWeight.BOLD, color="#0A0A0A")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=button_spacing),
                    bgcolor=Theme.SUCCESS,
                    padding=ft.padding.symmetric(horizontal=button_padding_h, vertical=button_padding_v),
                    border_radius=border_radius_btn,
                    height=button_height,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=button_padding_outer, left=button_padding_side, right=button_padding_side)
            )
        )
    else:
        # Botón normal de selección - BLANCO para contraste
        card_content.append(
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Text("SELECCIONAR", size=button_text_size, weight=ft.FontWeight.BOLD, color="#0A0A0A"),
                    style=ft.ButtonStyle(
                        bgcolor="#FFFFFF",  # Blanco para contraste
                        padding=ft.padding.symmetric(horizontal=button_padding_h, vertical=button_padding_v),
                        shape=ft.RoundedRectangleBorder(radius=border_radius_btn),
                        elevation=0,
                    ),
                    on_click=on_select_click,
                    height=button_height,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=button_padding_outer, left=button_padding_side, right=button_padding_side)
            )
        )

    # Calcular valores responsive para el contenedor de la tarjeta
    border_width = int(2 * (page_width / Theme.BASE_WIDTH)) if page_width else 2
    border_radius_card = int(20 * (page_width / Theme.BASE_WIDTH)) if page_width else 20
    shadow_blur = int(24 * (page_width / Theme.BASE_WIDTH)) if page_width else 24
    shadow_offset_y = int(8 * (page_width / Theme.BASE_WIDTH)) if page_width else 8
    shadow_blur_hover = int(30 * (page_width / Theme.BASE_WIDTH)) if page_width else 30
    shadow_offset_y_hover = int(10 * (page_width / Theme.BASE_WIDTH)) if page_width else 10

    # Crear contenedor de tarjeta MINIMAL
    card = ft.Container(
        width=card_width,
        bgcolor="rgba(26, 26, 26, 0.8)",  # Más transparente para que no se pierda
        border_radius=border_radius_card,
        padding=0,
        border=ft.border.all(border_width, select_color if is_selected else "rgba(255, 255, 255, 0.15)"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=shadow_blur,
            color="rgba(0, 0, 0, 0.5)",
            offset=ft.Offset(0, shadow_offset_y)
        ),
        animate=200,
        content=ft.Column(card_content, spacing=0, tight=True)
    )

    # 🎭 EFECTO HOVER - MINIMAL
    def on_hover(e):
        if e.data == "true":
            card.scale = ft.Scale(1.03)
            card.border = ft.border.all(border_width, select_color)
            card.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=shadow_blur_hover,
                color=f"{select_color}60",
                offset=ft.Offset(0, shadow_offset_y_hover)
            )
        else:
            card.scale = ft.Scale(1.0)
            card.border = ft.border.all(border_width, select_color if is_selected else "rgba(255, 255, 255, 0.15)")
            card.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=shadow_blur,
                color="rgba(0, 0, 0, 0.5)",
                offset=ft.Offset(0, shadow_offset_y)
            )
        card.update()

    card.on_hover = on_hover
    card.animate_scale = 200

    return card
