import dash
from dash import html
from widgets.content import introduction, content

dash.register_page(__name__, path="/")

def layout():
    return introduction(
        "Welcome to the Ottoman Bank Historical Dashboard",
"""The Ottoman Bank Historical Dashboard is an interactive data visualization and analytics platform built upon a rich dataset curated from the personnel files of the Ottoman Bank Archives. Spanning the late 19th and early 20th centuries, this dashboard transforms over 6,000 archival records into a dynamic experience, allowing you to explore individual career trajectories, uncover the institution's hidden social networks, and analyze agencies across the empire.""",
    content(
        "",
        """This tool is designed for anyone interested in exploring the historical, social, and organizational dimensions of the Ottoman Bank through data.

The Institutional Dashboard provides an overview of the Ottoman Bank and its overall structure. The Agency Dashboard allows for analysis and comparison of agencies while highlighting their interconnections. The Employee Dashboard offers a detailed view of individual employees and the relationships between them, capturing the social and professional networks within the Bank.

To begin your exploration, select a dashboard from the navigation bar above."""
        )
    )