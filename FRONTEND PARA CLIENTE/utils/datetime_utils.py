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

    El backend puede enviar:
    - Fecha completa ISO con hora: "2025-11-10T17:24:54.635364" (asumimos UTC, se convierte a local)
    - Solo fecha: "2025-11-15" (NO se convierte zona horaria, se usa tal cual)
    - Solo hora: "17:24:54.635364" (asumimos que es UTC del día de hoy)

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

        # Si tiene 'T' es fecha completa con hora (ej: "2025-11-10T17:24:54")
        if 'T' in datetime_str:
            # Limpiar Z final si existe
            datetime_str_clean = datetime_str.replace('Z', '').replace('+00:00', '')

            # Parsear como UTC
            dt = datetime.fromisoformat(datetime_str_clean)

            # Si no tiene timezone info, asumimos que es UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            # Convertir a hora local del sistema
            dt_local = dt.astimezone(local_tz)
            return dt_local

        # Si tiene '-' pero NO 'T', es solo fecha (ej: "2025-11-15")
        elif '-' in datetime_str:
            # Solo fecha, NO convertir zona horaria
            dt = datetime.fromisoformat(datetime_str)
            # Asignar timezone local SIN conversión
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=local_tz)
            return dt

        # Si es solo hora (HH:MM:SS o HH:MM:SS.mmmmmm)
        elif ':' in datetime_str:
            # Es solo hora, asumir que es UTC del día de hoy
            time_parts = datetime_str.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            second = int(float(time_parts[2])) if len(time_parts) > 2 else 0

            # Crear datetime UTC de hoy con esta hora
            now_utc = datetime.now(timezone.utc)
            dt_utc = now_utc.replace(hour=hour, minute=minute, second=second, microsecond=0)

            # Convertir a hora local del sistema
            dt_local = dt_utc.astimezone(local_tz)
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
