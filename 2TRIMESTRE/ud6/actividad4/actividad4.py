import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "databasemanager_motocicletas.log"
        ),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ],
)


class DatabaseManagerMotocicletas:
    def __init__(self, uri, database_name, collection_name):
        """Inicializa el componente DatabaseManagerMotocicletas."""
        self.uri = uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def conectar(self):
        """Conectar a la base de datos MongoDB"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            logging.info(
                f"Conectado a MongoDB: {self.database_name}.{self.collection_name}"
            )
        except PyMongoError as e:
            logging.error(f"Error al conectar a MongoDB: {e}")

    def desconectar(self):
        """Cerrar la conexión a MongoDB"""
        if self.client:
            self.client.close()
            logging.info("Conexión a MongoDB cerrada.")

    def crear_documento(self, documento):
        """Insertar un nuevo documento en la colección"""
        try:
            result = self.collection.insert_one(documento)
            logging.info(f"Documento insertado con ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            logging.error(f"Error al insertar el documento: {e}")

    def leer_documentos(self, filtro={}):
        """Leer documentos de la colección según un filtro"""
        try:
            documentos = list(self.collection.find(filtro))
            logging.info(f"Documentos recuperados: {len(documentos)}")
            for doc in documentos:
                logging.info(doc)
            return documentos
        except PyMongoError as e:
            logging.error(f"Error al leer los documentos: {e}")
            return []

    def actualizar_documento(self, filtro, actualizacion):
        """Actualizar un documento en la colección"""
        try:
            result = self.collection.update_one(filtro, {"$set": actualizacion})
            if result.modified_count > 0:
                logging.info(f"Documento actualizado: {filtro}")
            else:
                logging.warning(f"No se encontró documento para actualizar: {filtro}")
        except PyMongoError as e:
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

    def iniciar_transaccion(self):
        """Iniciar una transacción"""
        try:
            self.session = self.client.start_session()
            self.session.start_transaction()
            logging.info("Transacción iniciada.")
        except PyMongoError as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirmar (commit) una transacción"""
        try:
            if self.session:
                self.session.commit_transaction()
                logging.info("Transacción confirmada.")
        except PyMongoError as e:
            logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revertir (rollback) una transacción"""
        try:
            if self.session:
                self.session.abort_transaction()
                logging.info("Transacción revertida.")
        except PyMongoError as e:
            logging.error(f"Error al revertir la transacción: {e}")


# Ejemplo de uso del componente DatabaseManagerMotocicletas
if __name__ == "__main__":
    # Configurar el componente
    db_manager = DatabaseManagerMotocicletas(
        uri="mongodb://localhost:27017",
        database_name="1dam",
        collection_name="motocicletas",
    )
    db_manager.conectar()

    try:
        # Crear documentos dentro de una transacción
        db_manager.iniciar_transaccion()
        db_manager.crear_documento(
            {
                "marca": "Honda",
                "cilindrada": "500cc",
                "precio": 7500,
                "año": 2023,
            }
        )
        db_manager.crear_documento(
            {
                "marca": "Yamaha",
                "cilindrada": "689cc",
                "precio": 8500,
                "año": 2022,
            }
        )
        db_manager.confirmar_transaccion()

        # Leer todos los documentos
        db_manager.leer_documentos()

        # Actualizar un documento
        db_manager.iniciar_transaccion()
        db_manager.actualizar_documento({"marca": "Honda"}, {"precio": 7800})
        db_manager.confirmar_transaccion()

        # Eliminar un documento
        db_manager.iniciar_transaccion()
        db_manager.eliminar_documento({"marca": "Yamaha"})
        db_manager.confirmar_transaccion()

    except Exception as e:
        logging.error(f"Error general: {e}")
        db_manager.revertir_transaccion()

    finally:
        db_manager.desconectar()
