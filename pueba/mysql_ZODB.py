import mysql.connector
from persistent import Persistent
import ZODB, ZODB.FileStorage, transaction



# Clase Producto
class Producto(Persistent):
    def __init__(self, id, nombre, categoria, precio):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio


# 1. Función para conectar a ZODB y recuperar datos
def recuperar_de_zodb():
    # Abrir conexión a ZODB
    storage = ZODB.FileStorage.FileStorage('productos.fs')  # Archivo de la base de datos ZODB
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()


    # Recuperar productos desde ZODB
    productos = {}
    if 'productos' in root:
        productos = root['productos']
        print("Productos recuperados de ZODB:")
        for id_producto, producto in productos.items():
            print(f"ID: {producto.id}, Nombre: {producto.nombre}, Categoría: {producto.categoria}, Precio: {producto.precio}")
    else:
        print("No hay productos almacenados en ZODB.")


    # Cerrar la conexión
    connection.close()
    db.close()
    return productos


# 2. Función para insertar datos en MySQL
def insertar_en_mysql(productos):
    # Conectar a la base de datos MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='usuario',  # Cambia por tu usuario
        password='usuario',  # Cambia por tu contraseña
        database='2DAM'  # Cambia por tu base de datos
    )
    cursor = conn.cursor()


    # Crear la tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        id INT PRIMARY KEY,
        nombre VARCHAR(255),
        categoria VARCHAR(255),
        precio DECIMAL(10, 2)
    )
    """)


    # Insertar datos en la tabla producto
    for id_producto, producto in productos.items():
        cursor.execute("""
        INSERT INTO producto (id, nombre, categoria, precio)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        nombre = VALUES(nombre),
        categoria = VALUES(categoria),
        precio = VALUES(precio)
        """, (producto.id, producto.nombre, producto.categoria, producto.precio))
   
    conn.commit()  # Confirmar transacción
    print("Productos insertados/actualizados en MySQL.")


    # Cerrar la conexión
    cursor.close()
    conn.close()


# 3. Función principal
def main():
    productos = recuperar_de_zodb()  # Recuperar datos de ZODB
    insertar_en_mysql(productos)  # Insertar datos en MySQL


# Ejecutar el proceso
main()

