"""
Layouts - Plantillas de Diseño Reutilizables

Los layouts definen la estructura general de las páginas.
Incluyen sidebar, header y área de contenido.

Ejemplos: base_layout, dashboard_layout, form_layout
"""

from .base_layout import create_base_layout
from .dashboard_layout import (
    create_dashboard_layout,
    create_stats_grid,
    create_activity_widget,
    create_quick_actions_widget
)
from .crud_layout import (
    create_crud_layout,
    create_simple_list_layout
)

__all__ = [
    # Base Layout
    "create_base_layout",

    # Dashboard Layout
    "create_dashboard_layout",
    "create_stats_grid",
    "create_activity_widget",
    "create_quick_actions_widget",

    # CRUD Layout
    "create_crud_layout",
    "create_simple_list_layout",
]
