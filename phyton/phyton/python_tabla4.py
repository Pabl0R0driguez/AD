#Importamos librería math
import math
#Pedimos número
numero = int(input("Introduce número entero: "))

#Creamos la variable a que será igual a 1
a = 1
#Mientras a sea menor que 10: 
while a<10:
    #Guardamos en la variable resultado el número introducido * la variable a
    resultado = numero * a
    #Imprimimos 
    print(a, "* " , numero , "= " , resultado)
    #La variable a se irá incrementando de 1 en 1 al imprimir 
    a = a + 1
