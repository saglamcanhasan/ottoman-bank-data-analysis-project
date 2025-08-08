import pandas as pd
import numpy as np
from utils.server.data_loader import employee_df, agency_df

def employee_count(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, selected_time_period: list=[1855, 1925], end_inclusive: bool=False):
    # copy dataset
    df = employee_df.copy()

    # filter dataset
    if selected_ids is not None and len(selected_ids) != 0:
        df = df[df["ID"].isin(selected_ids)]
    
    if selected_grouped_functions is not None and len(selected_grouped_functions) != 0:
        df = df[df["Function"].isin(selected_grouped_functions)]

    if selected_religions is not None and len(selected_religions) != 0:
        df = df[df["Religion"].isin(selected_religions)]

    if selected_districts is not None and len(selected_districts) != 0:
        df = df[df["District"].isin(selected_districts)]

    if selected_cities is not None and len(selected_cities) != 0:
        df = df[df["City"].isin(selected_cities)]

    if selected_countries is not None and len(selected_countries) != 0:
        df = df[df["Country"].isin(selected_countries)]

    # drop employees with missing career start year
    df = df.dropna(subset=["Career Start Year"])

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # count active employees
    active_employees_df = pd.Series(0, dtype=int, index=np.arange(time_period_start_year, time_period_end_year+1))

    # group by employee ids
    id_records_group = df.groupby("ID")

    for _, records_group in id_records_group:
        carrer_start_year = records_group["Career Start Year"].iloc[0]
        carrer_end_year = records_group["Career End Year"].iloc[0]

        # clamp within range
        lower_bound = max(carrer_start_year, time_period_start_year)
        upper_bound = min(carrer_end_year, time_period_end_year)

        active_employees_df.loc[lower_bound:upper_bound] += 1

    # rename columns
    active_employees_df = active_employees_df.reset_index().rename(columns={"index": "Year", 0: "Employee Count"})
    return active_employees_df

def agency_count(selected_countries, selected_cities, selected_districts, selected_time_period: list=[1855, 1925], end_inclusive: bool=False):
    # copy dataset
    df = agency_df.copy()

    # filter dataset
    if selected_districts is not None and len(selected_districts) != 0:
        df = df[df["District"].isin(selected_districts)]

    if selected_cities is not None and len(selected_cities) != 0:
        df = df[df["City"].isin(selected_cities)]

    if selected_countries is not None and len(selected_countries) != 0:
        df = df[df["Country"].isin(selected_countries)]

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # change closing date type
    df["Closing date"] = df["Closing date"].fillna(str(time_period_end_year+1)).astype(int)

    # count open agencies
    open_agencies_df = pd.Series(0, dtype=int, index=np.arange(time_period_start_year, time_period_end_year+1))

    for _, agency in df.iterrows():
        open_year = agency["Opening date"]
        close_year = agency["Closing date"]

        # skip out-of-range
        if close_year < time_period_start_year or open_year > time_period_end_year:
            continue

        # clamp within range
        clamped_start = max(open_year, time_period_start_year)
        clamped_end = min(close_year if end_inclusive else close_year - 1, time_period_end_year)

        open_agencies_df.loc[clamped_start:clamped_end] += 1

    # rename columns
    open_agencies_df = open_agencies_df.reset_index().rename(columns={"index": "Year", 0: "Agency Count"})
    return open_agencies_df

def employee_turnover(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool = False):
    # copy dataset
    df = employee_df.copy()

    # filter dataset
    if selected_ids:
        df = df[df["ID"].isin(selected_ids)]

    if selected_grouped_functions:
        df = df[df["Function"].isin(selected_grouped_functions)]

    if selected_religions:
        df = df[df["Religion"].isin(selected_religions)]

    if selected_districts:
        df = df[df["District"].isin(selected_districts)]

    if selected_cities:
        df = df[df["City"].isin(selected_cities)]

    if selected_countries:
        df = df[df["Country"].isin(selected_countries)]

    # drop employees with missing start year
    df = df.dropna(subset=["Career Start Year"])

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # initialize empty counters
    year_range = np.arange(time_period_start_year, time_period_end_year + 1 if end_inclusive else time_period_end_year)
    hires_df = pd.Series(0, index=year_range, dtype=int)
    departures_df = pd.Series(0, index=year_range, dtype=int)

    # group by employee
    id_records_grouped = df.groupby("ID")

    for _, record_group in id_records_grouped:
        carrer_start_year = record_group["Career Start Year"].iloc[0]

        # skip if outside year range
        if carrer_start_year in year_range:
            hires_df[carrer_start_year] += 1

        carrer_end_year = record_group["Career End Year"].iloc[0]
        if carrer_end_year in year_range:
            departures_df[carrer_end_year] += 1

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
