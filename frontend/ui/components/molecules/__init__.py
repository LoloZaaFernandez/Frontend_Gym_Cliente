"""
Componentes Molecules - Nivel 2 (Componentes Compuestos)

Los molecules son componentes que combinan varios atoms.
Tienen una funcionalidad más compleja pero son reutilizables.

Ejemplos: cards, forms, headers de sección, tablas
"""

from .cards import (
    create_card_container,
    create_stat_card,
    create_info_card,
    create_empty_state,
)

from .dialogs import (
    create_confirmation_dialog,
    create_alert_dialog,
    create_form_dialog,
)

__all__ = [
    # Cards
    'create_card_container',
    'create_stat_card',
    'create_info_card',
    'create_empty_state',

    # Dialogs
    'create_confirmation_dialog',
    'create_alert_dialog',
    'create_form_dialog',
]
