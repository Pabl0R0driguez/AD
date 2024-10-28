import pymysql
import time


connection = pymysql.connect(
    host='localhost',
    user='usuario',       
    password='usuario',  
    database='2dam' 
)

try:
    with connection.cursor() as cursor:
        # Paso 1, Crear la tabla Clientes
        sql_crear_clientes = """
        CREATE TABLE IF NOT EXISTS Clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            direccion VARCHAR(100),
            telefono VARCHAR(15)
        );
        """
        cursor.execute(sql_crear_clientes)
        print("Tabla 'Clientes' creada.")

        # Paso 2, Modificar la tabla Motocicletas para añadir la columna cliente_id
        sql_alter_motocicletas = """
        ALTER TABLE motocicletas 
        ADD COLUMN cliente_id INT,
        ADD CONSTRAINT fk_cliente
        FOREIGN KEY (cliente_id) REFERENCES Clientes(id);
        """
        cursor.execute(sql_alter_motocicletas)
        print("Columna 'cliente_id' añadida a 'Motocicletas' y relación creada.")


        # Paso 3, Insertar datos en la tabla Clientes
        sql_insertar_clientes = """
        INSERT INTO Clientes (nombre, direccion, telefono) VALUES
        ('Pepe Cartagena', 'Calle Betis', '4444-9090'),
        ('Manuel Iglesias', 'Avenida Emilio Lemos', '4333-1111'),
        ('Pablo Aimar', 'Avenida de las Ciencias', '6677-5677'),
        ('Pedro Rico', 'Mirador de Montepinar', '3333-1122');
        """
        cursor.execute(sql_insertar_clientes)
        print("Datos insertados en la tabla 'Clientes'.")


    # Confirmar cambios
    connection.commit()
    print("Cambios confirmados en la base de datos.")
    
except pymysql.MySQLError as e:
    print(f"Ocurrió un error al ejecutar las instrucciones SQL: {e}")
    
finally:
    connection.close()
    print("Conexión cerrada.")
