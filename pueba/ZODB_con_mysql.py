import mysql.connector
from persistent import Persistent
import ZODB, ZODB.FileStorage, transaction


# 1. Clase Producto para la base de datos orientada a objetos ZODB
class Producto(Persistent):
    def __init__(self, id, nombre, categoria, precio):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    

# 2. Conectar a MySQL y agregar productos
def insertar_en_mysql():
    conn = mysql.connector.connect(
        host='localhost',
        user='usuario',  # Usuario de MySQL
        password='usuario',  # Contraseña de MySQL
        database='2DAM'
    )
   
    cursor = conn.cursor()


    # Insertar varias instancias de Producto en MySQL
    productos = [
        ('Martillo', 'Herramientas', 12.99),
        ('Taladro', 'Herramientas', 49.99),
        ('Sierra', 'Herramientas', 29.99)
    ]


    for producto in productos:
        cursor.execute("INSERT INTO producto (nombre, categoria, precio) VALUES (%s, %s, %s)", producto)
   
    conn.commit()  # Confirmar la transacción
    print("Productos insertados en MySQL")


    cursor.close()
    conn.close()

# Función para eliminar la tabla si existe, o crearla si no existe
def crear_o_eliminar_tabla():
    try:
        # Establecer la conexión a la base de datos MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='usuario',  # Usuario de MySQL
            password='usuario',  # Contraseña de MySQL
            database='2DAM'
        )
        cursor = conn.cursor()

        # Verificar si la tabla 'producto' existe
        cursor.execute("SHOW TABLES LIKE 'producto'")
        result = cursor.fetchone()

        if result:  # Si la tabla existe
            print("La tabla 'producto' existe. Eliminándola...")
            cursor.execute("DROP TABLE producto")  # Eliminar la tabla
            print("Tabla 'producto' eliminada.")
        else:  # Si la tabla no existe
            print("La tabla 'producto' no existe. Creándola...")
            # Crear la tabla 'producto'
            cursor.execute("""
            CREATE TABLE producto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                categoria VARCHAR(255),
                precio DECIMAL(10, 2)
            )
            """)
            print("Tabla 'producto' creada.")

        # Confirmar los cambios en la base de datos
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Cerrar la conexión y el cursor
        cursor.close()
        conn.close()



# 3. Consultar productos desde MySQL y almacenarlos en un diccionario
def consultar_y_almacenar():
    conn = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='2DAM'
    )
   
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")  # Consulta todos los productos


    productos = cursor.fetchall()  # Devuelve todas las filas
    productos_dict = {}


    # Almacenar los productos en un diccionario
    for producto in productos:
        id_producto = producto[0]
        nombre = producto[1]
        categoria = producto[2]
        precio = producto[3]


        # Almacenar en el diccionario
        productos_dict[id_producto] = Producto(id_producto, nombre, categoria, precio)


    cursor.close()
    conn.close()
   
    return productos_dict


# 4. Almacenar los productos en ZODB
def almacenar_en_zodb(productos_dict):
    storage = ZODB.FileStorage.FileStorage('productos.fs')  # Nombre del archivo de la base de datos ZODB
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()


    if 'productos' not in root:
        root['productos'] = {}


    # Almacenar los productos en ZODB
    for id_producto, producto in productos_dict.items():
        root['productos'][id_producto] = producto
   
    transaction.commit()  # Confirmar los cambios en ZODB
    print("Productos almacenados en ZODB")


    connection.close()
    db.close()


# 5. Función para mostrar los productos almacenados en ZODB
def mostrar_productos_zodb():
    storage = ZODB.FileStorage.FileStorage('productos.fs')  # Nombre del archivo de la base de datos ZODB
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()


    if 'productos' in root:
        productos = root['productos']
        print("Productos almacenados en ZODB:")
        for id_producto, producto in productos.items():
            print(f"ID: {producto.id}, Nombre: {producto.nombre}, Categoría: {producto.categoria}, Precio: {producto.precio}")
    else:
        print("No hay productos almacenados en ZODB.")


    connection.close()
    db.close()


# 6. Función principal para ejecutar todo el proceso
def main():
    crear_o_eliminar_tabla()
    insertar_en_mysql()  # Insertar productos en MySQL
    productos_dict = consultar_y_almacenar()  # Consultar y almacenar en un diccionario
    almacenar_en_zodb(productos_dict)  # Almacenar los productos en ZODB
    mostrar_productos_zodb()  # Mostrar los productos almacenados en ZODB


# Ejecutar el proceso directamente
main()




