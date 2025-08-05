import dash
from dash import html
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
            "This bar chart ranks agencies by their total number of employees, making it easy to distinguish major commercial hubs from smaller regional outposts. Use this to quickly identify the most significant branches in the network.",
            {
                "top-agencies": {
                    "figure": {},
                    "filter": filter("top-agencies", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This chart visualizes employee loyalty at the local level by showing the average number of years employees stayed at each agency. Branches with higher tenure may indicate greater stability or more favorable working conditions.",
            {
                "employee-tenure": {
                    "figure": {},
                    "filter": filter("employee-tenure", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[2],
            "This scatter plot explores the relationship between the number of employees at an agency (size) and how long they typically stayed (tenure). Look for patterns or outliers to understand if larger, central offices had different retention profiles than smaller, regional ones.",
            {
                "size-vs-tenure": {
                    "figure": {},
                    "filter": filter("size-vs-tenure", True, True, True, True, True)
                }
            }
        )
    ]