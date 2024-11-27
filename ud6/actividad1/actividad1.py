import json
import csv
import logging
import os
from copy import deepcopy

# Configuración de logging para guardar en un archivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log_datos.log"),  # Guardar logs en un archivo
    ],
)


class DataManager:
    def __init__(self, ruta_archivo, tipo_archivo="json"):
        self.ruta_archivo = ruta_archivo
        self.tipo_archivo = tipo_archivo
        self.version = 1
        self.transaccion_activa = False
        self.copia_datos = None

        # Cargar datos si el archivo existe, o inicializar con una lista vacía
        if os.path.exists(ruta_archivo):
            self.datos = self._leer_archivo()
            logging.info(
                f"Archivo {tipo_archivo.upper()} cargado con éxito. Versión actual: {self.version}"
            )
        else:
            self.datos = []
            self._guardar_archivo()

    def _leer_archivo(self):
        if self.tipo_archivo == "json":
            with open(self.ruta_archivo, "r") as archivo:
                return json.load(archivo)
        elif self.tipo_archivo == "csv":
            datos = []
            with open(self.ruta_archivo, mode="r") as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    datos.append(fila)
            return datos
        else:
            raise ValueError("Tipo de archivo no soportado. Use 'json' o 'csv'.")

    def _guardar_archivo(self):
        if self.tipo_archivo == "json":
            with open(self.ruta_archivo, "w") as archivo:
                json.dump(self.datos, archivo, indent=4)
        elif self.tipo_archivo == "csv":
            if self.datos:
                with open(self.ruta_archivo, mode="w", newline="") as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=self.datos[0].keys())
                    escritor.writeheader()
                    escritor.writerows(self.datos)
        logging.info(
            f"Archivo {self.tipo_archivo.upper()} guardado. Versión actual: {self.version}"
        )

    def iniciar_transaccion(self):
        if self.transaccion_activa:
            raise Exception("Ya hay una transacción activa.")
        self.transaccion_activa = True
        self.copia_datos = deepcopy(
            self.datos
        )  # Crear una copia de seguridad de los datos
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        if not self.transaccion_activa:
            raise Exception("No hay una transacción activa para confirmar.")
        self.version += 1  # Incrementa la versión al confirmar la transacción
        self.transaccion_activa = False
        self.copia_datos = None  # Limpiar la copia de seguridad
        self._guardar_archivo()  # Guardar cambios en el archivo
        logging.info("Transacción confirmada y cambios guardados.")

    def escribir_dato(self, nuevo_dato):
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        self.datos.append(nuevo_dato)
        logging.info(f"Dato agregado: {nuevo_dato}")

    def actualizar_configuracion(self, nueva_ruta, nuevo_tipo=None):
        if self.transaccion_activa:
            raise Exception(
                "No se puede cambiar la configuración durante una transacción."
            )
        self.ruta_archivo = nueva_ruta
        if nuevo_tipo:
            self.tipo_archivo = nuevo_tipo
        logging.info(
            f"Configuración actualizada. Nueva ruta del archivo: {self.ruta_archivo}"
        )


# Creamos una instancia de DataManager y escribimos en un JSON
motocicletas = [
    {"marca": "Yamaha", "cilindrada": "250cc", "precio": 4500},
    {"marca": "Honda", "cilindrada": "300cc", "precio": 5000},
    {"marca": "Kawasaki", "cilindrada": "400cc", "precio": 6000},
]

# Creamos el administrador para un archivo JSON
data_manager = DataManager(ruta_archivo="motocicletas.json", tipo_archivo="json")

# Iniciamos una transacción, escribimos los datos y confirmamos la transacción
data_manager.iniciar_transaccion()
for moto in motocicletas:
    data_manager.escribir_dato(moto)
data_manager.confirmar_transaccion()

# Cambiamos la configuración del archivo a CSV
data_manager.actualizar_configuracion(nueva_ruta="motocicletas.csv", nuevo_tipo="csv")

# Guardamos las mismas instancias en el archivo CSV
data_manager._guardar_archivo()
print("DATOS GUARDADOS")
