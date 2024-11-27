from peewee import MySQLDatabase, Model, CharField, IntegerField

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
        # Nombre de la tabla en la base de datos
        table_name = "motocicletas"


# Función para verificar si una tabla existe en MySQL
def tabla_existe(Motocicletas):
    consulta = """ SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"""
    cursor = db.execute_sql(consulta, ("2DAM", Motocicletas))
    resultado = cursor.fetchone()
    return resultado[0] > 0


# Eliminamos la tabla si ya existe para empezar a trabajar desde cero
if tabla_existe(Motocicletas._meta.table_name):
    print(f"La tabla '{Motocicletas._meta.table_name}' existe.")
    db.drop_tables([Motocicletas], cascade=True)
    print(f"Tabla '{Motocicletas._meta.table_name}' eliminada con éxito.")
else:
    print(f"La tabla '{Motocicletas._meta.table_name}' no existe.")

# Crear la tabla de nuevo
db.create_tables([Motocicletas])
print("Tabla 'motocicletas' creada o ya existente.")

# Insertar registros en la tabla
Motocicletas.create(marca="Opel", modelo="JJK-3", cilindrada=800, precio=2344)
Motocicletas.create(marca="Mercedes", modelo="GG45", cilindrada=780, precio=9000)
Motocicletas.create(marca="Martillo", modelo="Manual", cilindrada=567, precio=9876)
Motocicletas.create(marca="Hyundai", modelo="567-3", cilindrada=1188, precio=6000)
Motocicletas.create(marca="Mercedes", modelo="AT56", cilindrada=1234, precio=5609)

print("Motocicletas insertadas en la base de datos.")