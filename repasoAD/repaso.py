import csv
import mysql.connector
from mysql.connector import Error

# Establecer la conexión a la base de datos directamente fuera de la clase
try:
    connection = mysql.connector.connect(
        host="localhost",  # Conexión al servidor local de MySQL
        user="usuario",  # Usuario de MySQL
        password="usuario",  # Contraseña del usuario
        database="2DAM"  # Nombre de la base de datos
    )
    if connection.is_connected():
        print("Conexión a MySQL exitosa.")
except Error as e:
    print(f"Error de conexión: {e}")
    connection = None

class CSVToMySQL:
    def __init__(self, connection):
        self.connection = connection  # Recibe la conexión como parámetro

    def insert_csv_to_mysql(self, csv_file, table):
        if not self.connection or not self.connection.is_connected():
            print("No se pudo establecer conexión con MySQL.")
            return

        try:
            # Leer el archivo CSV
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                cursor = self.connection.cursor()

                # Insertar cada fila en la tabla de MySQL
                for row in csv_reader:
                    columns = ', '.join(row.keys())
                    values = ', '.join(['%s'] * len(row))
                    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
                    cursor.execute(insert_query, tuple(row.values()))

            self.connection.commit()
            print(f"Datos insertados en la tabla '{table}'.")

        except Exception as e:
            print(f"Error al insertar datos en MySQL: {e}")

        finally:
            cursor.close()

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")

# Uso del código
if connection:  # Solo si la conexión fue exitosa
    db = CSVToMySQL(connection)  # Pasar la conexión al constructor de la clase
    db.insert_csv_to_mysql(csv_file="leerfich_basedatos.csv", table="motocicletas")
    db.close_connection()

