import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import OrdinalEncoder


# Cargar el dataset
df = pd.read_csv("resultados.csv")

# Convertir las columnas a tipo numérico, forzando la conversión de errores a NaN
df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce")
df["Height"] = pd.to_numeric(df["Height"], errors="coerce")
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Gender"] = df["Gender"].map(
    {"Male": 1, "Female": 0}
)  # Convertir 'Gender' a valores numéricos

# Aplicar One-Hot Encoding a todas las columnas categóricas excepto "NObeyesdad"
columnas_categoricas = [
    "family_history_with_overweight",
    "FAVC",
    "CAEC",
    "SMOKE",
    "SCC",
    "CALC",
    "MTRANS",
]
df_encoded = pd.get_dummies(df, columns=columnas_categoricas, drop_first=True)

# Convertir la variable objetivo "NObeyesdad" a valores numéricos
obesity_mapping = {
    "Insufficient_Weight": 0,
    "Normal_Weight": 1,
    "Overweight_Level_I": 2,
    "Overweight_Level_II": 3,
    "Obesity_Type_I": 4,
    "Obesity_Type_II": 5,
    "Obesity_Type_III": 6,
}
df_encoded["NObeyesdad"] = df["NObeyesdad"].map(obesity_mapping)

# Crear las variables IMC, PBF y REE

# Calcular el Índice de Masa Corporal (IMC)
df_encoded["IMC"] = df_encoded["Weight"] / (df_encoded["Height"] ** 2)

# Calcular el Porcentaje de Grasa Corporal (PBF)
df_encoded["PBF"] = (
    (1.20 * (df_encoded["Weight"] / (df_encoded["Height"] ** 2)))
    + (0.23 * df_encoded["Age"])
    - (10.8 * df_encoded["Gender"])
    - 5.4
)

# Calcular el Gasto Energético en Reposo (REE)
df_encoded["REE"] = (
    (10 * df_encoded["Weight"])
    + (6.25 * df_encoded["Height"] * 100)
    - (5 * df_encoded["Age"])
    + (5 * df_encoded["Gender"] - 161 * (1 - df_encoded["Gender"]))
)
correlacion = df_encoded["Weight"].corr(df_encoded["NObeyesdad"])
print(f"Correlación entre 'Weight' y 'NObeyesdad': {correlacion:.4f}")


# 1. Identificación de valores nulos en las variables
valores_nulos = df_encoded[["IMC", "Weight", "PBF", "REE"]].isnull().sum()
porcentaje_nulos = (
    df_encoded[["IMC", "Weight", "PBF", "REE"]].isnull().sum() / len(df_encoded)
) * 100
print("Valores nulos por columna:")
print(valores_nulos)
print("\nPorcentaje de valores nulos por columna:")
print(porcentaje_nulos)

# 2. Identificación de errores en los datos
errores = {
    "Weight": df_encoded["Weight"] < 0,  # Peso negativo
    "IMC": df_encoded["IMC"] < 10,  # IMC poco realista
    "PBF": df_encoded["PBF"] < 0,  # Porcentaje de grasa corporal negativo
    "REE": df_encoded["REE"] < 0,  # Tasa metabólica en reposo negativa
}

# Mostrar registros con errores
for columna, condicion in errores.items():
    print(f"\nErrores en la columna {columna}:")
    print(df_encoded[condicion])

# 3. Identificación de outliers con boxplots
fig, axes = plt.subplots(1, 4, figsize=(16, 6))

# Graficamos boxplots para detectar outliers
sns.boxplot(y=df_encoded["Weight"], ax=axes[0], color="lightblue")
axes[0].set_title("Valores atípicos en Weight")

sns.boxplot(y=df_encoded["IMC"], ax=axes[1], color="lightcoral")
axes[1].set_title("Valores atípicos en IMC")

sns.boxplot(y=df_encoded["PBF"], ax=axes[2], color="lightgreen")
axes[2].set_title("Valores atípicos en PBF")

