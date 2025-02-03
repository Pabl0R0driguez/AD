import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("resultados.csv")
data = pd.DataFrame(df)

# Gráfico de líneas (Edad vs Peso, ignorando valores NaN)
plt.plot(df.dropna()["Age"], df.dropna()["Weight"], marker="o", linestyle="-", color="blue", label="Edad vs Peso")
plt.title("Gráfico de líneas: Edad vs Peso")
plt.xlabel("Edad")
plt.ylabel("Peso")
plt.legend()
plt.show()

# Gráfico de barras (Comparación de consumo de agua CH2O por género)
gender_groups = df.groupby("Gender")["CH2O"].mean()
plt.bar(gender_groups.index, gender_groups.values, color="orange", edgecolor="black")
plt.title("Consumo promedio de agua por género")
plt.xlabel("Género")
plt.ylabel("Consumo de agua (CH2O)")
plt.show()

# Histograma (Distribución del peso)
plt.hist(df["Weight"], bins=5, color="green", alpha=0.7, edgecolor="black")
plt.title("Distribución del peso")
plt.xlabel("Peso")
plt.ylabel("Frecuencia")
plt.show()

# Gráfico de dispersión (Altura vs Peso)
plt.scatter(df["Height"], df["Weight"], color="purple", alpha=0.6)
plt.title("Altura vs Peso")
plt.xlabel("Altura (m)")
plt.ylabel("Peso (kg)")
plt.show()

# Gráfico de sectores (Distribución por género)
gender_counts = df["Gender"].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", startangle=90)
plt.title("Distribución por género")
plt.show()

# Gráfico de caja (Distribución de actividad física FAF)
plt.boxplot(df.dropna()["FAF"], patch_artist=True, boxprops=dict(facecolor="lightblue"))
plt.title("Distribución de actividad física")
plt.show()


# Gráfico de líneas

# Gráfico de dispersión

# Gráfico de barras

# Histograma

# Diagrama de cajas