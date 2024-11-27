from peewee import MySQLDatabase, Model, CharField, IntegerField, fn , DateField
from datetime import date

# Configurar la base de datos
db = MySQLDatabase(
    "2DAM",
    user="usuario",
    password="usuario",
    host="localhost",
    port=3306,
)

# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")

# Definir el mapeo de la tabla motocicletas
class Motocicletas(Model):
    marca = CharField()
    modelo = CharField()
    precio = IntegerField()
    cilindrada = IntegerField()
    fecha_creacion = DateField(default = date.today)

    class Meta:
        database = db
        table_name = "motocicletas"

# Función para verificar si una tabla existe en MySQL
def tabla_existe(nombre_tabla):
    consulta = """
    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"""
    cursor = db.execute_sql(consulta, ("2DAM", nombre_tabla))
    resultado = cursor.fetchone()
    return resultado[0] > 0

# Eliminar la tabla si ya existe
if tabla_existe(Motocicletas._meta.table_name):
    print(f"La tabla '{Motocicletas._meta.table_name}' existe.")
    db.drop_tables([Motocicletas], cascade=True)
    print(f"Tabla '{Motocicletas._meta.table_name}' eliminada con éxito.")
else:
    print(f"La tabla '{Motocicletas._meta.table_name}' no existe.")

# Crear la tabla
db.create_tables([Motocicletas])
print("Tabla 'motocicletas' creada o ya existente.")

# Insertar registros en la tabla
Motocicletas.create(marca="Opel", modelo="JJK-3", cilindrada=800, precio=2344)
Motocicletas.create(marca="Mercedes", modelo="GG45", cilindrada=780, precio=9000)
Motocicletas.create(marca="Martillo", modelo="Manual", cilindrada=567, precio=9876)
Motocicletas.create(marca="Hyundai", modelo="567-3", cilindrada=1188, precio=6000)
Motocicletas.create(marca="Mercedes", modelo="AT56", cilindrada=1234, precio=5609)

#Mostrar motocicletas insertadas en la base de datos
print("Motocicletas insertadas en la base de datos:")

motocicletas_restantes = Motocicletas.select()
for moto in motocicletas_restantes:
    print(f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}")
print("\n")


# Función para contar el número de productos en la base de datos
def contar_productos():
    # Contar el número total de productos
    total_motocicletas = Motocicletas.select(fn.Count(Motocicletas.id)).scalar()  # 'scalar()' devuelve un valor único
    print(f"Total de productos en la base de datos: {total_motocicletas}")


# Llamar a la función de contar productos
contar_productos()


# Función para obtener la suma de los precios de todos los productos
def suma_precios():
    # Calcular la suma total de los precios de los productos
    total_precio = Motocicletas.select(fn.SUM(Motocicletas.precio)).scalar()
    print(f"Suma de los precios de todos los productos: {total_precio}€")


# Llamar a la función para obtener la suma de precios
suma_precios()


# Función para obtener productos creados hoy
def productos_hoy():
    productos = Motocicletas.select().where(Motocicletas.fecha_creacion == date.today())
   
    print("Productos creados hoy:")
    for producto in productos:
        print(f"{producto.marca} - {producto.precio}€")


# Llamamos a la función para obtener los productos creados hoy
productos_hoy()


# Función para obtener productos creados después de una fecha específica
def productos_despues_de(fecha):
    productos = Motocicletas.select().where(Motocicletas.fecha_creacion > fecha)
   
    print(f"Productos creados después de {fecha}:")
    for producto in productos:
        print(f"{producto.marca} - {producto.precio}€")


# Ejemplo: obtener productos creados después del 1 de enero de 2022
productos_despues_de(date(2022, 1, 1))


# Función para obtener la suma de precios de productos creados hoy
def suma_precios_hoy():
    total_precio_hoy = Motocicletas.select(fn.SUM(Motocicletas.precio)).where(Motocicletas.fecha_creacion == date.today()).scalar()
    print(f"Suma de los precios de los productos creados hoy: {total_precio_hoy}€")


# Llamamos a la función para obtener la suma de precios de productos creados hoy
suma_precios_hoy()


# Recuperar objetos de modelo GG45
print("Tarea 1")
modeloG = Motocicletas.select().where(Motocicletas.modelo == "GG45")
for moto in modeloG:
    print(f"Marca: {moto.marca}, Precio: {moto.precio}")
print("\n")

# Eliminar un registro específico en base a dos atributos
print("Tarea 2")
try:
    # Eliminar un registro específico, marca="Mercedes" y modelo="AT56"
    eliminar = Motocicletas.get((Motocicletas.marca == "Mercedes") & (Motocicletas.modelo == "AT56"))
    eliminar.delete_instance()
    print(f"Motocicleta Mercedes de modelo AT56 eliminada.")
except Motocicletas.DoesNotExist:
    print("No existe")

# Mostrar los registros restantes
motocicletas_restantes = Motocicletas.select()
for moto in motocicletas_restantes:
    print(f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}")
print("\n")

# TAREA 3: Eliminar todos los registros que cumplan que tenga un precio inferior a 6000
print("Tarea 3")
precioSuperior = Motocicletas.delete().where(Motocicletas.precio < 6000)
cantidad_eliminada = precioSuperior.execute()
print(f"Se han eliminado {cantidad_eliminada} motocicletas con precio inferior a 6000.")

# Mostrar los registros restantes para confirmar la eliminación
motocicletas_restantes = Motocicletas.select()
for moto in motocicletas_restantes:
    print(f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}")

# Cerrar la conexión
db.close()
