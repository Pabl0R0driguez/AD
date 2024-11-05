from peewee import MySQLDatabase, Model, CharField, IntegerField, IntegrityError

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

# Insertar registros en la tabla dentro de una transacción
try:
    with db.transaction():
        Motocicletas.create(marca="Opel", modelo="JJK-3", cilindrada=800, precio=2344)
        Motocicletas.create(marca="Mercedes", modelo="GG45", cilindrada=780, precio=9000)
        Motocicletas.create(marca="Martillo", modelo="Manual", cilindrada=567, precio=9876)
        Motocicletas.create(marca="Hyundai", modelo="567-3", cilindrada=1188, precio=6000)
        Motocicletas.create(marca="Mercedes", modelo="AT56", cilindrada=1234, precio=5609)
    print("Motocicletas insertadas en la base de datos:")
except IntegrityError as e:
    print("Error al insertar motocicletas:", e)

# Mostrar los registros restantes
motocicletas_restantes = Motocicletas.select()
for moto in motocicletas_restantes:
    print(f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}")
print("\n")

# Recuperar objetos de modelo GG45
print("Tarea 1")
modeloG = Motocicletas.select().where(Motocicletas.modelo == "GG45")
for moto in modeloG:
    print(f"Marca: {moto.marca}, Precio: {moto.precio}")
print("\n")

# Eliminar un registro específico en base a dos atributos
print("Tarea 2")
try:
    with db.transaction():
        eliminar = Motocicletas.get((Motocicletas.marca == "Mercedes") & (Motocicletas.modelo == "AT56"))
        eliminar.delete_instance()
        print(f"Motocicleta Mercedes de modelo AT56 eliminada.")
except Motocicletas.DoesNotExist:
    print("No existe")
except IntegrityError as e:
    print("Error al eliminar motocicleta:", e)

# Mostrar los registros restantes
motocicletas_restantes = Motocicletas.select()
for moto in motocicletas_restantes:
    print(f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}")
print("\n")

# Eliminar todos los registros que cumplan que tenga un precio inferior a 6000
print("Tarea 3")
try:
    with db.transaction():
        precioSuperior = Motocicletas.delete().where(Motocicletas.precio < 6000)
        cantidad_eliminada = precioSuperior.execute()
        print(f"Se han eliminado {cantidad_eliminada} motocicletas con precio inferior a 6000.")
except IntegrityError as e:
    print("Error al eliminar motocicletas:", e)

# Mostrar los registros restantes para confirmar la eliminación
motocicletas_restantes = Motocicletas.select()
for moto in motocicletas_restantes:
    print(f"Marca: {moto.marca}, Modelo: {moto.modelo}, Precio: {moto.precio}, Cilindrada: {moto.cilindrada}")

# Cerrar la conexión
db.close()
