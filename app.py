from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv(r'telemetry_data_4_12_2024_2.csv', low_memory=False)
gears = sorted(df['currentGear'].unique())

app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#474545'}, children=[
    html.H1(children='Telemetry Dashboard', style={'textAlign': 'center', 'margin': 'auto', 'width': '50%', 'color':'#00000', 'font-size': '64px'}),
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
            dcc.Graph(id='gear_graph', style={'width': '85%', 'display': 'inline-block'}),
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
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['Speed (MPH)'], mode='lines', line=dict(color='#07eb31')))


    fig.update_layout(
        title='Speed (MPH)',
        title_font=dict(color='white'),
        plot_bgcolor='#272a2e',
        paper_bgcolor='#050505',
        yaxis=dict(range=[0, max_speed + y_range_max], gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.4)'),
        margin=dict(l=10, r=10, t=45, b=15),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.2)'))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(tickfont=dict(color='white'))

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
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['Throttle %'], mode='lines', line=dict(color='#07eb31')))
    fig.update_layout(title='Throttle %',
        title_font=dict(color='white'),
        plot_bgcolor='#272a2e',
        paper_bgcolor='#050505',
        yaxis=dict(range=[0, 105], gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.4)'),
        margin=dict(l=10, r=10, t=45, b=15),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.2)'))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(tickfont=dict(color='white'))
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
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['Brake %'], mode='lines', line=dict(color='#07eb31')))
    fig.update_layout(title='Brake %',
        title_font=dict(color='white'),
        plot_bgcolor='#272a2e',
        paper_bgcolor='#050505',
        yaxis=dict(range=[0, 105], gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.4)'),
        margin=dict(l=10, r=10, t=45, b=15),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.2)'))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(tickfont=dict(color='white'))
    return fig

@app.callback(
    Output('gear_graph', 'figure'),
    Input('dropdown-selection', 'value'),
)

def update_gear_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].iloc[0]  # Set to the first lap completed value

    dff = df[df['LapCompleted'] == value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['currentGear'], mode='lines', line=dict(color='#07eb31')))
    fig.update_layout(title='CurrentGear',
        title_font=dict(color='white'),
        plot_bgcolor='#272a2e',
        paper_bgcolor='#050505',
        yaxis=dict(tickvals=gears, gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.4)'),
        margin=dict(l=10, r=10, t=45, b=15),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.2)'))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(tickfont=dict(color='white'))
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
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['LatAccel (m/s)'], mode='lines', line=dict(color='#07eb31')))
    fig.update_layout(title='Lat Accel (g)',
        title_font=dict(color='white'),
        plot_bgcolor='#272a2e',
        paper_bgcolor='#050505',
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.4)'),
        margin=dict(l=10, r=10, t=45, b=15),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.2)'))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(tickfont=dict(color='white'))
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
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['LongAccel (m/s)'], mode='lines', line=dict(color='#07eb31')))
    fig.update_layout(title='Long Accel (g)',
        title_font=dict(color='white'),
        plot_bgcolor='#272a2e',
        paper_bgcolor='#050505',
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.4)'),
        margin=dict(l=10, r=10, t=45, b=15),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.2)'))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(tickfont=dict(color='white'))



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
    fig.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['SteeringWheelAngle (deg)'], mode='lines', line=dict(color='#07eb31')))
    fig.update_layout(title='Steering Angle (deg)',
        title_font=dict(color='white'),
        plot_bgcolor='#272a2e',
        paper_bgcolor='#050505',
        yaxis=dict(range=[-190, 190], gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.4)'),
        margin=dict(l=10, r=10, t=45, b=15),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)', zerolinecolor='rgba(255, 255, 255, 0.2)'))
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(tickfont=dict(color='white'))
    return fig


if __name__ == '__main__':
    app.run(debug=True)