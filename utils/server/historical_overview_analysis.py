import pandas as pd
import numpy as np
from utils.server.data_loader import employee_dataset, agency_dataset

def employee_count(start: int=1856, end: int=1922, end_inclusive: bool=False):
    print(employee_dataset.dtypes)

def open_agencies(selected_countries, selected_cities, selected_districts, start: int=1856, end: int=1922, end_inclusive: bool=False):
    # copy dataset
    df = agency_dataset.copy()

    # change closing date type
    df["Closing date"] = df["Closing date"].fillna(str(end+1)).astype(int)

    # filter dataset
    if selected_countries is not None and len(selected_countries) != 0:
        df = df[df["Country"].isin(selected_countries)]

    if selected_cities is not None and len(selected_cities) != 0:
        df = df[df["City"].isin(selected_cities)]

    if selected_districts is not None and len(selected_districts) != 0:
        df = df[df["District"].isin(selected_districts)]

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
    open_agencies = open_agencies_df.reset_index().rename(columns={"index": "Year", 0: "Agency Count"})
    return open_agencies