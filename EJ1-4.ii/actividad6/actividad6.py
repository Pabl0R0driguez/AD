import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent
from copy import deepcopy

#Establecer conexión a la base de datos
storage = ZODB.FileStorage.FileStorage("2dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()


#Definir clase Motocicleta
class Motocicleta(Persistent):
    def __init__(self, marca, modelo, precio, cilindrada, cliente):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.cilindrada = cilindrada
        self.cliente = cliente  


#Definir clase Cliente
class Cliente(Persistent):
    def __init__(self, id_cliente, numero_telefono):
        self.id_cliente = id_cliente
        self.numero_telefono = numero_telefono


#Verificar y crear colecciones si no existen
if "motocicletas" not in root:
    root["motocicletas"] = {}

if "clientes" not in root:
    root["clientes"] = {}

#Insertar datos en Clientes
root["clientes"]["Cliente 1"] = Cliente("Cliente 1", "645234567")
root["clientes"]["Cliente 2"] = Cliente("Cliente 2", "78904631")

#Insertar motocicletas en la colección de Motocicletas
root["motocicletas"]["Honda"] = Motocicleta("Honda", "CB500X", 7000, "500cc", root["clientes"]["Cliente 1"])
root["motocicletas"]["Yamaha"] = Motocicleta("Yamaha", "MT-07", 7500, "689cc", root["clientes"]["Cliente 2"])
root["motocicletas"]["Kawasaki"] = Motocicleta("Kawasaki", "Ninja 400", 5000, "400cc", root["clientes"]["Cliente 1"])
transaction.commit()


#Función para listar las motocicletas actuales en la base de datos
def listar_motocicletas():
    print("Listando motocicletas en la base de datos:")
    for key, moto in root["motocicletas"].items():
        print(
            f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}, Cliente: {moto.cliente.id_cliente}"
        )


#Crear una copia profunda de una motocicleta y modificarla
def copiar_y_modificar_motocicleta(marca):
    #Obtener la motocicleta original
    moto_original = root["motocicletas"][marca]

    #Crear una copia de la motocicleta
    #Con esto conseguimos que cualquier cambio en moto_copia no afectara a moto_original
    moto_copia = deepcopy(moto_original)

    #Modificar la copia
    moto_copia.marca = "Suzuki"
    moto_copia.modelo = "GSX-R600"
    moto_copia.precio = 8500
    moto_copia.cilindrada = "9999cc"

    print("\nObjeto original después de la copia:")
    print(f"Marca: {moto_original.marca}, Modelo: {moto_original.modelo}, Precio: {moto_original.precio}, Cilindrada: {moto_original.cilindrada}, Cliente: {moto_original.cliente.id_cliente}")

    print("\nCopia modificada:")
    print(f"Marca: {moto_copia.marca}, Modelo: {moto_copia.modelo}, Precio: {moto_copia.precio}, Cilindrada: {moto_copia.cilindrada} ,Cliente: {moto_copia.cliente.id_cliente}")

    #Verificar que el cliente de la copia sigue siendo el mismo que el del original
    #Modificamos la motocicleta pero manteniendo el mismo cliente
    print("\nVerificación de cliente:")
    print(f"Cliente original: {moto_original.cliente.id_cliente}")
    print(f"Cliente de la copia: {moto_copia.cliente.id_cliente}")


#Llamar a la función para listar todas las motocicletas
listar_motocicletas()

#Copiar y modificar una motocicleta específica
copiar_y_modificar_motocicleta("Honda")

#Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()
