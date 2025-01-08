import pandas as pd
import numpy as np


# EJERCICIO 1

# Mostramos el dataset
print("Resultados del dataset")
df = pd.read_csv("resultados.csv")
print(df)

# EJERCICIO 2

# Exploración básica del DataFrame
print("Forma del DataFrame (filas, columnas):")
print(df.shape)

print("\nPrimeras 5 filas del DataFrame:")
print(df.head())

print("\nInformación general del DataFrame:")
print(df.info())

print("\nResumen estadístico de las columnas numéricas:")
print(df.describe())


# EJERCICIO 3

# Seleccionamos 4 columnas representativas
columnas_representativas = ["Gender", "Age", "MTRANS", "FAF"]
df_seleccion = df[columnas_representativas]

# Mostramos las primeras 5 filas de las columnas seleccionadas
print("\n")
print("Selección de 4 columnas representativas (5 primeras filas):")
print(df_seleccion.head())


# EJERICIO 4

# Añadir una nueva columna 'water_intake_per_meal' con la ingesta de agua por comida
df["water_intake_per_meal"] = df["CH2O"] / df["NCP"]

nuevas_columnas_representativas = [
    "Gender",
    "Age",
    "MTRANS",
    "FAF",
    "water_intake_per_meal",
]
df_seleccion_nueva_columna = df[nuevas_columnas_representativas]

print("\n")
print("Mostramos las columnas rerpesentativas + la nueva columna")
print(df_seleccion_nueva_columna.head())


# EJERCICIO 5

# Mostramos las filas donde el paciente es fumador y bebe frecuentemente
columnas_seleccion = [
    "Gender",
    "Age",
    "Height",
    "Weight",
    "SMOKE",
    "CALC",
]

fumadores_bebedores = df[(df["SMOKE"] == "yes") & (df["CALC"] == "Frequently")]
print("\n")
print("\nPersonas fumadoras y que consumen alchol de manera frecuente ")
print(fumadores_bebedores[columnas_seleccion])


# Añadir una fila de valores nulos
nueva_fila_nula = pd.DataFrame(
    [{col: np.nan for col in df.columns}]
)  # Crear una fila con NaN
df = pd.concat([df, nueva_fila_nula], ignore_index=True)  # Agregar la fila al DataFrame

# Verificar y mostrar las filas con valores nulos
valores_nulos = df[df.isnull().any(axis=1)]
print("\nFilas con valores nulos:")
print(valores_nulos)


# Contamos el número de filas de nuestro csv
print("\nNumero de registros del csv:")
print(df.shape[0])


# Borramos filas con valores nulos y mostramos el número luego de eliminarlas
df_limpio = df.dropna()  # Crear un nuevo DataFrame sin valores nulos
print("Numero de registros despues de eliminar las filas con valores nulos")
print(f"\nFilas después: {df_limpio.shape[0]}")


# Ejercicio 7
print("6 primeras filas, antes de rellenar valores nulos")
print(df.head(6))

# Reemplazar valores nulos con "Nulo Rellenado"
df_rellenado = df.fillna("Nulo rellenado")

# Mostrar el DataFrame después de reemplazar los valores nulos
print("6 primeras filas, después de rellenar valores nulos")
print(df_rellenado.head(6))

# Ejercicio
# Agrupamos por consumo de alimentos entre comidas
alimentos_entre_comidas = df.groupby("CAEC").size()
print("\nAgrupacion por consumo de alimentos entre comidas")
print(alimentos_entre_comidas)

# Agrupamos por frecuencia de consumo de alcohol ("CALC") y tipo de obesidad ("OBESITY")
agrupacion = (
    df.groupby(["CALC", "NObeyesdad"]).size().reset_index(name="Numero de Personas")
)

# Mostrar resultados
print(
    "\nNúmero de personas según la frecuencia de consumo de alcohol y tipo de obesidad:"
)
print(agrupacion)


# Calcular el promedio de una columna específica
promedio_peso = df["Weight"].mean()
print("\n")
# Imprimir el promedio
print(f"El promedio de la columna de peso es: {promedio_peso}" + " kg")