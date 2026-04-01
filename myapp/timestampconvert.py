# import pandas as pd
#
# # Load dataset
# solar = pd.read_csv(r"C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Solar//Solar_Energy_Generation_Final.csv")
#
# # Convert Timestamp safely
# solar['Timestamp'] = pd.to_datetime(solar['Timestamp'], errors='coerce')
#
# # Convert to weather format
# solar['Timestamp'] = solar['Timestamp'].dt.strftime("%m/%d/%Y %H:%M")
#
# # Fill missing SolarGeneration (night time) with 0
# solar['SolarGeneration'] = solar['SolarGeneration'].fillna(0)
#
# # Keep all required columns
# final_df = solar[['CampusKey', 'SiteKey', 'Timestamp', 'SolarGeneration']]
#
# # Save file
# final_df.to_csv(r"C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Solar//Solar_Energy_Generation_Formatted.csv", index=False)
#
# print("Done:", final_df.shape)
import pandas as pd

# Load dataset
solar = pd.read_csv(r"C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Solar//Solar_Energy_Generation_Final.csv")

# Step 1: Convert to datetime (safe parsing)
solar['Timestamp'] = pd.to_datetime(solar['Timestamp'], errors='coerce')

# Step 2: Drop invalid timestamps (important for strict format)
solar = solar.dropna(subset=['Timestamp'])

# Step 3: FORCE exact weather format (MM/DD/YYYY HH:MM with leading zeros)
solar['Timestamp'] = solar['Timestamp'].dt.strftime("%m/%d/%Y %H:%M")

# Step 4: Convert BACK to datetime (so merge works correctly)
solar['Timestamp'] = pd.to_datetime(solar['Timestamp'], format="%m/%d/%Y %H:%M")

# Step 5: Fill missing SolarGeneration
solar['SolarGeneration'] = solar['SolarGeneration'].fillna(0)

# Step 6: Select columns
final_df = solar[['CampusKey', 'SiteKey', 'Timestamp', 'SolarGeneration']]

# Save file
final_df.to_csv(
    r"C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//Dataset//Solar//Solar_Energy_Generation_Formatted.csv",
    index=False
)

print("✅ Done:", final_df.shape)