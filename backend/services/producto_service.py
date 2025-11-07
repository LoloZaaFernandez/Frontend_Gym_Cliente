from typing import List, Optional, Dict, Any
from repositories.producto_repository import ProductoRepository


class ProductoService:
    def __init__(self):
        self.repository = ProductoRepository()

    def crear_categoria(self, categoria_data: Dict[str, Any]) -> Dict[str, Any]:
        categoria_id = self.repository.create_categoria(categoria_data)
        return {"message": "Categoría creada", "id": categoria_id}

    def listar_categorias(self, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.repository.find_categorias(estado)

    def actualizar_categoria(self, categoria_id: int, categoria_data: Dict[str, Any]) -> Dict[str, Any]:
        # Verificar que la categoría existe
        categoria = self.repository.find_categoria_by_id(categoria_id)
        if not categoria:
            raise ValueError("Categoría no encontrada")

        # Actualizar la categoría
        success = self.repository.update_categoria(categoria_id, categoria_data)
        if not success:
            raise ValueError("Error al actualizar la categoría")

        # Retornar la categoría actualizada
        return self.repository.find_categoria_by_id(categoria_id)

    def eliminar_categoria(self, categoria_id: int) -> Dict[str, str]:
        # Verificar que la categoría existe
        categoria = self.repository.find_categoria_by_id(categoria_id)
        if not categoria:
            raise ValueError("Categoría no encontrada")

        # Eliminar la categoría
        success = self.repository.delete_categoria(categoria_id)
        if not success:
            raise ValueError("Error al eliminar la categoría")

        return {"message": "Categoría eliminada exitosamente"}

    def crear_producto(self, producto_data: Dict[str, Any]) -> Dict[str, Any]:
        # Verificar que la categoría existe
        categorias = self.repository.find_categorias()
        categoria_ids = [cat.get('id') or cat.get('Id') for cat in categorias]

        if producto_data['id_categoria'] not in categoria_ids:
            raise ValueError("Categoría no encontrada")

        producto_id = self.repository.create(producto_data)
        return self.repository.find_by_id(producto_id)

    def obtener_producto(self, producto_id: int) -> Dict[str, Any]:
        producto = self.repository.find_by_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        return producto

    def listar_productos(self, categoria_id: Optional[int] = None, estado: Optional[str] = None,
                         skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return self.repository.find_all(categoria_id, estado, skip, limit)

    def actualizar_producto(self, producto_id: int, producto_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.repository.find_by_id(producto_id):
            raise ValueError("Producto no encontrado")

        self.repository.update(producto_id, producto_data)
        return self.repository.find_by_id(producto_id)

    def eliminar_producto(self, producto_id: int) -> Dict[str, str]:
        # Verificar que el producto existe
        producto = self.repository.find_by_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")

        # Eliminar el producto
        success = self.repository.delete(producto_id)
        if not success:
            raise ValueError("Error al eliminar el producto")

        return {"message": "Producto eliminado exitosamente"}

    def registrar_movimiento_inventario(self, movimiento_data: Dict[str, Any]) -> Dict[str, Any]:
        # Obtener producto
        producto = self.repository.find_by_id(movimiento_data['id_producto'])
        if not producto:
            raise ValueError("Producto no encontrado")

        # Obtener stock actual
        stock_anterior = self.repository.get_stock_actual(
            movimiento_data['id_producto'])

        # Calcular nuevo stock
        if movimiento_data['tipo_movimiento'] == "Entrada":
            stock_actual = stock_anterior + movimiento_data['cantidad']
        else:  # Salida
            stock_actual = stock_anterior - movimiento_data['cantidad']
            if stock_actual < 0:
                raise ValueError("Stock insuficiente")

        # Preparar datos completos
        registro_data = {
            'id_producto': movimiento_data['id_producto'],
            'nombre_producto': producto.get('nombre') or producto.get('Nombre'),
            'tipo_movimiento': movimiento_data['tipo_movimiento'],
            'motivo': movimiento_data.get('motivo'),
            'cantidad': movimiento_data['cantidad'],
            'stock_anterior': stock_anterior,
            'stock_actual': stock_actual,
            'usuario_creacion': movimiento_data.get('usuario_creacion', 'admin')
        }

        movimiento_id = self.repository.create_movimiento_inventario(
            registro_data)

        # Obtener el registro creado
        movimientos = self.repository.find_movimientos_inventario(
            producto_id=movimiento_data['id_producto'],
            limit=1
        )
        return movimientos[0] if movimientos else None

    def listar_movimientos_inventario(self, producto_id: Optional[int] = None,
                                      tipo_movimiento: Optional[str] = None,
                                      skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return self.repository.find_movimientos_inventario(producto_id, tipo_movimiento, skip, limit)

    def obtener_stock_producto(self, producto_id: int) -> Dict[str, Any]:
        producto = self.repository.find_by_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")

        stock_actual = self.repository.get_stock_actual(producto_id)

        return {
            "id_producto": producto_id,
            "nombre_producto": producto.get('nombre') or producto.get('Nombre'),
            "stock_actual": stock_actual
        }