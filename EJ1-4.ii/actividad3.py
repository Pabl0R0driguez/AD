import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent


# Definir clase Motocicleta
class Motocicleta(Persistent):
    def __init__(self, marca, modelo, precio, cilindrada):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.cilindrada = cilindrada


# Establecer conexión a la base de datos
storage = ZODB.FileStorage.FileStorage("2dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()


# Almacenar tres motocicletas
root["moto1"] = Motocicleta("Yamaha", "MT-07", 7000, 689)
root["moto2"] = Motocicleta("Honda", "CB500F", 6500, 471)
root["moto3"] = Motocicleta("Yamaha", "Z900", 9000, 948)

transaction.commit()


# Recuperamso la segunda motocicleta
motocicletas = root.get("moto2")
if motocicletas:
    print("Antes de modificar ")
    print(f"Marca: {motocicletas.marca} , Modelo:{motocicletas.modelo}")

    # Modificar el modelo
    motocicletas.modelo = "TTY-90"
    transaction.commit()  # Confirmamos cambios
    print("Después de la modificación: ")
    print(f"Marca: {motocicletas.marca} , Modelo:{motocicletas.modelo}")

else:
    print("La motocicleta no se encontro en la base de datos")


# Cerrar la conexión
connection.close()
db.close()
storage.close()
