"""
https://shiny.rstudio.com/gallery/kmeans-example.html
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
