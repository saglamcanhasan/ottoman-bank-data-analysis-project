import dash_bootstrap_components as dbc
from dash import html, get_asset_url

# dropdown widget
def Dropdown(label: str, items: dict):
    return dbc.DropdownMenu(
        label=label,
        children=[dbc.DropdownMenuItem(item_label, href=item_url) for item_label, item_url in items.items()],
        className="navbar-dropdown-menu"
    )

# navbar widget
def Navbar():
    return html.Header([
        # top layer
        html.Div(
            dbc.Container(
                dbc.Row([
                    # logo container
                    dbc.Col(
                        html.A([
                            html.Img(src=get_asset_url("navbar-logo.png"), className="navbar-logo"),
                            dbc.NavbarBrand("Ottoman Bank Dataset", className="navbar-title"),
                            ],
                            href="/"
                        ),
                        className="container"
                    )],
                    className="container"
                )
            ),
            className="navbar-top-layer"
        ),

        # horizontal seperator
        html.Div(className="navbar-horizontal-separator"),

        # bottom layer
        dbc.Navbar(
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
            className="navbar-bottom-layer"
        ),
    ], className="navbar-header")