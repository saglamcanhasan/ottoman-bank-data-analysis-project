import dash
from dash import html
from widgets.content import introduction, content

dash.register_page(__name__, path="/")

def layout():
    return introduction(
        "Welcome to the Ottoman Bank Historical Dashboard",
"""Welcome to the Ottoman Bank Historical Dashboard, an interactive data visualization and analytics platform built upon a rich dataset curated from the personnel files of the Ottoman Bank Archives. Spanning the late 19th and early 20th centuries, this dashboard transforms over 6,000 archival records into a dynamic experience, allowing you to explore individual career trajectories, uncover the institution's hidden social networks, and analyze the performance of its many agencies across the empire.""",
    content(
        "",
        """This tool is designed for historians, researchers, data scientists, and anyone curious about the intersection of finance, society, and data in the late Ottoman era.

To begin your exploration, select a dashboard from the navigation bar above. Each tab offers a unique scale of analysis, from the high-level Institutional Dashboard to the granular Personnel Explorer."""
        )
    )