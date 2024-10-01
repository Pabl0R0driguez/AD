#Creamos un array llamado lista para almacenar los números
lista = []

#Recorremos del 1 al 10
for i in range (1,11):
    #La lista irá de 3 en 3, guardamos en la variable numero
    numero = i * 3

    #Finalmente añadimos la variable numero a la lista e imprimimos
    lista.append(numero)
    
print(lista)
