import dash
from dash import html
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
                "national-distribution": {
                    "figure": {},
                    "filter": filter("national-distribution", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This chart shows the percentage of employees belonging to different religious groups. When viewed alongside the nationality data, it provides a deeper insight into the bank's staffing policies and the diverse communities it employed.",
            {
                "religious-distribution": {
                    "figure": {},
                    "filter": filter("religious-distribution", True, True, True, True, True)
                }
            }
        )
    ]