#Importamos la librería random para posteriormente usar la función .append
import random
#Creamos un array para guardar los números que generemos 
numeros_aleatorios = []

#Creamos un bucle de 10 números
for i in range(1,11):
    #En la variable aleatorio se guardarán números aleatorios del 1 al 50
    numeros_aleatorios.append(random.randint(1,50))

#Creamos la varible auxiliar fallos
fallos = 0
#Pedimos número por teclado
numero = int(input("Introduce un número: "))

#Si la variable numero esta en la lista, devulve True e imprimimos Acierto
if ((numero) in numeros_aleatorios) == True:
    print("Acierto")
#Si no imprimimos fallo
else:
    print("Fallo")
    

#Imprimimos
print(numeros_aleatorios)

             
