import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent


# Definición de la clase Movil
class Movil(Persistent):
    def __init__(self, marca, modelo, anio_lanzamiento, sistema_operativo):
        super().__init__()  # Asegúrate de llamar al constructor de Persistent
        self.marca = marca
        self.modelo = modelo
        self.anio_lanzamiento = anio_lanzamiento
        self.sistema_operativo = sistema_operativo


# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage("moviles.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Inicializa el diccionario 'moviles' en la raíz si no existe
if "moviles" not in root:
    root["moviles"] = {}

# Crea 'movil1' solo si no existe
if "movil1" not in root["moviles"]:
    root["moviles"]["movil1"] = Movil("Apple", "iPhone 14", 2022, "iOS")
    root["moviles"]["movil2"] = Movil("Samsung", "Galaxy S22", 2022, "Android")
    transaction.commit()  # Asegúrate de guardar los objetos
    print("Objetos 'movil1' y 'movil2' creados en la base de datos.")
else:
    # Recuperar el objeto existente
    movil1 = root["moviles"]["movil1"]
    print("Antes de la modificación:")
    print(
        f"Marca: {movil1.marca}, Modelo: {movil1.modelo}, Año de lanzamiento: {movil1.anio_lanzamiento}, Sistema Operativo: {movil1.sistema_operativo}"
    )

    # Modificar el atributo 'sistema_operativo'
    movil1.sistema_operativo = "Android raro"
    transaction.commit()  # Confirmar los cambios en la base de datos
    print("Después de la modificación:")
    print(
        f"Marca: {movil1.marca}, Modelo: {movil1.modelo}, Año de lanzamiento: {movil1.anio_lanzamiento}, Sistema Operativo: {movil1.sistema_operativo}"
    )

# Cerrar la conexión
connection.close()
db.close()
