import dash
from dash import html
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.graph.graph import bar, plot_table, plot_box
from utils.server.agency_performance_analysis import generate_agency_vs_avgtenuredf, generate_top_agency_empcountdf, generate_emp_tenuredf
from utils.callbacks.filter_callbacks import create_agency_dropdown_callback

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
                    "figure": {},
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
                    "figure": {},
                    "filter": filter("size-vs-tenure", True, True, True, False, True)
                }
            }
        )
    ]
    
    
    
 
create_figure_callback(generate_top_agency_empcountdf, lambda df: bar(df, 'City','Unique Employee Count', "Top Agencies by Employee Count",0, "h", "Number of Employees", "Agencies"), "top-agencies", True, True, True, False, True, False, filter_id="top-agencies")

create_figure_callback(generate_emp_tenuredf, lambda df: plot_box(df, 'City', 'Tenure','City',"Average Employee Tenure by Agency", "Agencies","Tenure" , False), "employee-tenure", True, True, True, False, True, False, filter_id="employee-tenure")
create_agency_dropdown_callback("employee-tenure")

create_figure_callback(generate_agency_vs_avgtenuredf, lambda df: plot_table(df, None, "k"), "size-vs-tenure", True, True, True, False, True, False, filter_id="size-vs-tenure")