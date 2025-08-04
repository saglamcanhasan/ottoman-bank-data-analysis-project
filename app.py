# app.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from widgets.navbar import Navbar

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)