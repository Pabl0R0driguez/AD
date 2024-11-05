import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent


# Definición de la clase Movil
class Movil(Persistent):
    def __init__(self, marca, modelo, anio_lanzamiento, sistema_operativo):
        super().__init__()  # Llama al constructor de Persistent
        self.marca = marca
        self.modelo = modelo
        self.anio_lanzamiento = anio_lanzamiento
        self.sistema_operativo = sistema_operativo


# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage("moviles.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Inicializa la raíz si está vacía
if not hasattr(root, "moviles"):
    root.moviles = {}  # Inicializa el diccionario si no existe

# Crea 'movil1' solo si no existe
if "movil1" not in root.moviles:
    # Crea y almacena el objeto 'movil1' con iOS
    root.moviles["movil1"] = Movil("Apple", "iPhone 14", 2022, "iOS")
    transaction.commit()  # Asegúrate de guardar el objeto la primera vez
    print("Objeto 'movil1' creado en la base de datos con iOS.")
else:
    # Recuperar el objeto existente
    movil1 = root.moviles["movil1"]
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
