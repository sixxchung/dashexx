"""
https://shiny.rstudio.com/gallery/kmeans-example.html
"""
from dash import Input, Output, Dash, dcc, html
import dash_bootstrap_components as dbc

from model import iris


vars = [{"label": col, "value": col} for col in iris.columns]
sidebarPanel = dbc.Card([
    html.Div([
        dbc.Label("X variable"),
        dcc.Dropdown(
            id="x-variable",
            options=vars,
            value=vars[0]['value'],
        ),
    ]),
    html.Div([
        dbc.Label("Y variable"),
        dcc.Dropdown(
            id="y-variable",
            options=vars,
            value=vars[1]['value'],
        ),
    ]),
    html.Div([
        dbc.Label("Cluster count"),
        dbc.Input(id="cluster-count", type="number", min=1, max=6, value=3),
    ]),
], body=True,)
graphs = dcc.Graph(id="cluster-graph")
layout = dbc.Container(
    [
        html.H1("Iris k-means clustering"), html.Hr(),
        dbc.Row([
            dbc.Col(sidebarPanel, md=4),
            dbc.Col(graphs, md=8),
        ], align="center",),
    ],
    fluid=True,
)
