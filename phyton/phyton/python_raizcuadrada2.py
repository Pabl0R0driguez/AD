#Importamos libreria math
import math
#Pregunta por el número
numero = input("Introduce un número por favor. ");
#Transformamos la cadena de texto en float
numero_float = float(numero);
#LLamamos la funcion sqrt y guarda resultado en numero_float
raiz_cuadrada = math.sqrt(numero_float);
#Imprimimos 
print("La raíz cuadrada es: " , raiz_cuadrada);
