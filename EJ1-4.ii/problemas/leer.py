# Script para verificar el contenido de la base de datos
import ZODB, ZODB.FileStorage

# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage("moviles.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Listar todos los objetos en la base de datos
if "moviles" in root:
    for key, movil in root["moviles"].items():
        print(
            f"Key: {key}, Marca: {movil.marca}, Modelo: {movil.modelo}, Año: {movil.anio_lanzamiento}, SO: {movil.sistema_operativo}"
        )
else:
    print("No hay móviles en la base de datos.")

# Cerrar la conexión
connection.close()
db.close()
