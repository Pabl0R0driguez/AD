import logging
import mysql.connector
from mysql.connector import Error

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager.log"),
        logging.StreamHandler(),  # Logs también en consola
    ],
)


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def conectar(self):
        # Conectar a la base de datos MySQL
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                logging.info("Conexión exitosa a la base de datos.")
        except Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        # Cerrar la conexión a la base de datos
        if self.connection.is_connected():
            self.connection.close()
            logging.info("Conexión cerrada.")

    def crear_motocicleta(self, marca, modelo, cilindrada, precio):
        # Insertar una nueva motocicleta en la base de datos
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO motocicletas (marca, modelo, cilindrada, precio)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (marca, modelo, cilindrada, precio))
            logging.info(f"Motocicleta '{marca} {modelo}' insertada exitosamente.")
        except Error as e:
            logging.error(f"Error al insertar la motocicleta '{marca} {modelo}': {e}")

    def leer_motocicletas(self):
        # Leer todas las motocicletas de la base de datos
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM motocicletas")
            motocicletas = cursor.fetchall()
            logging.info("Motocicletas recuperadas:")
            for moto in motocicletas:
                logging.info(moto)
            return motocicletas
        except Error as e:
            logging.error(f"Error al leer las motocicletas: {e}")
            return None

    def actualizar_motocicleta(self, id, marca, modelo, cilindrada, precio):
        # Actualizar una motocicleta en la base de datos
        try:
            cursor = self.connection.cursor()
            query = """
            UPDATE motocicletas
            SET marca = %s, modelo = %s, cilindrada = %s, precio = %s
            WHERE id = %s
            """
            cursor.execute(query, (marca, modelo, cilindrada, precio, id))
            self.connection.commit()
            logging.info(f"Motocicleta con ID {id} actualizada exitosamente.")
        except Error as e:
            logging.error(f"Error al actualizar la motocicleta con ID {id}: {e}")

    def eliminar_motocicleta(self, id):
        # Eliminar una motocicleta de la base de datos
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM motocicletas WHERE id = %s"
            cursor.execute(query, (id,))
            self.connection.commit()
            logging.info(f"Motocicleta con ID {id} eliminada exitosamente.")
        except Error as e:
            logging.error(f"Error al eliminar la motocicleta con ID {id}: {e}")


# Ejemplo de uso del componente DatabaseManager
if __name__ == "__main__":
    # Conectar con la base de datos 2dam
    db_manager = DatabaseManager("localhost", "usuario", "usuario", "1dam")
    db_manager.conectar()

    # Operaciones CRUD en la tabla motocicletas

    # Crear una nueva motocicleta
    db_manager.crear_motocicleta("Yamaha", "YZF-R3", 321, 5500)

    # Leer todas las motocicletas
    motocicletas = db_manager.leer_motocicletas()

    # Actualizar una motocicleta
    db_manager.actualizar_motocicleta(1, "Kawasaki", "Ninja 400", 399, 7000)

    # Eliminar una motocicleta
    db_manager.eliminar_motocicleta(1)

    # Desconectar de la base de datos
    db_manager.desconectar()
