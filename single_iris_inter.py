"""
https://shiny.rstudio.com/gallery/kmeans-example.html
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import pandas as pd
from sklearn import datasets
from sklearn.cluster import KMeans

import plotly.graph_objs as go

iris_raw = datasets.load_iris()
iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

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
    html.Div([
        dcc.Store(id='intermediate-data'),
    ]),
], body=True,)
graphs = dcc.Graph(id="cluster-graph")
app.layout = dbc.Container(
    [
        html.H1("Iris k-means clustering"), html.Hr(),
        dbc.Row([
            dbc.Col(sidebarPanel, md=4),
            dbc.Col(graphs, md=8),
        ], align="center",),
    ],
    fluid=True,
)


@app.callback(
    Output('intermediate-data', 'data'),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
    ],
)
def make_data(x, y):
    df = iris.loc[:, [x, y]]
    print(df)
    return df.to_json()


@app.callback(
    Output("cluster-graph", "figure"),
    [
        # Input("x-variable", "value"),
        # Input("y-variable", "value"),
        Input('intermediate-data', 'data'),
        Input("cluster-count", "value"),
    ],
)
def make_graph(jsonified_data, n_clusters):
    # minimal input validation, make sure there's at least one cluster
    df = pd.read_json(jsonified_data)

    km = KMeans(n_clusters=max(n_clusters, 1))
    #df = iris.loc[:, [x, y]]
    km.fit(df.values)
    df["cluster"] = km.labels_

    centers = km.cluster_centers_

    data = [
        go.Scatter(
            x=df.loc[df.cluster == c, df.columns[0]],  # x],
            y=df.loc[df.cluster == c, df.columns[1]],  # y],
            mode="markers",
            marker={"size": 8},
            name="Cluster {}".format(c),
        )
        for c in range(n_clusters)
    ]

    data.append(
        go.Scatter(
            x=centers[:, 0],
            y=centers[:, 1],
            mode="markers",
            marker={"color": "#000", "size": 12, "symbol": "diamond"},
            name="Cluster centers",
        )
    )

    layout = {
        "xaxis": {"title": df.columns[0]},
        "yaxis": {"title": df.columns[0]}}

    return go.Figure(data=data, layout=layout)


# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option v"""
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in iris.columns
    ]


# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(
    Output("x-variable", "options"),
    [Input("y-variable", "value")])(
    filter_options
)
app.callback(
    Output("y-variable", "options"),
    [Input("x-variable", "value")])(
    filter_options
)


if __name__ == "__main__":
    app.run_server(
        debug=True, port=8050,  # host='localhost'
    )
