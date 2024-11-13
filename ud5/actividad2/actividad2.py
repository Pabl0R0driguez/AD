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


    # Listar todos los documentos de la colección
    motocicletas = coleccion_motocicletas.find()
    print("Objetos en la colección motocicletas:")
    for moto in motocicletas:
        print(moto)

    # 1.Motocicletas con cilindrada mayor a 500
    consulta = {"cilindrada": {"$gt": 500}}
    motocicletas = coleccion_motocicletas.find(consulta)

    print("\nMotocicletas con cilindrada mayor a 500 cc:")
    for moto in motocicletas:
        print(moto)

    # 2.Consultas con proyección mostrar solo marca y precio, excluyendo '_id'
    # Dentro del find metemos {} para que nos cojan todas las motocicletas de nuestra colección
    proyeccion = {"_id": 0, "marca": 1, "precio": 1}
    motocicletas_proyectadas = coleccion_motocicletas.find({}, proyeccion)

    print("\nConsulta con proyección mostrar solo marca y precio:")
    for moto in motocicletas_proyectadas:
        print(moto)

    # 3.Motocicletas limitadas y ordenadas por precio ascendente (de menor a mayor)
    motocicletas_limitadas = coleccion_motocicletas.find({}, proyeccion).sort("precio", 1).limit(2)

    print("\nMotocicletas limitadas y ordenadas por precio ascendente:")
    for moto in motocicletas_limitadas:
        print(moto)

except errors.ServerSelectionTimeoutError as err:
    # Este error ocurre si el servidor no está disponible o no se puede conectar
    print(f"No se pudo conectar a MongoDB: {err}")

except errors.OperationFailure as err:
    # Este error ocurre si las credenciales son incorrectas o no se tienen los permisos necesarios
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")

except Exception as err:
    # Manejar cualquier otro error inesperado
    print(f"Ocurrió un error inesperado: {err}")

finally:
    # Cerrar la conexión si se estableció correctamente
    if 'client' in locals():
        client.close()
        print("\nConexión cerrada.")
