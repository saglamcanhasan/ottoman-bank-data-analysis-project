from pandas import DataFrame

def filter(df: DataFrame, is_employee: bool, selected_countries=None, selected_cities=None, selected_districts=None, selected_functions=None, selected_religions=None, selected_ids=None, time_period_start_year=None, time_period_end_year=None) -> DataFrame:
    # filter dataset
    if is_employee:
        if selected_ids is not None and len(selected_ids) != 0:
            df = df[df["ID"].isin(selected_ids)]

        if selected_functions is not None and len(selected_functions) != 0:
            df = df[df["Function"].isin(selected_functions)]

        if selected_religions is not None and len(selected_religions) != 0:
            df = df[df["Religion"].isin(selected_religions)]

        if selected_districts is not None and len(selected_districts) != 0:
            df = df[df["District"].isin(selected_districts)]

        if selected_cities is not None and len(selected_cities) != 0:
            df = df[df["City"].isin(selected_cities)]

        if selected_countries is not None and len(selected_countries) != 0:
            df = df[df["Country"].isin(selected_countries)]

        if time_period_start_year is not None and time_period_end_year is not None:
            df = df[(df["Period End Year"] >= time_period_start_year) & (df["Period Start Year"] <= time_period_end_year)]

    else:
        if selected_districts is not None and len(selected_districts) != 0:
            df = df[df["District"].isin(selected_districts)]

        if selected_cities is not None and len(selected_cities) != 0:
            df = df[df["City"].isin(selected_cities)]

        if selected_countries is not None and len(selected_countries) != 0:
            df = df[df["Country"].isin(selected_countries)]

        if time_period_start_year is not None and time_period_end_year is not None:
            df = df[(df["Closing Year"] >= time_period_start_year) & (df["Opening Year"] <= time_period_end_year)]

    return df