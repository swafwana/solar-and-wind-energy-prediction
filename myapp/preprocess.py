import pandas as pd
import numpy as np

# File paths
p = "C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Solar//Weather_Data_reordered_all_Final.csv"
s = "C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Solar//Solar_Energy_Generation_Formatted.csv"

# ================= LOAD WEATHER DATA (FINAL FIX) =================

weatherdata = pd.read_csv(p, header=None)

# Split using tab
weatherdata = weatherdata[0].str.split('\t', expand=True)

print("Detected columns after split:", weatherdata.shape[1])
print(weatherdata.head(5))

# ✅ Drop first row (it's header garbage)
weatherdata = weatherdata.drop(0).reset_index(drop=True)

# ✅ Now assign correct 8 columns
if weatherdata.shape[1] == 8:
    weatherdata.columns = [
        "CampusKey",
        "Timestamp",
        "ApparentTemperature",
        "AirTemperature",
        "DewPointTemperature",
        "RelativeHumidity",
        "WindSpeed",
        "WindDirection"
    ]
else:
    print("❌ Unexpected format")
    exit()

# ================= LOAD SOLAR =================

solardata = pd.read_csv(s)

# ================= BASIC INFO =================

print("Weather rows:", len(weatherdata))
print("Solar rows:", len(solardata))

# ================= TIMESTAMP FIX =================

weatherdata['Timestamp'] = pd.to_datetime(weatherdata['Timestamp'], errors='coerce')
solardata['Timestamp'] = pd.to_datetime(solardata['Timestamp'], errors='coerce')

# Remove invalid timestamps
weatherdata = weatherdata.dropna(subset=['Timestamp'])
solardata = solardata.dropna(subset=['Timestamp'])

print("Weather unique timestamps:", weatherdata['Timestamp'].nunique())
print("Solar unique timestamps:", solardata['Timestamp'].nunique())

# ================= MERGE =================

merged = pd.merge(
    weatherdata,
    solardata[['Timestamp', 'SolarGeneration']],
    on='Timestamp',
    how='inner'
)

print("Merged rows:", len(merged))

# ================= SELECT COLUMNS =================

final_df = merged[
    [
        "Timestamp",
        "ApparentTemperature",
        "AirTemperature",
        "DewPointTemperature",
        "RelativeHumidity",
        "WindSpeed",
        "WindDirection",
        "SolarGeneration"
    ]
]

# ================= SAVE MERGED =================

fn = r'C:\Users\HK Technology\PycharmProjects\solar_and_wind_energy_prediction\myapp\Dataset\Solar\final1.csv'
final_df.to_csv(fn, index=False)

# ================= CLEANING =================

df = final_df.drop_duplicates()

# Fill SolarGeneration missing values with 0
df['SolarGeneration'] = df['SolarGeneration'].fillna(0)

# Convert numeric columns properly
for col in df.columns:
    if col != "Timestamp":
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill numeric nulls with median
for c in df.columns:
    if df[c].dtype in [np.float64, np.int64]:
        df[c] = df[c].fillna(df[c].median())

# ================= SAVE FINAL =================

output_path = r"C:\Users\HK Technology\PycharmProjects\solar_and_wind_energy_prediction\myapp\Dataset\Solar\preprocessed1.csv"
df.to_csv(output_path, index=False)

print("✅ Done. Final shape:", df.shape)