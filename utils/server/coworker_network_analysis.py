import pandas as pd
from itertools import combinations
from utils.server.data_loader import employee_df
from intervaltree import IntervalTree
from plotly.colors import sample_colorscale

def coworker_network(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False, top: int=50):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # drop employees with missing start year
    df = df.dropna(subset=["Career Start Year"])

    # drop records outside the range
    df = df[(df["Period End Year"] >= time_period_start_year) & (df["Period Start Year"] <= time_period_end_year)]

    # drop records with unknown location
    df = df[~((df["District"] == "Unknown") & (df["City"] == "Unknown") & (df["Country"] == "Unknown"))]

    # filter dataset
    if selected_ids:
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

    # build agency trees
    agency_trees = dict()
    for agency, agency_group in df.groupby("Agency"):
        employee_trees = dict()

        for id, employee_group in agency_group.groupby("ID"):
            employee_tree = IntervalTree()

            for _, record in employee_group.iterrows():
                employee_tree[record["Period Start Year"]:record["Period End Year"]+1] = record.to_dict()

            employee_trees[id] = employee_tree
            
        agency_trees[agency] = employee_trees

    # find overlaps
    overlaps = dict()
    for agency, trees in agency_trees.items():
        ids = list(trees.keys())

        for first_employee, second_employee in combinations(ids, 2):
            if first_employee < second_employee:
                first_employee, second_employee = second_employee, first_employee
            first_tree = trees[first_employee]
            second_tree = trees[second_employee]

            duration = 0

            for interval in first_tree:
                matches = second_tree.overlap(interval.begin, interval.end)
                for match in matches:
                    start_intersection = max(interval.begin, match.begin)
                    end_intersection = min(interval.end, match.end)

                    duration += end_intersection - start_intersection - (0 if end_inclusive else 1)

            if duration != 0:
                key = (first_employee, second_employee)

                if key in overlaps:
                    overlaps[key]["Duration"] += duration

                else:
                    overlaps[key] = {
                        "First Employee": first_employee,
                        "Second Employee": second_employee,
                        "Duration": duration,
                    }

    overlaps_df = pd.DataFrame(overlaps.values(), columns=["First Employee", "Second Employee", "Duration"])

    # filter most important connections
    edges_df = overlaps_df.sort_values(by="Duration", ascending=False).head(1000)
    
    first = edges_df.groupby("First Employee")["Duration"].sum()
    second = edges_df.groupby("Second Employee")["Duration"].sum()
    durations_df = first.add(second, fill_value=0)

    elements = list()
    min_duration = durations_df.min()
    max_duration = durations_df.max()
    for index, record in durations_df.items():
        normalized_weight = (record - min_duration)/max_duration
        elements.append({
            "data": {
                "id": index,
                "weight": record,
                "size": 10 + normalized_weight*40,
                "color": sample_colorscale([[0, "#B08D57"], [0.5, "#7C0A02"], [1, "#200000"]], [normalized_weight])[0]
            }
        })
    min_duration = edges_df["Duration"].min()
    max_duration = edges_df["Duration"].max()
    for _, record in edges_df.iterrows():
        normalized_weight = (record["Duration"] - min_duration)/max_duration
        elements.append({
            "data": {
                "source": record["First Employee"],
                "target": record["Second Employee"],
                "weight": record["Duration"],
                "size": 1 + normalized_weight*4,
            }
        })

    first = overlaps_df["First Employee"].value_counts()
    second = overlaps_df["Second Employee"].value_counts()
    connections_df = first.add(second, fill_value=0).sort_values(ascending=False).head(top).reset_index().rename(columns={"index": "Employee", "count": "Connections"})

    partnership_df = overlaps_df.sort_values(by="Duration", ascending=False).head(top)
    partnership_df["Co-Workers"] = (partnership_df["First Employee"] + " & " + partnership_df["Second Employee"])
    partnership_df.drop(columns=["First Employee", "Second Employee"], inplace=True)
    partnership_df.rename(columns={"Duration": "Years"}, inplace=True)

    return elements, connections_df, partnership_df