from utils.filter import filter
from plotly.colors import sample_colorscale
from services.data_loader import employee_df

async def coworker_network(selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False, top: int=10):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # drop employees with missing start year
    df = df.dropna(subset=["Career Start Year"])

    # drop records with unknown location
    df = df[~((df["District"] == "Unknown") & (df["City"] == "Unknown") & (df["Country"] == "Unknown"))]

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)

    # drop unnecessary columns and duplicates
    df = df[["Agency", "ID", "Period Start Year", "Period End Year"]].drop_duplicates()
    
    # couple employees on agency
    df = df.merge(df, on="Agency", how="inner", suffixes=(" Left", " Right"))

    # ensure no duplicate couples
    df = df[df["ID Left"] < df["ID Right"]]
    
    # filter non intersecting periods
    mask = (df["Period Start Year Left"] <= (df["Period End Year Right"] - (0 if end_inclusive else 1))) & (df["Period Start Year Right"] <= (df["Period End Year Left"] - (0 if end_inclusive else 1)))
    df = df[mask]
    
    # calculate durations
    df["Duration"] = df[["Period End Year Left", "Period End Year Right"]].min(axis=1) - df[["Period Start Year Left", "Period Start Year Right"]].max(axis=1) + (1 if end_inclusive else 0)
    
    # drop invalid durations
    df = df[df["Duration"] > 0]
    
    # find overlaps
    overlaps_df = df.groupby(["ID Left", "ID Right"], as_index=False)["Duration"].sum().rename(columns={"ID Left": "First Employee", "ID Right": "Second Employee"})

    # find top connections
    first = overlaps_df["First Employee"].value_counts()
    second = overlaps_df["Second Employee"].value_counts()
    connections_df = first.add(second, fill_value=0)

    # find top partnerships
    partnership_df = overlaps_df.copy()
    partnership_df["Co-Workers"] = (partnership_df["First Employee"] + " & " + partnership_df["Second Employee"])
    partnership_df.drop(columns=["First Employee", "Second Employee"], inplace=True)
    
    # filter first 1000 most important connections
    edges_df = overlaps_df.nlargest(1000, "Duration")
    
    first = edges_df.groupby("First Employee")["Duration"].sum()
    second = edges_df.groupby("Second Employee")["Duration"].sum()
    durations_df = first.add(second, fill_value=0)

    elements = list()
    min_duration, max_duration = durations_df.min(), durations_df.max()
    duration_range = max_duration - min_duration if max_duration != min_duration else 1
    normalized_weights = (durations_df - min_duration) / duration_range
    colors = sample_colorscale([[0, "#00587A"], [0.2, "#00487A"], [0.4, "#B08D57"], [0.6, "#7C0A02"],[0.8, "#300000"], [1, "#200000"]], normalized_weights.tolist())
    for index, id in enumerate(durations_df.index):
        links = int(connections_df[id])
        elements.append({
            "data": {
                "id": id,
                "label": f"{id} - {links} link{'s' if links > 1 else ''}",
                "weight": durations_df[id],
                "size": 10 + normalized_weights[id]*40,
                "color": colors[index]
            }
        })
    min_duration, max_duration = edges_df["Duration"].min(), edges_df["Duration"].max()
    duration_range = max_duration - min_duration if max_duration != min_duration else 1
    normalized_weights = (edges_df["Duration"] - min_duration) / duration_range
    for record, normalized_weight in zip(edges_df.to_dict("records"), normalized_weights):
        elements.append({
            "data": {
                "source": record["First Employee"],
                "target": record["Second Employee"],
                "weight": record["Duration"],
                "size": 1 + normalized_weight*4,
            }
        })

    # filter top most connected employees and longest working partnerships
    connections_df = connections_df.nlargest(top)
    partnership_df = partnership_df.nlargest(top, "Duration")

    # rename for clarity
    connections_df = connections_df.reset_index().rename(columns={"index": "Employee", "First Employee": "Employee", "count": "Connections"})
    partnership_df.rename(columns={"Duration": "Years"}, inplace=True)

    return elements, connections_df, partnership_df