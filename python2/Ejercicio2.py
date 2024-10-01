from pathlib import Path
class FileHandler:
    #Creamos la función read_file para leer el fichero
    def read_file(self, file_path, mode='r'):
        try:
            with open(file_path, mode) as f:
                 content = f.read()
                 return content
        except Exception as e:
            print(f"Error leyendo el archivo: {e}")

    #Función write_file para escribir el archivo       
    def write_file(self, file_path, content, mode='w'):
        try:
             with open(file_path, mode) as f:
                 f.write(content)
        except Exception as e:
             print(f"Error escribiendo en el archivo: {e}")


archivo = FileHandler()
#Escribimos en el fichero .txt 
archivo.write_file ("30216383H.txt" , "02-05-2005")
#Imprimimos el fichero
print(archivo.read_file("30216383H.txt"))

