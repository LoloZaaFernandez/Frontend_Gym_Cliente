"""
Vista de Finanzas - Gestión de Egresos y Reportes Financieros
Incluye: Tab 1: Egresos | Tab 2: Reporte Financiero
"""

import flet as ft
from datetime import datetime, timedelta
from config.theme import Theme
from services.api_service import APIService
from ui.layouts import create_base_layout
from ui.components.atoms import create_primary_button, create_outlined_button
from ui.components.molecules import create_card_container, create_stat_card
from ui.utils.messages import mostrar_exito, mostrar_error
from ui.utils.datetime_utils import get_now_local


def show_finanzas_view(page: ft.Page, auth_service, on_section_click, current_section):
    """Vista de finanzas con tabs: Egresos y Reporte Financiero"""
    page.title = "BLESSED GYM - Finanzas"
    page.padding = 0
    page.spacing = 0

    api = APIService()
    current_user = auth_service.get_current_user()
    user_info = {"nombre": current_user.get("nombre", "Admin"), "rol": "Administrador"}

    # Referencias para actualizar contenido
    content_ref = ft.Ref[ft.Container]()
    selected_tab = [0]  # 0: Egresos, 1: Reporte Financiero

    # ==========================================
    # TAB 1: GESTIÓN DE EGRESOS
    # ==========================================
    def create_tab_egresos():
        """Crear tab de gestión de egresos"""

        # Estado del tab
        categorias_list = []
        egresos_list = []
        filtro_periodo = ["mes"]  # hoy, semana, mes

        # Referencias
        tabla_egresos_ref = ft.Ref[ft.Column]()
        stats_total_ref = ft.Ref[ft.Text]()
        stats_cantidad_ref = ft.Ref[ft.Text]()

        # Campos del formulario
        categoria_dropdown = ft.Dropdown(
            label="Categoría de Egreso",
            hint_text="Selecciona categoría",
            border_color=Theme.BORDER_DEFAULT,
            width=300,
            options=[]
        )

        concepto_field = ft.TextField(
            label="Concepto",
            hint_text="Ej: Pago de luz, Sueldo enero",
            border_color=Theme.BORDER_DEFAULT,
            width=300
        )

        monto_field = ft.TextField(
            label="Monto (S/)",
            hint_text="0.00",
            border_color=Theme.BORDER_DEFAULT,
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        metodo_pago_dropdown = ft.Dropdown(
            label="Método de Pago",
            border_color=Theme.BORDER_DEFAULT,
            width=150,
            value="Efectivo",
            options=[
                ft.dropdown.Option("Efectivo"),
                ft.dropdown.Option("Transferencia"),
                ft.dropdown.Option("Tarjeta"),
                ft.dropdown.Option("Yape"),
            ]
        )

        fecha_field = ft.TextField(
            label="Fecha",
            value=get_now_local().strftime("%Y-%m-%d"),
            border_color=Theme.BORDER_DEFAULT,
            width=150
        )

        proveedor_field = ft.TextField(
            label="Proveedor (opcional)",
            border_color=Theme.BORDER_DEFAULT,
            width=300
        )

        descripcion_field = ft.TextField(
            label="Descripción (opcional)",
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=Theme.BORDER_DEFAULT,
            width=300
        )

        def cargar_categorias():
            """Cargar categorías de egresos desde el backend"""
            try:
                categorias = api.get_categorias_egresos(estado="Activa")
                categorias_list.clear()
                categorias_list.extend(categorias)

                # Actualizar dropdown
                categoria_dropdown.options = [
                    ft.dropdown.Option(key=str(cat['id']), text=cat['nombre'])
                    for cat in categorias
                ]

                if categorias:
                    categoria_dropdown.value = str(categorias[0]['id'])

                # Solo actualizar si el dropdown ya está en la página
                try:
                    if categoria_dropdown.page:
                        categoria_dropdown.update()
                except:
                    pass  # El dropdown aún no está agregado a la página

                print(f"✅ Categorías cargadas: {len(categorias)}")
            except Exception as e:
                print(f"❌ Error al cargar categorías: {e}")
                mostrar_error(page, f"Error al cargar categorías: {str(e)}")

        def get_fechas_filtro():
            """Obtener fechas según el filtro seleccionado"""
            hoy = get_now_local()

            if filtro_periodo[0] == "hoy":
                fecha_inicio = hoy.strftime("%Y-%m-%d")
                fecha_fin = hoy.strftime("%Y-%m-%d")
            elif filtro_periodo[0] == "semana":
                inicio_semana = hoy - timedelta(days=hoy.weekday())
                fecha_inicio = inicio_semana.strftime("%Y-%m-%d")
                fecha_fin = hoy.strftime("%Y-%m-%d")
            else:  # mes
                fecha_inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
                fecha_fin = hoy.strftime("%Y-%m-%d")

            return fecha_inicio, fecha_fin

        def cargar_egresos():
            """Cargar egresos del período seleccionado"""
            try:
                fecha_inicio, fecha_fin = get_fechas_filtro()

                print(f"\n{'='*60}")
                print(f"📊 CARGANDO EGRESOS")
                print(f"Período: {filtro_periodo[0]}")
                print(f"Desde: {fecha_inicio} | Hasta: {fecha_fin}")

                egresos = api.get_egresos(
                    fecha_desde=fecha_inicio,
                    fecha_hasta=fecha_fin
                )

                egresos_list.clear()
                egresos_list.extend(egresos)

                print(f"Egresos recibidos: {len(egresos)}")
                print(f"{'='*60}\n")

                actualizar_tabla_egresos()
                actualizar_stats()

            except Exception as e:
                print(f"❌ Error al cargar egresos: {e}")
                mostrar_error(page, f"Error al cargar egresos: {str(e)}")

        def actualizar_stats():
            """Actualizar estadísticas del período"""
            total_monto = sum(e.get('monto', 0) for e in egresos_list)
            cantidad = len(egresos_list)

            if stats_total_ref.current:
                stats_total_ref.current.value = f"S/ {total_monto:,.2f}"
                try:
                    if stats_total_ref.current.page:
                        stats_total_ref.current.update()
                except:
                    pass

            if stats_cantidad_ref.current:
                stats_cantidad_ref.current.value = f"{cantidad} egreso(s)"
                try:
                    if stats_cantidad_ref.current.page:
                        stats_cantidad_ref.current.update()
                except:
                    pass

        def actualizar_tabla_egresos():
            """Actualizar tabla de egresos"""
            if not tabla_egresos_ref.current:
                print("⚠️ Referencia a tabla_egresos no disponible")
                return

            try:
                tabla_egresos_ref.current.controls.clear()
            except Exception as ex:
                print(f"⚠️ Error al limpiar tabla: {ex}")
                return

            if not egresos_list:
                tabla_egresos_ref.current.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "No hay egresos en este período",
                            color=Theme.TEXT_SECONDARY,
                            size=14
                        ),
                        padding=20,
                        alignment=ft.alignment.center
                    )
                )
            else:
                # Encabezado de tabla
                tabla_egresos_ref.current.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text("Folio", weight=ft.FontWeight.BOLD, width=120),
                            ft.Text("Fecha", weight=ft.FontWeight.BOLD, width=100),
                            ft.Text("Categoría", weight=ft.FontWeight.BOLD, width=120),
                            ft.Text("Concepto", weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text("Monto", weight=ft.FontWeight.BOLD, width=100, text_align=ft.TextAlign.RIGHT),
                            ft.Text("Estado", weight=ft.FontWeight.BOLD, width=100),
                            ft.Text("Acciones", weight=ft.FontWeight.BOLD, width=140),
                        ]),
                        bgcolor=Theme.BACKGROUND_MEDIUM,
                        padding=10,
                        border_radius=8
                    )
                )

                # Filas de egresos
                for egreso in egresos_list:
                    folio = egreso.get('folio', f"EGR-{egreso.get('id', '')}")
                    fecha = egreso.get('fecha_egreso', '')[:10] if egreso.get('fecha_egreso') else 'N/A'
                    categoria = egreso.get('nombre_categoria', 'Sin categoría')
                    concepto = egreso.get('concepto', '')
                    monto = egreso.get('monto', 0)
                    estado = egreso.get('estado', 'Pagado')
                    egreso_id = egreso.get('id')

                    # Color del estado
                    estado_color = Theme.SUCCESS if estado == "Pagado" else Theme.WARNING

                    def crear_eliminar_handler(id_egreso):
                        def handler(e):
                            eliminar_egreso(id_egreso)
                        return handler

                    def crear_editar_handler(id_egreso):
                        def handler(e):
                            editar_egreso(id_egreso)
                        return handler

                    tabla_egresos_ref.current.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(folio, size=12, width=120),
                                ft.Text(fecha, size=12, width=100),
                                ft.Text(categoria, size=12, width=120),
                                ft.Text(concepto, size=12, expand=True),
                                ft.Text(f"S/ {monto:,.2f}", size=12, width=100, text_align=ft.TextAlign.RIGHT, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Text(estado, size=11, color="white"),
                                    bgcolor=estado_color,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=4,
                                    width=100
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=Theme.PRIMARY,
                                    tooltip="Editar",
                                    on_click=crear_editar_handler(egreso_id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=Theme.DANGER,
                                    tooltip="Eliminar",
                                    on_click=crear_eliminar_handler(egreso_id)
                                )
                            ]),
                            padding=10,
                            border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
                        )
                    )

            try:
                if tabla_egresos_ref.current.page:
                    tabla_egresos_ref.current.update()
                else:
                    print("⚠️ tabla_egresos_ref no está en la página aún")
            except Exception as ex:
                print(f"⚠️ Error al actualizar tabla: {ex}")

        def crear_egreso_handler(e):
            """Handler para crear nuevo egreso"""
            try:
                # Validaciones
                if not categoria_dropdown.value:
                    mostrar_error(page, "Selecciona una categoría")
                    return

                if not concepto_field.value or len(concepto_field.value.strip()) < 3:
                    mostrar_error(page, "El concepto debe tener al menos 3 caracteres")
                    return

                if not monto_field.value or float(monto_field.value) <= 0:
                    mostrar_error(page, "El monto debe ser mayor a 0")
                    return

                # Preparar datos
                data = {
                    "id_categoria": int(categoria_dropdown.value),
                    "concepto": concepto_field.value.strip(),
                    "descripcion": descripcion_field.value.strip() if descripcion_field.value else "",
                    "monto": float(monto_field.value),
                    "metodo_pago": metodo_pago_dropdown.value,
                    "fecha_egreso": fecha_field.value,
                    "proveedor": proveedor_field.value.strip() if proveedor_field.value else "",
                    "estado": "Pagado",
                    "usuario_creacion": current_user.get("nombre", "admin")
                }

                print(f"\n{'='*60}")
                print(f"💸 CREANDO EGRESO")
                print(f"Categoría: {categoria_dropdown.value}")
                print(f"Concepto: {data['concepto']}")
                print(f"Monto: S/ {data['monto']}")
                print(f"{'='*60}\n")

                # Crear egreso
                resultado = api.crear_egreso(data)

                print(f"✅ Egreso creado: {resultado.get('folio', 'N/A')}")

                # Limpiar formulario
                concepto_field.value = ""
                monto_field.value = ""
                proveedor_field.value = ""
                descripcion_field.value = ""
                concepto_field.update()
                monto_field.update()
                proveedor_field.update()
                descripcion_field.update()

                # Recargar lista
                cargar_egresos()

                mostrar_exito(page, f"Egreso registrado\nFolio: {resultado.get('folio', 'N/A')}\nMonto: S/ {data['monto']:.2f}")

            except Exception as e:
                print(f"❌ Error al crear egreso: {e}")
                mostrar_error(page, f"Error al crear egreso: {str(e)}")

        def editar_egreso(egreso_id):
            """Abrir diálogo para editar un egreso"""
            try:
                # Obtener datos del egreso
                egreso = api.get_egreso_por_id(egreso_id)
                if not egreso:
                    mostrar_error(page, "No se pudo cargar el egreso")
                    return

                # Campos del formulario de edición
                edit_categoria = ft.Dropdown(
                    label="Categoría",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=str(egreso.get('id_categoria'))
                )
                edit_concepto = ft.TextField(
                    label="Concepto",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=egreso.get('concepto', '')
                )
                edit_descripcion = ft.TextField(
                    label="Descripción (opcional)",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    multiline=True,
                    min_lines=2,
                    max_lines=3,
                    value=egreso.get('descripcion', '')
                )
                edit_monto = ft.TextField(
                    label="Monto",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    prefix_text="S/ ",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    value=str(egreso.get('monto', ''))
                )
                edit_metodo_pago = ft.Dropdown(
                    label="Método de Pago",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=egreso.get('metodo_pago', 'Efectivo'),
                    options=[
                        ft.dropdown.Option("Efectivo"),
                        ft.dropdown.Option("Transferencia"),
                        ft.dropdown.Option("Tarjeta"),
                        ft.dropdown.Option("Cheque"),
                    ]
                )
                edit_fecha = ft.TextField(
                    label="Fecha (YYYY-MM-DD)",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=egreso.get('fecha_egreso', '')[:10] if egreso.get('fecha_egreso') else ''
                )
                edit_proveedor = ft.TextField(
                    label="Proveedor (opcional)",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=egreso.get('proveedor', '')
                )
                edit_estado = ft.Dropdown(
                    label="Estado",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=egreso.get('estado', 'Pagado'),
                    options=[
                        ft.dropdown.Option("Pagado"),
                        ft.dropdown.Option("Pendiente"),
                        ft.dropdown.Option("Cancelado"),
                    ]
                )

                # Cargar categorías en el dropdown
                try:
                    categorias = api.get_categorias_egresos(estado="Activa")
                    edit_categoria.options = [
                        ft.dropdown.Option(key=str(cat['id']), text=cat['nombre'])
                        for cat in categorias
                    ]
                except Exception as ex:
                    print(f"Error cargando categorías: {ex}")

                def guardar_cambios(e):
                    """Guardar los cambios del egreso"""
                    try:
                        # Validaciones
                        if not edit_categoria.value:
                            mostrar_error(page, "Selecciona una categoría")
                            return
                        if not edit_concepto.value or len(edit_concepto.value.strip()) < 3:
                            mostrar_error(page, "El concepto debe tener al menos 3 caracteres")
                            return
                        if not edit_monto.value or float(edit_monto.value) <= 0:
                            mostrar_error(page, "El monto debe ser mayor a 0")
                            return

                        # Preparar datos actualizados
                        data_actualizada = {
                            "id_categoria": int(edit_categoria.value),
                            "concepto": edit_concepto.value.strip(),
                            "descripcion": edit_descripcion.value.strip() if edit_descripcion.value else "",
                            "monto": float(edit_monto.value),
                            "metodo_pago": edit_metodo_pago.value,
                            "fecha_egreso": edit_fecha.value,
                            "proveedor": edit_proveedor.value.strip() if edit_proveedor.value else "",
                            "estado": edit_estado.value
                        }

                        print(f"\n{'='*60}")
                        print(f"✏️ ACTUALIZANDO EGRESO ID: {egreso_id}")
                        print(f"Concepto: {data_actualizada['concepto']}")
                        print(f"Monto: S/ {data_actualizada['monto']}")
                        print(f"{'='*60}\n")

                        # Llamar al API
                        resultado = api.actualizar_egreso(egreso_id, data_actualizada)

                        if resultado:
                            mostrar_exito(page, "Egreso actualizado exitosamente")
                            cargar_egresos()
                            page.close(dialog_edicion)
                        else:
                            mostrar_error(page, "No se pudo actualizar el egreso")

                    except Exception as ex:
                        mostrar_error(page, f"Error: {str(ex)}")
                        print(f"Error actualizando egreso: {ex}")

                # Crear diálogo
                dialog_edicion = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"✏️ Editar Egreso - {egreso.get('folio', '')}"),
                    content=ft.Container(
                        content=ft.Column([
                            edit_categoria,
                            edit_concepto,
                            edit_descripcion,
                            edit_monto,
                            edit_metodo_pago,
                            edit_fecha,
                            edit_proveedor,
                            edit_estado,
                        ], spacing=15, tight=True),
                        width=400,
                        height=500
                    ),
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog_edicion)),
                        ft.ElevatedButton(
                            "Guardar Cambios",
                            on_click=guardar_cambios,
                            bgcolor=Theme.PRIMARY,
                            color="white"
                        ),
                    ],
                )
                page.open(dialog_edicion)

            except Exception as ex:
                mostrar_error(page, f"Error al cargar egreso: {str(ex)}")
                print(f"Error en editar_egreso: {ex}")

        def eliminar_egreso(egreso_id):
            """Eliminar egreso"""
            def confirmar_eliminar(e):
                try:
                    api.eliminar_egreso(egreso_id)
                    page.close(dialog)
                    cargar_egresos()
                    mostrar_exito(page, "Egreso eliminado correctamente")
                except Exception as ex:
                    mostrar_error(page, f"Error al eliminar: {str(ex)}")

            def cancelar(e):
                page.close(dialog)

            dialog = ft.AlertDialog(
                title=ft.Text("Confirmar eliminación"),
                content=ft.Text("¿Estás seguro de eliminar este egreso?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.TextButton("Eliminar", on_click=confirmar_eliminar, style=ft.ButtonStyle(color=Theme.DANGER)),
                ],
            )
            page.open(dialog)

        # Referencias para botones de filtro
        btn_hoy_ref = ft.Ref[ft.ElevatedButton]()
        btn_semana_ref = ft.Ref[ft.ElevatedButton]()
        btn_mes_ref = ft.Ref[ft.ElevatedButton]()

        def cambiar_periodo(periodo):
            """Cambiar período de visualización"""
            def handler(e):
                filtro_periodo[0] = periodo

                # Actualizar colores de botones
                if btn_hoy_ref.current:
                    btn_hoy_ref.current.bgcolor = Theme.PRIMARY if periodo == "hoy" else None
                    btn_hoy_ref.current.update()
                if btn_semana_ref.current:
                    btn_semana_ref.current.bgcolor = Theme.PRIMARY if periodo == "semana" else None
                    btn_semana_ref.current.update()
                if btn_mes_ref.current:
                    btn_mes_ref.current.bgcolor = Theme.PRIMARY if periodo == "mes" else None
                    btn_mes_ref.current.update()

                cargar_egresos()
            return handler

        # Layout del tab
        tab_content = ft.Container(
            content=ft.Column([
                # Fila superior: Formulario y Lista de Egresos
                ft.Row([
                    # Panel izquierdo: Formulario
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Nuevo Egreso", size=18, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=20),
                            categoria_dropdown,
                            concepto_field,
                            ft.Row([monto_field, metodo_pago_dropdown], spacing=10),
                            fecha_field,
                            proveedor_field,
                            descripcion_field,
                            ft.Container(height=10),
                            create_primary_button(
                                "Guardar Egreso",
                                crear_egreso_handler,
                                icon=ft.Icons.SAVE,
                                width=300
                            ),
                        ], spacing=15, scroll=ft.ScrollMode.AUTO),
                        width=350,
                        padding=20,
                        bgcolor=Theme.CARD_BG,
                        border_radius=12
                    ),

                    # Panel derecho: Lista de Egresos
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Lista de Egresos", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(expand=True),
                                ft.Row([
                                    ft.ElevatedButton(
                                        "Hoy",
                                        ref=btn_hoy_ref,
                                        on_click=cambiar_periodo("hoy"),
                                        bgcolor=Theme.PRIMARY if filtro_periodo[0] == "hoy" else None
                                    ),
                                    ft.ElevatedButton(
                                        "Semana",
                                        ref=btn_semana_ref,
                                        on_click=cambiar_periodo("semana"),
                                        bgcolor=Theme.PRIMARY if filtro_periodo[0] == "semana" else None
                                    ),
                                    ft.ElevatedButton(
                                        "Mes",
                                        ref=btn_mes_ref,
                                        on_click=cambiar_periodo("mes"),
                                        bgcolor=Theme.PRIMARY if filtro_periodo[0] == "mes" else None
                                    ),
                                ], spacing=10)
                            ]),
                            ft.Divider(height=20),
                            ft.Container(
                                content=ft.Column(
                                    ref=tabla_egresos_ref,
                                    scroll=ft.ScrollMode.AUTO,
                                    spacing=0
                                ),
                                expand=True
                            )
                        ], spacing=10, expand=True),
                        expand=True,
                        padding=20,
                        bgcolor=Theme.CARD_BG,
                        border_radius=12
                    ),
                ], spacing=15, expand=True),

                # Fila inferior: Resumen del Período
                ft.Container(
                    content=ft.Row([
                        create_stat_card(
                            "Total Egresos",
                            ft.Text("S/ 0.00", ref=stats_total_ref, size=24, weight=ft.FontWeight.BOLD, color=Theme.DANGER),
                            ft.Icons.MONEY_OFF,
                            Theme.DANGER
                        ),
                        ft.Container(width=20),
                        create_stat_card(
                            "Cantidad",
                            ft.Text("0 egreso(s)", ref=stats_cantidad_ref, size=16),
                            ft.Icons.RECEIPT_LONG,
                            Theme.INFO
                        ),
                    ], spacing=15),
                    padding=20,
                    bgcolor=Theme.CARD_BG,
                    border_radius=12
                ),
            ], spacing=15, expand=True),
            padding=20,
            expand=True
        )

        # Cargar datos después de que el componente esté montado
        # Usamos un pequeño delay para asegurar que las referencias estén disponibles
        def cargar_datos_iniciales():
            import time
            time.sleep(0.1)  # Esperar 100ms para que las refs estén disponibles
            cargar_categorias()
            cargar_egresos()

        # Ejecutar carga en background
        import threading
        threading.Thread(target=cargar_datos_iniciales, daemon=True).start()

        return tab_content

    # ==========================================
    # TAB 2: REPORTE FINANCIERO
    # ==========================================
    def create_tab_reporte_financiero():
        """Crear tab de reporte financiero integrado"""

        # Referencias
        ganancia_neta_ref = ft.Ref[ft.Text]()
        ingresos_ref = ft.Ref[ft.Text]()
        egresos_ref = ft.Ref[ft.Text]()
        margen_ref = ft.Ref[ft.Text]()

        def cargar_reporte():
            """Cargar reporte financiero del día"""
            try:
                fecha_hoy = get_now_local().strftime('%Y-%m-%d')

                print(f"\n{'='*60}")
                print(f"📊 CARGANDO REPORTE FINANCIERO")
                print(f"Fecha: {fecha_hoy}")

                reporte = api.get_reporte_financiero_diario(fecha=fecha_hoy)

                ganancia_neta = reporte.get('ganancia_neta', 0)
                total_ingresos = reporte.get('total_ingresos', 0)
                total_egresos = reporte.get('total_egresos', 0)
                margen_neto = reporte.get('margen_neto', 0)

                print(f"Ganancia Neta: S/ {ganancia_neta:,.2f}")
                print(f"Ingresos: S/ {total_ingresos:,.2f}")
                print(f"Egresos: S/ {total_egresos:,.2f}")
                print(f"Margen: {margen_neto:.2f}%")
                print(f"{'='*60}\n")

                # Actualizar UI
                if ganancia_neta_ref.current:
                    ganancia_neta_ref.current.value = f"S/ {ganancia_neta:,.2f}"
                    ganancia_neta_ref.current.color = Theme.SUCCESS if ganancia_neta >= 0 else Theme.DANGER
                    ganancia_neta_ref.current.update()

                if ingresos_ref.current:
                    ingresos_ref.current.value = f"S/ {total_ingresos:,.2f}"
                    ingresos_ref.current.update()

                if egresos_ref.current:
                    egresos_ref.current.value = f"S/ {total_egresos:,.2f}"
                    egresos_ref.current.update()

                if margen_ref.current:
                    margen_ref.current.value = f"{margen_neto:.1f}%"
                    margen_ref.current.update()

            except Exception as e:
                print(f"❌ Error al cargar reporte financiero: {e}")
                mostrar_error(page, f"Error al cargar reporte: {str(e)}")

        # Cargar datos iniciales
        cargar_reporte()

        # Layout del tab
        return ft.Container(
            content=ft.Column([
                ft.Text("Reporte Financiero del Día", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),

                # Card grande: Ganancia Neta
                ft.Container(
                    content=ft.Column([
                        ft.Text("GANANCIA NETA", size=16, color=Theme.TEXT_SECONDARY),
                        ft.Text("S/ 0.00", ref=ganancia_neta_ref, size=48, weight=ft.FontWeight.BOLD, color=Theme.SUCCESS),
                        ft.Text("Ingresos - Egresos del día", size=12, color=Theme.TEXT_SECONDARY),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=30,
                    bgcolor=Theme.CARD_BG,
                    border_radius=12,
                    alignment=ft.alignment.center
                ),

                ft.Container(height=20),

                # Cards de detalle
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.TRENDING_UP, color=Theme.SUCCESS, size=40),
                                ft.Column([
                                    ft.Text("Total Ingresos", size=14, color=Theme.TEXT_SECONDARY),
                                    ft.Text("S/ 0.00", ref=ingresos_ref, size=24, weight=ft.FontWeight.BOLD, color=Theme.SUCCESS),
                                ], spacing=5)
                            ], spacing=15)
                        ]),
                        padding=20,
                        bgcolor=Theme.CARD_BG,
                        border_radius=12,
                        expand=True
                    ),

                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.TRENDING_DOWN, color=Theme.DANGER, size=40),
                                ft.Column([
                                    ft.Text("Total Egresos", size=14, color=Theme.TEXT_SECONDARY),
                                    ft.Text("S/ 0.00", ref=egresos_ref, size=24, weight=ft.FontWeight.BOLD, color=Theme.DANGER),
                                ], spacing=5)
                            ], spacing=15)
                        ]),
                        padding=20,
                        bgcolor=Theme.CARD_BG,
                        border_radius=12,
                        expand=True
                    ),

                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.PERCENT, color=Theme.INFO, size=40),
                                ft.Column([
                                    ft.Text("Margen Neto", size=14, color=Theme.TEXT_SECONDARY),
                                    ft.Text("0%", ref=margen_ref, size=24, weight=ft.FontWeight.BOLD, color=Theme.INFO),
                                ], spacing=5)
                            ], spacing=15)
                        ]),
                        padding=20,
                        bgcolor=Theme.CARD_BG,
                        border_radius=12,
                        expand=True
                    ),
                ], spacing=15),

                ft.Container(height=20),

                # Información adicional
                ft.Container(
                    content=ft.Column([
                        ft.Text("ℹ️ Información", size=16, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.Text("• Los ingresos incluyen membresías y venta de productos", size=12),
                        ft.Text("• La ganancia neta = Ingresos - Egresos", size=12),
                        ft.Text("• El margen neto = (Ganancia / Ingresos) × 100", size=12),
                    ], spacing=8),
                    padding=20,
                    bgcolor=Theme.BACKGROUND_MEDIUM,
                    border_radius=12
                )
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True
        )

    # ==========================================
    # TAB 3: CATEGORÍAS DE EGRESOS
    # ==========================================
    def create_tab_categorias():
        """Tab para administrar categorías de egresos"""
        categorias_list_ref = ft.Ref[ft.Column]()

        # Campos para nueva categoría
        nombre_cat_field = ft.TextField(
            label="Nombre de Categoría",
            border_color=Theme.BORDER_DEFAULT,
            width=300
        )
        descripcion_cat_field = ft.TextField(
            label="Descripción (opcional)",
            border_color=Theme.BORDER_DEFAULT,
            width=300,
            multiline=True,
            min_lines=2,
            max_lines=3
        )

        def cargar_categorias_tabla():
            """Cargar categorías en la tabla"""
            print("\n" + "="*60)
            print("🗂️ CARGANDO CATEGORÍAS DE EGRESOS")
            print("="*60)

            if not categorias_list_ref.current:
                print("⚠️ categorias_list_ref.current no disponible")
                return

            categorias_list_ref.current.controls.clear()

            try:
                categorias = api.get_categorias_egresos()  # Todas, sin filtro

                print(f"📋 Categorías obtenidas del backend: {len(categorias)}")
                if categorias:
                    for cat in categorias[:3]:  # Mostrar primeras 3
                        print(f"  - {cat.get('nombre', 'N/A')}: {cat.get('descripcion', 'Sin desc')}")

                if not categorias:
                    categorias_list_ref.current.controls.append(
                        ft.Container(
                            content=ft.Text("No hay categorías registradas", size=14, color=Theme.TEXT_SECONDARY),
                            padding=20,
                            alignment=ft.alignment.center
                        )
                    )
                    categorias_list_ref.current.update()
                else:
                    # Encabezado
                    categorias_list_ref.current.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text("Nombre", weight=ft.FontWeight.BOLD, width=200),
                                ft.Text("Descripción", weight=ft.FontWeight.BOLD, expand=True),
                                ft.Text("Estado", weight=ft.FontWeight.BOLD, width=100),
                                ft.Text("Acciones", weight=ft.FontWeight.BOLD, width=140),
                            ]),
                            bgcolor=Theme.BACKGROUND_MEDIUM,
                            padding=10,
                            border_radius=8
                        )
                    )

                    # Filas
                    for cat in categorias:
                        cat_id = cat.get('id')
                        nombre = cat.get('nombre', '')
                        descripcion = cat.get('descripcion', '')
                        estado = cat.get('estado', 'Activa')

                        estado_color = Theme.SUCCESS if estado == "Activa" else Theme.TEXT_SECONDARY

                        def crear_editar_cat_handler(categoria_id):
                            def handler(e):
                                editar_categoria(categoria_id)
                            return handler

                        def crear_eliminar_cat_handler(categoria_id):
                            def handler(e):
                                eliminar_categoria(categoria_id)
                            return handler

                        categorias_list_ref.current.controls.append(
                            ft.Container(
                                content=ft.Row([
                                    ft.Text(nombre, size=12, width=200, weight=ft.FontWeight.BOLD),
                                    ft.Text(descripcion or "Sin descripción", size=12, expand=True),
                                    ft.Container(
                                        content=ft.Text(estado, size=11, color="white"),
                                        bgcolor=estado_color,
                                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                        border_radius=4,
                                        width=100,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        icon_color=Theme.PRIMARY,
                                        tooltip="Editar",
                                        on_click=crear_editar_cat_handler(cat_id)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=Theme.DANGER,
                                        tooltip="Eliminar",
                                        on_click=crear_eliminar_cat_handler(cat_id)
                                    )
                                ]),
                                padding=10,
                                border=ft.border.only(bottom=ft.border.BorderSide(1, Theme.BORDER_DEFAULT))
                            )
                        )

                categorias_list_ref.current.update()
                print("✅ Tabla de categorías actualizada correctamente")
                print("="*60 + "\n")

            except Exception as e:
                print(f"❌ Error cargando categorías: {e}")
                print("="*60 + "\n")
                mostrar_error(page, f"Error al cargar categorías: {str(e)}")

        def crear_categoria_handler(e):
            """Crear nueva categoría"""
            try:
                if not nombre_cat_field.value or len(nombre_cat_field.value.strip()) < 3:
                    mostrar_error(page, "El nombre debe tener al menos 3 caracteres")
                    return

                data = {
                    "nombre": nombre_cat_field.value.strip(),
                    "descripcion": descripcion_cat_field.value.strip() if descripcion_cat_field.value else "",
                    "estado": "Activa"
                }

                print(f"\n{'='*60}")
                print(f"🗂️ CREANDO CATEGORÍA DE EGRESO")
                print(f"Nombre: {data['nombre']}")
                print(f"{'='*60}\n")

                resultado = api.crear_categoria_egreso(data)

                if resultado:
                    mostrar_exito(page, "Categoría creada exitosamente")
                    nombre_cat_field.value = ""
                    descripcion_cat_field.value = ""
                    nombre_cat_field.update()
                    descripcion_cat_field.update()
                    cargar_categorias_tabla()

            except Exception as ex:
                print(f"❌ Error al crear categoría: {ex}")
                mostrar_error(page, f"Error: {str(ex)}")

        def editar_categoria(categoria_id):
            """Editar categoría existente"""
            try:
                print(f"\n{'='*60}")
                print(f"✏️ EDITANDO CATEGORÍA ID: {categoria_id}")
                print(f"{'='*60}")

                categoria = api.get_categoria_egreso_por_id(categoria_id)
                print(f"Categoría obtenida: {categoria}")

                if not categoria:
                    print("❌ No se pudo obtener la categoría del backend")
                    mostrar_error(page, "No se pudo cargar la categoría")
                    return

                edit_nombre = ft.TextField(
                    label="Nombre",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=categoria.get('nombre', '')
                )
                edit_descripcion = ft.TextField(
                    label="Descripción",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    multiline=True,
                    min_lines=2,
                    max_lines=3,
                    value=categoria.get('descripcion', '')
                )
                edit_estado = ft.Dropdown(
                    label="Estado",
                    border_color=Theme.BORDER_DEFAULT,
                    width=300,
                    value=categoria.get('estado', 'Activa'),
                    options=[
                        ft.dropdown.Option("Activa"),
                        ft.dropdown.Option("Inactiva"),
                    ]
                )

                def guardar_cambios_cat(e):
                    try:
                        if not edit_nombre.value or len(edit_nombre.value.strip()) < 3:
                            mostrar_error(page, "El nombre debe tener al menos 3 caracteres")
                            return

                        data_actualizada = {
                            "nombre": edit_nombre.value.strip(),
                            "descripcion": edit_descripcion.value.strip() if edit_descripcion.value else "",
                            "estado": edit_estado.value
                        }

                        print(f"📤 Enviando actualización al backend:")
                        print(f"   ID: {categoria_id}")
                        print(f"   Datos: {data_actualizada}")

                        resultado = api.actualizar_categoria_egreso(categoria_id, data_actualizada)
                        print(f"📥 Resultado del backend: {resultado}")

                        if resultado:
                            print("✅ Categoría actualizada exitosamente")
                            mostrar_exito(page, "Categoría actualizada exitosamente")
                            cargar_categorias_tabla()
                            page.close(dialog_editar)
                        else:
                            print("❌ Backend retornó None o False")
                            mostrar_error(page, "No se pudo actualizar la categoría")

                    except Exception as ex:
                        print(f"❌ Excepción al actualizar: {ex}")
                        import traceback
                        traceback.print_exc()
                        mostrar_error(page, f"Error: {str(ex)}")

                dialog_editar = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"✏️ Editar Categoría"),
                    content=ft.Container(
                        content=ft.Column([
                            edit_nombre,
                            edit_descripcion,
                            edit_estado,
                        ], spacing=15, tight=True),
                        width=400
                    ),
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog_editar)),
                        ft.ElevatedButton(
                            "Guardar",
                            on_click=guardar_cambios_cat,
                            bgcolor=Theme.PRIMARY,
                            color="white"
                        ),
                    ],
                )
                page.open(dialog_editar)

            except Exception as ex:
                mostrar_error(page, f"Error: {str(ex)}")

        def eliminar_categoria(categoria_id):
            """Eliminar categoría"""
            def confirmar(e):
                try:
                    print(f"\n{'='*60}")
                    print(f"🗑️ ELIMINANDO CATEGORÍA ID: {categoria_id}")
                    print(f"{'='*60}")

                    resultado = api.eliminar_categoria_egreso(categoria_id)
                    print(f"📥 Resultado del backend: {resultado}")

                    if resultado:
                        print("✅ Categoría eliminada exitosamente")
                        page.close(dialog_confirmar)
                        cargar_categorias_tabla()
                        mostrar_exito(page, "Categoría eliminada correctamente")
                    else:
                        print("❌ Backend retornó False - Puede tener egresos asociados")
                        page.close(dialog_confirmar)
                        mostrar_error(page, "No se pudo eliminar la categoría. Puede tener egresos asociados.")
                except Exception as ex:
                    print(f"❌ Excepción al eliminar: {ex}")
                    import traceback
                    traceback.print_exc()
                    page.close(dialog_confirmar)
                    mostrar_error(page, f"Error: {str(ex)}")

            dialog_confirmar = ft.AlertDialog(
                title=ft.Text("Confirmar eliminación"),
                content=ft.Text("¿Estás seguro de eliminar esta categoría? Solo se puede eliminar si no tiene egresos asociados."),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog_confirmar)),
                    ft.TextButton("Eliminar", on_click=confirmar, style=ft.ButtonStyle(color=Theme.DANGER)),
                ],
            )
            page.open(dialog_confirmar)

        # Layout del tab
        tab_content = ft.Container(
            content=ft.Row([
                # Panel izquierdo: Formulario
                ft.Container(
                    content=ft.Column([
                        ft.Text("Nueva Categoría", size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=20),
                        nombre_cat_field,
                        descripcion_cat_field,
                        ft.Container(height=10),
                        create_primary_button(
                            "Crear Categoría",
                            crear_categoria_handler,
                            icon=ft.Icons.ADD,
                            width=300
                        ),
                    ], spacing=15),
                    width=350,
                    padding=20,
                    bgcolor=Theme.CARD_BG,
                    border_radius=12
                ),

                # Panel derecho: Lista de categorías
                ft.Container(
                    content=ft.Column([
                        ft.Text("Categorías Registradas", size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.Column(
                            ref=categorias_list_ref,
                            spacing=0,
                            scroll=ft.ScrollMode.AUTO,
                            expand=True
                        ),
                    ], spacing=10, expand=True),
                    expand=True,
                    padding=20,
                    bgcolor=Theme.CARD_BG,
                    border_radius=12
                ),
            ], spacing=20, expand=True),
            padding=20,
            expand=True
        )

        # Cargar datos después de que el componente esté montado
        def cargar_datos_cat_iniciales():
            import time
            time.sleep(0.1)  # Esperar 100ms para que las refs estén disponibles
            cargar_categorias_tabla()

        # Ejecutar carga en background
        import threading
        threading.Thread(target=cargar_datos_cat_iniciales, daemon=True).start()

        return tab_content

    # ==========================================
    # NAVEGACIÓN DE TABS
    # ==========================================
    def on_tab_change(e):
        """Handler para cambio de tab"""
        selected_tab[0] = e.control.selected_index

        if selected_tab[0] == 0:
            content_ref.current.content = create_tab_egresos()
        elif selected_tab[0] == 1:
            content_ref.current.content = create_tab_reporte_financiero()
        elif selected_tab[0] == 2:
            content_ref.current.content = create_tab_categorias()

        content_ref.current.update()

    # Tabs
    tabs = ft.Tabs(
        selected_index=0,
        on_change=on_tab_change,
        tabs=[
            ft.Tab(
                text="Egresos",
                icon=ft.Icons.MONEY_OFF
            ),
            ft.Tab(
                text="Reporte Financiero",
                icon=ft.Icons.ASSESSMENT
            ),
            ft.Tab(
                text="Categorías",
                icon=ft.Icons.CATEGORY
            ),
        ],
    )

    # Contenedor principal del contenido
    main_content = ft.Container(
        ref=content_ref,
        content=create_tab_egresos(),  # Iniciar con tab de egresos
        expand=True
    )

    # Layout principal con sidebar
    content = ft.Column([
        tabs,
        ft.Divider(height=1),
        main_content
    ], spacing=0, expand=True)

    # Aplicar layout base
    create_base_layout(
        page=page,
        role="admin",
        current_section="Finanzas",
        on_section_click=on_section_click,
        content=content,
        user_info=user_info,
        on_logout=lambda _: on_section_click("logout")
    )
