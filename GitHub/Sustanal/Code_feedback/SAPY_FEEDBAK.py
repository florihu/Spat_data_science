# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:19:19 2023

@author: 
"""
# Importing pandas and other packages
import pandas as pd

# Step 3: Importing the metadata using pandas. The metadata chosen is from the world bank and is on Israel.
try:
    Env_forest_area_metadata = pd.read_csv(
        'Forest area metadata.csv', skiprows=4)
    Env_water_stress_metadata = pd.read_csv(
        'Level of water stress metadata.csv', skiprows=4)
    Env_renewable_energy_metadata = pd.read_csv(
        'Renewable energy consumption metadata.csv', skiprows=4)
    Soc_Gini_metadata = pd.read_csv(
        'Gini index metadata.csv', skiprows=4)
    Soc_internet_use_metadata = pd.read_csv(
        'Individuals using the Internet metadata.csv', skiprows=4)
    Soc_maternal_mortality_metadata = pd.read_csv(
        'Maternal mortality ratio metadata.csv', skiprows=4)
except FileNotFoundError as e:
    print(f"Error: {e}. Please check if the file paths are correct.")
except pd.errors.ParserError as e:
    print(f"Error: {e}. There was an issue parsing the CSV file. Please check the file format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}.")

# Step 4b: Filtering the data on Israel
Env_forest_area_alltime = Env_forest_area_metadata[Env_forest_area_metadata['Country Code'] == 'ISR']
Env_water_stress_alltime = Env_water_stress_metadata[
    Env_water_stress_metadata['Country Code'] == 'ISR']
Env_renewable_alltime = Env_renewable_energy_metadata[
    Env_renewable_energy_metadata['Country Code'] == 'ISR']
Soc_Gini_alltime = Soc_Gini_metadata[Soc_Gini_metadata['Country Code'] == 'ISR']
Soc_internet_use_alltime = Soc_internet_use_metadata[
    Soc_internet_use_metadata['Country Code'] == 'ISR']
Soc_maternal_mortality_alltime = Soc_maternal_mortality_metadata[
    Soc_maternal_mortality_metadata['Country Code'] == 'ISR']

# Step 4c: Checking for missing values
print("Missing values in Forest Area data:")
print(pd.isna(Env_forest_area_alltime).sum())

print("Missing values in Water Stress data:")
print(pd.isna(Env_water_stress_alltime).sum())

print("Missing values in Renewable Energy data:")
print(pd.isna(Env_renewable_alltime).sum())

print("Missing values in Gini Index data:")
print(pd.isna(Soc_Gini_alltime).sum())

print("Missing values in Internet Use data:")
print(pd.isna(Soc_internet_use_alltime).sum())

print("Missing values in Maternal Mortality data:")
print(pd.isna(Soc_maternal_mortality_alltime).sum())

# Step 4d: Check if f each indicator pair has at least 3 overlapping years with non-missing values and print a statement about it. Save the counts in a variable, as you will reuse them in task 5b

# Defining a function to check there are at least 3 overlapping years with non-missing values

def check_overlap(df1, df2):
    common_years = set(df1.columns[5:]).intersection(set(df2.columns[5:]))
    overlapping_years = [year for year in common_years if not df1[year].isna(
    ).any() and not df2[year].isna().any()]
    return len(overlapping_years) >= 3, overlapping_years

# Applying the function to each indicator:
forest_water_overlap, forest_water_years = check_overlap(
    Env_forest_area_alltime, Env_water_stress_alltime)
forest_renewable_overlap, forest_renewable_years = check_overlap(
    Env_forest_area_alltime, Env_renewable_alltime)
forest_gini_overlap, forest_gini_years = check_overlap(
    Env_forest_area_alltime, Soc_Gini_alltime)
forest_internet_overlap, forest_internet_years = check_overlap(
    Env_forest_area_alltime, Soc_internet_use_alltime)
forest_mortality_overlap, forest_mortality_years = check_overlap(
    Env_forest_area_alltime, Soc_maternal_mortality_alltime)

water_renewable_overlap, water_renewable_years = check_overlap(
    Env_water_stress_alltime, Env_renewable_alltime)
water_gini_overlap, water_gini_years = check_overlap(
    Env_water_stress_alltime, Soc_Gini_alltime)
water_internet_overlap, water_internet_years = check_overlap(
    Env_water_stress_alltime, Soc_internet_use_alltime)
water_mortality_overlap, water_mortality_years = check_overlap(
    Env_water_stress_alltime, Soc_maternal_mortality_alltime)


renewable_gini_overlap, renewable_gini_years = check_overlap(
    Env_renewable_alltime, Soc_Gini_alltime)
renewable_internet_overlap, renewable_internet_years = check_overlap(
    Env_renewable_alltime, Soc_internet_use_alltime)
renewable_mortality_overlap, renewable_mortality_years = check_overlap(
    Env_renewable_alltime, Soc_maternal_mortality_alltime)

gini_internet_overlap, gini_internet_years = check_overlap(
    Soc_Gini_alltime, Soc_internet_use_alltime)
gini_mortality_overlap, gini_mortality_years = check_overlap(
    Soc_Gini_alltime, Soc_maternal_mortality_alltime)

internet_mortality_overlap, internet_mortality_years = check_overlap(
    Soc_internet_use_alltime, Soc_maternal_mortality_alltime)

# Display the outcome of the overlaps and which years:
print(f"Forest Area and Water Stress have at least 3 overlapping years: {forest_water_overlap}. Overlapping years: {forest_water_years}")
print(f"Forest Area and Renewable Energy have at least 3 overlapping years: {forest_renewable_overlap}. Overlapping years: {forest_renewable_years}")
print(f"Forest Area and Gini Index have at least 3 overlapping years: {forest_gini_overlap}. Overlapping years: {forest_gini_years}")
print(f"Forest Area and Internet Use have at least 3 overlapping years: {forest_internet_overlap}. Overlapping years: {forest_internet_years}")
print(f"Forest Area and Maternal Mortality have at least 3 overlapping years: {forest_mortality_overlap}. Overlapping years: {forest_mortality_years}")

print(f"Water Stress and Renewable Energy have at least 3 overlapping years: {water_renewable_overlap}. Overlapping years: {water_renewable_years}")
print(f"Water Stress and Gini Index have at least 3 overlapping years: {water_gini_overlap}. Overlapping years: {water_gini_years}")
print(f"Water Stress and Internet Use have at least 3 overlapping years: {water_internet_overlap}. Overlapping years: {water_internet_years}")
print(f"Water Stress and Maternal Mortality have at least 3 overlapping years: {water_mortality_overlap}. Overlapping years: {water_mortality_years}")

print(f"Renewable Energy and Gini Index have at least 3 overlapping years: {renewable_gini_overlap}. Overlapping years: {renewable_gini_years}")
print(f"Renewable Energy and Internet Use have at least 3 overlapping years: {renewable_internet_overlap}. Overlapping years: {renewable_internet_years}")
print(f"Renewable Energy and Maternal Mortality have at least 3 overlapping years: {renewable_mortality_overlap}. Overlapping years: {renewable_mortality_years}")

print(f"Gini Index and Internet Use have at least 3 overlapping years: {gini_internet_overlap}. Overlapping years: {gini_internet_years}")
print(f"Gini Index and Maternal Mortality have at least 3 overlapping years: {gini_mortality_overlap}. Overlapping years: {gini_mortality_years}")

print(f"Internet Use and Maternal Mortality have at least 3 overlapping years: {internet_mortality_overlap}. Overlapping years: {internet_mortality_years}")

# store the count of overlap years in a variable
overlap_counts = {
    'forest_water': len(forest_water_years),
    'forest_renewable': len(forest_renewable_years),
    'forest_gini': len(forest_gini_years),
    'forest_internet': len(forest_internet_years),
    'forest_mortality': len(forest_mortality_years),
    'water_renewable': len(water_renewable_years),
    'water_gini': len(water_gini_years),
    'water_internet': len(water_internet_years),
    'water_mortality': len(water_mortality_years),
    'renewable_gini': len(renewable_gini_years),
    'renewable_internet': len(renewable_internet_years),
    'renewable_mortality': len(renewable_mortality_years),
    'gini_internet': len(gini_internet_years),
    'gini_mortality': len(gini_mortality_years),
    'internet_mortality': len(internet_mortality_years)
}

# Step 4e:Remove all leading years with only missing values to reduce the data size. In other words, take a subset of your data that starts in the earliest year, in which the data is not missing for all 6 indicators.
# First we make all df's into 1 dictionairy so it is easy to access/process
dataframes = {
    'Env_forest_area': Env_forest_area_alltime,
    'Env_water_stress': Env_water_stress_alltime,
    'Env_renewable_energy': Env_renewable_alltime,
    'Soc_Gini': Soc_Gini_alltime,
    'Soc_internet_use': Soc_internet_use_alltime,
    'Soc_maternal_mortality': Soc_maternal_mortality_alltime
}

# Secondly we find the earliest year with at least 1 indicator having non-missing values
earliest_year = min(int(year) for year in range(1960, 2023) if any(df[str(year)].notna().any() for df in dataframes.values()))

# Thirdly, we create a new set of dataframes with the leading years with NaN's removed
indicator_book = {
    name: df.loc[:, ['Country Name', 'Country Code'] + list(df.columns[df.columns.get_loc(str(earliest_year)):])]
    for name, df in dataframes.items()
}
