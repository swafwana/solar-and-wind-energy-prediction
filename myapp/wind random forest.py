import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Wind//wind.csv")

# -----------------------------
# 2. Convert Time Column
# -----------------------------
df["Time"] = pd.to_datetime(df["Time"])
df["hour"] = df["Time"].dt.hour
df["month"] = df["Time"].dt.month

# Drop original Time column
df = df.drop("Time", axis=1)

# -----------------------------
# 3. Separate Features & Target
# -----------------------------
X = df.drop("Power", axis=1)
y = df["Power"]

# -----------------------------
# 4. Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 5. Create Random Forest Model
# -----------------------------
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

# Train model
model.fit(X_train, y_train)

# 6. Evaluate Model
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("Model Performance")
print("-----------------")
print("R2 Score:", r2)
print("MAE:", mae)

# =============================
# 7. PLOTS (PASTE HERE)
# =============================

import matplotlib.pyplot as plt

# Actual vs Predicted Plot
plt.figure()
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Power")
plt.ylabel("Predicted Power")
plt.title("Actual vs Predicted Power")
plt.show()

# Feature Importance Plot
importances = model.feature_importances_
features = X.columns

plt.figure()
plt.bar(features, importances)
plt.xticks(rotation=45)
plt.xlabel("Features")
plt.ylabel("Importance")
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

# =============================
# 8. Save Model
# =============================

joblib.dump(model, "power_prediction_model1.pkl")
print("\nModel saved as power_prediction_model.pkl")