import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("resultados.csv")
data = pd.DataFrame(df)

import matplotlib.pyplot as plt
import pandas as pd


# 1.DIAGRAMA DE BARRAS

df_filtered = df.iloc[:100]  # Filtrar las primeras 400 personas
df_sorted = df_filtered.sort_values(by="Age")  # Ordenar por Edad

# Gráfico de líneas (Edad vs Peso, usando el DataFrame ordenado)
plt.plot(
    df_sorted["Age"],
    df_sorted["Weight"],  # Usamos el Peso del mismo DataFrame ordenado
    linestyle="-",
    color="red",
    linewidth=1,
    label="Edad y Peso",
)
# Configuración del gráfico
plt.title("Gráfico de líneas: Edad y Peso ")
plt.xlabel("Edad")
plt.ylabel("Peso")
plt.legend()
plt.grid()
correlacion = df_sorted["Age"].corr(df_sorted["Weight"])
print("Coeficiente de correlación:", correlacion)

plt.show()


# 2.DIAGRAMA DE BARRAS
# Contar el número de personas en cada categoría de CAEC
conteo_caec = df["CAEC"].value_counts()
# Crear gráfico de barras
plt.bar(conteo_caec.index, conteo_caec.values, color="orange", edgecolor="black")
# Etiquetas y título
plt.title("Número de Personas según Consumo de Alimentos Entre Comidas (CAEC)")
plt.xlabel("Categorías de Consumo (CAEC)")
plt.ylabel("Número de Personas")

# Mostrar el gráfico
plt.show()


# 3.HISTOGRAMA
# Crear histograma de la columna 'Height'
plt.figure(figsize=(8, 5))  # Ajustar el tamaño del gráfico
plt.hist(df["Height"], bins=20, color="green", alpha=0.7, edgecolor="black")
# Etiquetas y título
plt.title("Distribución de la Estatura (Height)")
plt.xlabel("Altura (cm)")
plt.ylabel("Frecuencia")
# Mostrar el gráfico
plt.show()


# 4.GRÁFICO DE DISPERSIÓN
# (Altura vs Peso)
plt.scatter(df["Height"], df["Weight"], color="purple", alpha=0.6)
plt.title("Altura vs Peso")
plt.xlabel("Altura (m)")
plt.ylabel("Peso (kg)")
plt.show()


# 5.GRÁFICO DE CAJA
# (Distribución de actividad física FAF)
plt.boxplot(df.dropna()["FAF"], patch_artist=True, boxprops=dict(facecolor="lightblue"))
plt.title("Distribución de actividad física")
plt.show()
