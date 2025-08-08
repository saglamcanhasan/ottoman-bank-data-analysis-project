import pandas as pd
import numpy as np
from collections import defaultdict
from utils.server.data_loader import employee_df, agency_df

# time period bounds
start = 1855
end = 1926

# dropdown values
location_cols = ["Country", "City", "District"]
location_df = pd.concat([agency_df[location_cols], employee_df[location_cols]], ignore_index=True)
location_df = location_df.dropna(subset=["Country"])

countries = set()
cities = defaultdict(set)
districts = defaultdict(set)

for _, location in location_df.iterrows():
    country = location["Country"]
    city = location["City"]
    district = location["District"]

    countries.add(country)

    if pd.notna(city):
        cities[country].add(city)

        if pd.notna(district):
            districts[city].add(district)

countries = sorted(countries - {"Unknown"})
cities = {country: sorted(city_set - {"Unknown"}) for country, city_set in cities.items()}
districts = {city: sorted(district_set - {"Unknown"}) for city, district_set in districts.items()}

grouped_functions = np.unique(employee_df["Function"])
grouped_functions = grouped_functions[grouped_functions != "Unknown"].tolist()

religions = np.unique(employee_df["Religion"].dropna())
religions = religions[(religions != "Unknown") & (religions != "Other")].tolist()

ids = np.unique(employee_df["ID"].dropna()).tolist()