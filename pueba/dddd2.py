import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent
import copy  # Import the copy module

storage = ZODB.FileStorage.FileStorage('2DAM.fs')  
db = ZODB.DB(storage)  
connection = db.open()  
root = connection.root()

# Defino las clases para Comidas y Países de Origen.
class Comidas(Persistent):
    def __init__(self, nombre, ingrediente_principal, id_pais_origen, tipo_plato):
        self.nombre = nombre  
        self.ingrediente_principal = ingrediente_principal 
        self.id_pais_origen = id_pais_origen 
        self.tipo_plato = tipo_plato  

class PaisDeOrigen(Persistent):
    def __init__(self, nombre_pais, continente):
        self.nombre_pais = nombre_pais  
        self.continente = continente  

# Verifico y creo colecciones si no existen ya en la base de datos.
if 'comidas' not in root:
    root['comidas'] = {}  # Creo un diccionario para almacenar las comidas.
    
if 'paises' not in root:
    root['paises'] = {}  # Creo un diccionario para almacenar los países.

# Inserto datos en Países de Origen.
root['paises']['Mexico'] = PaisDeOrigen("México", "América del Norte")
root['paises']['Italia'] = PaisDeOrigen("Italia", "Europa")
root['paises']['Japón'] = PaisDeOrigen("Japón", "Asia")

# Inserto datos en Comidas, incluyendo el id_pais_origen.
root['comidas']['Taco'] = Comidas("Taco", "Maíz", "Mexico", "Plato Principal")
root['comidas']['Pizza'] = Comidas("Pizza", "Harina", "Italia", "Plato Principal")
root['comidas']['Sushi'] = Comidas("Sushi", "Arroz", "Japón", "Plato Principal")
root['comidas']['Risotto'] = Comidas("Risotto", "Arroz", "Italia", "Plato Principal")

# Hago una copia de un objeto de comida existente.
comida1 = root['comidas']['Taco']  # Defino comida1 como el Taco en la base de datos
comida_copia = copy.deepcopy(comida1)  # Hago una copia de comida1
comida_copia.tipo_plato = "Entrante"  # Modifico el tipo_plato en la copia
print(comida1.nombre, comida1.ingrediente_principal, comida1.id_pais_origen, comida1.tipo_plato)
# Tiene que salir Plato Principal

# Realizo la transacción para guardar todos los cambios en la base de datos.
transaction.commit()

# Cierra la conexión y la base de datos al final
connection.close()
db.close()