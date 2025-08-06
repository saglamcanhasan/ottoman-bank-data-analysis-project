import dash_bootstrap_components as dbc
from dash import html, dcc, get_asset_url
import dash_cytoscape as cyto
from utils.filter_parameters import agencies, grouped_functions, religions, ids, start, end

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

def section(title: str, description: str, figures: dict=dict(), is_cytoscape=False):
    figure_rows = list()
    for figure_id in figures:
        # extract figure info
        figure_dict = figures[figure_id]

        figure = figure_dict["figure"]
        filter = figure_dict.get("filter", None)

        # generate a row
        cols = list()

        if is_cytoscape: # Render Cytoscape with passed elements
            graph_component = cyto.Cytoscape(
                id=figure_id,
                style={'width': '100%', 'height': '100%'},
                layout={'name': 'cose', 'animate': False},
                elements=figure,  # assuming figure is cyto elements list here
                stylesheet=[
                    {"selector": "node", "style": {"label": "data(id)", "width": "data(size)", "height": "data(size)","background-color": "data(color)"}},
                    {"selector": "edge", "style": {"curve-style": "bezier", "line-color": "#B08D57"}},                   
                ],
            )
        else: # Usual Plotly Graph inside Loading
            graph_component = dcc.Loading(
                dcc.Graph(figure=figure, id=figure_id, className="graph"),
                type="dot",
                color="#00487A",
                id="loader"
            )
            
        cols.append(dbc.Col(graph_component, width=8, className="figure-container", id="deneme"))
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


def filter(filter_id: str, agency: bool, grouped_function: bool, religion: bool, id: bool, time_period: bool):
    filter_rows = []

    if agency:
        filtered_options = agencies.tolist()
        final_options = [{"label": "Unknown", "value": "Unknown"}] + [{"label": "", "value": "", "disabled": True}] + [{"label": agency, "value": agency} for agency in filtered_options]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Agency", html_for=f"{filter_id}-agency-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-agency-dropdown",
                    options=final_options,
                    multi=True,
                    placeholder="select agencies",
                    className="filter-dropdown"
                )
            ])
        )

    if grouped_function:
        filtered_options = grouped_functions.tolist()
        final_options = [{"label": "Unknown", "value": "Unknown"}] + [{"label": "", "value": "", "disabled": True}] + [{"label": grouped_function, "value": grouped_function} for grouped_function in filtered_options]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Grouped Function", html_for=f"{filter_id}-grouped_function-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-grouped_function-dropdown",
                    options=final_options,
                    multi=True,
                    placeholder="select grouped functions",
                    className="filter-dropdown"
                )
            ])
        )

    if religion:
        filtered_options = religions.tolist()
        filtered_options.remove("Other")
        final_options = [{"label": "Other", "value": "Other"}, {"label": "Unknown", "value": "Unknown"}] + [{"label": "", "value": "", "disabled": True}] + [{"label": religion, "value": religion} for religion in filtered_options]
        filter_rows.append(
            dbc.Row([
                dbc.Label("Religion", html_for=f"{filter_id}-religion-dropdown", className="filter-title"),
                dcc.Dropdown(
                    id=f"{filter_id}-religion-dropdown",
                    options=final_options,
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
                    placeholder="select an employee ID",
                    className="filter-dropdown"
                )
            ])
        )

    if time_period:
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
        fluid=True
    )