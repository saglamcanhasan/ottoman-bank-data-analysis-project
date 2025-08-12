import dash
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

dash.register_page(__name__, path="/geographic-footprint")

sections = ["Agency Map"]

def layout():
    return [introduction(
            "Geographic Footprint",
            "Visualize the global reach of the Ottoman Bank across the empire and beyond. This interactive map provides a clear spatial understanding of the bank's operational presence and its most significant commercial hubs.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This map plots the location of every bank agency. Hover over a marker to see the agency's name and details. The size of each marker corresponds to the number of employees, making it easy to identify major operational centers. Use the timeline slider below to filter the agencies that were active in any specific year.",
            {
                "agency-map": {
                    "figure": {},
                    "filter": filter("agency-map", True, True, True, True, True)
                }
            }
        )
    ]