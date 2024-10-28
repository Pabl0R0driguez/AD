import pymysql

# Conexión a la base de datos MySQL usando pymysql
conexion = pymysql.connect(
    host="localhost",
    user="usuario",  
    password="usuario", 
    database="2dam"  
)

# Crear un cursor para interactuar con la base de datos
cursor = conexion.cursor()

# Ejecutar una consulta para obtener las 5 filas de la tabla Herramientas
cursor.execute("SELECT * FROM Clientes LIMIT 5")
print("Resultados uno por uno usando fetchone:")

# Muestra uno a uno los 5 resultados
fila = cursor.fetchone()
while fila:
    print(fila)  
    # Obtener la siguiente fila
    fila = cursor.fetchone()  

print("\n Resultados mostrados, repetimos el proceso")

# Ejecutar nuevamente la consulta para mostrar los resultados otra vez
cursor.execute("SELECT * FROM Clientes LIMIT 5")
fila = cursor.fetchone()
while fila:
    print(fila)
    fila = cursor.fetchone()

cursor.close()
conexion.close()