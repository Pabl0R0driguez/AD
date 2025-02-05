import json
from pymongo import MongoClient, errors


def insertar_json_en_mongo(client, base_datos, ruta_json, coleccion_nombre):
    try:
        # Seleccionar base de datos y colección
        db = client[base_datos]
        coleccion = db[coleccion_nombre]

        # Leer archivo JSON
        with open(ruta_json, mode="r", encoding="utf-8") as archivo:
            datos = json.load(
                archivo
            )  # Cargar el archivo JSON como una lista de diccionarios

            # Verificar que los datos sean una lista
            if isinstance(datos, list):
                # Insertar datos en la colección
                if datos:
                    coleccion.insert_many(datos)  # Inserta múltiples documentos
                    print(
                        f"Se insertaron {len(datos)} documentos en la colección '{coleccion_nombre}'."
                    )
                else:
                    print("El archivo JSON está vacío o no tiene datos válidos.")
            else:
                print("El archivo JSON no contiene una lista de objetos.")

    except Exception as e:
        print(f"Error al procesar el archivo JSON o insertar datos: {e}")


### Conexión a MongoDB
try:
    # Parámetros de conexión
    usuario = "usuario"
    clave = "usuario"
    host = "localhost"
    puerto = 27017
    base_datos = "1dam"
    ruta_json = "archivo.json"  # Ruta del archivo JSON
    coleccion_nombre = "JSON"  # Nombre de la colección en MongoDB

    # Crear cliente MongoDB
    client = MongoClient(
        f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}",
        serverSelectionTimeoutMS=5000,
    )

    # Verificar conexión
    db = client[base_datos]
    print("Conexión a MongoDB exitosa.")

    # Llamar a la función para insertar datos
    insertar_json_en_mongo(client, base_datos, ruta_json, coleccion_nombre)

except errors.ServerSelectionTimeoutError as err:
    print("No se pudo conectar a MongoDB. Verifica los datos de conexión.")
    print(f"Error: {err}")

except Exception as e:
    print(f"Error inesperado: {e}")

finally:
    # Cerrar conexión al cliente MongoDB
    client.close()
    print("Conexión a MongoDB cerrada.")
