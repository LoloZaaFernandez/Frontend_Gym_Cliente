"""
Sistema de Diseño Centralizado - BLESSED GYM (Cliente Tablet)
Todos los colores, espaciados, tipografías y estilos en un solo lugar
"""
import flet as ft


class BlessedTheme:
    """
    Tema principal del sistema BLESSED GYM para cliente (tablet)
    Basado en la filosofía de diseño oscuro con naranja como color principal
    """

    # ========================================
    # 🎨 COLORES PRINCIPALES
    # ========================================
    PRIMARY = "#F05D23"         # Naranja BLESSED - Color principal del sistema
    SECONDARY = "#FFFFFF"       # Blanco - Para textos y elementos secundarios
    ACCENT = "#F05D23"          # Naranja - Para acentos y highlights

    # ========================================
    # 🎨 COLORES SEMÁNTICOS
    # ========================================
    SUCCESS = "#00C853"         # Verde - Operaciones exitosas
    WARNING = "#FF9100"         # Naranja advertencia - Alertas
    INFO = "#2196F3"            # Azul - Información general
    ERROR = "#EF5350"           # Rojo error - Errores críticos
    DANGER = "#FF5252"          # Rojo peligro - Acciones peligrosas

    # ========================================
    # 🎨 FONDOS
    # ========================================
    BACKGROUND_DARK = "#0A0A0A"     # Fondo principal oscuro
    BACKGROUND_MEDIUM = "#121212"    # Fondo medio
    CARD_BG = "#1A1A1A"             # Fondo de tarjetas/cards
    CARD_BG_DARK = "#1E1E1E"        # Fondo de tarjetas más oscuras
    CARD_BG_LIGHT = "#2A2A2A"       # Fondo de tarjetas más claras

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
    # 📐 DIMENSIONES COMUNES (Tablet)
    # ========================================
    DIMENSIONS = {
        # Anchos
        "card_width_sm": 200,
        "card_width_md": 350,
        "card_width_lg": 450,
        "button_width_sm": 120,
        "button_width_md": 180,
        "button_width_lg": 250,
        "input_width_md": 400,
        "input_width_lg": 500,

        # Alturas
        "button_height_sm": 45,
        "button_height_md": 55,
        "button_height_lg": 70,
        "input_height": 55,
        "card_height_sm": 120,
        "card_height_md": 180,
        "card_height_lg": 250,
    }

    # ========================================
    # 🎯 ÍCONOS - TAMAÑOS
    # ========================================
    ICON_SIZE = {
        "xs": 16,
        "sm": 20,
        "md": 28,     # Mayor tamaño para tablet
        "lg": 40,
        "xl": 56,
        "2xl": 64,
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
