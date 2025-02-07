import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "databasemanager_productos.log"
        ),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ],
)


class ProductManager:
    def __init__(self, uri, db_name="1dam", collection_name="productos"):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.collection_name = collection_name

    def conectar(self):
        """Conectar a la base de datos MongoDB"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            logging.info(f"Conectado a MongoDB: {self.db_name}.{self.collection_name}")
        except PyMongoError as e:
            logging.error(f"Error al conectar a MongoDB: {e}")

    def cerrar_conexion(self):
        """Cerrar la conexión a MongoDB"""
        if self.client:
            self.client.close()
            logging.info("Conexión a MongoDB cerrada.")

    # Insertqar producto
    def insertar_productos(self, productos):
        """Insertar un nuevo producto en la colección"""
        try:
            result = self.collection.insert_one(productos)
            logging.info(f"Producto insertado con ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            logging.error(f"Error al insertar el producto: {e}")

    # Consultar proyección y ordenar
    def consultar_proyeccion_ordenada(self, filtro, proyeccion):
        filtro = {"categoria": "auriculares"}
        proyeccion = {"nombre", "precio", "stock"}
        productos = productos.find(filtro, proyeccion)
        productos.find().sort("precio")
        for busqueda in productos:
            print(busqueda)

    # Actualizar producto
    def actualizar_productos(self, filtro, actualizacion):
        """Actualizar un producto en la colección"""
        try:
            result = self.collection.update_one(filtro, {"$set": actualizacion})
            if result.modified_count > 0:
                logging.info(f"Producto actualizado: {filtro}")
            else:
                logging.warning(f"No se encontró producto para actualizar: {filtro}")
        except PyMongoError as e:
            logging.error(f"Error al actualizar el documento: {e}")

    # Mostrar todos los productos
    def mostrar_todos_productos(self):
        """Leer todos los productos de la colección"""
        try:
            productos = list(self.collection.find())
            logging.info(f"Productos recuperados: {len(productos)}")
            for doc in productos:
                logging.info(doc)
            return productos
        except:
            logging.error(f"Error al actualizar el documento: {e}")

    # Eliminar producto
    def eliminar_producto(self, filtro):
        """Eliminar un producto de la colección"""
        try:
            result = self.collection.delete_one(filtro)
            if result.deleted_count > 0:
                logging.info(f"Producto eliminado: {filtro}")
            else:
                logging.warning(f"No se encontró producto para eliminar: {filtro}")
        except PyMongoError as e:
            logging.error(f"Error al eliminar el producto: {e}")


if __name__ == "__main__":
    # Configurar el componente
    db_manager = ProductManager(
        uri="mongodb://localhost:27017",
        db_name="1dam",
        collection_name="productos",
    )
    db_manager.conectar()

    try:

        db_manager.insertar_productos(
            {
                "nombre": "Drone Phantom X",
                "categoria": "Drones",
                "precio": 1200.50,
                "stock": 8,
            }
        )
        db_manager.insertar_productos(
            {
                "nombre": "Auriculares Sonic Boom",
                "categoria": "Auriculares",
                "precio": 299.99,
                "stock": 15,
            }
        )

        db_manager.insertar_productos(
            {
                "nombre": "Cámara Action Pro",
                "categoria": "Cámaras",
                "precio": 499.99,
                "stock": 10,
            }
        )

        db_manager.insertar_productos(
            {
                "nombre": "Asistente SmartBuddy",
                "categoria": "Asistentes Inteligentes",
                "precio": 199.99,
                "stock": 20,
            }
        )

        db_manager.insertar_productos(
            {
                "nombre": "Cargador Solar Ultra",
                "categoria": "Accesorios",
                "precio": 49.99,
                "stock": 3,
            }
        )

        db_manager.mostrar_todos_productos()
        db_manager.actualizar_productos({"nombre": "Drone Phantom X"}, {"precio": 1300})
        db_manager.eliminar_producto({"stock": 3})
        # db_manager.consultar_proyeccion_ordenada()

        db_manager.cerrar_conexion()

    except Exception as e:
        logging.error(f"Error general: {e}")

    finally:
        db_manager.desconectar()
