#Pedimos dos núemros por teclado
numero = float(input("Introduce el primer número:"))
numero2 = float(input("Introduce el segundo número: "))

#Creamos una función para poder comparar los números 
def numero_mayor(numero,numero2):
    if(numero > numero2):
        return numero
    else:
        return numero2

#Guardamos en la variable mayor la función numero_mayor   
mayor = numero_mayor(numero,numero2)
#Imprimimos la variable mayor
print ("El número mayor es: " ,mayor)
