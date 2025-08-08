import dash
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents
from utils.graph.graph import plot_bar, plot, bar
from utils.server.coworker_network_analysis import generate_filtered_cowork_networkdf, generate_filtered_cowork_elements, generate_filtered_cowork_bardf, generate_filtered_top_connected_emp
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.callbacks.filter_callbacks import create_agency_dropdown_callback

dash.register_page(__name__, path="/coworker-network")

sections = ["Top Co-workers Graph", "Most Connected Employees", "Longest Working Partnerships"]


def layout():
    return [introduction(
            "Co-worker Network",
            "Uncover the hidden social fabric of the Ottoman Bank. This section visualizes the professional relationships between top employees, allowing you to identify influential connectors and understand the bank's internal community structure.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This graph displays the top 50 employee's social network. Each node is an employee, and a link is created between two nodes if they worked at the same agency during the same time period. Explore this network to find clusters of colleagues (professional cliques) and central individuals who connected disparate parts of the organization.",
            {
                "cowork-network-graph": {
                    "figure":{},
                    "filter": filter("cowork-network-graph", True, True, True, True, True)

                }
            },
            is_cyto = True
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This table ranks employees by their 'degree centrality' - the number of unique colleagues they worked with during their tenure. Individuals at the top of this list were the most central social connectors in the bank's network.",
            {
                "degree-centrality": {
                    "figure": {},
                    "filter": filter("degree-centrality", True, True, True, True, True)
                }
            }
        ),
        
        horizontal_separator(),
        
        section(
            sections[2],
            "This bar chart showcases the top 10 employee pairs who have spent the longest time working together at the same agency. By analyzing their overlap years, we identify the most enduring professional partnerships within the Ottoman Bank.",
            {
                "connected-employees": {
                    "figure": {},
                    "filter": filter("connected-employees", True, True, True, True, True)
                }
            }
        )
    ]
    
    
# callbacks
create_agency_dropdown_callback("cowork-network-graph")
create_figure_callback(
    generate_df=generate_filtered_cowork_networkdf,
    generate_figure=generate_filtered_cowork_elements,
    figure_id="cowork-network-graph",
    agency=True,
    grouped_function=False,
    religion=True,
    id=False,
    time_period=True,
    is_cyto=True
)

create_agency_dropdown_callback("degree-centrality")
create_figure_callback(
    generate_df=generate_filtered_top_connected_emp, 
    generate_figure=lambda df: plot_bar(df,"connections",  "employee", "Employee vs. Degree Centrality", "Degree of Centrality - Unique Collauges", "Employee", horizontal=True),
    figure_id="degree-centrality",    
    agency=True, grouped_function=True, religion=True, id=True, time_period=True  
)



create_agency_dropdown_callback("connected-employees")
create_figure_callback(
    generate_df=generate_filtered_cowork_bardf,  # The named argument (keyword argument)
    generate_figure=lambda df: plot_bar(df,"overlap_years",  "employee_pair", "Employee Pairs vs. Years of Cowork","overlap years",  "employees", horizontal=True),
    figure_id="connected-employees",              # The figure ID as a positional argument
    agency=True, grouped_function=True, religion=True, id=True, time_period=True  # Other boolean arguments
)