sns.boxplot(y=df_encoded["REE"], ax=axes[3], color="lightyellow")
axes[3].set_title("Valores atípicos en REE")

plt.tight_layout()
plt.show()

# 4. Tratamiento de valores nulos, errores y outliers
# Imputar valores nulos con la media (puede usar mediana si se prefiere)
df_encoded["IMC"] = df_encoded["IMC"].fillna(df_encoded["IMC"].mean())
df_encoded["Weight"] = df_encoded["Weight"].fillna(df_encoded["Weight"].mean())
df_encoded["PBF"] = df_encoded["PBF"].fillna(df_encoded["PBF"].mean())
df_encoded["REE"] = df_encoded["REE"].fillna(df_encoded["REE"].mean())

# 5. Corregir errores en datos
# Eliminamos registros con datos erróneos (por ejemplo, peso negativo)
df_encoded = df_encoded[~(df_encoded["Weight"] < 0)]
df_encoded = df_encoded[~(df_encoded["IMC"] < 10)]
df_encoded = df_encoded[~(df_encoded["PBF"] < 0)]
df_encoded = df_encoded[~(df_encoded["REE"] < 0)]

# 6. Tratamiento de outliers
# Limitar valores atípicos en columnas, sustituyendo por valores máximos/mínimos permitidos
# Para simplificar, sustituimos outliers de IMC y PBF por percentiles 1% y 99%

# Limitar outliers en IMC
IMC_lower = df_encoded["IMC"].quantile(0.01)
IMC_upper = df_encoded["IMC"].quantile(0.99)
df_encoded["IMC"] = df_encoded["IMC"].clip(lower=IMC_lower, upper=IMC_upper)

# Limitar outliers en PBF
PBF_lower = df_encoded["PBF"].quantile(0.01)
PBF_upper = df_encoded["PBF"].quantile(0.99)
df_encoded["PBF"] = df_encoded["PBF"].clip(lower=PBF_lower, upper=PBF_upper)

# 7. Mostrar el DataFrame limpio
print("\nDataset después de limpieza:")
print(df_encoded.head())


# Evaluación de la necesidad de normalizar/escalar:

# Evaluación de si necesitamos normalizar/escala
numeric_columns = df_encoded.select_dtypes(include=["float64", "int64"]).columns

# Para columnas con escalas muy distintas, normalizamos o estandarizamos
scaler = StandardScaler()  # Para estandarización (media=0, std=1)
df_encoded[numeric_columns] = scaler.fit_transform(df_encoded[numeric_columns])

# Si preferimos usar Min-Max Scaling (rango entre 0 y 1)
# scaler = MinMaxScaler()
# df_encoded[numeric_columns] = scaler.fit_transform(df_encoded[numeric_columns])

# Comprobación de los resultados
print(df_encoded.head())


# Evaluación de la necesidad de hacer One-Hot Encoding o Codificación Ordinal

# Identificación de columnas categóricas
categorical_columns = df.select_dtypes(include=["object"]).columns

# Evaluar el número de categorías únicas
for col in categorical_columns:
    print(f"Columna: {col} - Número de categorías únicas: {df[col].nunique()}")

# Aplicar One-Hot Encoding a las columnas con pocas categorías únicas
one_hot_columns = [col for col in categorical_columns if df[col].nunique() <= 10]
df_encoded = pd.get_dummies(df, columns=one_hot_columns, drop_first=True)

print("\nDespués del One-Hot Encoding:")
print(df_encoded.head())

# Identificar columnas con muchas categorías (más de 10)
ordinal_columns = [col for col in categorical_columns if df[col].nunique() > 10]

# Aplicar codificación ordinal a las columnas seleccionadas
encoder = OrdinalEncoder()
df_encoded[ordinal_columns] = encoder.fit_transform(df[ordinal_columns])

print("\nDespués de la Codificación Ordinal:")
print(df_encoded.head())
