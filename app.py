from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv(r'C:\Users\jedin\projects\helloworld\telemetry_data_3_29_2024_1.csv')


app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': 'darkgrey'}, children=[
    html.H1(children='Telemetry Dashboard', style={'textAlign': 'center', 'margin': 'auto', 'width': '50%', 'font-size': '64px'}),
    html.Div([
        dcc.Dropdown(
            options=[{'label': lap, 'value': lap} for lap in df['LapCompleted'].unique()],
            value=df['LapBestLap'].iloc[-1],
            id='dropdown-selection',
            clearable=False,
            searchable=False,
            style={'width': '100px', 'font-size': '24px'}
        ),
        
        html.Div([
            dcc.Graph(id='speed_graph', style={'width': '85%', 'display': 'inline-block'}),
            dcc.Graph(id='accel_graph', style={'width': '85%', 'display': 'inline-block'}),
            dcc.Graph(id='brake_graph', style={'width': '85%', 'display': 'inline-block'}),
            dcc.Graph(id='lataccel_graph', style={'width': '85%', 'display': 'inline-block'}),
            dcc.Graph(id='longaccel_graph', style={'width': '85%', 'display': 'inline-block'}),
            dcc.Graph(id='steering_graph', style={'width': '85%', 'display': 'inline-block'})
        ], style={'textAlign': 'center', 'margin': 'auto', 'width': '100%', 'overflow': 'hidden'})
    ])
])



@app.callback(
    Output('speed_graph', 'figure'),
    Input('dropdown-selection', 'value'),
)
def update_speed_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].iloc[0]  # Set to the first lap completed value

    max_speed = df['Speed (MPH)'].max()  # Find the maximum value of the 'Speed (MPH)' column
    y_range_max = max_speed * 0.20 

    dff = df[df['LapCompleted'] == value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['Speed (MPH)'], mode='lines'))


    fig.update_layout(
        title='Speed (MPH)',
        yaxis=dict(range=[0, max_speed + y_range_max]),
        xaxis=dict(showticklabels=False),
        margin=dict(l=10, r=10, t=45, b=15)  # Adjust the margins (left, right, top, bottom)

    )

    return fig

@app.callback(
    Output('accel_graph', 'figure'),
    Input('dropdown-selection', 'value'),
)

def update_accel_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].iloc[0]  # Set to the first lap completed value



    dff = df[df['LapCompleted'] == value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['Throttle %'], mode='lines'))
    fig.update_layout(title='Throttle %', yaxis=dict(range=[0, 105]))
    fig.update_xaxes(showticklabels=False)
    return fig

@app.callback(
    Output('brake_graph', 'figure'),
    Input('dropdown-selection', 'value'),
)

def update_brake_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].iloc[0]  # Set to the first lap completed value

    dff = df[df['LapCompleted'] == value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['Brake %'], mode='lines'))
    fig.update_layout(title='Brake %', yaxis=dict(range=[0, 105]))
    fig.update_xaxes(showticklabels=False)
    return fig



@app.callback(
    Output('lataccel_graph', 'figure'),
    Input('dropdown-selection', 'value'),
)

def update_lataccel_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].iloc[0]  # Set to the first lap completed value

    dff = df[df['LapCompleted'] == value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['LatAccel (m/s)'], mode='lines'))
    fig.update_layout(title='Lat Accel')
    fig.update_xaxes(showticklabels=False)
    return fig

@app.callback(
    Output('longaccel_graph', 'figure'),
    Input('dropdown-selection', 'value'),
)

def update_longaccel_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].iloc[0]  # Set to the first lap completed value

    dff = df[df['LapCompleted'] == value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['LongAccel (m/s)'], mode='lines'))
    fig.update_layout(title='Long Accel')
    fig.update_xaxes(showticklabels=False)
    return fig


@app.callback(
    Output('steering_graph', 'figure'),
    Input('dropdown-selection', 'value'),
)

def update_steering_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].iloc[0]  # Set to the first lap completed value

    dff = df[df['LapCompleted'] == value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['SteeringWheelAngle (deg)'], mode='lines'))
    fig.update_layout(title='Steering Angle', yaxis=dict(range=[-180, 180]))
    fig.update_xaxes(showticklabels=False)
    return fig

if __name__ == '__main__':
    app.run(debug=True)