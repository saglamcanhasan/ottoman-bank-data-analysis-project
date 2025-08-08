from itertools import combinations
from utils.graph.graph  import build_cyto_from_networkx
import pandas as pd
import networkx as nx
from utils.server.data_loader import employee_df


def find_coworking_network_df(df, min_years=5): # for all data
    overlaps = []
    for emp1, emp2 in combinations(df.to_dict("records"), 2):
        if emp1["Agency"] == emp2["Agency"]:
            if (pd.isna(emp1["Career Start Year"]) or pd.isna(emp1["Career End Year"]) or
                pd.isna(emp2["Career Start Year"]) or pd.isna(emp2["Career End Year"])):
                continue

            if emp1["ID"] == emp2["ID"]:
                continue
                
            if emp1["Career Start Year"] <= emp2["Career End Year"] and emp2["Career Start Year"] <= emp1["Career End Year"]:
                overlap_start = max(emp1["Career Start Year"], emp2["Career Start Year"])
                overlap_end = min(emp1["Career End Year"], emp2["Career End Year"])
                overlap_years = overlap_end - overlap_start + 1
                
                if overlap_years >= min_years:
                    overlaps.append({
                        "employee_1": emp1["ID"],
                        "employee_2": emp2["ID"],
                        "Agency": emp1["Agency"],
                        "overlap_years": overlap_years,
                        "start": overlap_start,
                        "end": overlap_end
                    })

    return pd.DataFrame(overlaps)

def sample_rand_df(df, num): # sample num amount of random rows from df does not give err if df < num
    sample_size = min(num, len(df))
    return df.sample(n=sample_size, random_state=42)


sample_df = sample_rand_df(employee_df, 1000)

def generate_filtered_cowork_networkdf(
    selected_countries=None,
    selected_cities=None,
    selected_districts=None,
    selected_agencies=None,
    selected_time_period=None,
    selected_religions=None,
    selected_id=None
):
    filtered = sample_df.copy()
    selected_startyear, selected_endyear = selected_time_period if selected_time_period else (None, None)
    
    # Basic filters
    if selected_countries:
        filtered = filtered[filtered["Country"].isin(selected_countries)]
    if selected_cities:
        filtered = filtered[filtered["City"].isin(selected_cities)]
    if selected_districts:
        filtered = filtered[filtered["District"].isin(selected_districts)]
    if selected_agencies:
        filtered = filtered[filtered["Agency"].isin(selected_agencies)]
    if selected_religions:
        filtered = filtered[filtered["Religion"].isin(selected_religions)]

    # Timeframe filtering
    if selected_startyear is not None and selected_endyear is not None:
        filtered = filtered.copy()
        filtered["Career Start Year"] = pd.to_numeric(filtered["Career Start Year"], errors="coerce").fillna(0).astype(int)
        filtered["Career End Year"] = pd.to_numeric(filtered["Career End Year"], errors="coerce").fillna(9999).astype(int)

        # Keep only rows where the time range overlaps with selected range
        filtered = filtered[
            (filtered["Career Start Year"] <= selected_endyear) &
            (filtered["Career End Year"] >= selected_startyear)
        ]

    return sample_rand_df(filtered, 100)

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
            agency=row["Agency"],
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
    return df_degree