from pathlib import Path

class FileManager:
    #Método constructor siempre contiene self.
    #Path, para trabajar con rutas de archivos
 def __init__(self, path):
     self.path = Path(path)

 def create_directory(self):
     #Comprobamos que no haya un directorio ya creado
     if not self.path.exists():
         #Creamos directorio
         self.path.mkdir()
         print(f'Directorio {self.path} creado.')
     else:
         print(f'El directorio {self.path} ya existe.')
         
 def list_files(self):
     #Comprobamos que no haya un directorio ya creado y
     #is_dir comprueba si se ha creado un directorio
     if self.path.exists() and self.path.is_dir():
         #iterdir, lista los archios y directorios creados
         return list(self.path.iterdir())
    #Si no existe devuelve una lista vacía 
     return []

 def delete_directory(self):
     if self.path.exists() and self.path.is_dir():
         #rmdir borra el directorio creado 
         self.path.rmdir()
         print(f'Directorio {self.path} eliminado.')


#Creación del directorio
file_manager = FileManager('test_directory')
file_manager.create_directory()
#Imprimimos los archivos que contenga el drierctorio
print(file_manager.list_files())
#Borramos el directorio
file_manager.delete_directory()
