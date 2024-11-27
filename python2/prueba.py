import mysql.connector
from mysql.connector import Error
import csv
import json
import pymysql
from pymysql import Error

try:
    # Establecer conexión con la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
    )
    if conexion.is_connected():
        print("Conexión a MySQL exitosa.")
        
        cursor = conexion.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Libros (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(100),
        autor VARCHAR(100),
        genero VARCHAR(100),
        año_publicacion INT,
        libreria_origen VARCHAR(100)
        );
    """)
        
    print("Tabla 'Libros' creada o ya existe.")

    cursor.execute("""
    INSERT INTO Libros (titulo, autor, genero, año_publicacion,libreria_origen)
    VALUES ("Don Quijote de la Mancha", "Miguel de Cervantes", "Novela", 1605, "Ramón Valle Inclán");
    """)
    
    cursor.execute("""
    INSERT INTO Libros (titulo, autor, genero, año_publicacion,libreria_origen)
    VALUES ("Cien Años de Soledad", "Gabriel García Márquez", "Novela", 1967, "Ramón Valle Inclán");
    """)
    
    cursor.execute("""
    INSERT INTO Libros (titulo, autor, genero, año_publicacion,libreria_origen)
    VALUES ("Crimen y Castigo", "Fiódor Dostoyevski", "Novela", 1866, "Ramón Valle Inclán");
    """)
    
    cursor.execute("""
    INSERT INTO Libros (titulo, autor, genero, año_publicacion,libreria_origen)
    VALUES ("La Casa de los Espíritus", "Isabel Allende", "Novela", 1982, "Ramón Valle Inclán");
    """)
     
    cursor.execute("""
    INSERT INTO Libros (titulo, autor, genero, año_publicacion,libreria_origen)
    VALUES ("El Nombre de la Rosa", "Umberto Eco", "Misterio", 1980, "Ramón Valle Inclán");
    """)
    print("Insertando los libros originales de la Librería Ramón Valle Inclán...")
    
    conexion.commit()
    

except Error as e:
    print(f"Error de conexión: {e}")


class CSVToMySQL:
    def __init__(self, connection):
        self.connection = connection


    def insert_csv_to_mysql(self, csv_file, table):
        if not self.connection or not self.connection.is_connected():
            print("No se pudo establecer conexión con MySQL.")
            return

        try:
            print("Leyendo datos desde el archivo CSV: libros_unamuno.csv")
            # Leer el archivo CSV
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                cursor = self.connection.cursor()
                
                print("Iniciando transacción para insertar libros en la base de datos...")
                for row in csv_reader:
                    columns = ', '.join(row.keys())
                    values = ', '.join(['%s'] * len(row))
                    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
                    
                    cursor.execute(insert_query, tuple(row.values()))
            self.connection.commit()

            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Unamuno', 'Don Quijote de la Mancha'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Unamuno', 'Rayuela'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Unamuno', 'Fahrenheit 451'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Unamuno', 'La Sombra del Viento'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Unamuno', 'Los Miserables'))
                
            conexion.commit()
            
            print("Libreria_origen añadida correctamente")

            print(f"Datos insertados en la tabla '{table}'.")
            
        except Exception as e:
            print(f"Error al insertar datos en MySQL: {e}")
            cursor.rollback()
            print("Se realizó un rollback")
            
        finally:
            cursor.close()
            
        def close_connection(self):
            if self.connection and self.connection.is_connected():
                self.connection.close()
            print("Conexión cerrada.")
            
            
class JSONToMySQL:
    def __init__(self, connection):
        self.connection = connection

    def insert_json_to_mysql(self, json_file, table):
        if not self.connection or not self.connection.is_connected():
            print("No se pudo establecer conexión con MySQL.")
            return

        try:
            print("Leyendo datos desde el archivo JSON: libros_machado.csv")
            # Leer el archivo CSV
            with open(json_file, 'r') as file:
                data = json.load(file)
                
                print("Iniciando transacción para insertar libros en la base de datos...")
                if isinstance(data, dict):
                    data = [data]
                
                # Insertar cada registro en la tabla de MySQL
                for record in data:
                    columns = ', '.join(record.keys())
                    values = ', '.join(['%s'] * len(record))
                    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
                
                cursor.execute(insert_query, tuple(record.values()))
            

            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Machado', 'Cien Años de Soledad'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Machado', 'La Colmena'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Machado', '1984'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Machado', 'El Principito'))
            cursor.execute("UPDATE Libros SET libreria_origen = %s WHERE titulo = %s", ('Machado', 'El Nombre de la Rosa'))
                
            conexion.commit()
            
            print("Libreria_origen añadida correctamente")

            print(f"Datos insertados en la tabla '{table}'.")
            
        except Exception as e:
            print(f"Error al insertar datos en MySQL: {e}")
            cursor.rollback()
            print("Se realizó un rollback")
            
        finally:
            cursor.close()
            
        def close_connection(self):
            if self.connection and self.connection.is_connected():
                self.connection.close()
            print("Conexión cerrada.")

try:
    connection = pymysql.connect(
    host="localhost", # Servidor local de MySQL
    user="usuario", # Nombre de usuario de MySQL
    password="usuario", # Contraseña del usuario
    database="1dam" # Nombre de la base de datos
    )
    
except Error as e:
    print(f"Error de conexión: {e}")

class MySQLToFile:
    def __init__(self, connection):
        self.connection = connection
        
    def write_to_json(self, table_name, json_file):
        if not self.connection or not self.connection.open:
            print("No se pudo establecer conexión con MySQL.")
            return
        
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            
            # Escribir los registros en el archivo JSON
            with open(json_file, 'w') as file:
                json.dump(records, file, indent=4)
                print(f"Datos de '{table_name}' guardados en '{json_file}'.")

        except Exception as e:
            print(f"Error al escribir en JSON: {e}")
        
        finally:
            cursor.close()
            def close_connection(self):
                if self.connection and self.connection.open:
                    self.connection.close()
            print("Conexión cerrada.")
            

# Uso del código
if conexion: # Solo si la conexión fue exitosa
    db1 = CSVToMySQL(conexion) 
    db1.insert_csv_to_mysql(csv_file="libros_unamuno.csv",table="Libros")
    
    db2 = JSONToMySQL(conexion)
    db2.insert_json_to_mysql(json_file="libros_machado.json", table="Libros")
    
    db3 = MySQLToFile(conexion)
    db3.write_to_json(table_name="Libros", json_file="inventario_final.json")
    
    
    db3.close_connection()
