import dash
from services.request import request
from utils.graph.graph import plot, pie, combine, graph
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.callbacks.filter_callbacks import create_agency_dropdown_callback
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

dash.register_page(__name__, path="/workforce-demographics")

sections = ["National Distribution", "Religious Distribution"]

def layout():
    return [introduction(
            "Workforce Demographics",
            "Discover the human fabric of the institution. This section analyzes the composition of the entire workforce, reflecting the bank's hiring practices and the multicultural context in which it operated.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This chart breaks down the entire employee population by their recorded nationality. Use it to understand the diversity of the workforce and identify the dominant national groups that staffed the bank, both in the Levant and internationally.",
            {
                "nation-count": {
                    "filter": filter("nation-count", True, True, True, True, True)
                },
                "nation-distribution": {}
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This section shows the percentage of employees belonging to different religious groups. When viewed alongside the nationality data, it provides a deeper insight into the bank's staffing policies and the diverse communities it employed.",
            {
                "religion-count": {
                    "filter": filter("religion-count", True, True, False, True, True)
                },
                "religion-distribution": {}
            }
        )
    ]

# callbacks
create_agency_dropdown_callback("nation-count")
create_figure_callback(lambda **kwargs: request("nation-count", **kwargs), lambda df: graph(pie(df, "Nationality Composition of Employees")), "nation-count", True, True, True, True, True)
create_figure_callback(lambda **kwargs: request("nation-distribution", **kwargs), lambda df: graph(combine([plot(df, "Year", nationality, "", index) for index, nationality in enumerate(df.drop(columns=["Year"]).columns if df is not None and type(df) is not str else [df])], [], "Year", ["Ratio of Nationality"], "Nationality Composition vs. Year", "right")), "nation-distribution", True, True, False, True, True, filter_id="nation-count")

create_agency_dropdown_callback("religion-count")
create_figure_callback(lambda **kwargs: request("religion-count", **kwargs), lambda df: graph(pie(df, "Religious Composition of Employees")), "religion-count", True, True, False, True, True)
create_figure_callback(lambda **kwargs: request("religion-distribution", **kwargs), lambda df: graph(combine([plot(df, "Year", religion, "", index) for index, religion in enumerate(df.drop(columns=["Year"]).columns if df is not None and type(df) is not str else [df])], [], "Year", ["Ratio of Believing Employees"], "Religious Composition vs. Year", "right")), "religion-distribution", True, True, False, True, True, filter_id="religion-count")