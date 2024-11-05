from peewee import MySQLDatabase, Model, CharField, IntegerField,IntegrityError

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
def tabla_existe(nombre_tabla):
    consulta = """
    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"""
    cursor = db.execute_sql(consulta, ("2DAM", nombre_tabla))
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
print("Tabla motocicletas creada")

try:
    # Iniciar una transacción utilizando db.atomic()
    with db.atomic():
        #Insertar registros en la tabla con los campos actuales
        Motocicletas.create(marca="Opel", modelo="56-Ñ", cilindrada=1500, precio=2300)        
        Motocicletas.create(marca="Bosch", modelo="FE-3", cilindrada=500, precio=4500)     
        Motocicletas.create(marca="Stanley", modelo="6565-I", cilindrada=250, precio=1200)  
        Motocicletas.create(marca="Makita", modelo="TY-0", cilindrada=350, precio=3200)    
        Motocicletas.create(marca="DeWalt", modelo="NDN-4", cilindrada=800, precio=6400)   

        print("Registros insertados con una transacción")

 # Si hay un fallo en cualquier inserción, el bloque except capturará el error y la transacción se deshará automáticamente
except IntegrityError as e:
    print(f"Error al insertar herramientas: {e}")
print("\n")
# Recuperar todas las motocicletas de la base de datos
motos = Motocicletas.select()
for motocicletas in motos:
   
    print(
        f"Marca: {motocicletas.marca}, Modelo: {motocicletas.modelo} ,Precio:{motocicletas.precio},Cilindrada:{motocicletas.cilindrada}"
       
    )