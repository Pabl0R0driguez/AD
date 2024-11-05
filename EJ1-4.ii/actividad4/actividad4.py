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


# Función para gestionar la insercción de varias motocicletas con transacciçon
def agregar_motocicletas():
    try:
        print("Iniciando la transacción para agregar motocicletas...")

        # Verificar y crear 'motocicletas' en root si no existe
        if "motocicletas" not in root:
            root["motocicletas"] = (
                {}
            )  # Inicializar una colección de motocicletas si no existe
            transaction.commit()  # Confirmar la creación en la base de datos

            # Crear y añadir nuevas motocicletas
            moto1 = Motocicleta("Honda", "CB500X", "500cc", 7000)
            moto2 = Motocicleta("Yamaha", "MT-07", "689cc", 7500)
            moto3 = Motocicleta("Kawasaki", "Ninja 400", "400cc", 5000)

            # Añadir motocicletas a la colección en la raíz de ZODB
            root["motocicletas"]["CB500X"] = moto1
            root["motocicletas"]["MT-07"] = moto2
            root["motocicletas"]["Ninja 400"] = moto3

            # Confirmar la transacción
            transaction.commit()
            print("Transacción completada: Motocicletas añadidas correctamente.")

    except Exception as e:
        # Si ocurre un error, revertimos la transacción
        transaction.abort()
        print(f"Error durante la transacción: {e}. Transacción revertida.")


# Llamar a la función para añadir motocicletas
agregar_motocicletas()

# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()
