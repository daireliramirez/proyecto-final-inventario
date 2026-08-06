#PARTE DE DAIRELY
from model.producto import Producto
from model.categoria import Categoria
from repository.inventario_repository import ProductRepository
from repository.inventario_repository import CategoryRepository

# 1. SERVICIO DE CATEGORÍAS
# Encargado de coordinar la lógica de negocio para las Categorías.
class CategoryService:
    def __init__(self, category_repository: CategoryRepository) -> None:
        # Inyección de dependencias.
        self.__category_repository = category_repository

    def get_all_categories(self) -> list[Categoria]:
        """Recupera la lista completa de categorías desde la persistencia."""
        return self.__category_repository.find_all()

    def get_category_by_id(self, categoria_uuid: str) -> Categoria:
        """Busca una categoría específica"""
        
        categoria = self.__category_repository.find_one(categoria_uuid)
        if not categoria:
            raise ValueError(f"La categoría con UUID {categoria_uuid} no existe.")
        return categoria

    def create_category(self, categoria: Categoria) -> Categoria:

        if not categoria.nombre or len(categoria.nombre.strip()) == 0:
            raise ValueError("El nombre de la categoría no puede estar vacío.")

        
        self.__category_repository.create_one(categoria)
        return categoria

    def update_category(self, categoria_uuid: str, categoria_actualizada: Categoria) -> Categoria:
      
        self.get_category_by_id(categoria_uuid)

         # Validar que los datos nuevos sean correctos
        if not categoria_actualizada.nombre or len(categoria_actualizada.nombre.strip()) == 0:
            raise ValueError("El nuevo nombre de la categoría no puede estar vacío.")

        # Aplicar la actualización en la persistencia
        self.__category_repository.update_one(categoria_uuid, categoria_actualizada)
        return categoria_actualizada

    def delete_category(self, categoria_uuid: str) -> None:
        """Elimina una categoría del sistema."""
        # Valida que la categoría exista antes de intentar eliminarla
        self.get_category_by_id(categoria_uuid)
        
        # Procede a eliminarla del repositorio
        self.__category_repository.delete_one(categoria_uuid)


# 2. SERVICIO DE PRODUCTOS 
# Encargado de las reglas de negocio de Productos y su relación con Categorías.
class ProductService:
    def __init__(
        self, 
        product_repository: ProductRepository, 
        category_repository: CategoryRepository
    ) -> None:
        # Inyectamos AMBOS repositorios porque ProductService necesita validar
        # la existencia de las categorías asociadas a los productos.
        self.__product_repository = product_repository
        self.__category_repository = category_repository

    def get_all_products(self) -> list[Producto]:
        """Obtiene el listado general de productos."""
        return self.__product_repository.find_all()

    def get_product_by_id(self, producto_uuid: str) -> Producto:
        """Obtiene un producto o lanza un error claro si no es encontrado."""
        producto = self.__product_repository.find_one(producto_uuid)
        if not producto:
            raise ValueError(f"El producto con UUID {producto_uuid} no existe.")
        return producto

    def create_product(self, producto: Producto) -> Producto:
        """Valida precios, stock e integridad referencial antes de crear un producto."""
        # El precio debe ser un valor válido
        if producto.precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")

        # El stock debe ser mayor o igual a 0
        if producto.stock < 0:
            raise ValueError("El stock del producto no puede ser negativo.")

        # Si el producto tiene una categoría asignada, verificamos que esa categoría EXISTA en el sistema.
        if hasattr(producto, 'categoria_uuid') and producto.categoria_uuid:
            categoria_existe = self.__category_repository.find_one(producto.categoria_uuid)
            if not categoria_existe:
                raise ValueError(f"No se puede crear el producto: La categoría asociativa con UUID {producto.categoria_uuid} no existe.")

        # Guardar en repositorio 
        self.__product_repository.create_one(producto)
        return producto

    def update_product(self, producto_uuid: str, producto_actualizado: Producto) -> Producto:
        """Actualiza los datos de un producto existente."""
        # Comprobar que el producto existe en el sistema
        self.get_product_by_id(producto_uuid)

        # Validar valores numéricos coherentes
        if producto_actualizado.precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")
        if producto_actualizado.stock < 0:
            raise ValueError("El stock del producto no puede ser negativo.")

        # Validar que la nueva categoría (si cambió) exista realmente
        if hasattr(producto_actualizado, 'categoria_uuid') and producto_actualizado.categoria_uuid:
            if not self.__category_repository.find_one(producto_actualizado.categoria_uuid):
                raise ValueError(f"No se puede actualizar: La categoría {producto_actualizado.categoria_uuid} no existe.")

        # Efectuar el cambio en el repositorio
        self.__product_repository.update_one(producto_uuid, producto_actualizado)
        return producto_actualizado

    def delete_product(self, producto_uuid: str) -> None:
        """Elimina un producto del sistema."""
        # Garantiza que el producto exista antes de invocar la eliminación
        self.get_product_by_id(producto_uuid)
        
        self.__product_repository.delete_one(producto_uuid)
