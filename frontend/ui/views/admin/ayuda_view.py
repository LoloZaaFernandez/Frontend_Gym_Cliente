"""
Vista de Ayuda y Soporte - Información de contacto del equipo
"""

import flet as ft
from config.theme import Theme
from ui.layouts import create_base_layout
from ui.components.molecules import create_card_container


def show_ayuda_view(page: ft.Page, auth_service, on_section_click, current_section):
    """
    Vista de ayuda con información de contacto del equipo de desarrollo
    """
    page.title = "BLESSED GYM - Ayuda y Soporte"
    page.padding = 0
    page.spacing = 0

    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Usuario"), "rol": "Administrador"}

    def create_contact_card(icon, title, subtitle, color=Theme.PRIMARY):
        """Crear tarjeta de contacto con diseño moderno"""
        return ft.Container(
            content=ft.Row([
                # Ícono con círculo de fondo
                ft.Container(
                    content=ft.Icon(icon, size=28, color="white"),
                    bgcolor=color,
                    width=60,
                    height=60,
                    border_radius=30,
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=Theme.SPACING["lg"]),
                # Información
                ft.Column([
                    ft.Text(
                        title,
                        size=Theme.FONT_SIZE["md"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                    ft.Text(
                        subtitle,
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.TEXT_SECONDARY
                    ),
                ], spacing=4, expand=True),
            ], spacing=0),
            padding=Theme.SPACING["xl"],
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["lg"],
            border=ft.border.all(1, Theme.BORDER_DEFAULT),
        )

    def create_developer_card(name, role, phone):
        """Crear tarjeta de desarrollador con foto de perfil circular"""
        # Iniciales del nombre
        initials = "".join([word[0].upper() for word in name.split()[:2]])

        return ft.Container(
            content=ft.Column([
                # Avatar circular con iniciales
                ft.Container(
                    content=ft.Text(
                        initials,
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color="white"
                    ),
                    width=100,
                    height=100,
                    border_radius=50,
                    bgcolor=Theme.PRIMARY,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=Theme.SPACING["md"]),
                # Nombre
                ft.Text(
                    name,
                    size=Theme.FONT_SIZE["lg"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER
                ),
                # Rol
                ft.Container(
                    content=ft.Text(
                        role,
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.PRIMARY,
                        weight=Theme.FONT_WEIGHT["medium"]
                    ),
                    bgcolor=f"{Theme.PRIMARY}20",
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=Theme.RADIUS["md"],
                ),
                ft.Container(height=Theme.SPACING["sm"]),
                # Teléfono
                ft.Row([
                    ft.Icon(ft.Icons.PHONE, size=16, color=Theme.TEXT_SECONDARY),
                    ft.Text(
                        phone,
                        size=Theme.FONT_SIZE["sm"],
                        color=Theme.TEXT_SECONDARY
                    ),
                ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["sm"]),
            padding=Theme.SPACING["2xl"],
            bgcolor=Theme.CARD_BG,
            border_radius=Theme.RADIUS["lg"],
            border=ft.border.all(1, Theme.BORDER_DEFAULT),
            expand=True,
        )

    # Dots decorativos (círculos de fondo)
    def create_decorative_dots():
        """Crear dots decorativos para el fondo"""
        dots = []
        positions = [
            (50, 50, 20, f"{Theme.PRIMARY}10"),
            (150, 100, 30, f"{Theme.PRIMARY}15"),
            (80, 200, 15, f"{Theme.PRIMARY}08"),
            (200, 150, 25, f"{Theme.PRIMARY}12"),
        ]

        for x, y, size, color in positions:
            dots.append(
                ft.Container(
                    width=size,
                    height=size,
                    border_radius=size/2,
                    bgcolor=color,
                    left=x,
                    top=y,
                )
            )
        return ft.Stack(dots, height=300)

    # Contenido principal
    content = ft.Column([
        # Encabezado con decoración
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.HELP_OUTLINE, size=48, color=Theme.PRIMARY),
                    ft.Container(width=Theme.SPACING["lg"]),
                    ft.Column([
                        ft.Text(
                            "Ayuda y Soporte",
                            size=Theme.FONT_SIZE["3xl"],
                            weight=Theme.FONT_WEIGHT["bold"],
                            color=Theme.TEXT_PRIMARY
                        ),
                        ft.Text(
                            "Estamos aquí para ayudarte",
                            size=Theme.FONT_SIZE["md"],
                            color=Theme.TEXT_SECONDARY
                        ),
                    ], spacing=4),
                ], spacing=0),
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["3xl"],
            bgcolor=f"{Theme.PRIMARY}08",
            border_radius=Theme.RADIUS["lg"],
        ),

        ft.Container(height=Theme.SPACING["2xl"]),

        # Sección de Contacto
        create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MAIL, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text(
                        "Contáctanos",
                        size=Theme.FONT_SIZE["xl"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                ], spacing=Theme.SPACING["md"]),

                ft.Divider(height=20, color=Theme.BORDER_DEFAULT),

                create_contact_card(
                    ft.Icons.EMAIL,
                    "Correo Electrónico",
                    "devtools@gmail.com",
                    Theme.PRIMARY
                ),
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        ),

        ft.Container(height=Theme.SPACING["xl"]),

        # Sección de Desarrolladores
        create_card_container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CODE, size=Theme.ICON_SIZE["md"], color=Theme.PRIMARY),
                    ft.Text(
                        "Nuestro Equipo de Desarrollo",
                        size=Theme.FONT_SIZE["xl"],
                        weight=Theme.FONT_WEIGHT["bold"],
                        color=Theme.TEXT_PRIMARY
                    ),
                ], spacing=Theme.SPACING["md"]),

                ft.Divider(height=20, color=Theme.BORDER_DEFAULT),

                # Grid de desarrolladores
                ft.ResponsiveRow([
                    ft.Container(
                        content=create_developer_card("Frans", "Desarrollador Full Stack", "950 000 513"),
                        col={"sm": 12, "md": 6, "lg": 4}
                    ),
                    ft.Container(
                        content=create_developer_card("Crys", "Desarrolladora Backend", "955 668 607"),
                        col={"sm": 12, "md": 6, "lg": 4}
                    ),
                    ft.Container(
                        content=create_developer_card("Lolo", "Desarrollador Frontend", "952 375 791"),
                        col={"sm": 12, "md": 6, "lg": 4}
                    ),
                ], spacing=Theme.SPACING["lg"], run_spacing=Theme.SPACING["lg"]),
            ], spacing=Theme.SPACING["lg"]),
            padding=Theme.SPACING["2xl"],
            shadow="md"
        ),

        ft.Container(height=Theme.SPACING["xl"]),

        # Información adicional
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.INFO_OUTLINE, size=32, color=Theme.PRIMARY),
                ft.Text(
                    "¿Necesitas ayuda?",
                    size=Theme.FONT_SIZE["lg"],
                    weight=Theme.FONT_WEIGHT["bold"],
                    color=Theme.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Contáctanos a través de cualquiera de los canales mostrados arriba.\n"
                    "Nuestro equipo estará encantado de asistirte.",
                    size=Theme.FONT_SIZE["sm"],
                    color=Theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=Theme.SPACING["md"]),
            padding=Theme.SPACING["2xl"],
            bgcolor=f"{Theme.PRIMARY}08",
            border_radius=Theme.RADIUS["lg"],
            alignment=ft.alignment.center,
        ),

        ft.Container(height=Theme.SPACING["xl"]),

    ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

    # Aplicar layout base
    create_base_layout(
        page=page,
        role="admin",
        current_section=current_section,
        on_section_click=on_section_click,
        content=ft.Container(content=content, padding=Theme.SPACING["2xl"]),
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )
