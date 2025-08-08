import numpy as np
import time
import pandas as pd
import networkx as nx
from intervaltree import IntervalTree
from itertools import combinations
from data_loader import employee_df
#from utils.graph.graph  import build_cyto_from_networkx

def coworker_network(selected_countries, selected_cities, selected_districts, selected_grouped_functions, selected_religions, selected_ids, selected_time_period: list = [1855, 1925], end_inclusive: bool=False, top: int=50):
    # copy dataset
    START = time.time()
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


    overlaps_df = pd.DataFrame(overlaps.values())

    # filter top employees
    first = overlaps_df.groupby("First Employee")["Duration"].sum()
    second = overlaps_df.groupby("Second Employee")["Duration"].sum()
    durations_df = first.add(second, fill_value=0)

    top_employees = durations_df.sort_values(ascending=False).head(top).index.tolist()

    overlaps_df = overlaps_df[(overlaps_df["First Employee"].isin(top_employees)) & (overlaps_df["Second Employee"].isin(top_employees))]
    print(len(overlaps_df))
    print(time.time() - START)

    START = time.time()

    G = nx.Graph()
    for _, record in overlaps_df.iterrows():
        G.add_edge(
            record["First Employee"],
            record["Second Employee"],
            weight=record["Duration"],
        )
    print(time.time() - START)
    return G
coworker_network([],[],[],[],[],[])
"""
def generate_filtered_cowork_elements(df): #wrapper function just to pass
    cowork_df = find_coworking_network_df(df, 5)
    G = build_cowork_graph_from_df(cowork_df)
    
    return build_cyto_from_networkx(G, is_colored=True)





def generate_filtered_cowork_bardf(
    selected_countries=None,
    selected_cities=None,
    selected_districts=None,
    selected_agencies=None,
    selected_time_period=None,
    selected_religions=None,
    selected_grouped_functions=None,
    selected_ids=None,
):
    df = generate_filtered_cowork_networkdf(selected_countries,selected_cities,selected_districts,selected_agencies,
    selected_time_period,selected_religions,None)

    if df.empty:
        return pd.DataFrame()  # Return an empty dataframe if no data is found
    
    if selected_grouped_functions:
        df = df[df["Grouped_Functions"].isin(selected_grouped_functions)]
        
    cowork_df = find_coworking_network_df(df, 5)
    
    print(cowork_df.columns)
    
    if 'employee_1' in cowork_df.columns and 'employee_2' in cowork_df.columns:
        cowork_df['employee_pair'] = cowork_df['employee_1'].astype(str) + " - " + cowork_df['employee_2'].astype(str)
    else:
        return pd.DataFrame()  # Return empty DataFrame if columns are missing

    return cowork_df.nlargest(10, 'overlap_years')


# graph node places precomputation, if needed
def build_cowork_graph_from_df(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(
            row["employee_1"],
            row["employee_2"],
            weight=row["overlap_years"],
            agency=row["agency"],
            start=row["start"],
            end=row["end"],
        )
    return G



#for bar plot
def get_most_connected_employees(G, top_n=10):
    degrees = dict(G.degree())  # dict: {employee_id: degree}
    # Convert to DataFrame for plotting
    df_degree = pd.DataFrame(degrees.items(), columns=['employee', 'connections'])
    df_degree = df_degree.sort_values(by='connections', ascending=False).head(top_n)
    return df_degree"""