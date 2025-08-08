import dash
from dash import html
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.graph.graph import plot_gantt
from utils.server.employee_profiles_analysis import get_multiple_employees_gantt_data
dash.register_page(__name__, path="/employee-profiles")

sections = ["Profile Card & Career Timeline"]

def layout():
    return [introduction(
            "Employee Profiles",
            "Transform the dataset from anonymous points into rich, human histories. Use the search tools to find any individual in the archives and explore their entire career journey with the bank from start to finish.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "Use the search bar to find an employee by name. The profile card will populate with their key information, including nationality, religion, total career length, and the number of unique agencies they served in, providing an at-a-glance summary.\n\nThis Gantt-style chart maps the selected employee's entire career chronologically. Each bar represents a position held at a specific agency, with its length indicating the duration. Hover over any bar to see detailed information about that specific assignment.",
            {
                "profile-card": {
                    "figure": {},
                    "filter": filter("profile-card", False, False, False, False, False, True)
                },
                "career-timeline": {
                    "figure": {}
                }
            }
        )
    ]
    

create_figure_callback(
    generate_df=get_multiple_employees_gantt_data,  # The named argument (keyword argument)
    generate_figure=lambda df: plot_gantt(df,"Start",  "Finish", "Task" ,"Task",  "How many years", "Countries Employee Worked in"),
    figure_id="profile-card",       
    agency=False, grouped_function=False, religion=False, id=False, time_period=False, search = True
)