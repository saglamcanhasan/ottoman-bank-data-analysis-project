from dash import html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from services.filter_parameters import countries, functions, religions, ids, start, end

def introduction(title: str, description: str, right_widget=list()):
    return dbc.Container([
        dbc.Row([
            dbc.Col(content(title, description), lg=12, xl=6),
            
            dbc.Col(right_widget, lg=12, xl=6, className="introduction-right-widget-container")],
            className="container"
        )],
        className="introduction-container"
    )

def content(title: str, description: str):
    return dbc.Row([
        dbc.Col([
            html.Header(
                title,
                className="introduction-title"
            ),

            dcc.Markdown(
                description,
                className="content-body"
            )],
            className="container"
        )],
        className="container"
    )

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

def section(title: str, description: str, graphs: dict=dict()):
    figure_rows = list()
    for figure_id in graphs:
        # extract figure info
        graph_dict = graphs[figure_id]
        filter = graph_dict.get("filter", None)

        # check figure type
        graph_component = dcc.Loading(
            html.Div(
                id=figure_id,
                className="figure-frame"
            ),
            type="dot",
            color="#00487A",
            id="loader"
        )

        # generate a row
        cols = list()
        if filter is not None:
            cols.append(dbc.Col(filter, lg=12, xl=3))
            cols.append(dbc.Col(vertical_separator(), lg=12, xl=1))
        cols.append(dbc.Col(graph_component, lg=12, xl=8, className="figure-container"))

        row = dbc.Row(cols, justify="center", className="figure-row")
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
                ),
                className="container"
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


def filter(filter_id: str, agency: bool, function: bool, religion: bool, id: bool, time_period: bool):
    filter_rows = []

    if agency:
        filtered_options = countries
        final_options = [{"label": "Unknown", "value": "Unknown"}] + [{"label": "", "value": "", "disabled": True}] + [{"label": agency, "value": agency} for agency in filtered_options if agency != "Unknown"]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Agency", html_for=f"{filter_id}-agency-country-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-agency-country-dropdown",
                    options=final_options,
                    value=[],
                    multi=True,
                    placeholder="select countries",
                    className="filter-dropdown"
                ),
                dcc.Dropdown(
                    id=f"{filter_id}-agency-city-dropdown",
                    options=[],
                    value=[],
                    multi=True,
                    disabled=True,
                    placeholder="select cities",
                    className="filter-dropdown"
                ),
                dcc.Dropdown(
                    id=f"{filter_id}-agency-district-dropdown",
                    options=[],
                    value=[],
                    multi=True,
                    disabled=True,
                    placeholder="select districts",
                    className="filter-dropdown"
                )
            ])
        )

    if function:
        filtered_options = functions
        final_options = [{"label": "Unknown", "value": "Unknown"}] + [{"label": "", "value": "", "disabled": True}] + [{"label": function, "value": function} for function in filtered_options if agency != "Unknown"]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Function", html_for=f"{filter_id}-function-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-function-dropdown",
                    options=final_options,
                    value=[],
                    multi=True,
                    placeholder="select functions",
                    className="filter-dropdown"
                )
            ])
        )

    if religion:
        filtered_options = religions
        final_options = [{"label": "Unknown", "value": "Unknown"}, {"label": "Other", "value": "Other"}] + [{"label": "", "value": "", "disabled": True}] + [{"label": religion, "value": religion} for religion in filtered_options if agency != "Unknown" and agency != "Other"]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Religion", html_for=f"{filter_id}-religion-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-religion-dropdown",
                    options=final_options,
                    value=[],
                    multi=True,
                    placeholder="select religions",
                    className="filter-dropdown"
                )
            ])
        )

    if id:
        filter_rows.append(
            dbc.Row([
                dbc.Label("Employee ID", html_for=f"{filter_id}-id-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-id-dropdown",
                    options=[{"label": id, "value": id} for id in ids],
                    value=[],
                    multi=True,
                    placeholder="select employee IDs",
                    className="filter-dropdown"
                )
            ])
        )

    if time_period:
        filter_rows.append(
            dbc.Row([
                dbc.Label("Time Period", html_for=f"{filter_id}-time-period-slider", className="filter-title"),
                dcc.RangeSlider(
                    id=f"{filter_id}-time-period-slider",
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
        fluid=True
    )