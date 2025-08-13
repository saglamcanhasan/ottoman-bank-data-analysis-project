import pandas as pd
from utils.filter import filter
from services.data_loader import agency_df, employee_df

async def geo_footprint(selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=True):
    # copy datasets
    records_df = employee_df.copy()
    agencies_df = agency_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period
    
    # filter unknown locations
    records_df = records_df[~((records_df["District"] == "Unknown") & (records_df["City"] == "Unknown") & (records_df["Country"] == "Unknown"))]
    agencies_df = agencies_df[~((agencies_df["District"] == "Unknown") & (agencies_df["City"] == "Unknown") & (agencies_df["Country"] == "Unknown"))]
    agencies_df = agencies_df[(agencies_df["Latitude"].notna()) & (agencies_df["Longitude"].notna())]

    # filter
    records_df = filter(records_df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)
    agencies_df = filter(agencies_df, False, selected_countries, selected_cities, selected_districts, None, None, None, time_period_start_year, time_period_end_year)

    # drop unnecessary columns
    agencies_df.drop(columns=["Opening Year", "Closing Year"], inplace=True)

    # enlarge records according to years
    employee_records = list()
    for _, record in records_df.iterrows():
        start = max(record["Career Start Year"], time_period_start_year)
        end = min(record["Career End Year"], time_period_end_year)

        for year in range(int(start), int(end)+1):
            employee_records.append({"Agency": record["Agency"], "Year": year, "ID": record["ID"]})
    records_df = pd.DataFrame(employee_records)

    # compute employee counts
    employee_counts_df = records_df.groupby(["Agency", "Year"])["ID"].count().reset_index(name="Employee Count")

    # compute per-agency average, min, and max employee counts
    stats_df = employee_counts_df.groupby("Agency")["Employee Count"].agg(["mean", "min", "max"]).reset_index()
    stats_df.rename(columns={"mean": "Average Employee Count", "min": "Min Employee Count", "max": "Max Employee Count"}, inplace=True)

    # compute per-agency unique employee counts
    unique_df = records_df.groupby("Agency")["ID"].nunique().reset_index(name="Unique Employee Count")

    # merge stats and unique counts
    agencies_df = agencies_df.merge(stats_df, on="Agency", how="left")
    agencies_df = agencies_df.merge(unique_df, on="Agency", how="left")

    # fill NAs with 0
    agencies_df.loc[:, ["Average Employee Count", "Min Employee Count", "Max Employee Count", "Unique Employee Count"]] = agencies_df[["Average Employee Count", "Min Employee Count", "Max Employee Count", "Unique Employee Count"]].fillna(0)

    # label each agency
    labels = list()
    for agency in agencies_df["Agency"].to_list():
        found = False
        for location in agency.split(","):
            location = location.strip()
            if location != "Unknown":
                labels.append(location)
                found = True
                break
        if not found:
            labels.append("Unknown")
    agencies_df["Label"] = labels

    return agencies_df

