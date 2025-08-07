import pandas as pd
import numpy as np
from utils.server.data_loader import employee_dataset, agency_dataset

def employee_count(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, start: int=1856, end: int=1922, end_inclusive: bool=False):
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

    # drop employees with unknown start year
    df = df.dropna(subset=["start_year"])

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

def agency_count(selected_countries, selected_cities, selected_districts, start: int=1856, end: int=1922, end_inclusive: bool=False):
    # copy dataset
    df = agency_dataset.copy()

    # change closing date type
    df["Closing date"] = df["Closing date"].fillna(str(end+1)).astype(int)

    # filter dataset
    if selected_districts is not None and len(selected_districts) != 0:
        df = df[df["District"].isin(selected_districts)]

    if selected_cities is not None and len(selected_cities) != 0:
        df = df[df["City"].isin(selected_cities)]

    if selected_countries is not None and len(selected_countries) != 0:
        df = df[df["Country"].isin(selected_countries)]

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