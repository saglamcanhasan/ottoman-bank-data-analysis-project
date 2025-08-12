import dash
import dash_bootstrap_components as dbc
from widgets.content import introduction, content

dash.register_page(__name__, path="/about-us")

def layout():
    return introduction(
        "About the Project",
"""The Ottoman Bank Through Graphs project was developed as a graduation project (ENS 491-492) at Sabancı University. Our core mission was to bridge the gap between historical inquiry and modern data science, demonstrating how computational tools can bring archival records to life in an accessible, interactive, and analytically powerful way.
By transforming passive historical records into an interactive dashboard, we aimed to create a platform that not only aids academic research but also serves as a compelling interactive educational tool.""",
        [dbc.Container([
            content(
            "Project Supervisor",
            """- [Selim Balcısoy](mailto:selim.balcisoy@sabanciuniv.edu)"""    
            ),
            content(
            "Project Team",
        """- [Utku Can Yıldız](mailto:utkuyildiz@sabanciuniv.edu)
- [Ahmet Burak Ekmekçioğlu](mailto:eahmet@sabanciuniv.edu)
- [Yusuf Eralp Kızıloğlu](mailto:ekiziloglu@sabanciuniv.edu)"""
            )],
            className="container"
        )
    ])