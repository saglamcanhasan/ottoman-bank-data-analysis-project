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
            "Transform the dataset from anonymous points into rich, human histories. Use the filtering tools to find any individual in the archives and explore their entire career journey with the bank from start to finish.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "Use the filters to locate an employee. This table displays key details such as religion, total career length, and the number of unique agencies served, offering a concise overview of filtered employees. The accompanying Gantt-style chart traces the employees’ career in chronological order, displaying only 100 periods for visual clarity. Each bar represents a distinct period marked by events such as position changes, agency transfers, or salary adjustments with its length showing the duration. Hovering over a bar reveals detailed information about that period.",
            {
                "profile-card": {
                    "filter": filter("profile-card", True, True, True, True, True)
                },
                "career-timeline": {}
            }
        )
    ]

# callbacks
create_figure_callback(lambda **kwargs: request("employee-profiles", **kwargs), lambda df: graph(table(df, "Employee Profile Card")), "profile-card", True, True, True, True, True, filter_id="profile-card")
create_figure_callback(lambda **kwargs: request("career-timeline", **kwargs), lambda df: graph(gantt(df, "Years", "Employees", "Employee Career Timeline by Agency")), "career-timeline", True, True, True, True, True, filter_id="profile-card")