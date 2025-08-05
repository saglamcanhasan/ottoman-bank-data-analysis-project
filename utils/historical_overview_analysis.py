import pandas as pd
import numpy as np
from data_loader import employee_dataset, agency_dataset

def employee_count(start: int=1856, end: int=1922, end_inclusive: bool=False):
    print(employee_dataset.dtypes)

def open_agencies(start: int=1856, end: int=1922, end_inclusive: bool=False):
    # filter redundant values
    df = agency_dataset.iloc[:, :3].copy()

    # change rodos closing date
    mask = df["City"] == "Rodos"
    if mask.any():
        closing_date = df.loc[mask, "Closing date"].values[0]
        if isinstance(closing_date, str) and "," in closing_date:
            second_date = closing_date.split(",")[1].strip()
            df.loc[mask, "Closing date"] = second_date

    # change closing date type
    df["Closing date"] = df["Closing date"].fillna(end+1).astype(int)

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
    return open_agencies_df.reset_index().rename(columns={"index": "Year", 0: "Agency Count"})
    
print(employee_count())