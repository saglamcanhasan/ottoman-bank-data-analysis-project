# app.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from widgets.navbar import Navbar

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    Navbar(),
    dcc.Loading(
        dash.page_container,
        type="dot",
        color="#00487A",
        fullscreen=True
    )],
    className="page-container"
)

if __name__ == '__main__':
    app.run(debug=True)