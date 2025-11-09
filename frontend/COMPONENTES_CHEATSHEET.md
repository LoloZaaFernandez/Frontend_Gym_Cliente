# 📋 CHEATSHEET - COMPONENTES BLESSED GYM

Referencia rápida de todos los componentes disponibles.

---

## 🎨 THEME

```python
from config.theme import Theme

# Colores
Theme.PRIMARY           # #F05D23 (Naranja)
Theme.SUCCESS           # #00C853 (Verde)
Theme.ERROR             # #EF5350 (Rojo)
Theme.WARNING           # #FF9800 (Naranja advertencia)
Theme.INFO              # #42A5F5 (Azul)
Theme.BACKGROUND_DARK   # #0A0A0A
Theme.CARD_BG           # #1A1A1A
Theme.SIDEBAR_BG        # #0F0F0F
Theme.TEXT_PRIMARY      # #FFFFFF
Theme.TEXT_SECONDARY    # #CCCCCC
Theme.TEXT_MUTED        # #999999
Theme.TEXT_DISABLED     # #666666
Theme.BORDER_DEFAULT    # #333333
Theme.BORDER_LIGHT      # #444444

# Espaciado
Theme.SPACING["xs"]     # 4px
Theme.SPACING["sm"]     # 8px
Theme.SPACING["md"]     # 12px
Theme.SPACING["lg"]     # 16px
Theme.SPACING["xl"]     # 20px
Theme.SPACING["2xl"]    # 24px
Theme.SPACING["3xl"]    # 32px
Theme.SPACING["4xl"]    # 40px
Theme.SPACING["5xl"]    # 48px

# Border Radius
Theme.RADIUS["sm"]      # 8px
Theme.RADIUS["md"]      # 10px
Theme.RADIUS["lg"]      # 12px
Theme.RADIUS["xl"]      # 16px
Theme.RADIUS["2xl"]     # 20px
Theme.RADIUS["full"]    # 9999px

# Font Size
Theme.FONT_SIZE["xs"]   # 10px
Theme.FONT_SIZE["sm"]   # 12px
Theme.FONT_SIZE["md"]   # 14px
Theme.FONT_SIZE["lg"]   # 16px
Theme.FONT_SIZE["xl"]   # 18px
Theme.FONT_SIZE["2xl"]  # 20px
Theme.FONT_SIZE["3xl"]  # 24px
Theme.FONT_SIZE["4xl"]  # 32px
Theme.FONT_SIZE["5xl"]  # 40px

# Font Weight
Theme.FONT_WEIGHT["normal"]     # 400
Theme.FONT_WEIGHT["medium"]     # 500
Theme.FONT_WEIGHT["semibold"]   # 600
Theme.FONT_WEIGHT["bold"]       # 700
Theme.FONT_WEIGHT["extrabold"]  # 800

# Sombras
Theme.get_shadow("sm")
Theme.get_shadow("md")
Theme.get_shadow("lg")
Theme.get_shadow("xl")
Theme.get_shadow("2xl")

# Dimensiones
Theme.DIMENSIONS["sidebar_width"]       # 260
Theme.DIMENSIONS["header_height"]       # 70
Theme.DIMENSIONS["card_width_sm"]       # 280
Theme.DIMENSIONS["card_width_md"]       # 320
Theme.DIMENSIONS["card_width_lg"]       # 400
Theme.DIMENSIONS["card_height_sm"]      # 140
Theme.DIMENSIONS["card_height_md"]      # 180
```

---

## 🔘 ATOMS - BUTTONS

```python
from ui.components.atoms import (
    create_primary_button,
    create_outlined_button,
    create_text_button,
    create_icon_button,
    create_danger_button,
    create_success_button
)

# Botón Primario (Naranja)
create_primary_button("Guardar", on_click, icon=ft.Icons.SAVE)

# Botón Con Borde
create_outlined_button("Cancelar", on_click, icon=ft.Icons.CLOSE)

# Botón de Texto
create_text_button("Ver más", on_click)

# Botón de Ícono
create_icon_button(ft.Icons.DELETE, on_click, tooltip="Eliminar")

# Botón de Peligro (Rojo)
create_danger_button("Eliminar", on_click, icon=ft.Icons.DELETE)

# Botón de Éxito (Verde)
create_success_button("Confirmar", on_click, icon=ft.Icons.CHECK)
```

---

## 🏷️ ATOMS - BADGES

