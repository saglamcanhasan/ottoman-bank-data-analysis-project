from itertools import combinations
import pandas as pd
import networkx as nx

def find_coworking_network_df(df, min_years=5): # for all data
    overlaps = []
    for emp1, emp2 in combinations(df.to_dict("records"), 2):
        if emp1["agency"] == emp2["agency"]:
            if (pd.isna(emp1["start_year"]) or pd.isna(emp1["end_year"]) or
                pd.isna(emp2["start_year"]) or pd.isna(emp2["end_year"])):
                continue

            if emp1["employee_code"] == emp2["employee_code"]:
                continue
                
            if emp1["start_year"] <= emp2["end_year"] and emp2["start_year"] <= emp1["end_year"]:
                overlap_start = max(emp1["start_year"], emp2["start_year"])
                overlap_end = min(emp1["end_year"], emp2["end_year"])
                overlap_years = overlap_end - overlap_start + 1
                
                if overlap_years >= min_years:
                    overlaps.append({
                        "employee_1": emp1["employee_code"],
                        "employee_2": emp2["employee_code"],
                        "agency": emp1["agency"],
                        "overlap_years": overlap_years,
                        "start": overlap_start,
                        "end": overlap_end
                    })

    return pd.DataFrame(overlaps)

def sample_rand_df(df, num): # sample num amount of random rows from df does not give err if df < num
    sample_size = min(num, len(df))
    return df.sample(n=sample_size, random_state=42)


def get_most_connected_employees(G, top_n=10):
    degrees = dict(G.degree())  # dict: {employee_id: degree}
    # Convert to DataFrame for plotting
    df_degree = pd.DataFrame(degrees.items(), columns=['employee', 'connections'])
    df_degree = df_degree.sort_values(by='connections', ascending=False).head(top_n)
    return df_degree


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
