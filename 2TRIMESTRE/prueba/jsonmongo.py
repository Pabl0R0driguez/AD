import json
import csv
import logging
from copy import deepcopy

# Configuración de logging para guardar los mensajes en un archivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log_datos.log"),  # Guardar logs en el archivo
    ]
)

class DataManager:
    def __init__(self, ruta_archivo, tipo_archivo='json'):
        self.ruta_archivo = ruta_archivo
        self.tipo_archivo = tipo_archivo
        self.version = 1
        self.transaccion_activa = False
        self.copia_datos = None
        self.datos = self._leer_archivo() if self._existe_archivo() else []
    
    def _existe_archivo(self):
        try:
            with open(self.ruta_archivo, 'r'):
                return True
        except FileNotFoundError:
            return False
    
    def _leer_archivo(self):
        if self.tipo_archivo == 'json':
            with open(self.ruta_archivo, 'r') as archivo:
                return json.load(archivo)
        elif self.tipo_archivo == 'csv':
            datos = []
            with open(self.ruta_archivo, mode='r') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    datos.append(fila)
            return datos
    
    def _guardar_archivo(self):
        if self.tipo_archivo == 'json':
            with open(self.ruta_archivo, 'w') as archivo:
                json.dump(self.datos, archivo, indent=4)
        elif self.tipo_archivo == 'csv' and self.datos:
            with open(self.ruta_archivo, mode='w', newline='') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=self.datos[0].keys())
                escritor.writeheader()
                escritor.writerows(self.datos)
        logging.info(f"Archivo {self.tipo_archivo.upper()} guardado. Versión actual: {self.version}")
    
    def iniciar_transaccion(self):
        if self.transaccion_activa:
            raise Exception("Ya hay una transacción activa.")
        self.transaccion_activa = True
        self.copia_datos = deepcopy(self.datos)
        logging.info("Transacción iniciada.")
    
    def confirmar_transaccion(self):
        if not self.transaccion_activa:
            raise Exception("No hay una transacción activa para confirmar.")
        self.version += 1
        self.transaccion_activa = False
        self.copia_datos = None
        self._guardar_archivo()
        logging.info("Transacción confirmada y cambios guardados.")
    
    def revertir_transaccion(self):
        if not self.transaccion_activa:
            raise Exception("No hay una transacción activa para revertir.")
        self.datos = self.copia_datos
        self.transaccion_activa = False
        self.copia_datos = None
        logging.warning("Transacción revertida. Los cambios no se guardaron.")
    
    def escribir_dato(self, nuevo_dato):
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        self.datos.append(nuevo_dato)
        logging.info(f"Dato agregado: {nuevo_dato}")
    
    def actualizar_configuracion(self, nueva_ruta, nuevo_tipo=None):
        if self.transaccion_activa:
            raise Exception("No se puede cambiar la configuración durante una transacción.")
        self.ruta_archivo = nueva_ruta
        if nuevo_tipo:
            self.tipo_archivo = nuevo_tipo
        logging.info(f"Configuración actualizada. Nueva ruta del archivo: {self.ruta_archivo}")

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# Instancias de comida
comidas = [
    {"nombre": "Sushi", "tipo": "Japonesa", "precio": 20.0, "ingrediente_principal": "Pescado", "tipo_plato": "Principal"},
    {"nombre": "Helado", "tipo": "Postre", "precio": 5.0, "ingrediente_principal": "Leche", "tipo_plato": "Postre"},
    {"nombre": "Ensalada César", "tipo": "Internacional", "precio": 10.0, "ingrediente_principal": "Lechuga", "tipo_plato": "Entrante"}
]

# Uso del DataManager
# Crear instancia para JSON
data_manager = DataManager('comidas.json', 'json')

# Iniciar transacción y escribir datos
data_manager.iniciar_transaccion()
for comida in comidas:
    data_manager.escribir_dato(comida)
data_manager.confirmar_transaccion()

# Cambiar configuración para CSV y escribir los mismos datos
data_manager.actualizar_configuracion('comidas.csv', 'csv')

# Iniciar nueva transacción para guardar en CSV
data_manager.iniciar_transaccion()
data_manager.confirmar_transaccion()

print("Datos guardados en JSON y CSV con éxito.")