```python
from ui.components.atoms import (
    create_status_badge,
    create_info_badge,
    create_count_badge,
    create_outline_badge
)

# Badge de Estado
create_status_badge("Activo", status="success", icon=ft.Icons.CHECK_CIRCLE)
create_status_badge("Pendiente", status="warning")
create_status_badge("Vencido", status="error")
create_status_badge("Info", status="info")

# Badge Informativo
create_info_badge("Nuevo", icon=ft.Icons.STAR, color=Theme.PRIMARY)

# Badge Contador
create_count_badge(5)       # Muestra "5"
create_count_badge(150)     # Muestra "99+"

# Badge Con Borde
create_outline_badge("Premium", color=Theme.PRIMARY)
```

---

## 🎴 MOLECULES - CARDS

```python
from ui.components.molecules import (
    create_card_container,
    create_stat_card,
    create_info_card,
    create_empty_state
)

# Card Container (Universal)
create_card_container(
    content=mi_contenido,
    padding=Theme.SPACING["xl"],
    shadow="lg",
    on_click=lambda e: print("Click")
)

# Card de Estadística
create_stat_card(
    title="Ingresos",
    value="S/. 12,450",
    icon=ft.Icons.ATTACH_MONEY,
    color=Theme.SUCCESS,
    trend="+12%",
    trend_positive=True,
    on_click=lambda e: ver_detalles()
)

# Card de Información
create_info_card(
    title="Clientes",
    value="156",
    icon=ft.Icons.PEOPLE,
    subtitle="Total activos"
)

# Estado Vacío
create_empty_state(
    message="No hay clientes registrados",
    icon=ft.Icons.PEOPLE_OUTLINE,
    action_text="Agregar Cliente",
    on_action=lambda e: add_client(),
    secondary_message="Comienza agregando tu primer cliente"
)
```

---

## 💬 MOLECULES - DIALOGS

```python
from ui.components.molecules import (
    create_confirmation_dialog,
    create_alert_dialog,
    create_form_dialog
)

# Diálogo de Confirmación
dialog = create_confirmation_dialog(
    page,
    title="Eliminar Cliente",
    message="¿Estás seguro de eliminar este cliente?",
    on_confirm=lambda e: delete(),
    warning_message="Esta acción no se puede deshacer",
    is_danger=True
)
page.open(dialog)

# Diálogo de Alerta
dialog = create_alert_dialog(
    page,
    title="Éxito",
    message="Cliente guardado correctamente",
    type="success"  # info, warning, error, success
)
page.open(dialog)

# Diálogo con Formulario
name_field = ft.TextField(label="Nombre")
email_field = ft.TextField(label="Email")

dialog = create_form_dialog(
    page,
    title="Nuevo Cliente",
    form_fields=[name_field, email_field],
    on_submit=lambda e: save(name_field.value, email_field.value)
)
page.open(dialog)
```

---

## 🏗️ LAYOUTS

```python
from ui.layouts import (
    create_base_layout,
    create_dashboard_layout,
    create_stats_grid,
    create_activity_widget,
    create_quick_actions_widget
)

# Base Layout (Universal)
create_base_layout(
    page=page,
    role="admin",  # o "client"
    current_section="Dashboard",
    on_section_click=navegar,
    content=mi_contenido,
    user_info={"nombre": "Juan", "rol": "Admin"},
    on_logout=cerrar_sesion,
    show_back_button=False,
    on_back=None
)

# Dashboard Layout
create_dashboard_layout(
    page=page,
    role="admin",
    current_section="Dashboard",
    on_section_click=navegar,
    user_info=user_data,
    on_logout=cerrar_sesion,
    stats_cards=[stat1, stat2, stat3],
    main_content=mi_contenido,
    activity_feed=activity_widget,
    widgets=[quick_actions]
)

# Grid de Estadísticas
grid = create_stats_grid(
    stats_cards=[stat1, stat2, stat3, stat4],
    columns=2  # Default: 3
)

# Widget de Actividad
activity = create_activity_widget(
    title="Actividad Reciente",
    items=[
        ft.ListTile(
            leading=ft.Icon(ft.Icons.PERSON_ADD, color=Theme.SUCCESS),
            title=ft.Text("Nuevo cliente"),
            subtitle=ft.Text("Hace 5 min")
        )
    ],
    icon=ft.Icons.HISTORY,
    empty_message="No hay actividad"
)

# Widget de Acciones Rápidas
quick_actions = create_quick_actions_widget(
    title="Acciones Rápidas",
    actions=[
        ("Nuevo Cliente", ft.Icons.PERSON_ADD, lambda e: add()),
        ("Nueva Venta", ft.Icons.SHOPPING_CART, lambda e: sell()),
    ]
)
```

