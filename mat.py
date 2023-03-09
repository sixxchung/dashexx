from dash import Input, Output, Dash, dcc, html
import dash_bootstrap_components as dbc
import dash
import matplotlib.pyplot as plt
import numpy as np
import plotnine as p9
from plotnine.data import mpg

# Define the Dash app
app = Dash(__name__)

ggplot_obj = (
    p9.ggplot(mpg) +
    p9.aes(x='class', fill='class') +
    p9.geom_bar() +
    p9.theme_minimal() +
    p9.ggtitle("Number of Cars by Class")
)

fig = ggplot_obj.draw()

app.layout = html.Div(children=[
    html.H1(children='Number of Cars by Class'),

    dcc.Graph(
        id='car-class',
        figure={
            'data': [],
            'layout': {
                'title': 'Number of Cars by Class'
            }
        }
    )
])


@app.callback(
    dash.dependencies.Output('car-class', 'figure'),
    [],
    state=[dash.dependencies.State('car-class', 'figure')]
)
def update_figure(_, previous_figure):
    if not previous_figure:
        return {
            'data': [],
            'layout': {
                'title': 'Number of Cars by Class'
            }
        }

    ggplot_obj = p9.ggplot(mpg) + p9.aes(x='class', fill='class') + p9.geom_bar() + \
        p9.theme_minimal() + p9.ggtitle("Number of Cars by Class")
    fig = ggplot_obj.draw()
    previous_figure['data'] = fig['data']
    return previous_figure


if __name__ == '__main__':
    app.run_server(debug=True)
