from typing import List, Optional, Dict, Any
from datetime import datetime, date
from repositories.asistencia_repository import AsistenciaRepository


class AsistenciaService:
    def __init__(self):
        self.repository = AsistenciaRepository()

    def registrar_asistencia(self, asistencia_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registrar asistencia de un cliente verificando:
        - Existencia del cliente
        - Estado activo
        - Membresía vigente
        - No duplicidad en el mismo día
        """
        # Obtener información del cliente por DNI
        cliente_info = self.repository.get_cliente_info_by_dni(asistencia_data["dni"])

        if not cliente_info:
            raise ValueError("Cliente no encontrado con ese DNI")

        # Verificar estado del cliente
        if cliente_info.get("estado") != "Activo":
            raise ValueError("Cliente inactivo")

        # Verificar membresía vigente
        if not cliente_info.get("fecha_membresia"):
            raise ValueError("Cliente sin membresía activa")

        fecha_venc = datetime.fromisoformat(cliente_info["fecha_membresia"])
        if fecha_venc < datetime.now():
            raise ValueError("Membresía vencida")

        # VERIFICAR ASISTENCIA DUPLICADA (MEJORA CLAVE)
        if self.repository.verificar_asistencia_hoy(cliente_info["id"]):
            raise ValueError("El cliente ya registró asistencia el día de hoy")

        # Preparar datos de asistencia
        nombre_completo = f"{cliente_info['nombre']} {cliente_info['apellidos']}"
        tipo_membresia = cliente_info.get("tipo_membresia") or "Sin tipo"

        registro_data = {
            "id_cliente": cliente_info["id"],
            "nombre_cliente": nombre_completo,
            "tipo_membresia": tipo_membresia,
            "usuario_creacion": asistencia_data.get("usuario_creacion", "admin"),
        }

        asistencia_id = self.repository.create(registro_data)
        return self.repository.find_by_id(asistencia_id)

    def listar_asistencias(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        cliente_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Listar asistencias con filtros opcionales
        """
        return self.repository.find_all(
            fecha_inicio, fecha_fin, cliente_id, skip, limit
        )

    # ✅ MÉTODOS POR DNI (MEJORA IMPORTANTE)
    def listar_asistencias_por_dni(
        self,
        dni: str,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Listar asistencias de un cliente por DNI
        """
        cliente = self.repository.get_cliente_info_by_dni(dni)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        return self.repository.find_all(None, None, cliente["id"], skip, limit)

    def obtener_estadisticas_cliente_por_dni(self, dni: str) -> Dict[str, Any]:
        """
        Obtener estadísticas de asistencias de un cliente por DNI
        """
        cliente = self.repository.get_cliente_info_by_dni(dni)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        return self.obtener_estadisticas_cliente(cliente["id"])

    def obtener_estadisticas_dia(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de asistencias del día actual
        """
        fecha_hoy = date.today().isoformat()
        asistencias_hoy = self.repository.find_all(fecha_hoy, fecha_hoy, None, 0, 1000)

        return {
            "fecha": fecha_hoy,
            "total_asistencias": len(asistencias_hoy),
            "asistencias": asistencias_hoy,
        }

    def obtener_estadisticas_mes(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de asistencias del mes actual
        """
        fecha_actual = date.today()
        primer_dia = date(fecha_actual.year, fecha_actual.month, 1).isoformat()
        fecha_hoy = fecha_actual.isoformat()

        asistencias_mes = self.repository.find_all(primer_dia, fecha_hoy, None, 0, 1000)

        return {
            "mes": fecha_actual.strftime("%Y-%m"),
            "total_asistencias": len(asistencias_mes),
            "promedio_diario": round(len(asistencias_mes) / fecha_actual.day, 1),
        }

    def obtener_estadisticas_cliente(self, cliente_id: int) -> Dict[str, Any]:
        """
        Obtener estadísticas de asistencias de un cliente
        """
        cliente = self.repository.get_cliente_info(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        # Obtener todas las asistencias del cliente
        asistencias = self.repository.find_all(None, None, cliente_id, 0, 1000)

        # Asistencias del mes actual
        fecha_actual = date.today()
        primer_dia = date(fecha_actual.year, fecha_actual.month, 1).isoformat()
        asistencias_mes = self.repository.find_all(
            primer_dia, fecha_actual.isoformat(), cliente_id, 0, 1000
        )

        # Encontrar última asistencia
        ultima_asistencia = asistencias[0].get("fecha_asistencia") if asistencias else None

        return {
            "cliente_id": cliente_id,
            "nombre_cliente": f"{cliente.get('nombre', '')} {cliente.get('apellidos', '')}",
            "total_asistencias": len(asistencias),
            "asistencias_mes_actual": len(asistencias_mes),
            "ultima_asistencia": ultima_asistencia,
            "membresia_activa": cliente.get("fecha_membresia") and 
                               datetime.fromisoformat(cliente["fecha_membresia"]) > datetime.now()
        }