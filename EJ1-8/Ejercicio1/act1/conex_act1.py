import mysql.connector  # El módulo correcto para conectar MySQL

host = 'localhost'
user = 'usuario'
password = 'usuario'
database = '2dam'

connection = None

try:
    # Corrección: usar mysql.connector.connect()
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Conexión exitosa a la base de datos.")

    # Usar el cursor para ejecutar consultas SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print("Versión de MySQL:", version[0])

# Capturar la excepción correcta del módulo mysql.connector
except mysql.connector.Error as e:
    print(f"Error al conectar a la base de datos: {e}")

finally:
    # Verificar si la conexión fue establecida y cerrarla
    if connection:
        connection.close()
        print("Conexión cerrada.")
