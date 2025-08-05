import dash_bootstrap_components as dbc
from dash import html, dcc, get_asset_url

def introduction(title: str, description: str, right_widget=list()):
    return dbc.Container([
        dbc.Row([
            dbc.Col(content(title, description)),
            
            dbc.Col(right_widget)]
        )],
        className="introduction-container"
    )

def content(title: str, description: str):
    return [
        html.Header(
            title,
            className="introduction-title"
        ),

        dcc.Markdown(
            description,
            className="content-body"
        )
    ]

def table_of_contents(sections: list):
    return dbc.Container([
        dbc.Row([
            html.Header("Table of Contents", className="table-of-contents-title"),
        ]),
        html.Div(className="table-of-contents-horizontal-separator"),
        html.Ol([
            html.Li(
                html.A(
                    section_name,
                    href=f"#{section_name}",
                    className="table-of-contents-section-link"
                ),
                className="table-of-contents-title"
            )
            for section_name in sections],
            className="table-of-contents-section-container"
        )],
        className="table-of-contents-container"
    )

def vertical_separator():
    return html.Div(className="content-vertical-separator")

def horizontal_separator():
    return html.Div(className="content-horizontal-separator")

def section(title: str, description: str, figures: dict=dict()):
    figure_rows = list()
    for figure_id in figures:
        # extract figure info
        figure_dict = figures[figure_id]

        figure = figure_dict["figure"]
        filter = figure_dict.get("filter", None)

        # generate a row
        cols = list()

        cols.append(dbc.Col(dcc.Graph(figure=figure, id=figure_id, className="graph"), width=8, className="figure-container"))
        if filter is not None:
            cols.append(dbc.Col(vertical_separator(), width=1))
            cols.append(dbc.Col(filter, width=3))

        row = dbc.Row(cols, justify="center")
        figure_rows.append(row)

    containers = list()
    containers.append(
        dbc.Container([
            # title and description
            dbc.Row(
                dbc.Col([
                    html.Header(
                        title,
                        id=title,
                        className="content-title"
                    ),

                    html.P(
                        description,
                        className="content-body"
                    )]
                )
            )],
            className="content-container",
            fluid=True
        )
    )
    if len(figure_rows) != 0:
        containers.append(
            dbc.Container(figure_rows, className="figure-filter-container", fluid=True)
        )

    return dbc.Container(containers, className="section-container", fluid=True)

def filter(filter_id: str, id: bool, agency: bool, nationality: bool, religion: bool, time_period: bool):
    filter_rows = []

    if id:
        ids = ["ID1", "ID2", "ID3"]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Employee ID", html_for=f"{filter_id}-id-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-id-dropdown",
                    options=[{"label": id, "value": id} for id in ids],
                    placeholder="select an employee ID",
                    className="filter-dropdown"
                )
            ])
        )

    if agency:
        agencies = ["Agency A", "Agency B", "Agency C"]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Agency", html_for=f"{filter_id}-agency-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-agency-dropdown",
                    options=[{"label": agency, "value": agency} for agency in agencies],
                    multi=True,
                    placeholder="select one or more agencies",
                    className="filter-dropdown"
                )
            ])
        )

    if nationality:
        nationalities = ["Turkish", "Greek", "Armenian"]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Nationality", html_for=f"{filter_id}-nationality-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-nationality-dropdown",
                    options=[{"label": nationality, "value": nationality} for nationality in nationalities],
                    multi=True,
                    placeholder="select nationalities",
                    className="filter-dropdown"
                )
            ])
        )

    if religion:
        religions = ["Islam", "Christianity", "Judaism"]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Religion", html_for=f"{filter_id}-religion-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-religion-dropdown",
                    options=[{"label": religion, "value": religion} for religion in religions],
                    multi=True,
                    placeholder="select religions",
                    className="filter-dropdown"
                )
            ])
        )

    if time_period:
        start, end = 1855, 1926
        filter_rows.append(
            dbc.Row([
                dbc.Label("Time Period", html_for=f"{filter_id}-time-slider", className="filter-title"),
                dcc.RangeSlider(
                    id=f"{filter_id}-time-slider",
                    min=start,
                    max=end,
                    step=1,
                    value=[start, end],
                    marks={i: str(i) for i in range(start, end+1, 10)},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className="filter-slider"
                )
            ])
        )

    return dbc.Container(
        filter_rows,
        class_name="filter-container",
    )