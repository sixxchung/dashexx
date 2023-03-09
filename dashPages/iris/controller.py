from dash import Input, Output, Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from model import iris, cluster_data
from view import layout


app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = layout


# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option v"""
    return [{"label": col, "value": col, "disabled": col == v} for col in iris.columns]


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


# @app.callback(
#     Output("cluster-graph", "figure"),
#     [
#         Input("x-variable", "value"),
#         Input("y-variable", "value"),
#     ],
# )
# def make_graph(x, y, n_clusters):

#     return p


@app.callback(
    Output("cluster-graph", "figure"),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("cluster-count", "value"),
    ],
)
def make_graph(x, y, n_clusters):
    # minimal input validation, make sure there's at least one cluster
    dd_graph, centers = cluster_data(iris, x, y, n_clusters)

    data = [
        go.Scatter(
            x=dd_graph.loc[dd_graph.cluster == c, x],
            y=dd_graph.loc[dd_graph.cluster == c, y],
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
    layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}
    p = go.Figure(data=data, layout=layout)
    return p


if __name__ == "__main__":
    app.run_server(
        debug=True, port=8050
    )
