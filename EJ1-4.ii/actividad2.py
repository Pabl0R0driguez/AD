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
# Filtrar herramientas por marca
marca1 = "Yamaha"
for clave, motocicletas in root.items():
    if hasattr(motocicletas, "marca") and motocicletas.marca == marca1:
        print(
            f"Marca: {motocicletas.marca}, Modelo: {motocicletas.modelo}, Precio: {motocicletas.
precio }, Cilindrada: {motocicletas.cilindrada}"
        )

# Cerrar la conexión
connection.close()
db.close()
storage.close()
