#PARTE DE ONABEL Y JOSHUA

#Crud productos---------------------------
from model.producto import Producto

class ProductRepository:
    # Simula la base de datos
    __productos: list[Producto] = []

    def __init__(self) -> None:
        pass

    # Obtener todos los productos
    def find_all(self) -> list[Producto]:
        return self.__productos

    # Crear un producto
    def create_one(self, producto: Producto):
        self.__productos.append(producto)

    # Buscar un producto por UUID
    def find_one(self, producto_uuid: str) -> Producto | None:
        for producto in self.__productos:
            if producto.uuid == producto_uuid:
                return producto
        return None

    # Actualizar un producto
    def update_one(self, producto_uuid: str, producto_actualizado: Producto):
        for index, producto in enumerate(self.__productos):
            if producto.uuid == producto_uuid:
                self.__productos[index] = producto_actualizado
                return

    # Eliminar un producto
    def delete_one(self, producto_uuid: str):
        for producto in self.__productos:
            if producto.uuid == producto_uuid:
                self.__productos.remove(producto)
                return

#Crud categorias---------------------------------
from model.categoria import Categoria


class CategoryRepository:
    # Repositorio en memoria para la gestion de categorias.
    __categorias: list[Categoria] = []

    def __init__(self) -> None:
        pass

    # Obtener todas las categorias
    def find_all(self) -> list[Categoria]:
        return self.__categorias

    # Crear una categoria
    def create_one(self, categoria: Categoria) -> None:
        self.__categorias.append(categoria)

    # Buscar una categoria por UUID
    def find_one(self, categoria_uuid: str) -> Categoria | None:
        for categoria in self.__categorias:
            if categoria.uuid == categoria_uuid:
                return categoria
        return None

    # Actualizar una categoria
    def update_one(self, categoria_uuid: str, categoria_actualizada: Categoria) -> None:
        for index, categoria in enumerate(self.__categorias):
            if categoria.uuid == categoria_uuid:
                self.__categorias[index] = categoria_actualizada
                return

    # Eliminar una categoria
    def delete_one(self, categoria_uuid: str) -> None:
        for categoria in self.__categorias:
            if categoria.uuid == categoria_uuid:
                self.__categorias.remove(categoria)
                return