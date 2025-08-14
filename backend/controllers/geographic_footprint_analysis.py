import pandas as pd
from utils.filter import filter
from plotly.colors import sample_colorscale
from services.data_loader import agency_df, employee_df

async def geo_footprint(selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=True):
    # copy datasets
    employees_df = employee_df.copy()
    agencies_df = agency_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period
    
    # filter unknown locations
    agencies_df = agencies_df[(agencies_df["Latitude"].notna()) & (agencies_df["Longitude"].notna())]
    employees_df = employees_df[employees_df["Agency"].isin(agencies_df["Agency"])]

    # filter
    employees_df = filter(employees_df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)
    agencies_df = filter(agencies_df, False, selected_countries, selected_cities, selected_districts, None, None, None, time_period_start_year, time_period_end_year)

    # drop unnecessary columns
    agencies_df.drop(columns=["Opening Year", "Closing Year"], inplace=True)

    # enlarge records according to years
    employee_records = list()
    for _, record in employees_df.iterrows():
        start = max(record["Career Start Year"], time_period_start_year)
        end = min(record["Career End Year"], time_period_end_year)

        for year in range(int(start), int(end)+1):
            employee_records.append({"Agency": record["Agency"], "Year": year, "ID": record["ID"]})
    records_df = pd.DataFrame(employee_records, columns=["Agency", "Year", "ID"]).drop_duplicates(subset=["Agency", "Year", "ID"])

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
    agencies_df.loc[:, ["Average Employee Count", "Min Employee Count", "Max Employee Count", "Unique Employee Count"]] = agencies_df[["Average Employee Count", "Min Employee Count", "Max Employee Count", "Unique Employee Count"]].fillna(0).round(1)

    # calculate colors and sizes
    min_employees, max_employees = agencies_df["Average Employee Count"].min(), agencies_df["Average Employee Count"].max()
    employees_range = max_employees - min_employees if max_employees != min_employees else 1
    normalized_weights = (agencies_df["Average Employee Count"] - min_employees)/employees_range
    colors = sample_colorscale([[0, "#00587A"], [0.025, "#00487A"], [0.05, "#B08D57"], [0.1, "#7C0A02"],[0.5, "#300000"], [1, "#200000"]], normalized_weights.tolist())
    sizes = 10 + normalized_weights*40

    # generate hover texts
    hover_texts  = (
        agencies_df["Agency"] + "<br>" +
        "<br>Latitude: " + agencies_df["Latitude"].round(3).astype(str) +
        "<br>Longitude: " + agencies_df["Longitude"].round(3).astype(str) +
        "<br>Unique Employee Count: " + agencies_df["Unique Employee Count"].astype(str) +
        "<br>Average Employee Count: " + agencies_df["Average Employee Count"].astype(str) +
        "<br>Minimum Employee Count: " + agencies_df["Min Employee Count"].astype(str) +
        "<br>Maximum Employee Count: " + agencies_df["Max Employee Count"].astype(str)
    )

    nodes = {
        "nodes": agencies_df["Agency"].to_list(),
        "latitudes": agencies_df["Latitude"].to_list(),
        "longitudes": agencies_df["Longitude"].to_list(),
        "sizes": sizes.to_list(),
        "colors": colors,
        "hovertexts": hover_texts.to_list()
    }

    # find transfers
    transfers = list()
    for _, group in employees_df.groupby("ID"):
        # iterate over consecutive pairs to find transfers
        group.sort_values(by="Period Start Year", inplace=True)
        agencies = group["Agency"].tolist()
        for index in range(len(agencies) - 1):
            source = agencies[index]
            target = agencies[index+1]
            if source != target:
                transfers.append({"Source": source, "Target": target, "Count": 1})
    
    transfers_df = pd.DataFrame(transfers, columns=["Source", "Target"]).value_counts().reset_index(name="Total Transfers")

    # get source coordinates
    transfers_df = transfers_df.merge(agencies_df[["Agency", "Latitude", "Longitude"]].rename(columns={"Agency": "Source", "Latitude": "Source Latitude", "Longitude": "Source Longitude"}), on="Source", how="left")

    # get target coordinates
    transfers_df = transfers_df.merge(agencies_df[["Agency", "Latitude", "Longitude"]].rename(columns={"Agency": "Target", "Latitude": "Target Latitude", "Longitude": "Target Longitude"}), on="Target", how="left")

    # calculate sizes for edges
    min_transfers, max_transfers = transfers_df["Total Transfers"].min(), transfers_df["Total Transfers"].max()
    transfers_range = max_transfers - min_transfers if max_transfers != min_transfers else 1
    sizes = 1 + ((transfers_df["Total Transfers"] - min_transfers)/transfers_range)*4

    # build edges dictionary
    edges = {
        "latitudes": transfers_df[["Source Latitude", "Target Latitude"]].values.tolist(),
        "longitudes": transfers_df[["Source Longitude", "Target Longitude"]].values.tolist(),
        "sizes": sizes.tolist()
    }

    return nodes, edges

