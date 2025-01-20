from pymongo import MongoClient, errors
usuario = "usuario"
clave = "usuario"
base_datos = "2DAM"
host = "localhost"
puerto = 27017
try:
    # Intentar conectarse al servidor MongoDB
    client = MongoClient(
        f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}",
        serverSelectionTimeoutMS=5000
    )
    # Seleccionar la base de datos y la colección
    db = client[base_datos]
    coleccion_series = db.series
    # Añadir tres documentos a la colección
    nuevas_series = [{"nombre": "Juego de Tronos", "temporada": "8", "género": "Drama", "canal": "HBO", "puntuación": "9,3"},
        {"nombre": "Rick y Morty", "temporada": "6", "género": "Animada", "canal": "Swim", "puntuación": "9,2"},
        {"nombre": "El Ministerio del Tiempo", "temporada": "4", "género": "Ciencia Ficción", "canal": "TVE", "puntuación": "8,1"}
    ]
    resultado_insertar = coleccion_series.insert_many(nuevas_series)
    print("Series añadidas con éxito:", resultado_insertar.inserted_ids)
    # Actualizar un campo de un sólo documento
    consulta_actualizar = {"nombre": "Rick y Morty"}
    nuevo_valor = {"$set": {"puntuación": "9,5"}}
    resultado_actualizar = coleccion_series.update_one(consulta_actualizar, nuevo_valor)
    print("Documentos actualizados:", resultado_actualizar.modified_count)
    # Eliminar uno de los documentos
    consulta_eliminar = {"nombre": "El Ministerio del Tiempo"}
    resultado_eliminar = coleccion_series.delete_one(consulta_eliminar)
    print("Documentos eliminados:", resultado_eliminar.deleted_count)

except errors.ServerSelectionTimeoutError as err:
    print(f"No se pudo conectar a MongoDB: {err}")
finally:
    # Cerrar la conexión si se estableció correctamente
    if 'client' in locals():
        client.close()
        print("Conexión cerrada.")
