import dash
from utils.graph import plot
from utils.historical_overview_analysis import open_agencies
from widgets.content import introduction, horizontal_separator, section, filter, table_of_contents

dash.register_page(__name__, path="/historical-overview")

agency_number_fig = plot(open_agencies(), "Year", "Agency Count", "Number of Agencies vs Year")

sections = ["Total Employees", "Number of Agencies", "Employee Turnover"]

def layout():
    return [introduction(
            "Historical Overview",
            "Trace the life cycle of the Ottoman Bank from its founding years to its later stages. This section features core institutional metrics that reveal periods of growth, consolidation, and workforce stability.",
            table_of_contents(sections)
        ),

        horizontal_separator(),

        section(
            sections[0],
            "This line chart displays the total number of active employees across all branches for each year. Look for steep inclines, which indicate periods of rapid hiring and expansion, versus plateaus or declines, which may correspond to historical events or strategic shifts.",
            {
                "total-employees": {
                    "figure": {},
                    "filter": filter("total-employees", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[1],
            "This line chart tracks the growth of the bank's physical presence by showing the total number of active agencies over time. Compare this with the employee chart to see if workforce growth was driven by opening new branches or expanding existing ones.",
            {
                "agency-number": {
                    "figure": agency_number_fig,
                    "filter": filter("agency-number", True, True, True, True, True)
                }
            }
        ),

        horizontal_separator(),

        section(
            sections[2],
            "This chart visualizes the bank's workforce dynamics by plotting new hires against departures for each year. Spikes in departures can indicate periods of instability, while sustained hiring shows institutional confidence and expansion. The net change reveals the overall workforce growth or shrinkage.",
            {
                "employee-turnover": {
                    "figure": {},
                    "filter": filter("employee-turnover", True, True, True, True, True)
                }
            }
        )
    ]