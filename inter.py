
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
import pandas as pd
from sklearn import datasets
from sklearn.cluster import KMeans

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

iris_raw = datasets.load_iris()
iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])
iris['target'] = iris_raw.target

# Create a hidden div to store intermediate data
app.layout = dbc.Container([
    html.Div([
        dcc.Store(id='intermediate-data'),
        # Other layout components go here
    ]),
    html.Div([
        dbc.Label("X variable"),
        dcc.Dropdown(
            id="my-dropdown",
        ),
        dcc.Graph(id="my-graph")
    ]),
])


# Define the callback to update the intermediate data


@app.callback(Output('intermediate-data', 'data'),
              [Input('my-dropdown', 'value')])
def update_intermediate_data(value):
    # Read in a new dataframe based on the dropdown value
    df = iris
    # Do some processing on the dataframe
    df = df.groupby('target').sum()
    # Convert the processed dataframe to JSON and return it
    return df.to_json()

# Define a second callback to update a Plotly graph based on the intermediate data


@app.callback(Output('my-graph', 'figure'),
              [Input('intermediate-data', 'data')])
def update_graph(jsonified_data):
    # Convert the JSON data back to a pandas dataframe
    df = pd.read_json(jsonified_data)
    # Create a Plotly figure based on the dataframe
    fig = px.bar(df, x='target', y='value')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
