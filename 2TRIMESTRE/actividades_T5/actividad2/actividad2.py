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
    # Seleccionar la base de datos
    db = client[base_datos]
    # Consultar las series del género comedia
    series_comedia = db.series.find({"género": "Comedia"})
    print("Series de Comedia:")
    for serie in series_comedia:
        print(serie)
    # Proyectar solo dos campos (nombre y canal) excluyendo _id
    series_proyectadas = db.series.find(
        {"género": "Comedia"},
        {"_id": 0, "nombre": 1, "canal": 1}
    )
    print("\nSeries de Comedia (proyección de campos):")
    for serie in series_proyectadas:
        print(serie)
    # Limitar a 2 resultados y ordenar por nombre en orden alfabético ascendente
    series_limitadas = db.series.find(
        {"género": "Comedia"},
        {"_id": 0, "nombre": 1, "canal": 1}
    ).sort("nombre", 1).limit(2)
    print("\nSeries de Comedia (proyección, orden y límite):")
    for serie in series_limitadas:
        print(serie)
except errors.ServerSelectionTimeoutError as err:
    print(f"No se pudo conectar a MongoDB: {err}")
except errors.OperationFailure as err:
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")
except Exception as err:
    print(f"Ocurrió un error inesperado: {err}")
finally:
    # Cerrar la conexión si se estableció correctamente
    if 'client' in locals():
        client.close()
        print("Conexión cerrada.")
