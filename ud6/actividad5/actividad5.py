import logging
import transaction
from ZODB import DB, FileStorage
from persistent import Persistent

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "databasemanager_object.log"
        ),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ],
)


class Motocicleta(Persistent):
    """Clase que representa una motocicleta."""

    def __init__(self, marca, cilindrada, precio):
        self.marca = marca
        self.cilindrada = cilindrada
        self.precio = precio


class DatabaseManagerObject:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""

    def __init__(self, filepath="1dam.fs"):
        self.filepath = filepath
        self.db = None
        self.connection = None
        self.root = None
        self.transaccion_iniciada = False

    def conectar(self):
        """Conecta a la base de datos ZODB."""
        try:
            storage = FileStorage.FileStorage(self.filepath)
            self.db = DB(storage)
            self.connection = self.db.open()
            self.root = self.connection.root()
            if "motocicletas" not in self.root:
                self.root["motocicletas"] = {}
                transaction.commit()
            logging.info("Conexión establecida con ZODB.")
        except Exception as e:
            logging.error(f"Error al conectar a ZODB: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        try:
            if self.connection:
                self.connection.close()
            if self.db:
                self.db.close()
            logging.info("Conexión a ZODB cerrada.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión a ZODB: {e}")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        try:
            transaction.begin()
            self.transaccion_iniciada = True
            logging.info("Transacción iniciada.")
        except Exception as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirma la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.commit()
                self.transaccion_iniciada = False
                logging.info("Transacción confirmada.")
            except Exception as e:
                logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.abort()
                self.transaccion_iniciada = False
                logging.info("Transacción revertida.")
            except Exception as e:
                logging.error(f"Error al revertir la transacción: {e}")

    def crear_motocicleta(self, id, marca, cilindrada, precio):
        """Crea y almacena una nueva motocicleta."""
        try:
            if id in self.root["motocicletas"]:
                raise ValueError(f"Ya existe una motocicleta con ID {id}.")
            self.root["motocicletas"][id] = Motocicleta(marca, cilindrada, precio)
            logging.info(f"Motocicleta con ID {id} creada exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear la motocicleta con ID {id}: {e}")

    def leer_motocicletas(self):
        """Lee y muestra todas las motocicletas almacenadas."""
        try:
            motocicletas = self.root["motocicletas"]
            for id, motocicleta in motocicletas.items():
                logging.info(
                    f"ID: {id}, Marca: {motocicleta.marca}, Cilindrada: {motocicleta.cilindrada}, Precio: {motocicleta.precio}"
                )
            return motocicletas
        except Exception as e:
            logging.error(f"Error al leer las motocicletas: {e}")

    def actualizar_motocicleta(self, id, marca, cilindrada, precio):
        """Actualiza los atributos de una motocicleta."""
        try:
            motocicleta = self.root["motocicletas"].get(id)
            if not motocicleta:
                raise ValueError(f"No existe una motocicleta con ID {id}.")
            motocicleta.marca = marca
            motocicleta.cilindrada = cilindrada
            motocicleta.precio = precio
            logging.info(f"Motocicleta con ID {id} actualizada exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar la motocicleta con ID {id}: {e}")

    def eliminar_motocicleta(self, id):
        """Elimina una motocicleta por su ID."""
        try:
            if id not in self.root["motocicletas"]:
                raise ValueError(f"No existe una motocicleta con ID {id}.")
            del self.root["motocicletas"][id]
            logging.info(f"Motocicleta con ID {id} eliminada exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar la motocicleta con ID {id}: {e}")


if __name__ == "__main__":
    manager = DatabaseManagerObject()
    manager.conectar()

    try:
        # 1) Crear motocicletas con transacción
        manager.iniciar_transaccion()
        manager.crear_motocicleta(1, "Yamaha", 600, 12000)
        manager.crear_motocicleta(2, "Honda", 750, 15000)
        manager.crear_motocicleta(3, "Kawasaki", 1000, 18000)
        manager.confirmar_transaccion()

        # 2) Mostrar todos los objetos
        manager.leer_motocicletas()

        # 3) Intentar insertar un objeto con un ID ya creado, controlado con transacciones
        manager.iniciar_transaccion()
        manager.crear_motocicleta(
            1, "Suzuki", 800, 14000
        )  # Intentar crear un ID duplicado
        manager.confirmar_transaccion()

        # 4) Mostrar todos los objetos nuevamente
        manager.leer_motocicletas()

        # 5) Actualiza un objeto cambiando cualquier atributo, controlado con transacciones
        manager.iniciar_transaccion()
        manager.actualizar_motocicleta(
            1, "Yamaha", 650, 11500
        )  # Cambiar cilindrada y precio
        manager.confirmar_transaccion()

        # 6) Mostrar todos los objetos
        manager.leer_motocicletas()

        # 7) Elimina un objeto con id que no exista, controlado con transacciones
        manager.iniciar_transaccion()
        manager.eliminar_motocicleta(99)  # Intentar eliminar un ID que no existe
        manager.confirmar_transaccion()

        # 8) Mostrar todos los objetos
        manager.leer_motocicletas()

    except Exception as e:
        logging.error(f"Error general: {e}")
        manager.revertir_transaccion()

    finally:
        manager.desconectar()
