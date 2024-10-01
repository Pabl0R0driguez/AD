#Pedimos los lados del rectángulo
lado1 = float(input("Introduce el tamaño del lado del rectángulo:"))
lado2 = float(input("Introduce el tamaño del segundo lado del rectángulo:"))

#Función para calcular el area del rectángulo
def calcular_area(lado1,lado2):
    resultado = lado1 * lado2
    return "El área del rectángulo es: " , resultado 

#Imprimimos la función     
print(calcular_area(lado1,lado2))
