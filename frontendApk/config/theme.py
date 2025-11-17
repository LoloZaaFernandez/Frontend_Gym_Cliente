"""
Sistema de Diseño Centralizado - BLESSED GYM (Cliente Tablet)
Todos los colores, espaciados, tipografías y estilos en un solo lugar
"""
import flet as ft


class BlessedTheme:
    """
    Tema principal del sistema BLESSED GYM para cliente (tablet)
    Basado en la filosofía de diseño oscuro con verde lima como color principal
    """

    # ========================================
    # 🎨 COLORES PRINCIPALES - FILOSOFÍA SERIA Y PROFESIONAL
    # ========================================
    PRIMARY = "#9FFF33"         # Verde Lima BLESSED - Color principal del sistema
    PRIMARY_LIGHT = "#B8FF66"   # Verde Lima claro - Variante suave
    PRIMARY_DARK = "#7ACC00"    # Verde Lima oscuro - Variante fuerte
    SECONDARY = "#FFFFFF"       # Blanco - Para textos y elementos secundarios
    ACCENT = "#9FFF33"          # Verde Lima principal - Para acentos

    # ========================================
    # 🎨 COLORES SEMÁNTICOS - PALETA PROFESIONAL
    # ========================================
    SUCCESS = "#4CAF50"         # Verde - Operaciones exitosas
    SUCCESS_LIGHT = "#66BB6A"   # Verde claro
    WARNING = "#FF9800"         # Naranja advertencia - Alertas
    WARNING_LIGHT = "#FFB74D"   # Naranja claro advertencia
    INFO = "#2196F3"            # Azul - Información general
    INFO_LIGHT = "#64B5F6"      # Azul claro
    ERROR = "#EF5350"           # Rojo error - Errores críticos
    DANGER = "#FF5252"          # Rojo peligro - Acciones peligrosas

    # ========================================
    # 🎨 FONDOS
    # ========================================
    BACKGROUND_DARK = "#0A0A0A"     # Fondo principal oscuro
    BACKGROUND_MEDIUM = "#121212"    # Fondo medio
    CARD_BG = "rgba(26, 26, 26, 0.92)"  # Fondo de tarjetas semi-transparente
    CARD_BG_DARK = "rgba(20, 20, 20, 0.95)"  # Fondo de tarjetas más oscuras
    CARD_BG_LIGHT = "rgba(42, 42, 42, 0.85)"  # Fondo de tarjetas más claras
    CARD_BG_GLASS = "rgba(30, 30, 30, 0.75)"  # Efecto glass morphism
    OVERLAY_DARK = "rgba(10, 10, 10, 0.65)"   # Overlay oscuro para background
    GRADIENT_PRIMARY = "linear-gradient(135deg, #9FFF33 0%, #B8FF66 100%)"  # Gradiente verde lima
    GRADIENT_SUCCESS = "linear-gradient(135deg, #4CAF50 0%, #81C784 100%)"  # Gradiente verde

    # ========================================
    # 🎨 TEXTOS
    # ========================================
    TEXT_PRIMARY = "#FFFFFF"        # Texto principal - Blanco
    TEXT_SECONDARY = "#CCCCCC"      # Texto secundario - Gris claro
    TEXT_DISABLED = "#666666"       # Texto deshabilitado - Gris medio
    TEXT_MUTED = "#999999"          # Texto apagado - Gris
    TEXT_DARK = "#1A1A1A"           # Texto oscuro (para fondos claros)

    # ========================================
    # 🎨 BORDES
    # ========================================
    BORDER_DEFAULT = "#333333"      # Borde estándar
    BORDER_LIGHT = "#444444"        # Borde claro
    BORDER_DARK = "#222222"         # Borde oscuro
    BORDER_FOCUS = PRIMARY          # Borde cuando está enfocado

    # ========================================
    # 📏 ESPACIADO (en píxeles)
    # ========================================
    SPACING = {
        "none": 0,
        "xs": 4,      # Extra small
        "sm": 8,      # Small
        "md": 12,     # Medium
        "lg": 16,     # Large
        "xl": 20,     # Extra large
        "2xl": 24,    # 2x Extra large
        "3xl": 32,    # 3x Extra large
        "4xl": 40,    # 4x Extra large
        "5xl": 48,    # 5x Extra large
    }

    # ========================================
    # 🔲 BORDER RADIUS (redondeo de esquinas)
    # ========================================
    RADIUS = {
        "none": 0,
        "sm": 8,      # Small - Botones pequeños
        "md": 10,     # Medium - Cards pequeños
        "lg": 12,     # Large - Cards medianos
        "xl": 16,     # Extra large - Cards grandes
        "2xl": 20,    # 2x Extra large - Badges y pills
        "full": 9999, # Completamente redondo
    }

    # ========================================
    # 📝 TIPOGRAFÍA - TAMAÑOS DE FUENTE
    # ========================================
    FONT_SIZE = {
        "xs": 10,     # Extra small - Etiquetas pequeñas
        "sm": 12,     # Small - Texto secundario
        "md": 14,     # Medium - Texto normal
        "lg": 16,     # Large - Texto destacado
        "xl": 18,     # Extra large - Subtítulos
        "2xl": 20,    # 2x Extra large - Títulos
        "3xl": 24,    # 3x Extra large - Títulos grandes
        "4xl": 32,    # 4x Extra large - Números destacados
        "5xl": 40,    # 5xl - Títulos hero
        "6xl": 48,    # 6xl - Títulos muy grandes
    }

    # ========================================
    # 📝 TIPOGRAFÍA - PESOS DE FUENTE
    # ========================================
    FONT_WEIGHT = {
        "thin": ft.FontWeight.W_100,
        "light": ft.FontWeight.W_300,
        "normal": ft.FontWeight.W_400,
        "medium": ft.FontWeight.W_500,
        "semibold": ft.FontWeight.W_600,
        "bold": ft.FontWeight.W_700,
        "extrabold": ft.FontWeight.W_800,
        "black": ft.FontWeight.W_900,
    }

    # ========================================
    # ☁️ SOMBRAS (BoxShadow preconfiguradas)
    # ========================================
    SHADOWS = {
        "none": {
            "spread_radius": 0,
            "blur_radius": 0,
            "color": ft.Colors.TRANSPARENT,
            "offset": ft.Offset(0, 0),
        },
        "sm": {
            "spread_radius": 0,
            "blur_radius": 10,
            "color": ft.Colors.BLACK26,
            "offset": ft.Offset(0, 2),
        },
        "md": {
            "spread_radius": 1,
            "blur_radius": 15,
            "color": ft.Colors.BLACK45,
            "offset": ft.Offset(0, 4),
        },
        "lg": {
            "spread_radius": 2,
            "blur_radius": 20,
            "color": ft.Colors.BLACK45,
            "offset": ft.Offset(0, 8),
        },
        "xl": {
            "spread_radius": 2,
            "blur_radius": 30,
            "color": ft.Colors.BLACK45,
            "offset": ft.Offset(0, 12),
        },
    }

    # ========================================
    # 📐 DIMENSIONES COMUNES (Tablet Landscape 1280x800)
    # ========================================
    # NOTA: Estas dimensiones son para referencia base (1280x800)
    # Usar get_responsive_dimensions() para calcular dimensiones adaptativas
    DIMENSIONS = {
        # Anchos
        "card_width_sm": 250,
        "card_width_md": 400,
        "card_width_lg": 550,
        "button_width_sm": 150,
        "button_width_md": 220,
        "button_width_lg": 300,
        "input_width_md": 450,
        "input_width_lg": 550,

        # Alturas
        "button_height_sm": 50,
        "button_height_md": 65,
        "button_height_lg": 80,
        "input_height": 60,
        "card_height_sm": 140,
        "card_height_md": 200,
        "card_height_lg": 280,
    }

    # ========================================
    # 📐 DIMENSIONES RESPONSIVE (Porcentajes basados en viewport)
    # ========================================
    # Porcentajes del ancho de la página para diferentes elementos
    RESPONSIVE_WIDTHS = {
        # Cards
        "card_sm_percent": 19.5,    # ~250px en 1280px
        "card_md_percent": 31.25,   # ~400px en 1280px
        "card_lg_percent": 42.97,   # ~550px en 1280px

        # Botones
        "button_sm_percent": 11.72, # ~150px en 1280px
        "button_md_percent": 17.19, # ~220px en 1280px
        "button_lg_percent": 23.44, # ~300px en 1280px

        # Inputs
        "input_md_percent": 35.16,  # ~450px en 1280px
        "input_lg_percent": 42.97,  # ~550px en 1280px
    }

    # Dimensiones base para cálculos responsive
    BASE_WIDTH = 1280
    BASE_HEIGHT = 800

    # ========================================
    # 🎯 ÍCONOS - TAMAÑOS (Optimizado para tablet)
    # ========================================
    ICON_SIZE = {
        "xs": 20,
        "sm": 28,
        "md": 36,     # Mayor tamaño para tablet
        "lg": 48,
        "xl": 64,
        "2xl": 80,
        "3xl": 96,
    }

    # ========================================
    # 🎭 ESTADOS (hover, focus, active)
    # ========================================
    STATES = {
        "hover_opacity": 0.8,
        "active_opacity": 0.6,
        "disabled_opacity": 0.4,
        "transition_duration": 200,  # milisegundos
    }

    @staticmethod
    def get_shadow(size="md"):
        """
        Obtener una sombra preconfigurada

        Args:
            size: Tamaño de la sombra ("none", "sm", "md", "lg", "xl")

        Returns:
            ft.BoxShadow configurado
        """
        shadow_config = BlessedTheme.SHADOWS.get(size, BlessedTheme.SHADOWS["md"])
        return ft.BoxShadow(
            spread_radius=shadow_config["spread_radius"],
            blur_radius=shadow_config["blur_radius"],
            color=shadow_config["color"],
            offset=shadow_config["offset"]
        )

    @staticmethod
    def get_responsive_width(page_width: float, element_type: str, size: str = "lg") -> float:
        """
        Calcular ancho responsive basado en el ancho de la página

        Args:
            page_width: Ancho actual de la página
            element_type: Tipo de elemento ("card", "button", "input")
            size: Tamaño del elemento ("sm", "md", "lg")

        Returns:
            Ancho calculado en píxeles
        """
        key = f"{element_type}_{size}_percent"
        percent = BlessedTheme.RESPONSIVE_WIDTHS.get(key, 30)
        return (page_width * percent) / 100

    @staticmethod
    def get_responsive_height(page_height: float, base_height: float) -> float:
        """
        Calcular altura responsive basada en la altura de la página

        Args:
            page_height: Altura actual de la página
            base_height: Altura base del elemento (en 800px)

        Returns:
            Altura calculada en píxeles
        """
        # Escalar proporcionalmente basado en la altura base de 800px
        scale_factor = page_height / BlessedTheme.BASE_HEIGHT
        return base_height * scale_factor

    @staticmethod
    def get_responsive_font_size(page_width: float, base_size: int) -> int:
        """
        Calcular tamaño de fuente responsive

        Args:
            page_width: Ancho actual de la página
            base_size: Tamaño base de la fuente (en 1280px)

        Returns:
            Tamaño de fuente calculado
        """
        # Escalar proporcionalmente basado en el ancho base de 1280px
        scale_factor = page_width / BlessedTheme.BASE_WIDTH
        # Limitar el factor de escala entre 0.75 y 1.5
        scale_factor = max(0.75, min(1.5, scale_factor))
        return int(base_size * scale_factor)

    @staticmethod
    def get_responsive_spacing(page_width: float, base_spacing: int) -> int:
        """
        Calcular espaciado responsive

        Args:
            page_width: Ancho actual de la página
            base_spacing: Espaciado base (en 1280px)

        Returns:
            Espaciado calculado
        """
        scale_factor = page_width / BlessedTheme.BASE_WIDTH
        # Limitar el factor de escala entre 0.8 y 1.2
        scale_factor = max(0.8, min(1.2, scale_factor))
        return int(base_spacing * scale_factor)

    @staticmethod
    def get_responsive_dimensions(page_width: float, page_height: float) -> dict:
        """
        Obtener todas las dimensiones responsive calculadas

        Args:
            page_width: Ancho actual de la página
            page_height: Altura actual de la página

        Returns:
            Diccionario con todas las dimensiones responsive
        """
        return {
            # Anchos de cards
            "card_width_sm": BlessedTheme.get_responsive_width(page_width, "card", "sm"),
            "card_width_md": BlessedTheme.get_responsive_width(page_width, "card", "md"),
            "card_width_lg": BlessedTheme.get_responsive_width(page_width, "card", "lg"),

            # Anchos de botones
            "button_width_sm": BlessedTheme.get_responsive_width(page_width, "button", "sm"),
            "button_width_md": BlessedTheme.get_responsive_width(page_width, "button", "md"),
            "button_width_lg": BlessedTheme.get_responsive_width(page_width, "button", "lg"),

            # Anchos de inputs
            "input_width_md": BlessedTheme.get_responsive_width(page_width, "input", "md"),
            "input_width_lg": BlessedTheme.get_responsive_width(page_width, "input", "lg"),

            # Alturas
            "button_height_sm": BlessedTheme.get_responsive_height(page_height, BlessedTheme.DIMENSIONS["button_height_sm"]),
            "button_height_md": BlessedTheme.get_responsive_height(page_height, BlessedTheme.DIMENSIONS["button_height_md"]),
            "button_height_lg": BlessedTheme.get_responsive_height(page_height, BlessedTheme.DIMENSIONS["button_height_lg"]),
            "input_height": BlessedTheme.get_responsive_height(page_height, BlessedTheme.DIMENSIONS["input_height"]),
            "card_height_sm": BlessedTheme.get_responsive_height(page_height, BlessedTheme.DIMENSIONS["card_height_sm"]),
            "card_height_md": BlessedTheme.get_responsive_height(page_height, BlessedTheme.DIMENSIONS["card_height_md"]),
            "card_height_lg": BlessedTheme.get_responsive_height(page_height, BlessedTheme.DIMENSIONS["card_height_lg"]),
        }


# ========================================
# 🎨 ALIAS PARA ACCESO RÁPIDO
# ========================================
Theme = BlessedTheme

# ========================================
# 📦 EXPORTACIONES
# ========================================
__all__ = [
    'BlessedTheme',
    'Theme',
]
