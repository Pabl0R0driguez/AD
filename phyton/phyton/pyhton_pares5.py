#Pedimos número entero
numero = int(input("Introduce número entero: "))

#Mientras numero sea < 0, introduce número positivo
while(numero < 0):
    input("Introduce número positivo: ")

#Recorre del 0 al número introducido de 2 en 2
for i in range (0,numero,2):
        print (i)
