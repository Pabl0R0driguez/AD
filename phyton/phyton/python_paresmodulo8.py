#Pedimos número
numero = int(input("Introduce un número: "))

#Si el número introducido dividido entre 2 es 0
#Recorreme desde el 0 hasta el número introducido mostrandome solo los números pares
if(numero % 2 == 0):
    print("Números pares hasta el " ,numero)
    for i in range(0 , numero,2):
        print(i)
#Si no imprimeme el número impar introducido
else:
    print("Número impar introducido" , numero)

