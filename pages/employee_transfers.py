import dash
from dash import html
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

dash.register_page(__name__, path="/employee-transfers")

sections = ["Agency Transfer Network", "Transfer Flow"]

def layout():
    return [introduction(
            "Employee Transfers",
            "Follow the flow of talent across the bank's network. These visualizations reveal the primary pathways for personnel movement, highlighting the connections between central and regional offices.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This directed graph visualizes the movement of employees between agencies. Each node represents an agency, and the thickness of the connecting lines indicates the volume of transfers. This map reveals the central 'hubs' that processed the most employee movement.",
            {
                "transfer-network": {
                    "figure": {},
                    "filter": filter("transfer-network", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This Sankey diagram provides an alternative and intuitive view of employee transfers. The width of each flow is directly proportional to the number of employees moving from a source agency (left) to a target agency (right), making it easy to quantify the most significant transfer routes.",
            {
                "transfer-flow": {
                    "figure": {},
                    "filter": filter("transfer-flow", True, True, True, True, True)
                }
            }
        )
    ]