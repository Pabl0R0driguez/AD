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
        #Actualizar un registro en la tabla Clientes
        cursor.execute("UPDATE Clientes SET direccion = %s ,telefono =%s WHERE nombre = %s",
        ('Calle Mirador das Flores', '5657-4321','Juan Pérez'))
        connection.commit()
        print(cursor.rowcount, "Registro(s) actualizado(s) en la tabla Clientes")


        # Confirmar cambios
        connection.commit()

except pymysql.MySQLError as e:
    print(f"Ocurrió un error al ejecutar las instrucciones SQL: {e}")

finally:
    connection.close()
    print("Conexión cerrada.")
