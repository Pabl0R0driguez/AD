import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Cargar el dataset
df = pd.read_csv("resultados.csv")  # Asegúrate de tener el archivo CSV

# Calcular el IMC
df["IMC"] = df["Weight"] / (df["Height"] ** 2)

# Convertir "NObeyesdad" a valores numéricos
encoder = LabelEncoder()
df["NObeyesdad_Num"] = encoder.fit_transform(df["NObeyesdad"])

# Convertir la columna "Gender" a valores numéricos
df["Gender_Num"] = encoder.fit_transform(df["Gender"])

# Convertir "family_history_with_overweight" a valores numéricos
df["family_history_with_overweight_Num"] = encoder.fit_transform(
    df["family_history_with_overweight"]
)

# Regresión Lineal Simple
# Seleccionar variables (IMC como X, NObeyesdad como y numérico)
X = df[["IMC"]].values  # Variable independiente
y = df["NObeyesdad_Num"].values  # Variable dependiente convertida

# Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X, y)

# Hacer predicciones
y_pred = model.predict(X)

# Calcular RMSE para regresión lineal simple
rmse_linear = np.sqrt(mean_squared_error(y, y_pred))
print(f"RMSE de la Regresión Lineal Simple: {rmse_linear:.2f}")

# Mostrar coeficientes
print(f"Regresión Lineal Simple:")
print(f"Intercepto (w₀): {model.intercept_:.2f}")
print(f"Pendiente (w₁): {model.coef_[0]:.2f}")

# Seleccionar 30 puntos aleatorios para mostrar en la visualización
indices = np.random.choice(df.index, size=30, replace=False)
X_sample = X[indices]
y_sample = y[indices]
y_pred_sample = y_pred[indices]

# Crear un índice para el eje X
x_indices = np.arange(1, 31)

# Visualización de los datos y las predicciones
plt.scatter(x_indices, y_sample, color="blue", label="Valores reales")  # Puntos reales
plt.plot(
    x_indices, y_pred_sample, color="orange", label="Predicciones"
)  # Línea de predicción
plt.title("Regresión Lineal: IMC vs NObeyesdad")
plt.xlabel("Personas (1 a 30)")
plt.ylabel("NObeyesdad (numérico)")
plt.xticks(x_indices)
plt.legend()
plt.grid(True)
plt.show()

# Regresión Lasso
# Seleccionar múltiples variables predictoras para la regresión Lasso
X_lasso = df[
    ["IMC", "Age", "Gender_Num", "family_history_with_overweight_Num"]
].values  # Variables independientes
y_lasso = df["NObeyesdad_Num"].values  # Variable dependiente

# Separar en conjunto de entrenamiento y prueba (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(
    X_lasso, y_lasso, test_size=0.2, random_state=42
)

# Crear y entrenar el modelo de Regresión Lasso
lasso = Lasso(alpha=1.0)  # Parámetro de regularización λ
lasso.fit(X_train, y_train)

# Hacer predicciones
y_pred_lasso = lasso.predict(X_test)

# Calcular RMSE para regresión Lasso
rmse_lasso = np.sqrt(mean_squared_error(y_test, y_pred_lasso))
print(f"RMSE de la Regresión Lasso: {rmse_lasso:.2f}")

# Mostrar coeficientes para regresión Lasso
print(f"Regresión Lasso:")
print(f"Intercepto (w₀): {lasso.intercept_:.2f}")
for i, col in enumerate(
    ["IMC", "Age", "Gender_Num", "family_history_with_overweight_Num"]
):
    print(f"Pendiente (w₁ para {col}): {lasso.coef_[i]:.2f}")


# Seleccionar 30 puntos aleatorios para mostrar en la visualización
indices = np.random.choice(len(y_test), size=30, replace=False)
y_test_sample = y_test[indices]
y_pred_sample = y_pred_lasso[indices]

# Crear un índice para el eje X
x_indices_lasso = np.arange(1, 31)

# Visualización de resultados: Predicciones vs Valores Reales
plt.scatter(x_indices_lasso, y_test_sample, color="blue", label="Valores reales")
plt.plot(
    x_indices_lasso, y_pred_sample, color="orange", label="Predicciones"
)  # Línea de predicción
plt.xlabel("Personas (1 a 30)")
plt.ylabel("NObeyesdad (numérico)")
plt.title("Regresión Lasso: Predicciones vs Reales (Muestra de 30 datos)")
plt.xticks(x_indices_lasso)
plt.legend()
plt.grid(True)
plt.show()

# Regresión con Random Forest
# Seleccionar múltiples variables predictoras para Random Forest
X_rf = df[
    ["IMC", "Age", "Gender_Num", "family_history_with_overweight_Num"]
].values  # Variables independientes
y_rf = df["NObeyesdad_Num"].values  # Variable dependiente

