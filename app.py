from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv(r'C:\Users\jedin\projects\helloworld\telemetry_data_3_28_2024_2.csv')
df_f = df[df['LapCompleted'] > 0]

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Telemetry Dashboard', style={'textAlign':'center'}),
    dcc.Dropdown(df.LapCompleted.unique(), '1', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])



@app.callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
)
def update_graph(value):
    if value is None:  # Handle the initial callback triggering
        value = df['LapCompleted'].unique()[1]

    dff = df[df.LapCompleted==value]
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(x=dff['SessionTime'], y=dff['Speed (MPH)'], mode='lines'))


    fig1.update_xaxes(showticklabels=False)
    # fig1 = px.line(dff, x='SessionTime', y='Speed (MPH)')
    # fig1.update_xaxes(showticklabels=False)

    return fig1



if __name__ == '__main__':
    app.run(debug=True)