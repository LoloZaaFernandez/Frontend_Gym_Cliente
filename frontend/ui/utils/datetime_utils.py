"""
Utilidades para manejo de fechas y horas con detección automática de zona horaria
El sistema detecta automáticamente la zona horaria del sistema operativo
"""

from datetime import datetime, timezone


def get_local_tz():
    """
    Obtener la zona horaria local del sistema operativo

    Returns:
        timezone: Zona horaria local del sistema
    """
    # Obtener la zona horaria local del sistema automáticamente
    return datetime.now().astimezone().tzinfo


def get_now_local() -> datetime:
    """
    Obtener la fecha y hora actual en la zona horaria local del sistema

    Returns:
        datetime: Datetime actual en zona horaria local con timezone info
    """
    return datetime.now().astimezone()


def parse_datetime_from_api(datetime_str: str) -> datetime:
    """
    Parsear datetime desde la API

    IMPORTANTE: El backend guarda fechas/horas en ZONA HORARIA LOCAL (Perú, UTC-5)
    NO hacer conversión de timezone porque ya viene en hora local.

    El backend puede enviar:
    - Fecha completa ISO: "2025-11-10T17:24:54.635364" (ya es hora local)
    - Solo hora: "17:24:54.635364" (hora local del día de hoy)

    Args:
        datetime_str: String con fecha/hora del backend

    Returns:
        datetime: Objeto datetime en zona horaria local del sistema, o None si falla
    """
    if not datetime_str:
        return None

    try:
        datetime_str = str(datetime_str).strip()
        local_tz = get_local_tz()

        # Si tiene formato ISO completo con fecha
        if 'T' in datetime_str or '-' in datetime_str:
            # Limpiar Z final si existe
            datetime_str_clean = datetime_str.replace('Z', '').replace('+00:00', '')

            # Parsear el datetime
            dt = datetime.fromisoformat(datetime_str_clean)

            # CAMBIO IMPORTANTE: El backend ya envía en hora local
            # Solo agregar timezone info si no la tiene, pero SIN convertir
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=local_tz)

            return dt

        # Si es solo hora (HH:MM:SS o HH:MM:SS.mmmmmm)
        elif ':' in datetime_str:
            # Es solo hora en zona local del día de hoy
            time_parts = datetime_str.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            second = int(float(time_parts[2])) if len(time_parts) > 2 else 0

            # Crear datetime LOCAL de hoy con esta hora
            now_local = datetime.now(local_tz)
            dt_local = now_local.replace(hour=hour, minute=minute, second=second, microsecond=0)

            return dt_local

        return None

    except Exception as e:
        print(f"Error parseando datetime '{datetime_str}': {e}")
        return None


def format_datetime_display(dt: datetime, include_seconds: bool = False) -> str:
    """
    Formatear datetime para mostrar en la UI

    Args:
        dt: Objeto datetime
        include_seconds: Si incluir segundos

    Returns:
        str: Fecha formateada (ej: "10/11/2025 12:24" o "10/11/2025 12:24:54")
    """
    if not dt:
        return "Sin registro"

    try:
        if include_seconds:
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        else:
            return dt.strftime("%d/%m/%Y %H:%M")
    except Exception as e:
        print(f"Error formateando datetime: {e}")
        return "Fecha inválida"


def format_date_display(dt: datetime) -> str:
    """
    Formatear solo la fecha para mostrar en la UI

    Args:
        dt: Objeto datetime

    Returns:
        str: Fecha formateada (ej: "10/11/2025")
    """
    if not dt:
        return "Sin fecha"

    try:
        return dt.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Error formateando fecha: {e}")
        return "Fecha inválida"


def format_time_display(dt: datetime) -> str:
    """
    Formatear solo la hora para mostrar en la UI

    Args:
        dt: Objeto datetime

    Returns:
        str: Hora formateada (ej: "12:24")
    """
    if not dt:
        return "--:--"

    try:
        return dt.strftime("%H:%M")
    except Exception as e:
        print(f"Error formateando hora: {e}")
        return "--:--"


def format_header_time() -> str:
    """
    Formatear hora para el header (HH:MM)

    Returns:
        str: Hora actual en zona horaria local formateada
    """
    return get_now_local().strftime("%H:%M")


def format_header_date() -> str:
    """
    Formatear fecha para el header (DD/MM/YYYY)

    Returns:
        str: Fecha actual en zona horaria local formateada
    """
    return get_now_local().strftime("%d/%m/%Y")
