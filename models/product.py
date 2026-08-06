#PARTE DE MONICA
import uuid  # Importa la libreria para generar identificadores unicos.

class Producto:
    # Constructor de la clase Producto.
    def __init__(self, nombre, precio, stock, categoria_uuid):
        self.uuid = str(uuid.uuid4())  # Identificador unico del producto.
        self.nombre = nombre  # Nombre del producto.
        self.precio = precio  # Precio del producto.
        self.stock = stock  # Cantidad disponible en inventario.
        self.categoria_uuid = categoria_uuid  # UUID de la categoria a la que pertenece.

    # Convierte el objeto en un diccionario.
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria_uuid": self.categoria_uuid
        }

    # Crea un objeto Producto a partir de un diccionario.
    @classmethod
    def from_dict(cls, data):
        producto = cls(
            data["nombre"],
            data["precio"],
            data["stock"],
            data["categoria_uuid"]
        )
        producto.uuid = data["uuid"]
        return producto
