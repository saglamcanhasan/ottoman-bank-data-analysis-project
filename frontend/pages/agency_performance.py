import dash
from services.request import request
from utils.graph.graph import bar, box, scatter, graph
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.callbacks.filter_callbacks import create_agency_dropdown_callback
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

dash.register_page(__name__, path="/agency-performance")

sections = ["Top Agencies by Employee Count", "Average Employee Tenure by Agency", "Agency Size vs. Employee Tenure"]

def layout():
    return [introduction(
            "Agency Performance",
            "How did individual branches stack up against each other? This section allows you to compare agencies using key metrics related to their size, employee experience, and operational nature.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This bar chart ranks agencies by their total number of unique employees, making it easy to distinguish major commercial hubs from smaller regional outposts. Use this to quickly identify the most significant branches in the network.",
            {
                "top-agencies": {
                    "filter": filter("top-agencies", True, True, True, False, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This chart visualizes employee loyalty at the local level by showing the average number of years employees stayed at each agency. Branches with higher tenure may indicate greater stability or more favorable working conditions.",
            {
                "employee-tenure": {
                    "filter": filter("employee-tenure", True, True, True, False, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[2],
            "This scatter plot explores the relationship between the number of employees at an agency (size) and how long they typically stayed (tenure). Look for patterns or outliers to understand if larger, central offices had different retention profiles than smaller, regional ones.",
            {
                "size-vs-tenure": {
                    "filter": filter("size-vs-tenure", True, True, True, False, True)
                }
            }
        )
    ]
  
# callbacks
create_agency_dropdown_callback("top-agencies")
create_figure_callback(lambda **kwargs: request("top-agencies", **kwargs), lambda df: graph(bar(df, "Agency", "Unique Employee Count", "Top Agencies by Unique Employee Count", -1, "h", "Number of Employees", "Agencies")), "top-agencies", True, True, True, False, True, filter_id="top-agencies")

create_agency_dropdown_callback("employee-tenure")
create_figure_callback(lambda **kwargs: request("employee-tenure", **kwargs), lambda df: graph(box(df, "Agency", "Tenure", "Agency", "Average Employee Tenure by Agency", "Agencies","Tenure" , False)), "employee-tenure", True, True, True, False, True, filter_id="employee-tenure")

create_figure_callback(lambda **kwargs: request("size-vs-tenure", **kwargs), lambda df: graph(scatter(df,  "Average Tenure", "Average Employee Count", "Average Agency Size vs. Average Employee Tenure", "Average Tenure", "Average Employee Count of Agency", ["Agency", "Min Employee Count", "Max Employee Count", "Min Tenure", "Max Tenure"])), "size-vs-tenure", True, True, True, False, True, filter_id="size-vs-tenure")