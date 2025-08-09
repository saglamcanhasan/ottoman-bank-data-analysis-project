import pandas as pd
from itertools import combinations
from intervaltree import IntervalTree
from utils.server.filter import filter
from plotly.colors import sample_colorscale
from collections import defaultdict
from utils.server.data_loader import employee_df

def coworker_network(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False, top: int=50):
    # copy dataset
    df = employee_df.copy()

    # extract start and end
    time_period_start_year, time_period_end_year = selected_time_period

    # drop employees with missing start year
    df = df.dropna(subset=["Career Start Year"])

    # drop records with unknown location
    df = df[~((df["District"] == "Unknown") & (df["City"] == "Unknown") & (df["Country"] == "Unknown"))]

    # filter dataset
    df = filter(df, True, selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, time_period_start_year, time_period_end_year)

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
    overlaps = defaultdict(dict)
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
                overlaps[key] = {
                    "First Employee": first_employee,
                    "Second Employee": second_employee,
                    "Duration": duration,
                }

    overlaps_df = pd.DataFrame(overlaps.values(), columns=["First Employee", "Second Employee", "Duration"])

    # find top connections
    first = overlaps_df["First Employee"].value_counts()
    second = overlaps_df["Second Employee"].value_counts()
    connections_df = first.add(second, fill_value=0).sort_values(ascending=False)

    # find top partnerships
    partnership_df = overlaps_df.sort_values(by="Duration", ascending=False)
    partnership_df["Co-Workers"] = (partnership_df["First Employee"] + " & " + partnership_df["Second Employee"])
    partnership_df.drop(columns=["First Employee", "Second Employee"], inplace=True)
    
    # filter first 1000 most important connections
    edges_df = overlaps_df.sort_values(by="Duration", ascending=False).head(1000)
    
    first = edges_df.groupby("First Employee")["Duration"].sum()
    second = edges_df.groupby("Second Employee")["Duration"].sum()
    durations_df = first.add(second, fill_value=0)

    elements = list()
    min_duration = durations_df.min()
    max_duration = durations_df.max()
    for index, record in durations_df.items():
        links = int(connections_df[index])
        normalized_weight = (record - min_duration)/max_duration
        elements.append({
            "data": {
                "id": index,
                "label": f"{index} - {links} link{'s' if links > 1 else ''}",
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

    # filter top most connected employees and longest working partnerships
    connections_df = connections_df.head(top)
    partnership_df = partnership_df.head(top)

    # rename for clarity
    connections_df = connections_df.reset_index().rename(columns={"index": "Employee", "First Employee": "Employee", "count": "Connections"})
    partnership_df.rename(columns={"Duration": "Years"}, inplace=True)

    return elements, connections_df, partnership_df