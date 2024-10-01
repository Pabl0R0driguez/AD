import json
from pathlib import Path

class JSONFileHandler:
    def write_json(self,file_path,content):
        try:                
            with open(file_path, mode='w') as f:
                json.dump(content,f)                  
        except Exception as e:
            print(f"Error escribiendo en el archivo: {e}")
                             
    def read_json(self,file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error escribiendo en el archivo: {e}")
                                       
        
archivo = JSONFileHandler()
a = {"30216383H" : "02/05/2005"}
#Creo archivo y le añadimos el mapa
archivo.write_json('data.json', a)
print(archivo.read_json('data.json'))
