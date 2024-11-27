import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent



#Definimos la clase Motocicleta
class Motocicleta(Persistent):
      def __init__(self,marca, modelo, precio, cilindrada):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.cilindrada = cilindrada 


# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage("2dam.fs")  # Almacenamiento en archivo
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()  # Diccionario raíz para acceder a los objetos almacenados


# Almacenar tres motocicletas
root["moto1"] = Motocicleta("Yamaha", "MT-07", 9000, 689)
root["moto2"] = Motocicleta("Honda", "CB500F", 6500, 471)
root["moto3"] = Motocicleta("Yamaha", "Z900", 6000, 948)

#Confirmamos los cambios
transaction.commit()


#Filtrar por precio
precio_filtrar = 9000
for clave, motocicletas in root.items():
    if hasattr (motocicletas,"precio") and motocicletas.precio == precio_filtrar:
        print(
            f"Marca: {motocicletas.marca}, Modelo: {motocicletas.modelo}, Precio: {motocicletas.precio }, Cilindrada: {motocicletas.cilindrada}"
        )

# Cerrar la conexión y la base de datos
connection.close()
db.close()
storage.close
