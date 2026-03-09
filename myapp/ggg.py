import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
df = pd.read_csv("C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Solar//preprocessed.csv")

# Convert Timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Optional time features (VERY IMPORTANT for solar)
df["hour"] = df["Timestamp"].dt.hour
df["month"] = df["Timestamp"].dt.month

# Features
X = df[[
    "ApparentTemperature",
    "AirTemperature",
    "DewPointTemperature",
    "RelativeHumidity",
    "WindSpeed",
    "WindDirection",
    "hour",
    "month"
]]

y = df["SolarGeneration"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
train_score = model.score(X_train, y_train)
print("Train R2 Score:", train_score)
score = model.score(X_test, y_test)
print("Test R2 Score:", score)


# Save model
joblib.dump(model, "solar_model.pkl")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Predict on test data
y_pred = model.predict(X_test)

# ===============================
# 1️⃣ ACTUAL vs PREDICTED
# ===============================
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()])

plt.xlabel("Actual Solar Generation")
plt.ylabel("Predicted Solar Generation")
plt.title("Actual vs Predicted Solar Generation")
plt.show()


# ===============================
# 2️⃣ FEATURE IMPORTANCE
# ===============================
importance = model.feature_importances_
feature_names = X.columns

feat_imp = pd.Series(importance, index=feature_names)
feat_imp = feat_imp.sort_values()

plt.figure(figsize=(8,6))
feat_imp.plot(kind='barh')

plt.xlabel("Importance Score")
plt.title("Feature Importance")
plt.show()


# ===============================
# 3️⃣ SOLAR GENERATION vs HOUR
# ===============================
hourly_avg = df.groupby("hour")["SolarGeneration"].mean()

plt.figure(figsize=(8,6))
hourly_avg.plot()

plt.xlabel("Hour of Day")
plt.ylabel("Average Solar Generation")
plt.title("Average Solar Generation by Hour")
plt.show()