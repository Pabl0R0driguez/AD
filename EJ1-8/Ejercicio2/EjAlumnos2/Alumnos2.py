import pymysql

host = 'localhost'
user = 'usuario'
password = 'usuario'
database = '2dam'

connection = None

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Conexión exitosa a la base de datos.")

    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print("Versión de MySQL:", version[0])

except pymysql.MySQLError as e:
    print(f"Error al conectar a la base de datos: {e}")

finally:
    if connection:
        connection.close()
        print("Conexión cerrada.")