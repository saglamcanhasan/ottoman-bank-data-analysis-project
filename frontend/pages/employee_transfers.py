import dash
from services.request import request
from utils.graph.graph import sankey, graph
from utils.callbacks.figure_callbacks import create_figure_callback
from utils.callbacks.filter_callbacks import create_agency_dropdown_callback
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
            "This undirected graph visualizes the movement of employees between agencies. Each node represents an agency, and the thickness of the connecting lines indicates the volume of transfers. This map reveals the central 'hubs' that processed the most employee movement.",
            {
                "transfer-network": {
                    "filter": filter("transfer-network", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This Sankey diagram provides an alternative and intuitive view of employee transfers, elaborating on the transfer network above by showing them in a directed way - distinguishing between incoming and outgoing employees. with the bar color ranging from blue to gold to red indicating this value on an increasing scale. The width of each flow is directly proportional to the number of employees moving from a source agency to a target agency, making it easy to identify the most significant transfer routes.",
            {
                "transfer-flow": {
                    "filter": filter("transfer-flow", True, True, True, True, True)
                }
            }
        )
    ]

# callbacks
create_agency_dropdown_callback("transfer-network")
create_figure_callback(lambda **kwargs: request("employee-transfers", **kwargs), lambda elements: graph(elements), "transfer-network", True, True, True, True, True)

create_agency_dropdown_callback("transfer-flow")
create_figure_callback(lambda **kwargs: request("employee-flow", **kwargs), lambda elements: graph(sankey(elements, "Employee Flow Between Agencies")), "transfer-flow", True, True, True, True, True)