---

## 💬 UTILS - MESSAGES

```python
from ui.utils.messages import (
    mostrar_mensaje,
    mostrar_exito,
    mostrar_error,
    mostrar_advertencia,
    mostrar_info,
    mostrar_loading
)

# Mensaje Genérico
mostrar_mensaje(page, "Operación completada", error=False)

# Mensaje de Éxito (Verde)
mostrar_exito(page, "Cliente guardado correctamente")

# Mensaje de Error (Rojo)
mostrar_error(page, "Error al guardar cliente")

# Mensaje de Advertencia (Naranja)
mostrar_advertencia(page, "La membresía vence pronto")

# Mensaje Informativo (Azul)
mostrar_info(page, "Nuevo cliente registrado")

# Indicador de Carga
mostrar_loading(page, "Guardando datos...")
# ... hacer operación ...
page.snack_bar.open = False
page.update()
```

---

## 📝 EJEMPLO COMPLETO

```python
import flet as ft
from config.theme import Theme
from ui.layouts import create_dashboard_layout
from ui.components.atoms import create_primary_button, create_status_badge
from ui.components.molecules import create_stat_card
from ui.utils.messages import mostrar_exito, mostrar_error

def mi_dashboard(page: ft.Page, user_data: dict):
    # Stats
    stats = [
        create_stat_card(
            "Ingresos",
            "S/. 12,450",
            ft.Icons.ATTACH_MONEY,
            color=Theme.SUCCESS,
            trend="+12%"
        ),
        create_stat_card(
            "Clientes",
            "156",
            ft.Icons.PEOPLE,
            color=Theme.PRIMARY,
            trend="+8%"
        ),
    ]

    # Función de guardado
    def guardar(e):
        # Lógica...
        mostrar_exito(page, "Guardado correctamente")

    # Contenido
    contenido = ft.Column([
        ft.Text("Mi Dashboard", size=Theme.FONT_SIZE["2xl"],
               weight=Theme.FONT_WEIGHT["bold"]),
        ft.Row([
            create_status_badge("Activo", status="success"),
            create_status_badge("Pendiente", status="warning"),
        ]),
        create_primary_button("Guardar", guardar, icon=ft.Icons.SAVE),
    ], spacing=Theme.SPACING["lg"])

    # Crear dashboard
    create_dashboard_layout(
        page=page,
        role="admin",
        current_section="Dashboard",
        on_section_click=lambda s: print(s),
        user_info=user_data,
        on_logout=lambda e: print("Logout"),
        stats_cards=stats,
        main_content=contenido
    )

# Llamar
mi_dashboard(page, {"nombre": "Admin", "rol": "Administrador"})
```

---

## 🎯 IMPORTS RÁPIDOS

```python
# Todo en uno
import flet as ft
from config.theme import Theme
from ui.layouts import create_base_layout, create_dashboard_layout
from ui.components.atoms import (
    create_primary_button, create_outlined_button,
    create_status_badge, create_count_badge
)
from ui.components.molecules import (
    create_stat_card, create_card_container,
    create_confirmation_dialog, create_alert_dialog
)
from ui.utils.messages import (
    mostrar_exito, mostrar_error,
    mostrar_advertencia, mostrar_info
)
```

---

## 💡 TIPS RÁPIDOS

### 1. Colores
```python
# ✅ USAR Theme
bgcolor=Theme.PRIMARY

# ❌ NO hardcodear
bgcolor="#F05D23"
```

### 2. Espaciado
```python
# ✅ USAR Theme.SPACING
padding=Theme.SPACING["lg"]

# ❌ NO números
padding=16
```

### 3. Botones
```python
# ✅ USAR componentes
create_primary_button("Texto", handler)

# ❌ NO crear desde cero
ft.ElevatedButton(...)
```

### 4. Mensajes
```python
# ✅ USAR utils
mostrar_exito(page, "OK")

# ❌ NO crear SnackBar
page.snack_bar = ft.SnackBar(...)
```

### 5. Layouts
```python
# ✅ USAR layouts
create_base_layout(page, ..., content=x)

# ❌ NO agregar directo
page.add(sidebar)
page.add(header)
page.add(content)
```

---

## 📚 DOCUMENTACIÓN COMPLETA

- `GUIA_COMPONENTES.md` - Guía detallada de cada componente
- `GUIA_MIGRACION.md` - Paso a paso para migrar vistas
- `SISTEMA_COMPONENTES_README.md` - Overview completo del sistema

---

**Imprime esta hoja y tenla a mano! 🚀**
