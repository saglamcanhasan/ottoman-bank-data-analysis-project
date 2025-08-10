import dash_bootstrap_components as dbc
from dash import html, get_asset_url, Input, Output, State, callback

# dropdown widget
def Dropdown(label: str, items: dict):
    return dbc.DropdownMenu(
        label=label,
        children=[dbc.DropdownMenuItem(item_label, href=item_url) for item_label, item_url in items.items()],
        className="navbar-dropdown-menu"
    )

# navbar widget
def Navbar():
    return dbc.Navbar([
        # top layer
        dbc.Container([
            dbc.Row([
                # logo container
                dbc.Col(
                    html.A([
                        html.Img(src=get_asset_url("navbar-logo.png"), className="navbar-logo"),
                        dbc.NavbarBrand("Ottoman Bank Dataset", className="navbar-title"),
                        ],
                        href="/"
                    ),
                    width=10,
                    className="navbar-logo-container"
                ),
                dbc.Col(
                    dbc.NavbarToggler(
                        id="navbar-toggler",
                        className="navbar-toggler"
                    ),
                    width=2,
                    className="navbar-toggler-container"
                )],
                className="navbar-top-layer"
            ),

            # horizontal seperator
            dbc.Row(
                dbc.Col(
                    html.Div(className="navbar-horizontal-separator"),
                    className="container"
                ),
                className="navbar-row"
            ),

            # bottom layer
            dbc.Row(
                dbc.Col(
                    dbc.Collapse(
                        dbc.Nav([
                            # history group
                            dbc.NavItem(
                                Dropdown(
                                    label="Institutional Dashboard",
                                    items={
                                        "Historical Overview": "/historical-overview",
                                        "Geographic Footprint": "/geographic-footprint",
                                        "Workforce Demographics": "/workforce-demographics",
                                        }
                                    )
                                ),

                            # vertical seperator
                            html.Div(className="navbar-vertical-separator"),

                            # agency group
                            dbc.NavItem(
                                Dropdown(
                                    label="Agency Dashboard",
                                    items={
                                        "Agency Performance": "/agency-performance",
                                        "Employee Transfers": "/employee-transfers",
                                        }
                                    )
                                ),

                            # vertical seperator
                            html.Div(className="navbar-vertical-separator"),

                            # employee group
                            dbc.NavItem(
                                Dropdown(
                                    label="Personnel Dashboard",
                                    items={
                                        "Employee Profiles": "/employee-profiles",
                                        "Co-worker Network": "/coworker-network",
                                        }
                                    )
                                ),
                            # vertical seperator
                            html.Div(className="navbar-vertical-separator"),

                            # information group
                            dbc.NavItem(dbc.NavLink("About Us", href="/about-us")),
                            dbc.NavItem(dbc.NavLink("About Dataset", href="/about-dataset"))],
                            className="navbar-nav"
                        ),
                        is_open=False,
                        id="navbar-collapse",
                        className="navbar-bottom-layer"
                    ),
                    className="navbar-column"
                ),
                className="navbar-row"
            )],
            fluid=True,
            className="navbar-container"
        )],
        expand=False,
        className="navbar-header"
    )

# Callback for toggler
@callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
    prevent_initial_call=True
)
def toggle_navbar(click_count, is_open):
    return not is_open