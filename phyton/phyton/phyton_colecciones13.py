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
#Recorremos el array
for l in numeros_aleatorios:
#Si el número introducido por teclado coincide
#con algún número del array imprime BINGO
    if(numero == l):
        print("BINGO")
    #Si no coincide el número, se le sumará uno la variable 
    else:
        fallos = fallos +1
#Si tu número no es igual a ninguno de los 10, imprimes has perdido
if(fallos == 10):
    print("Has perdido")
    

#Imprimimos
print(numeros_aleatorios)

             
