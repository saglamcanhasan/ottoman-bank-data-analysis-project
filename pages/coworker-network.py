import pandas as pd
from itertools import combinations
from dash import dcc, html, Input, Output, callback
import networkx as nx
import dash_cytoscape as cyto
import numpy as np
import dash

# page path
dash.register_page(__name__, path="/coworker-network")

# Load data
df = pd.read_excel("combined_data.xlsx")

# Build coworking overlap df
def find_coworking_network(df):
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
                overlaps.append({
                    "employee_1": emp1["employee_code"],
                    "employee_2": emp2["employee_code"],
                    "agency": emp1["agency"],
                    "overlap_years": overlap_years,
                    "start": overlap_start,
                    "end": overlap_end
                })

    return pd.DataFrame(overlaps)



cowork_df = find_coworking_network(df)
cowork_df = cowork_df[cowork_df["overlap_years"] >= 5]
cowork_df = cowork_df.nlargest(1000000, "overlap_years") # for optimization rn holds all graph in memory



# Precompute full graph for layout, for optimization
full_graph = nx.Graph()
for _, row in cowork_df.iterrows():
    full_graph.add_edge(row["employee_1"], row["employee_2"])

# Fix node positions once globally
fixed_positions = nx.spring_layout(full_graph, seed=42)


# Dropdown options for agency
agency_options = [{'label': 'All', 'value': 'All'}] + [
    {'label': agency, 'value': agency} for agency in sorted(cowork_df['agency'].unique())
]



# Layout
# Required layout variable for Dash Pages
layout = html.Div([
    html.H1("Coworking Employee Network"),

    html.Div([
        html.Label("Select Agency:"),
        dcc.Dropdown(id='agency-dropdown', options=agency_options, value='All'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Year Range:"),
        dcc.RangeSlider(
            id='year-range-slider',
            min=1855,
            max=1925,
            step=1,
            value=[1855, 1925],
            marks={year: str(year) for year in range(1855, 1926, 10)},
            tooltip={"placement": "bottom", "always_visible": False}
        )
    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),

    cyto.Cytoscape(
        id='cytoscape-network',
        style={'width': '100%', 'height': '700px'},
        layout={'name': 'preset', 'animate': False}
    )
])

# Callback to filter graph - event listener
@callback(
    Output('cytoscape-network', 'elements'),
    Input('agency-dropdown', 'value'),
    Input('year-range-slider', 'drag_value')
)
def update_graph(selected_agency, year_range):
    start_year, end_year = year_range

    # Filter by agency
    if selected_agency == 'All':
        filtered =  cowork_df.nlargest(10000, "overlap_years") # there is 4 mil connections too much to show. looking at all, show only top 50k
    else:
        filtered = cowork_df[cowork_df['agency'] == selected_agency]

    # Filter by time range 
    filtered = filtered[
        (filtered['start'] <= end_year) & (filtered['end'] >= start_year)
    ]

    filtered = filtered.nlargest(10000, "overlap_years")

    # Build network
    G = nx.Graph()
    for _, row in filtered.iterrows():
        G.add_edge(
            row["employee_1"],
            row["employee_2"],
            weight=row["overlap_years"],
            agency=row["agency"]
        )

    elements = []
    for node in G.nodes():
        pos = fixed_positions.get(node, [0, 0])
        elements.append({
            "data": {"id": node, "label": node},
            "position": {"x": pos[0] * 1000, "y": pos[1] * 1000}
        })


    for source, target, data in G.edges(data=True):
        elements.append({
            "data": {
                "source": source,
                "target": target,
                "label": f"{data['weight']} years"
            }
        })

    return elements
