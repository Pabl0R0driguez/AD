from pymongo import MongoClient, errors

# Datos de conexión
usuario = "usuario"
clave = "usuario"
base_datos = "2dam"  # La base de datos que quieres usar
host = "localhost"
puerto = 27017

try:
    # Intentar conectarse al servidor MongoDB usando autenticación
    client = MongoClient(
        f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}",
        serverSelectionTimeoutMS=5000
    )

    # Seleccionar la base de datos
    db = client[base_datos]
    


    # Intentar acceder a la base de datos para verificar la conexión
    colecciones = db.list_collection_names()
    print("Conexión exitosa, colecciones en la bd: ")
    print(colecciones)

    # Seleccionar la colección motocicletas
    coleccion_motocicletas = db["motocicletas"]

# Eliminar todos los documentos de la colección motocicletas
    coleccion_motocicletas.delete_many({})  # Borra todos los documentos
    print("\nTodos los documentos de la colección 'motocicletas' han sido eliminados.")

    
    # Verificar si la colección está vacía
    if coleccion_motocicletas.count_documents({}) == 0:
        print("\nLa colección 'motocicletas' está vacía. Insertando datos de prueba...")
        # Insertar documentos de ejemplo
        coleccion_motocicletas.insert_many([
            {"marca": "Honda", "cilindrada": 500, "precio": 6000},
            {"marca": "Yamaha", "cilindrada": 300, "precio": 4500},
            {"marca": "Kawasaki", "cilindrada": 650, "precio": 7000},
            {"marca": "Suzuki", "cilindrada": 800, "precio": 8000}
        ])
        print("Datos de prueba insertados correctamente.")

    # Listar todas las motocicletas
    print("\nLista de todas las motocicletas:")
    for moto in coleccion_motocicletas.find():
        print(moto)

    # Consultar motocicletas con cilindrada mayor a 500 cc
    consulta_cilindrada = {"cilindrada": {"$gt": 500}}
    motocicletas_cilindrada = coleccion_motocicletas.find(consulta_cilindrada)
    print("\nMotocicletas con cilindrada mayor a 500 cc:")
    for moto in motocicletas_cilindrada:
        print(moto)

    # Proyección: mostrar solo 'marca' y 'precio', excluyendo '_id'
    proyeccion = {"_id": 0, "marca": 1, "precio": 1}
    motocicletas_proyectadas = coleccion_motocicletas.find({}, proyeccion)
    print("\nMotocicletas (proyección de campos 'marca' y 'precio'):")
    for moto in motocicletas_proyectadas:
        print(moto)


    # Limitar a 2 resultados y ordenar por 'precio' en orden ascendente
    motocicletas_ordenadas_limitadas = coleccion_motocicletas.find({}, proyeccion).sort("precio", 1).limit(2)
    print("\nMotocicletas limitadas y ordenadas por precio ascendente:")
    for moto in motocicletas_ordenadas_limitadas:
        print(moto)

    


except errors.ServerSelectionTimeoutError as err:
    print(f"No se pudo conectar a MongoDB: {err}")

except errors.OperationFailure as err:
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")

except Exception as err:
    print(f"Ocurrió un error inesperado: {err}")

finally:
    if 'client' in locals():
        client.close()
        print("\nConexión cerrada.")
