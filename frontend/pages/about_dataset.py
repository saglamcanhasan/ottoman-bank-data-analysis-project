import dash
from dash import html
from widgets.content import introduction, content

dash.register_page(__name__, path="/about-dataset")

def layout():
    return introduction(
        "About the Dataset",
"""The data powering this dashboard is sourced directly from the rich historical collections of the Ottoman Bank Archives, now managed by SALT Research. This project would not be possible without their extensive archival and digitization efforts.
The dataset comprises over 6,000 digitized personnel files from the late 19th and early 20th centuries. Each record contains valuable, though sometimes incomplete, information including employee names, genders, positions held, agency assignments, transfer histories, and promotion dates.""",
    content(
        "Processing & Limitations",
        "As is common with historical records, the raw data presented significant challenges, including missing values, ambiguous dates, and inconsistencies in spelling and formatting across entries. Our team undertook a considerable data cleaning, standardization, and imputation process to create the structured dataset used in these visualizations. While every effort was made to ensure accuracy, users should interpret the data with an awareness of its historical nature and inherent imperfections."
        )
    )