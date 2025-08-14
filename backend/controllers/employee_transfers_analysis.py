import pandas as pd
from utils.filter import filter
from plotly.colors import sample_colorscale
from services.data_loader import employee_df

async def employee_transfers(selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False, top: int=50):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # drop employees with missing start year
    df = df.dropna(subset=["Career Start Year"])

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)

    # find transfers
    transfers = list()
    for _, group in df.groupby("ID"):
        # iterate over consecutive pairs to find transfers
        group.sort_values(by="Period Start Year", inplace=True)
        agencies = group["Agency"].tolist()
        for index in range(len(agencies) - 1):
            if agencies[index] != agencies[index+1]:
                transfers.append({"Source": agencies[index], "Target": agencies[index+1]})
    transfers_df = pd.DataFrame(transfers, columns=["Source", "Target"]).value_counts().reset_index(name="Count")

    # get agencies
    agencies = pd.Index(transfers_df["Source"]).union(transfers_df["Target"]).unique().tolist()

    # calculate incoming and outgoing transfers
    incoming_df = pd.Series(transfers_df.groupby("Target")["Count"].sum().rename("Incoming Transfers"), index=agencies).fillna(0)
    outgoing_df = pd.Series(transfers_df.groupby("Source")["Count"].sum().rename("Outgoing Transfers"), index=agencies).fillna(0)
    
    # associate agencies with transfers
    agencies_df = pd.DataFrame(index=agencies)
    agencies_df = agencies_df.join(incoming_df, how='left').join(outgoing_df, how='left').fillna(0)
    agencies_df["Total Transfers"] = agencies_df["Incoming Transfers"] + agencies_df["Outgoing Transfers"]

    # find edges
    edges_df = transfers_df.copy()
    mask = edges_df["Source"] > edges_df["Target"]
    edges_df.loc[mask, ["Source", "Target"]] = edges_df.loc[mask, ["Target", "Source"]].values
    edges_df = edges_df.groupby(["Source", "Target"])["Count"].sum().reset_index()

    # create elements for the network graph
    elements = []
    min_transfers, max_transfers = agencies_df["Total Transfers"].min(), agencies_df["Total Transfers"].max()
    transfers_range = max_transfers - min_transfers if max_transfers != min_transfers else 1
    normalized_weights = (agencies_df["Total Transfers"] - min_transfers) / transfers_range
    colors = sample_colorscale([[0, "#00587A"], [0.2, "#00487A"], [0.4, "#B08D57"], [0.6, "#7C0A02"],[0.8, "#300000"], [1, "#200000"]], normalized_weights.tolist())
    for index, agency in enumerate(agencies_df.index):
        elements.append({
            "data": {
                "id": agency,
                "label": f"{agency} - {int(agencies_df.loc[agency, 'Incoming Transfers'])} in, {int(agencies_df.loc[agency, 'Outgoing Transfers'])} out",
                "weight": agencies_df.loc[agency, "Total Transfers"],
                "size": 10 + normalized_weights.iloc[index]*40,
                "color": colors[index]
            }
        })
    min_transfers, max_transfers = edges_df["Count"].min(), edges_df["Count"].max()
    transfers_range = max_transfers - min_transfers if max_transfers != min_transfers else 1
    normalized_weights = (edges_df["Count"] - min_transfers) / transfers_range
    for index, row in edges_df.iterrows():
        elements.append({
            "data": {
                "source": row["Source"],
                "target": row["Target"],
                "weight": row["Count"],
                "size": 1 + normalized_weights[index]*4,
            }
        })

    return elements

async def employee_flow(selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, selected_time_period: list= [1855, 1925], end_inclusive: bool = False):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # drop employees with missing start year
    df = df.dropna(subset=["Career Start Year"])

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)

    # find transfers
    transfers = list()
    for _, group in df.groupby("ID"):
        # iterate over consecutive pairs to find transfers
        group.sort_values(by="Period Start Year", inplace=True)
        agencies = group["Agency"].tolist()
        for index in range(len(agencies) - 1):
            if agencies[index] != agencies[index+1]:
                transfers.append({"Source": agencies[index], "Target": agencies[index+1], "Count": 1})
    
    transfers_df = pd.DataFrame(transfers, columns=["Source", "Target"]).value_counts().reset_index(name="Count")

    # get all unique agencies
    agencies = pd.Index(transfers_df["Source"]).union(transfers_df["Target"]).unique().tolist()

    # shorten agency names
    nodes = list()
    for agency in agencies:
        found = False
        for location in agency.split(","):
            location = location.strip()
            if location != "Unknown":
                nodes.append(location)
                found = True
                break
        if not found:
            nodes.append("Unknown")

    # map agency name to index
    agency_to_idx = {agency: index for index, agency in enumerate(agencies)}

    # calculate incoming and outgoing transfers
    incoming_df = pd.Series(transfers_df.groupby("Target")["Count"].sum().rename("Incoming Transfers"), index=agencies).fillna(0)
    outgoing_df = pd.Series(transfers_df.groupby("Source")["Count"].sum().rename("Outgoing Transfers"), index=agencies).fillna(0)
    
    # associate agencies with transfers
    agencies_df = pd.DataFrame(index=agencies)
    agencies_df = agencies_df.join(incoming_df, how='left').join(outgoing_df, how='left').fillna(0)
    agencies_df["Total Transfers"] = agencies_df["Incoming Transfers"] + agencies_df["Outgoing Transfers"]

    # generate dictionary
    min_transfers, max_transfers = agencies_df["Total Transfers"].min(), agencies_df["Total Transfers"].max()
    transfers_range = max_transfers - min_transfers if max_transfers != min_transfers else 1
    normalized_weights = (agencies_df["Total Transfers"] - min_transfers) / transfers_range
    elements = {
        "nodes": nodes,
        "node_customdata": list(zip(agencies, incoming_df.loc[agencies].values, outgoing_df.loc[agencies].values)),
        "node_hovertemplate": "%{customdata[0]}<br>Incoming: %{customdata[1]}<br>Outgoing: %{customdata[2]}",
        "colors": sample_colorscale([[0, "#00587A"], [0.2, "#00487A"], [0.4, "#B08D57"], [0.6, "#7C0A02"],[0.8, "#300000"], [1, "#200000"]], normalized_weights.tolist()),
        "sources": transfers_df["Source"].map(agency_to_idx).tolist(),
        "targets": transfers_df["Target"].map(agency_to_idx).tolist(),
        "values": transfers_df["Count"].tolist(),
        "link_customdata": list(zip(transfers_df["Source"], transfers_df["Target"])),
        "line_hovertemplate": "From %{customdata[0]}<br>To %{customdata[1]}"
    }

    return elements