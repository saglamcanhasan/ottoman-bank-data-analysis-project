import dash
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

dash.register_page(__name__, path="/coworker-network")

sections = ["Co-worker Graph", "Most Connected Employees"]

def layout():
    return [introduction(
            "Co-worker Network",
            "Uncover the hidden social fabric of the Ottoman Bank. This section visualizes the professional relationships between all employees, allowing you to identify influential connectors and understand the bank's internal community structure.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This graph displays the entire employee social network. Each node is an employee, and a link is created between two nodes if they worked at the same agency during the same time period. Explore this network to find clusters of colleagues (professional cliques) and central individuals who connected disparate parts of the organization.",
            {
                "coworker-graph": {
                    "figure": {},
                    "filter": filter("coworker-graph", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This table ranks employees by their 'degree centrality' - the number of unique colleagues they worked with during their tenure. Individuals at the top of this list were the most central social connectors in the bank's network.",
            {
                "connected-employees": {
                    "figure": {},
                    "filter": filter("connected-employees", True, True, True, True, True)
                }
            }
        )
    ]