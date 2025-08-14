import pandas as pd
from utils.filter import filter
from services.data_loader import employee_df

async def career_timeline(selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False, top: int=100):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)

    df["Start"] = df["Period Start Year"].astype(int).clip(lower=time_period_start_year)
    df["End"] = df["Period End Year"].astype(int).clip(upper=time_period_end_year)

    gantt_df = pd.DataFrame(df.loc[:, ["ID", "Start", "End"]], columns=["ID", "Start", "End"]).rename(columns={"Start": "starts", "End": "ends", "ID": "tasks"})
    
    mask = df["Start"] == df["End"]
    gantt_df.loc[mask, "ends"] = gantt_df.loc[mask, "ends"] + 1
    gantt_df["starts"] = pd.to_datetime(gantt_df["starts"], format="%Y")
    gantt_df["ends"] = pd.to_datetime(gantt_df["ends"], format="%Y")

    gantt_df["hovertexts"] = (
        "ID: " + df["ID"].astype(str) + "<br>" +
        "<br>Agency: " + df["Agency"].astype(str) +
        "<br>Function: " + df["Function"].astype(str) +
        "<br>Religion: " + df["Religion"].astype(str) +
        "<br>Period: " + df["Start"].astype(str) + " - " + df["End"].astype(str)
    )

    gantt_df["colors"] = df["ID"]

    gantt_data = gantt_df[:top].to_dict("list")

    return gantt_data

async def employee_profiles(selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)
    
    profiles = []
    for id, group in df.groupby("ID"):
        agencies = group["Agency"].unique()
        functions = group["Function"].unique()
        religions = group["Religion"].unique()
        active_period = f"{group['Career Start Year'].iloc[0]} - {group['Career End Year'].iloc[0]}"
        
        # prepare the profile data
        profiles.append({
            "ID": id,
            "Agency": '; '.join(agencies),
            "Active Period": active_period,
            "Function": ', '.join(functions),
            "Religion": ', '.join(religions),
        })
    
    profile_df = pd.DataFrame(profiles)
    
    return profile_df