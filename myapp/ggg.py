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
score = model.score(X_test, y_test)
print("R2 Score:", score)

# Save model
joblib.dump(model, "solar_model1.pkl")