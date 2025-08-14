import dash
from services.request import request
from utils.graph.graph import bar, graph
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.callbacks.filter_callbacks import create_agency_dropdown_callback
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

dash.register_page(__name__, path="/coworker-network")

sections = ["Co-workers Graph", "Most Connected Employees", "Longest Working Partnerships"]


def layout():
    return [introduction(
            "Co-worker Network",
            "Uncover the hidden social fabric of the Ottoman Bank. This section visualizes the professional relationships between top employees, allowing you to identify influential connectors and understand the bank's internal community structure.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This graph displays the employee social network. Each node represents an employee, with its size proportional to the sum of the durations of all their connections. Each edge represents one of the top 1,000 longest overlapping work periods between two employees after the current filters are applied, with edge thickness proportional to the duration of that connection. This focus on the strongest professional ties helps highlight central connectors and clusters in the network. Adjusting the filters may reveal different relationships, shift the relative importance of employees, or bring other links into view.",
            {
                "coworker-network": {
                    "filter": filter("coworker-network", True, True, True, True, True)

                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This table ranks employees by their 'degree centrality' - the number of unique colleagues they worked with during their tenure. Individuals at the top of this list were the most central social connectors in the bank's network.",
            {
                "employee-connection": {
                    "filter": filter("employee-connection", True, True, True, True, True)
                }
            }
        ),
        
        horizontal_separator(),
        
        section(
            sections[2],
            "This bar chart showcases the top 10 employee pairs who have spent the longest time working together at the same agency. By analyzing their overlap years, we identify the most enduring professional partnerships within the Ottoman Bank.",
            {
                "partner-employees": {
                    "filter": filter("partner-employees", True, True, True, True, True)
                }
            }
        )
    ]
    
    
# callbacks
create_agency_dropdown_callback("coworker-network")
create_figure_callback(lambda **kwargs: (lambda data, index: data[index] if isinstance(data, list) else data)(request("coworker-network", **kwargs), 0), lambda elements: graph(elements), "coworker-network", True, True, True, True, True)

create_agency_dropdown_callback("employee-connection")
create_figure_callback(lambda **kwargs: (lambda data, index: data[index] if isinstance(data, list) else data)(request("coworker-network", **kwargs), 1), lambda df: graph(bar(df, "Employee", "Connections", "Degree Centrality", -1, "h")), "employee-connection", True, True, True, True, True)

create_agency_dropdown_callback("partner-employees")
create_figure_callback(lambda **kwargs: (lambda data, index: data[index] if isinstance(data, list) else data)(request("coworker-network", **kwargs), 2), lambda df: graph(bar(df, "Co-Workers", "Years", "Longest Professional Partnerships", -1, "h")), "partner-employees", True, True, True, True, True)