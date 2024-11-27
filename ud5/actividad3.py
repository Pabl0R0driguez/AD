from pymongo import MongoClient, errors

# Datos de conexión
usuario = "usuario"
clave = "usuario"
base_datos = "2dam"
host = "localhost"
puerto = 27017

try:
      # Conexión al servidor MongoDB
      client = MongoClient(
            f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}",
            serverSelectionTimeoutMS=5000
      )

      # Seleccionar la base de datos y la colección motocicletas
      db = client[base_datos]
      coleccion_motocicletas = db["motocicletas"]

      print("Conexión exitosa a la base de datos.")

      # Borrar todos los objetos de la colección
      # Con esto conseguimos que no se nos acumulen las motociletas en la base de datos
      coleccion_motocicletas.delete_many({})
      print("\nSe han eliminado todos los objetos de la colección motocicletas.")

      # 1. Añadir tres objetos a la colección
      nuevas_motocicletas = [
            {"marca": "BMW", "cilindrada": 1000, "precio": 12000},
            {"marca": "Ducati", "cilindrada": 850, "precio": 9500},
            {"marca": "Harley-Davidson", "cilindrada": 1200, "precio": 15000}
      ]
      resultado = coleccion_motocicletas.insert_many(nuevas_motocicletas)
      print("\nSe han añadido las siguientes motocicletas: ")
      for moto in nuevas_motocicletas:
            print(moto)


      # 2. Actualizar un campo de un solo documento
       # Filtro para encontrar la motocicleta BMW
      filtro_actualizacion = {"marca": "BMW"} 

       # Establecemos un nuevo precio
      nuevos_valores = {"$set": {"precio": 12500}} 
      resultado = coleccion_motocicletas.update_one(filtro_actualizacion, nuevos_valores)
      if resultado.modified_count > 0:
            print("\nEl precio de la motocicleta BMW se ha actualizado con éxito.")
            
            #Imprimimos solo la motocicleta actualizada
            moto_actualizada = coleccion_motocicletas.find_one(filtro_actualizacion)
            print("Motocicleta actualizada:", moto_actualizada)
      else:
            print("No se encontró la motocicleta BMW o no hubo cambios.")

      
            
      # 3. Eliminar un documento
      filtro_eliminacion = {"marca": "Ducati"} 
      resultado = coleccion_motocicletas.delete_one(filtro_eliminacion)
      if resultado.deleted_count > 0:
            print("\nLa motocicleta Ducati se ha eliminado con éxito.")
      else:
            print("No se encontró la motocicleta Ducati para eliminar.")

      # Verificar el estado final de la colección
      print("Motocicletas restantes en la colección:")
      motocicletas_restantes = coleccion_motocicletas.find()
      for moto in motocicletas_restantes:
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
