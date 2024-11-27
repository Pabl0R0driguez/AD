import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent
from peewee import fn

# Establecer conexión a la base de datos
storage = ZODB.FileStorage.FileStorage("2dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()


# Definir clase Motocicleta
class Motocicleta(Persistent):
    def __init__(self, marca, modelo, precio, cilindrada, id_cliente):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.cilindrada = cilindrada
        self.id_cliente = id_cliente  # ID del cliente


# Definir clase Cliente
class Cliente(Persistent):
    def __init__(self, nombre_cliente, numero_telefono):
        self.nombre_cliente = nombre_cliente
        self.numero_telefono = numero_telefono


# Verificar y crear colecciones si no existen
if "motocicletas" not in root:
    root["motocicletas"] = {} #Creamos diccionario motocicletas

if "clientes" not in root:
    root["clientes"] = {} #Creamos diccionario de clientes

# Insertar datos en Clientes
root["clientes"]["Pepe"] = Cliente("Pepe", "645234567")
root["clientes"]["Messi"] = Cliente("Messi", "78904631")

# Insertar motocicletas en la colección de Motocicletas
root["motocicletas"]["Honda"] = Motocicleta("Honda", "CB500X", 7000, "500cc", "Messi")
root["motocicletas"]["Yamaha"] = Motocicleta("Yamaha", "MT-07", 7500, "689cc", "Pepe")
root["motocicletas"]["Kawasaki"] = Motocicleta("Kawasaki", "Ninja 400", 5000, "400cc", "Messi")
#Guardamos los cambios
transaction.commit()


# Función para listar las motocicletas actuales en la base de datos
def listar_motocicletas():
    print("Listando motocicletas en la base de datos:")
    for key, moto in root["motocicletas"].items():
        print(
            f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}"
        )
    






# Llamar a la función para listar todas las motocicletas
listar_motocicletas()

# Filtrar motocicletas por un cliente específico, en este caso Cliente 1

# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()