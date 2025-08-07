import pandas as pd
import numpy as np
from utils.server.data_loader import employee_dataset, agency_dataset

def employee_count(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, selected_time_period: list=[1855, 1925], end_inclusive: bool=False):
    # copy dataset
    df = employee_dataset.copy()

    # filter dataset
    if selected_ids is not None and len(selected_ids) != 0:
        df = df[df["employee_code"].isin(selected_ids)]
    
    if selected_grouped_functions is not None and len(selected_grouped_functions) != 0:
        df = df[df["Grouped_Functions"].isin(selected_grouped_functions)]

    if selected_religions is not None and len(selected_religions) != 0:
        df = df[df["merged_religion"].isin(selected_religions)]

    if selected_districts is not None and len(selected_districts) != 0:
        df = df[df["District"].isin(selected_districts)]

    if selected_cities is not None and len(selected_cities) != 0:
        df = df[df["City"].isin(selected_cities)]

    if selected_countries is not None and len(selected_countries) != 0:
        df = df[df["Country"].isin(selected_countries)]

    # drop employees with missing start year
    df = df.dropna(subset=["start_year"])

    # extract start and end
    start, end = selected_time_period

    # count active employees
    active_employees_df = pd.Series(0, dtype=int, index=np.arange(start, end+1))

    # group by employee ids
    id_records_group = df.groupby("employee_code")

    for _, records_group in id_records_group:
        start_year = records_group["start_year"].iloc[0]
        end_year = records_group["end_year"].iloc[0]

        # clamp within range
        lower_bound = max(start_year, start)
        upper_bound = min(end_year, end)

        active_employees_df.loc[lower_bound:upper_bound] += 1

    # rename columns
    active_employees_df = active_employees_df.reset_index().rename(columns={"index": "Year", 0: "Employee Count"})
    return active_employees_df

def agency_count(selected_countries, selected_cities, selected_districts, selected_time_period: list=[1855, 1925], end_inclusive: bool=False):
    # copy dataset
    df = agency_dataset.copy()

    # filter dataset
    if selected_districts is not None and len(selected_districts) != 0:
        df = df[df["District"].isin(selected_districts)]

    if selected_cities is not None and len(selected_cities) != 0:
        df = df[df["City"].isin(selected_cities)]

    if selected_countries is not None and len(selected_countries) != 0:
        df = df[df["Country"].isin(selected_countries)]

    # extract start and end
    start, end = selected_time_period

    # change closing date type
    df["Closing date"] = df["Closing date"].fillna(str(end+1)).astype(int)

    # count open agencies
    open_agencies_df = pd.Series(0, dtype=int, index=np.arange(start, end+1))

    for _, agency in df.iterrows():
        open_year = agency["Opening date"]
        close_year = agency["Closing date"]

        # skip out-of-range
        if close_year < start or open_year > end:
            continue

        # clamp within range
        clamped_start = max(open_year, start)
        clamped_end = min(close_year if end_inclusive else close_year - 1, end)

        open_agencies_df.loc[clamped_start:clamped_end] += 1

    # rename columns
    open_agencies_df = open_agencies_df.reset_index().rename(columns={"index": "Year", 0: "Agency Count"})
    return open_agencies_df

def employee_turnover(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool = False):
    # copy dataset
    df = employee_dataset.copy()

    # filter dataset
    if selected_ids:
        df = df[df["employee_code"].isin(selected_ids)]

    if selected_grouped_functions:
        df = df[df["Grouped_Functions"].isin(selected_grouped_functions)]

    if selected_religions:
        df = df[df["merged_religion"].isin(selected_religions)]

    if selected_districts:
        df = df[df["District"].isin(selected_districts)]

    if selected_cities:
        df = df[df["City"].isin(selected_cities)]

    if selected_countries:
        df = df[df["Country"].isin(selected_countries)]

    # drop employees with missing start year
    df = df.dropna(subset=["start_year"])

    # extract start and end
    start, end = selected_time_period

    # initialize empty counters
    year_range = np.arange(start, end + 1 if end_inclusive else end)
    hires_df = pd.Series(0, index=year_range, dtype=int)
    departures_df = pd.Series(0, index=year_range, dtype=int)

    # group by employee
    id_records_grouped = df.groupby("employee_code")

    for _, record_group in id_records_grouped:
        start_year = record_group["start_year"].iloc[0]

        # skip if outside year range
        if start_year in year_range:
            hires_df[start_year] += 1

        end_year = record_group["end_year"].iloc[0]
        if end_year in departures_df.index:
            departures_df[end_year] += 1

    # calculate net change
    net_change_df = hires_df - departures_df

    # gather all in a dataframe
    employee_turnover_df = pd.DataFrame({
        "Year": year_range,
        "Hires": hires_df.values,
        "Departures": departures_df.values,
        "Net Change": net_change_df.values
    })
    return employee_turnover_df
