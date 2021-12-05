
# data manipulation
import pandas as pd

# plotly 
import plotly.express as px
import plotly.graph_objects as go
# dashboards
import dash 
from jupyter_dash import JupyterDash #for running the dashboard in jupyter notebook
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc #for dashboard themes

import numpy as np

# read data
data= pd.read_csv('schedule.csv', index_col=0)
# adding long and lat staring points
data['start_long']= [data['team_long'][i] if x=='Home' else data['team_long'][i] for i,x in enumerate(data['location'])]
data['start_lat']= [data['team_lat'][i] if x=='Home' else data['team_lat'][i] for i,x in enumerate(data['location'])]
data['end_long']= [data['team_long'][i] if x=='Home' else data['opponent_long'][i] for i,x in enumerate(data['location'])]
data['end_lat']= [data['team_lat'][i] if x=='Home' else data['opponent_lat'][i] for i,x in enumerate(data['location'])]

# copy Madi's drop down
app = JupyterDash(__name__,external_stylesheets = [dbc.themes.BOOTSTRAP])

# read the data
data = pd.read_csv('schedule.csv')

# list of all unique teams
teams=data['opponent_name'].unique()

#list of all unique quarters
data['quarter']=pd.PeriodIndex(data.datetime, freq='Q')
q= data['quarter'].unique()


app.layout = html.Div([
    
    # top left drop menu for teams
    html.Div([
            dcc.Dropdown(
                id='team_value',
                options=[{'label': i, 'value': i} for i in teams],
                value='Teams'
            )
    ], style={'width': '48%', 'display': 'inline-block'}), 
    
    # top right drop menu for teams
    html.Div([
            dcc.Dropdown(
                id='quarter_value',
                options=[{'label': i.strftime('%YQ%q'), 'value': i.strftime('%YQ%q')} for i in q],
                value='Quarter'
            )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
# adding map
    dcc.Graph(id='map')
])
@app.callback(
    Output('map', 'figure'),
    Input('team_value', 'value'),
    Input('quarter_value', 'value'))
def update_graph(team_value, quarter_value):
    df=data.loc[(data.quarter==quarter_value) & (data.team==team_value), ('start_long', 'start_lat','end_long', 'end_lat','team_long','team_lat')]
    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df['team_long'].unique(),
        lat = df['team_lat'].unique(),
        hoverinfo = 'text',
        text = df['team'],
        mode = 'markers',
        marker = dict(
            size = 2,
            color = 'rgb(255, 0, 0)',
            line = dict(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))

    lons = []
    lats = []
    import numpy as np
    lons = np.empty(3 * len(data))
    lons[::3] = df['start_long']
    lons[1::3] = df['end_long']
    lons[2::3] = None
    lats = np.empty(3 * len(data))
    lats[::3] = df['start_lat']
    lats[1::3] = df['end_lat']
    lats[2::3] = None

    fig.add_trace(
        go.Scattergeo(
            locationmode = 'USA-states',
            lon = lons,
            lat = lats,
            mode = 'lines',
            line = dict(width = 1,color = 'blue'),
            opacity = 0.5
        )
    )
    fig.update_layout(
    title_text = f'{team_value} travels for {quarter_value}',
    showlegend = False,
    geo = go.layout.Geo(
        scope = 'north america',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),
    height=700,
)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

