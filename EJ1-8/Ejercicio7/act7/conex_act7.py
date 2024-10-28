import pymysql
try:
    # Conexión a la base de datos MySQL usando pymysql
    conexion = pymysql.connect(
        host="localhost",
        user="usuario",  
        password="usuario", 
        database="2dam"  
    )
    # Crear un cursor para interactuar con la base de datos
    cursor = conexion.cursor()
    # Iniciamos la transacción
    conexion.begin()
    print("Iniciando la transacción...")
    # Ejecutar una consulta para obtener las 5 filas de la tabla Clientes
    cursor.execute("SELECT * FROM Clientes LIMIT 5")
    print("Resultados uno por uno usando fetchone:")
    
    # Muestra uno a uno los 5 resultados
    fila = cursor.fetchone()
    while fila:
        print(fila)  
        fila = cursor.fetchone()  
    print("\nResultados mostrados, repetimos el proceso con la tabla PEPE, forzamos el error: ")

    # Esta consulta generará un error porque la tabla PEPE no existe
    cursor.execute("SELECT * FROM PEPE LIMIT 5")
    fila = cursor.fetchone()
    while fila:
        print(fila)
        fila = cursor.fetchone()

    # Si todo fue bien, se hace commit
    conexion.commit()

except pymysql.MySQLError as e:
    # Si ocurre un error, hacer rollback
    print(f"Error en la transacción: {e}")
    print("Se realizó rollback.")
    conexion.rollback()
finally:
    # Asegurar que se cierre la conexión y el cursor
    if conexion:
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")
