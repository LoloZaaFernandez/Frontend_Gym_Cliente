"""
Componentes Atoms - Nivel 1 (Componentes Básicos)

Los atoms son los componentes más básicos y atómicos del sistema.
No contienen otros componentes, solo elementos nativos de Flet.

Ejemplos: botones, inputs, badges, iconos, textos
"""

from .buttons import (
    create_primary_button,
    create_outlined_button,
    create_text_button,
    create_icon_button,
    create_danger_button,
    create_success_button,
)

from .badges import (
    create_status_badge,
    create_info_badge,
    create_count_badge,
    create_outline_badge,
)

__all__ = [
    # Buttons
    'create_primary_button',
    'create_outlined_button',
    'create_text_button',
    'create_icon_button',
    'create_danger_button',
    'create_success_button',

    # Badges
    'create_status_badge',
    'create_info_badge',
    'create_count_badge',
    'create_outline_badge',
]
