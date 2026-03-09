# ==============================
# WIND ENERGY PREDICTION
# Using Linear Regression
# ==============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# ------------------------------
# 1. Read CSV File
# ------------------------------
df = pd.read_csv("C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Wind//wind.csv")

print("Dataset Preview:")
print(df.head())

print("\nColumns in Dataset:")
print(df.columns)

# ------------------------------
# 2. Select Input and Output
# (Change column names if needed)
# ------------------------------
X = df[["windspeed_100m"]]        # Independent variable
y = df["Power"]          # Dependent variable

# ------------------------------
# 3. Train Test Split
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------------
# 4. Create & Train Model
# ------------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# ------------------------------
# 5. Model Equation
# ------------------------------
intercept = model.intercept_
slope = model.coef_[0]

print("\nModel Equation:")
print(f"WindPower = {intercept:.4f} + ({slope:.4f} × WindSpeed)")

# ------------------------------
# 6. Prediction
# ------------------------------
y_pred = model.predict(X_test)

# Example: Predict for new value
new_speed = np.array([[10]])  # Wind speed = 10
predicted_power = model.predict(new_speed)
print("\nPrediction for WindSpeed=10:", predicted_power[0])

# ------------------------------
# 7. Evaluation
# ------------------------------
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("\nModel Performance:")
print("R2 Score:", r2)
print("MSE:", mse)

# ------------------------------
# 8. Graph 1: Scatter + Regression Line
# ------------------------------
plt.figure(figsize=(8,6))
plt.scatter(X, y)
plt.plot(X, model.predict(X), linewidth=2)
plt.xlabel("Wind Speed")
plt.ylabel("Wind Power")
plt.title("Wind Speed vs Wind Power (Linear Regression)")
plt.show()

# ------------------------------
# 9. Graph 2: Actual vs Predicted
# ------------------------------
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Wind Power")
plt.ylabel("Predicted Wind Power")
plt.title("Actual vs Predicted Wind Power")
plt.show()