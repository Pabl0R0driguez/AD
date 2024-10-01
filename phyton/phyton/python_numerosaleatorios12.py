#Importamos la librería random para posteriormente usar la función .append
import random
#Creamos un array para guardar los números que generemos 
numeros_aleatorios = []

#Creamos un bucle de 10 números
for i in range(1,10):
    #En la variable aleatorio se guardarán números aleatorios del 1 al 50
    aleatorio = random.randint(1,50)
    #Añadimos la variable aleatorio a nuestra lista
    numeros_aleatorios.append(aleatorio)

#Imprimimos
print(numeros_aleatorios)
