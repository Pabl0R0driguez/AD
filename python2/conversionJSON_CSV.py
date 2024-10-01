import csv
import json
class FileConverter:
    #Creamos la función write_json, con la que crearemos nuestro archivo .json
    def write_json(self,file_path,content):
        try:                
            with open(file_path, mode='w') as f:
                #Usamos el método .dump para escribir en json(le pasamos el content que
                #es la variable diccionario y el file(f)
                json.dump(content,f)                  
        except Exception as e:
            print(f"Error escribiendo en el archivo: {e}")
    #Creamos la función read_json, que usaremos para leer el json creado 
    def read_json(self,file_path):
        try:
            with open(file_path, 'r') as file:
                #Esta función nos devolverá el fichero creado
                return json.load(file)
        except Exception as e:
            print(f"Error escribiendo en el archivo: {e}")

    #Con la función json_to_csv, conseguiremos convertir el archivo en csv, para ello
    #le pasaremos como parámetros json_file y csv_file que usaremos dentro
    def json_to_csv(self,json_file,csv_file):
         try:
             with open(json_file, mode='r', newline='') as f:
                
                reader = json.load(f)
                rows = list(reader.keys())     
             with open(csv_file, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows)
                writer.writeheader() 
                writer.writerow(reader) 
         except Exception as e:
             print(f"Error en la conversión: {e}")


                                       
        
archivo = FileConverter()
diccionario = {"DNI" : "30216383H" , "FechaNacimiento" : "02-05-2005"}
#Creo archivo y le añadimos el mapa
archivo.write_json('data.json', diccionario)
archivo.read_json('data.json')

converter = FileConverter()
converter.json_to_csv( 'data.json','data.csv')
