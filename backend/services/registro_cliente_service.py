from typing import Dict, Any
from datetime import datetime, timedelta
from repositories.cliente_repository import ClienteRepository
from repositories.membresia_repository import MembresiaRepository


class RegistroClienteService:
    def __init__(self):
        self.cliente_repo = ClienteRepository()
        self.membresia_repo = MembresiaRepository()

    def registrar_cliente_completo(self, registro_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registrar un cliente completo con su membresía en un solo proceso
        """
        try:
            # 1. Verificar que el DNI no esté registrado
            cliente_existente = self.cliente_repo.find_by_dni(
                registro_data['dni'])
            if cliente_existente:
                raise ValueError("El DNI ya se encuentra registrado")

            # 2. Verificar que la membresía existe y está activa
            membresia = self.membresia_repo.find_by_id(
                registro_data['id_membresia'])
            if not membresia:
                raise ValueError("La membresía seleccionada no existe")
            if membresia.get('estado') != 'Activa':
                raise ValueError("La membresía seleccionada no está activa")

            # 3. Obtener precio vigente de la membresía
            precio_vigente = self.membresia_repo.get_precio_vigente(
                registro_data['id_membresia'])
            if not precio_vigente:
                raise ValueError(
                    "No se encontró un precio vigente para la membresía")

            monto = precio_vigente['precio_actual']

            # 4. Crear el cliente
            cliente_data = {
                'dni': registro_data['dni'],
                'nombre': registro_data['nombre'],
                'apellidos': registro_data['apellidos'],
                'correo': registro_data['correo'],
                'telefono': registro_data.get('telefono'),
                'usuario_creacion': registro_data.get('usuario_creacion', 'admin')
            }

            cliente_id = self.cliente_repo.create(cliente_data)
            cliente = self.cliente_repo.find_by_id(cliente_id)

            # 5. Calcular fecha de vencimiento de la membresía
            tipo_membresia = membresia['tipo_membresia']
            dias_duracion = {
                "Dia": 1,
                "Mensual": 30,
                "Trimestral": 90,
                "Semestral": 180,
                "Anual": 365
            }

            fecha_actual = datetime.now()
            fecha_vencimiento = fecha_actual + \
                timedelta(days=dias_duracion.get(tipo_membresia, 30))

            # 6. Registrar el pago de la membresía
            pago_data = {
                'id_cliente': cliente_id,
                'id_membresia': registro_data['id_membresia'],
                'monto': monto,
                'metodo_pago': registro_data['metodo_pago'],
                'usuario_creacion': registro_data.get('usuario_creacion', 'admin')
            }

            pago_id = self.membresia_repo.create_pago(pago_data)
            pago = self.membresia_repo.find_pago_by_id(pago_id)

            # 7. Actualizar la fecha de membresía del cliente
            self.cliente_repo.update(cliente_id, {
                'fecha_membresia': fecha_vencimiento.isoformat()
            })

            # 8. Obtener cliente actualizado
            cliente_actualizado = self.cliente_repo.find_by_id(cliente_id)

            return {
                'cliente': cliente_actualizado,
                'pago_membresia': pago,
                'mensaje': f'Cliente registrado exitosamente con membresía {tipo_membresia}'
            }

        except Exception as e:
            # En caso de error, realizar rollback manual
            if 'cliente_id' in locals():
                # Si se creó el cliente pero falló algo más, eliminarlo
                self.cliente_repo.delete(cliente_id)
            raise e

    def obtener_opciones_registro(self) -> Dict[str, Any]:
        """
        Obtener las opciones disponibles para el registro (membresías activas con precios)
        """
        try:
            # Obtener todas las membresías activas
            membresias = self.membresia_repo.find_all(estado='Activa')

            opciones_membresias = []
            for membresia in membresias:
                precio_vigente = self.membresia_repo.get_precio_vigente(
                    membresia['id'])
                if precio_vigente:
                    opciones_membresias.append({
                        'id': membresia['id'],
                        'nombre_membresia': membresia['nombre_membresia'],
                        'tipo_membresia': membresia['tipo_membresia'],
                        'precio_actual': precio_vigente['precio_actual'],
                        'duracion_dias': self._obtener_duracion_dias(membresia['tipo_membresia'])
                    })

            return {
                'membresias_disponibles': opciones_membresias,
                'metodos_pago': ['Efectivo', 'Tarjeta', 'Transferencia', 'Yape', 'Plin']
            }

        except Exception as e:
            raise e

    def _obtener_duracion_dias(self, tipo_membresia: str) -> int:
        """Obtener duración en días según el tipo de membresía"""
        duraciones = {
            "Dia": 1,
            "Mensual": 30,
            "Trimestral": 90,
            "Semestral": 180,
            "Anual": 365
        }
        return duraciones.get(tipo_membresia, 30)
