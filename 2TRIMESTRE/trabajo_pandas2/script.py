import pandas as pd 
from sklearn.model_selection import train_test_split

import numpy as np
import matplotlib.pyplot as plt


# Mostramos el dataset
df = pd.read_csv("resultados.csv")
print(df)


# EJERCICIO 1
print("EJERCICIO 1")
# Calcular el rango intercuartil (IQR) para la columna height
print("Primer cuartil:")
q1 = df["Age"].quantile(0.25)  # Primer cuartil
print(q1)
print("Segundo cuartil:")
q3 = df["Age"].quantile(0.75)  # Tercer cuartil
print(q3)
iqr = q3 - q1  # Rango intercuartil


# Definir los límites inferior y superior
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
print(f"Límite inferior: {lower_bound}, Límite superior: {upper_bound}")




# Filtrar valores dentro de los límites
df_sin_atipicos = df[(df["Age"] >= lower_bound) & (df["Age"] <= upper_bound)]
# Comparar el número de filas antes y después
print(f"Filas antes: {df.shape[0]}")
print(f"Filas después de eliminar atípicos: {df_sin_atipicos.shape[0]}")




# EJERCICIO 2
print("EJERCICIO 2")


# Calcular los valores mínimo y máximo de la columna 'Height'
min_height = df["Height"].min()
max_height = df["Height"].max()


print(f"Mínimo altura: {min_height}")
print(f"Máximo altura: {max_height}")


# Normalizar la columna 'Height'
df["Height_norm"] = (df["Height"] - min_height) / (max_height - min_height)
# Mostrar los resultados
print(df[["Height", "Height_norm"]].head())




# EJERCICIO 3
print("EJERCICIO 3")


# Crear una nueva columna para determinar si hay historial familiar de sobrepeso
def determinar_resultado(row):
   # Puedes definir el resultado según la lógica que necesites
   return row[
       "family_history_with_overweight"
   ]  # En este caso solo regresamos la misma categoría.


df["resultado"] = df.apply(determinar_resultado, axis=1)


# Mostrar un ejemplo de los datos con la nueva columna 'resultado'
print("\nDatos con la nueva columna 'resultado':")
print(df[["Gender", "Age", "Height", "Weight", "resultado"]].head())


# Aplicar One-Hot Encoding a la columna "resultado"
df_encoded = pd.get_dummies(df, columns=["resultado"], drop_first=False)


# Mostrar un ejemplo de los datos codificados
print("\nDatos después de aplicar One-Hot Encoding:")
print(df_encoded.head())


# EJERCICIO 4
# Separar las variables predictoras (X) y objetivo (y)
X = df.drop(columns=["Weight", "CALC", "MTRANS"])  # Columnas predictoras
y = df["NObeyesdad"]                # Variable objetivo

# Mostrar las primeras filas de las columnas predictoras (X)
print("Primeras filas de las columnas predictoras (X):")
print(X.head())

# Mostrar las primeras filas de la variable objetivo (y)
print("\nPrimeras filas de la variable objetivo (y):")
print(y.head())
