import numpy as np
import pandas as pd
from collections import defaultdict
from utils.server.filter import filter
from utils.server.filter_parameters import religions
from utils.server.data_loader import employee_df

def religion_count(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # drop employees with missing career start year
    df = df.dropna(subset=["Career Start Year"])

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_grouped_functions, None, selected_ids, time_period_start_year, time_period_end_year)

    # get religious counts
    religion_counts = defaultdict(int)
    for _, record_group in df.groupby("ID"):
        total_duration = 0
        religion_durations = defaultdict(float)

        for _, record in record_group.iterrows():
            period_start_year = max(record["Period Start Year"], time_period_start_year)
            period_end_year = min(record["Period End Year"] - (0 if end_inclusive else 1), time_period_end_year)

            overlap_duration = period_end_year - period_start_year + 1

            total_duration += overlap_duration
            religion_durations[record["Religion"]] += overlap_duration

        if total_duration == 0:
            continue

        for religion, duration in religion_durations.items():
            religion_counts[religion] += duration / total_duration

    religion_counts = pd.DataFrame([dict(religion_counts)])

    return religion_counts

def religion_distribution(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # drop employees with missing career start year
    df = df.dropna(subset=["Career Start Year"])

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_grouped_functions, None, selected_ids, time_period_start_year, time_period_end_year)

    # get religious counts
    religion_counts_df = pd.DataFrame(0, index=np.arange(time_period_start_year, time_period_end_year+1), columns=religions+["Unknown", "Other"])
    for _, record_group in df.groupby("ID"):
        for _, record in record_group.iterrows():
            period_start_year = int(max(record["Period Start Year"], time_period_start_year))
            period_end_year = int(min(record["Period End Year"] - (0 if end_inclusive else 1), time_period_end_year))

            religion_counts_df.loc[period_start_year:period_end_year, record["Religion"]] += 1

    religion_counts_df = religion_counts_df.div(religion_counts_df.sum(axis=1).replace(0, 1), axis=0)

    religion_counts_df.reset_index(inplace=True)
    religion_counts_df.rename(columns={"index": "Year"}, inplace=True)

    return religion_counts_df