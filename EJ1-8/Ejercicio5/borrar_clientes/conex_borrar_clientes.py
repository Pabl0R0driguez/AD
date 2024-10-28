
import pymysql

# Conexión a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='usuario',         
    password='usuario',     
    database='2dam'       
)

try:
    with connection.cursor() as cursor:
        # Paso 2: Eliminar un registro de la tabla Clientes
        cursor.execute("DELETE FROM Clientes WHERE nombre = %s", ('Pablo Aimar',))
        connection.commit()
        print(cursor.rowcount, "registro(s) eliminado(s) de la tabla Clientes")
        # Confirmar cambios
        connection.commit()

except pymysql.MySQLError as e:
    print(f"Ocurrió un error al ejecutar las instrucciones SQL: {e}")

finally:
    connection.close()
    print("Conexión cerrada.")
