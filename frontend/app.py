import os
import dash
from dash import html
from dotenv import load_dotenv
from widgets.navbar import Navbar
import dash_bootstrap_components as dbc

load_dotenv()
port = int(os.getenv("PORT_FRONTEND"))

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    Navbar(),
    dash.page_container],
    className="page-container"
)

if __name__ == '__main__':
    app.run(debug=True, port=port)