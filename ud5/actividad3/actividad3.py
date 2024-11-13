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

      # Seleccionar la colección motocicletas (o la colección de tu elección)
      coleccion_motocicletas = db["motocicletas"]


      motocicletas_restantes = coleccion_motocicletas.find()
      for moto in motocicletas_restantes:
            print(moto)

      # 1. Añadir tres documentos a la colección
      motocicletas_nuevas = [
            {"marca": "BMW", "cilindrada": 1000, "precio": 12000},
            {"marca": "Ducati", "cilindrada": 850, "precio": 9500},
            {"marca": "Harley-Davidson", "cilindrada": 1200, "precio": 15000}
      ]
      
      # Insertar los documentos
      resultado = coleccion_motocicletas.insert_many(motocicletas_nuevas)
      print("IDs de documentos insertados:", resultado.inserted_ids)

      # 2. Actualizar un campo de un solo documento
      # Actualizar el precio de la motocicleta de BWM
      resultado = coleccion_motocicletas.update_one(
            # Filtro para encontrar el documento
            {"marca": "BMW"},  
            # Actualizar el precio
            {"$set": {"precio": 12500}} 
      )
      if resultado.modified_count > 0:
            print("Documento modificado con éxito.")
      else:
            print("No se encontró el documento o no hubo cambios.")

      # 3. Eliminar un documento
      # Eliminar la motocicleta de Ducati
      resultado = coleccion_motocicletas.delete_one({"marca": "Ducati"})
      if resultado.deleted_count > 0:
            print("Documento eliminado con éxito.")
      else:
            print("No se encontró el documento para eliminar.")

      # Verificar el estado final de la colección
      print("\nObjetos restantes en la colección motocicletas:")
      motocicletas_restantes = coleccion_motocicletas.find()
      for moto in motocicletas_restantes:
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
