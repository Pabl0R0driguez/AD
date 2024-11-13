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


# Función para eliminar todas las motocicletas
def eliminar_motocicletas():
    try:
        # Verificar que existen motocicletas antes de eliminarlas
        if "motocicletas" in root:
            del root["motocicletas"]  # Eliminar todas las motocicletas

            # Confirmar la transacción de eliminación
            transaction.commit()
            print("Transacción completada, motocicletas eliminadas correctamente.")
        else:
            print("No existen motocicletas para eliminar.")
    except Exception as e:
        # Si ocurre un error, revertimos la transacción
        transaction.abort()
        print(f"Error durante la transacción: {e}. Transacción revertida.")
        

# Función para gestionar la insercción de varias motocicletas con transacciçon
def agregar_motocicletas():
    try:
        print("Iniciando la transacción para agregar motocicletas...")

        # Verificar y crear 'motocicletas' en root si no existe
        if "motocicletas" not in root:
            root["motocicletas"] = (
                {}
            )  # Inicializar una colección de motocicletas si no existe
            transaction.commit() 

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
            print("Transacción completada, motocicletas añadidas correctamente.")

    except Exception as e:
        # Si ocurre un error, revertimos la transacción
        transaction.abort()
        print(f"Error durante la transacción: {e}. Transacción revertida.")

def listar_motocicletas():
    print("\nMotocicletas en la base de datos: ")
    for key, moto in root["motocicletas"].items():
            print(f"Marca: {moto.marca}, Modelo: {moto.modelo}, Cilindrada: {moto.cilindrada}, Precio: {moto.precio}")




#Función para eliminar motocicletas con esto conseguimos que nos aparezca el mensaje de transacción completa, ya que borra las que habia antes
eliminar_motocicletas()


# Llamar a la función para añadir las motocicletas
agregar_motocicletas()

# Llamar a la función para listar las motocicletas
listar_motocicletas()


# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()
