import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent

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
    def __init__(self, id_cliente, numero_telefono):
        self.id_cliente = id_cliente
        self.numero_telefono = numero_telefono


# Verificar y crear colecciones si no existen
if "motocicletas" not in root:
    root["motocicletas"] = {}

if "clientes" not in root:
    root["clientes"] = {}

# Insertar datos en Clientes
root["clientes"]["Cliente 1"] = Cliente("Cliente 1", "645234567")
root["clientes"]["Cliente 2"] = Cliente("Cliente 2", "78904631")

# Insertar motocicletas en la colección de Motocicletas
root["motocicletas"]["Honda"] = Motocicleta("Honda", "CB500X", 7000, "500cc", "Cliente 1")
root["motocicletas"]["Yamaha"] = Motocicleta("Yamaha", "MT-07", 7500, "689cc", "Cliente 2")
root["motocicletas"]["Kawasaki"] = Motocicleta("Kawasaki", "Ninja 400", 5000, "400cc", "Cliente 1")
transaction.commit()


# Función para listar las motocicletas actuales en la base de datos
def listar_motocicletas():
    print("Listando motocicletas en la base de datos:")
    for key, moto in root["motocicletas"].items():
        print(
            f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}, ID Cliente: {moto.id_cliente}"
        )
    



# Función para filtrar motocicletas de un cliente específico usando root.items()
def filtrar_motocicletas_por_cliente(id_cliente):
    print("\n")
    print(f"Mostrando motocicletas usadas por '{id_cliente}':")
    for key, motocicletas in root.items():
        # Verificar si estamos en la colección de motocicletas
        if key == "motocicletas":
            for moto_clave, moto in motocicletas.items():
                if moto.id_cliente == id_cliente:
                    print(
                        f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}, ID Cliente: {moto.id_cliente}"
                    )


# Llamar a la función para listar todas las motocicletas
listar_motocicletas()

# Filtrar motocicletas por un cliente específico, en este caso Cliente 1
filtrar_motocicletas_por_cliente("Cliente 1")

# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()
