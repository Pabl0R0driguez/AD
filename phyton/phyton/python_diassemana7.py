#Pedimos un número del 1 al 7
numero = int(input("Introduce un número del 1 al 7 : "))
while numero < 1 | numero > 7:
    numero = int(input("Introduce un número del 1 al 7 : "))
#Si introducimos 1, imprimirá lunes y así sucesivamente hasta el 7  
if numero == 1:
    print("Lunes")
elif numero == 2:
    print("Martes")
if numero == 3:
    print("Miércoles")
elif numero == 4:
    print("Jueves")
elif numero == 5:
    print("Viernes")
elif numero == 6:
    print("Sábado")
elif numero == 7:
    print("Domingo")
