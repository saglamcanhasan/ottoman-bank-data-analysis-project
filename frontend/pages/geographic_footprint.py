import dash
from utils.graph.graph import geo
from services.request import request
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.callbacks.filter_callbacks import create_agency_dropdown_callback
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

# callbacks
create_agency_dropdown_callback("agency-map")
create_figure_callback(lambda **kwargs: request("geo-footprint", **kwargs), lambda elements: geo(elements[0] if elements is not None and type(elements) is not str else elements, elements[1] if elements is not None and type(elements) is not str else None), "agency-map", True, True, True, True, True)