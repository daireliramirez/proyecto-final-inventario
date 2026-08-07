#PARTE DE MONICA
import uuid #Importa la libreria para generar identificadore unicos.

class Categoria:
    #Constructor de la clase categoria.
    def __init__(self, nombre):
        self.uuid = str(uuid.uuid4()) #Genera un UUDI unico.
        self.nombre = nombre #Guarda el nombre de la categoria. 

        #Convierte el objeto en un diccionario.

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "nombre": self.nombre
        }
#Crea un objeto categoria a partir de un diccionario.
    @classmethod
    def from_dict(cls, data):
        categoria = cls(data["nombre"])
        categoria.uuid = data["uuid"]
        return categoria