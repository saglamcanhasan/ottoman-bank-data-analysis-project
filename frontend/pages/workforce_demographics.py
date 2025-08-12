import dash
from services.request import request
from utils.graph.graph import plot, pie, combine
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
                    "figure": {},
                    "filter": filter("nation-distribution", True, True, True, True, True)
                },
                "nation-distribution": {
                    "figure": {}
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This section shows the percentage of employees belonging to different religious groups. When viewed alongside the nationality data, it provides a deeper insight into the bank's staffing policies and the diverse communities it employed.",
            {
                "religion-count": {
                    "figure": {},
                    "filter": filter("religion-count", True, True, False, True, True)
                },
                "religion-distribution": {
                    "figure": {}
                }
            }
        )
    ]

# callbacks
create_agency_dropdown_callback("religion-count")
create_figure_callback(lambda **kwargs: request("religion-count", **kwargs), lambda df:pie(df, "Religious Composition of Employees"), "religion-count", True, True, False, True, True)
create_figure_callback(lambda **kwargs: request("religion-distribution", **kwargs), lambda df: combine([plot(df, "Year", religion, "", index) for index, religion in enumerate(df.drop(columns=["Year"]).columns)], [], "Year", ["Ratio of Believing Employees"], "Religious Composition vs. Year", "right"), "religion-distribution", True, True, False, True, True, filter_id="religion-count")