from pymongo import MongoClient, errors
import logging
# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log_biblioteca.log"), logging.StreamHandler()],
)


# Componente para la conexión a MongoDB
class MongoDBConnection:
    def __init__(self, uri, database_name):
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.db = None

    def conectar(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.database_name]
            logging.info(f"Conexión exitosa a la base de datos {self.database_name}.")
        except errors.ServerSelectionTimeoutError as e:
            logging.error(f"Error al conectar a MongoDB: {e}")
            raise
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
            raise

    def desconectar(self):
        if self.client:
            self.client.close()
            logging.info("Conexión a MongoDB cerrada.")


# Componente para CRUD y gestión de colecciones
class BibliotecaManager:
    def __init__(self, db):
        self.db = db

    def crear_coleccion(self, nombre_coleccion):
        try:
            self.db.create_collection(nombre_coleccion)
            logging.info(f"Colección '{nombre_coleccion}' creada exitosamente.")
        except errors.CollectionInvalid:
            logging.warning(f"La colección '{nombre_coleccion}' ya existe.")

    def eliminar_coleccion(self, nombre_coleccion):
        if nombre_coleccion in self.db.list_collection_names():
            self.db.drop_collection(nombre_coleccion)
            logging.info(f"Colección '{nombre_coleccion}' eliminada.")
        else:
            logging.warning(f"La colección '{nombre_coleccion}' no existe.")

    def insertar_libro(self, coleccion, libro):
        try:
            result = self.db[coleccion].insert_one(libro)
            logging.info(f"Libro insertado con ID: {result.inserted_id}")
        except Exception as e:
            logging.error(f"Error al insertar el libro: {e}")

    def consultar_libros(self, coleccion, filtro=None, proyeccion=None):
        try:
            filtro = filtro or {}
            libros = self.db[coleccion].find(filtro, proyeccion)
            logging.info("Consulta realizada exitosamente.")
            return list(libros)
        except Exception as e:
            logging.error(f"Error al consultar libros: {e}")
            return []

    def actualizar_libro(self, coleccion, filtro, actualizacion):
        try:
            result = self.db[coleccion].update_one(filtro, {"$set": actualizacion})
            if result.modified_count > 0:
                logging.info("Libro actualizado exitosamente.")
            else:
                logging.warning("No se encontró un libro que coincida con el filtro.")
        except Exception as e:
            logging.error(f"Error al actualizar el libro: {e}")

    def eliminar_libros(self, coleccion, filtro):
        try:
            result = self.db[coleccion].delete_many(filtro)
            logging.info(f"{result.deleted_count} libros eliminados.")
        except Exception as e:
            logging.error(f"Error al eliminar libros: {e}")


# Componente para mapeo objeto-relacional
class Libro:
    def __init__(self, titulo, autor, genero, resumen=None):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.resumen = resumen

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "resumen": self.resumen,
        }
# Pruebas e integración de los componentes
if __name__ == "__main__":
    # Conexión a MongoDB
    conexion = MongoDBConnection("mongodb://localhost:27017", "biblioteca_db")
    conexion.conectar()
    db = conexion.db

    # Gestión de la colección
    manager = BibliotecaManager(db)
    coleccion = "libros"
    manager.crear_coleccion(coleccion)

    # Insertar libros
    libro1 = Libro("1984", "George Orwell", "Distopía", "Una novela sobre un régimen totalitario.")
    libro2 = Libro("Cien años de soledad", "Gabriel García Márquez", "Realismo mágico")
    libro3 = Libro("El principito", "Antoine de Saint-Exupéry", "Fábula", "Un niño que vive en un asteroide.")
    
    manager.insertar_libro(coleccion, libro1.to_dict())
    manager.insertar_libro(coleccion, libro2.to_dict())
    manager.insertar_libro(coleccion, libro3.to_dict())

    # Consultar libros
    libros = manager.consultar_libros(coleccion, proyeccion={"_id": 0, "titulo": 1, "autor": 1})
    print("Libros en la colección:")
    for libro in libros:
        print(libro)

    # Actualizar un libro
    manager.actualizar_libro(coleccion, {"titulo": "1984"}, {"resumen": "Actualización del resumen."})

    # Eliminar libros por género
    manager.eliminar_libros(coleccion, {"genero": "Realismo mágico"})

    # Verificar cambios
    libros_actualizados = manager.consultar_libros(coleccion)
    print("Libros después de las operaciones:")
    for libro in libros_actualizados:
        print(libro)

    # Eliminar colección
    manager.eliminar_coleccion(coleccion)

    # Cerrar conexión
    conexion.desconectar()