# Separar en conjunto de entrenamiento y prueba (80%-20%)
X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(
    X_rf, y_rf, test_size=0.2, random_state=42
)

# Crear y entrenar el modelo de Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_rf, y_train_rf)

# Hacer predicciones
y_pred_rf = rf.predict(X_test_rf)

# Calcular RMSE para regresión Random Forest
rmse_rf = np.sqrt(mean_squared_error(y_test_rf, y_pred_rf))
print(f"RMSE de la Regresión Random Forest: {rmse_rf:.2f}")

# Nota: Random Forest no tiene un intercepto y coeficientes interpretables como en la regresión lineal.
print(
    "Regresión Random Forest: No hay coeficientes interpretables como en la regresión lineal."
)


# Seleccionar 30 puntos aleatorios para mostrar en la visualización
indices_rf = np.random.choice(len(y_test_rf), size=30, replace=False)
y_test_sample_rf = y_test_rf[indices_rf]
y_pred_sample_rf = y_pred_rf[indices_rf]

# Crear un índice para el eje X
x_indices_rf = np.arange(1, 31)

# Visualización de resultados: Predicciones vs Valores Reales
plt.scatter(x_indices_rf, y_test_sample_rf, color="blue", label="Valores reales")
plt.plot(
    x_indices_rf, y_pred_sample_rf, color="orange", label="Predicciones"
)  # Línea de predicción
plt.xlabel("Personas (1 a 30)")
plt.ylabel("NObeyesdad (numérico)")
plt.title("Regresión con Random Forest: Predicciones vs Reales (Muestra de 30 datos)")
plt.xticks(x_indices_rf)
plt.legend()
plt.grid(True)
plt.show()

# Identificación y eliminación de outliers utilizando el método IQR
Q1 = df["NObeyesdad_Num"].quantile(0.25)
Q3 = df["NObeyesdad_Num"].quantile(0.75)
IQR = Q3 - Q1

# Definir límites para detectar outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtrar el DataFrame para eliminar outliers
df_no_outliers = df[
    (df["NObeyesdad_Num"] >= lower_bound) & (df["NObeyesdad_Num"] <= upper_bound)
]

# Regresión con Random Forest (sin outliers)
# Seleccionar múltiples variables predictoras para Random Forest
X_rf_no_outliers = df_no_outliers[
    ["IMC", "Age", "Gender_Num", "family_history_with_overweight_Num"]
].values  # Variables independientes
y_rf_no_outliers = df_no_outliers["NObeyesdad_Num"].values  # Variable dependiente

# Separar en conjunto de entrenamiento y prueba (80%-20%)
(
    X_train_rf_no_outliers,
    X_test_rf_no_outliers,
    y_train_rf_no_outliers,
    y_test_rf_no_outliers,
) = train_test_split(X_rf_no_outliers, y_rf_no_outliers, test_size=0.2, random_state=42)

# Crear y entrenar el modelo de Random Forest (sin outliers)
rf_no_outliers = RandomForestRegressor(n_estimators=100, random_state=42)
rf_no_outliers.fit(X_train_rf_no_outliers, y_train_rf_no_outliers)

# Hacer predicciones
y_pred_rf_no_outliers = rf_no_outliers.predict(X_test_rf_no_outliers)

# Calcular RMSE para regresión Random Forest (sin outliers)
rmse_rf_no_outliers = np.sqrt(
    mean_squared_error(y_test_rf_no_outliers, y_pred_rf_no_outliers)
)
print(f"RMSE de la Regresión Random Forest (sin outliers): {rmse_rf_no_outliers:.2f}")

# Seleccionar 30 puntos aleatorios para mostrar en la visualización
indices_rf_no_outliers = np.random.choice(
    len(y_test_rf_no_outliers), size=30, replace=False
)
y_test_sample_rf_no_outliers = y_test_rf_no_outliers[indices_rf_no_outliers]
y_pred_sample_rf_no_outliers = y_pred_rf_no_outliers[indices_rf_no_outliers]

# Crear un índice para el eje X
x_indices_rf_no_outliers = np.arange(1, 31)

# Visualización de resultados: Predicciones vs Valores Reales
plt.scatter(
    x_indices_rf_no_outliers,
    y_test_sample_rf_no_outliers,
    color="blue",
    label="Valores reales",
)
plt.plot(
    x_indices_rf_no_outliers,
    y_pred_sample_rf_no_outliers,
    color="orange",
    label="Predicciones",
)  # Línea de predicción
plt.xlabel("Personas (1 a 30)")
plt.ylabel("NObeyesdad (numérico)")
plt.title(
    "Regresión con Random Forest (sin outliers): Predicciones vs Reales (Muestra de 30 datos)"
)
plt.xticks(x_indices_rf_no_outliers)
plt.legend()
plt.grid(True)
plt.show()
