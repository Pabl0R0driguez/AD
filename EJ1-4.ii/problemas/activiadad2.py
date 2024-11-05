import transaction
from ZODB import FileStorage, DB
from persistent import Persistent


# Definición de la clase Movil
class Movil(Persistent):
    def __init__(self, marca, modelo, anio_lanzamiento, sistema_operativo):
        super().__init__()  # Llamar al constructor de Persistent
        self.marca = marca
        self.modelo = modelo
        self.anio_lanzamiento = anio_lanzamiento
        self.sistema_operativo = sistema_operativo


# Configuración de la base de datos
storage = FileStorage.FileStorage("moviles.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

# Inicializa la raíz si está vacía
if not hasattr(root, "moviles"):
    root.moviles = {}


# Almacenar varios objetos Movil
def almacenar_moviles():
    # Solo crear nuevos móviles si no existen
    if "movil1" not in root.moviles:
        root.moviles["movil1"] = Movil("Apple", "iPhone 14", 2022, "iOS")
    if "movil2" not in root.moviles:
        root.moviles["movil2"] = Movil("Samsung", "Galaxy S22", 2022, "Android")
    if "movil3" not in root.moviles:
        root.moviles["movil3"] = Movil("Xiaomi", "Redmi Note 11", 2022, "Android")

    # Confirmar los cambios
    transaction.commit()


# Consultar objetos Movil
def consultar_moviles(sistema_operativo_filtro):
    print(f"Moviles con sistema operativo {sistema_operativo_filtro}:")
    for key in root.moviles.keys():
        movil = root.moviles[key]
        # Verifica si el objeto tiene el atributo 'sistema_operativo' y filtra
        if (
            hasattr(movil, "sistema_operativo")
            and movil.sistema_operativo == sistema_operativo_filtro
        ):
            print(
                f"Marca: {movil.marca}, Modelo: {movil.modelo}, Año: {movil.anio_lanzamiento}, SO: {movil.sistema_operativo}"
            )


# Función principal
def main():
    almacenar_moviles()
    consultar_moviles(
        "Android"
    )  # Cambia "Android" por "iOS" si deseas consultar los móviles de Apple


# Ejecuta el programa
if __name__ == "__main__":
    main()

# Cierra la conexión
connection.close()
db.close()
