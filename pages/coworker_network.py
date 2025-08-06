import dash
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents
from utils.graph import plot_bar, build_cyto_from_networkx, plot_cyto
from utils.coworker_network_analysis import find_coworking_network_df, build_cowork_graph_from_df, sample_rand_df
from utils.data_loader import employee_dataset

dash.register_page(__name__, path="/coworker-network")

sections = ["Co-worker Graph", "Most Connected Employees"]

df = find_coworking_network_df(employee_dataset, min_years=5)
df = sample_rand_df(df, 500)
G = build_cowork_graph_from_df(df)
network_fig = build_cyto_from_networkx(G,None,True)
#network_fig = plot_cyto(G, "network_fig")

def layout():
    return [introduction(
            "Co-worker Network",
            "Uncover the hidden social fabric of the Ottoman Bank. This section visualizes the professional relationships between all employees, allowing you to identify influential connectors and understand the bank's internal community structure.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This graph displays the entire employee social network. Each node is an employee, and a link is created between two nodes if they worked at the same agency during the same time period. Explore this network to find clusters of colleagues (professional cliques) and central individuals who connected disparate parts of the organization.",
            {
                "coworker-graph": {
                    "figure": network_fig
                    #"filter": filter("agency", True, True, True, True, True)
                }
            },
            is_cytoscape = True
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This table ranks employees by their 'degree centrality' - the number of unique colleagues they worked with during their tenure. Individuals at the top of this list were the most central social connectors in the bank's network.",
            {
                "connected-employees": {
                    "figure": {},
                    "filter": filter("connected-employees", True, True, True, True, True)
                }
            }
        )
    ]