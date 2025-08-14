import dash
from services.request import request
from utils.graph.graph import gantt, table, graph
from utils.callbacks.figure_callbacks import create_figure_callback
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

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
            "Use the search bar to find an employee by name. The profile card will populate with their key information, including nationality, religion, total career length, and the number of unique agencies they served in, providing an at-a-glance summary.\n\nThis Gantt-style chart maps the selected employee's entire career chronologically. Each bar represents a position held at a specific agency, with its length indicating the duration. Hover over any bar to see detailed information about that specific assignment. To improve visual clarity, we have limited the chart to display only 100 periods.",
            {
                "profile-card": {
                    "filter": filter("profile-card", True, True, True, True, True)
                },
                "career-timeline": {}
            }
        )
    ]
    
create_figure_callback(lambda **kwargs: request("employee-profiles", **kwargs), lambda df: graph(table(df, "Employee Profile Card")), "profile-card", True, True, True, True, True, filter_id="profile-card")
create_figure_callback(lambda **kwargs: request("career-timeline", **kwargs), lambda df: graph(gantt(df, "Years", "Agencies", "Employee Career Timeline by Agency")), "career-timeline", True, True, True, True, True, filter_id="profile-card")