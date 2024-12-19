from peewee import (
    MySQLDatabase,
    Model,
    CharField,
    AutoField,
    IntegerField,
    fn,
    DateField,
)
from datetime import date
import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent
from copy import deepcopy


# Configurar la base de datos
db = MySQLDatabase(
    "1dam",
    # Nombre de la base de datos
    user="usuario",
    # Usuario de MySQL
    password="usuario",
    host="localhost",
    port=3306,
)
# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")


# Definir el mapeo de la tabla motocicletas
class Libros(Model):
    id = AutoField()
    titulo = CharField()
    autor = CharField()
    anio_publicacion = IntegerField()
    genero = CharField()

    class Meta:
        database = db
        table_name = "Libros"


# Función para verificar si una tabla existe en MySQL
def tabla_existe(nombre_tabla):
    consulta = """
    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"""
    cursor = db.execute_sql(consulta, ("2DAM", nombre_tabla))
    resultado = cursor.fetchone()
    return resultado[0] > 0


# Eliminar la tabla si ya existe
if tabla_existe(Libros._meta.table_name):
    print(f"La tabla '{Libros._meta.table_name}' existe.")
    db.drop_tables([Libros], cascade=True)
    print(f"Tabla '{Libros._meta.table_name}' eliminada con éxito.")
else:
    print(f"La tabla '{Libros._meta.table_name}' no existe.")

# Crear la tabla
db.create_tables([Libros])
print("Tabla 'Libros' creada o ya existente.")


def insertar_datos(nombre_tabla):
    nombre_tabla.create(
        titulo="Cien años de soledad",
        autor="Gabriel García Márquez",
        anio_publicacion="1967",
        genero="Novela",
    )

    nombre_tabla.create(
        titulo="Don Quijote de la Mancha",
        autor="Miguel de Cervantes",
        anio_publicacion=1605,
        genero="Novela",
    )

    nombre_tabla.create(
        titulo="El Principito",
        autor="Antoine de Saint-Exupéry",
        anio_publicacion=1943,
        genero="Infantil",
    )

    nombre_tabla.create(
        titulo="Crónica de una muerte anunciada",
        autor="Gabriel García Márquez",
        anio_publicacion=1981,
        genero="Novela",
    )

    nombre_tabla.create(
        titulo="1984", autor="George Orwell", anio_publicacion=1949, genero="Distopía"
    )


# Insertamos datos a la tabla Libro
insertar_datos(Libros)


# Conecto a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage("1dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()


# Definir clase Motocicleta
class Prestamo(Persistent):
    def __init__(self, libro_id, nombre_usuario, fecha_prestamo, fecha_devolucion):
        self.libro_id = libro_id
        self.nombre_usuario = nombre_usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion


def agregar_prestamos():
    try:
        print("Iniciando la transacción para agregar motocicletas...")

        # Verificar y crear colecciones si no existen
        if "prestamo" not in root:
            root["prestamo"] = {}
            # Inicializar una colección de motocicletas si no existe
            transaction.commit()

            # Insertar prestamos
            root["prestamo"][1] = Prestamo(1, "Juan Perez", "2023-10-01", "2023-11-01")
            root["prestamo"][2] = Prestamo(2, "Ana Lopez", "2023-09-15", "2023-10-15")
            root["prestamo"][4] = Prestamo(4, "Maria Gomez", "2023-09-20", "2023-10-20")

            # Guardamos los cambios
            transaction.commit()
            print("Transacción completada, prestamos insertados correctamente.")

    except Exception as e:
        # Si ocurre un error, revertimos la transacción
        transaction.abort()
        print(f"Error durante la transacción: {e}. Transacción revertida.")


def listar_prestamo():
    print("Listando prestamo en la base de datos:")
    for key, prestamo in root["prestamo"].items():
        print(
            f"Libro_id: {prestamo.libro_id}, Nombre: {prestamo.nombre_usuario}, Fecha préstamo: {prestamo.fecha_prestamo}, Fecha devolución: {prestamo.fecha_devolucion}"
        )


# Llamamos a las funciones creadas
agregar_prestamos()
listar_prestamo()


# Recorro la tabla Libros
libros = Libros.select()
for motocicletas in libros:

    print(
        f"Titulo: {Libros.titulo}, Autor: {Libros.autor}, Año publicación: {Libros.anio_publicacion}, Género: {Libros.genero}"
    )


# Función para filtrar pestamo de un cliente específico usando root.items()
def buscar_prestamos_por_genero(genero):
    print("\n")


# Filtramos por novela
buscar_prestamos_por_genero("Novela")

connection.close()
db.close()
