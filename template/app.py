# data manipulation
import pandas as pd

# plotly 
import plotly.express as px

# dashboards
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date

import numpy as np

app = dash.Dash(__name__)

# read the data
data = pd.read_csv('schedule.csv')

# list of all unique teams
teams=data['opponent_name'].unique()

#list of all unique quarters
# data['quarter']=pd.PeriodIndex(data.datetime, freq='Q')
# q= data['quarter'].unique()

seasons=data['season'].unique()


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
#     html.Div([
#             dcc.Dropdown(
#                 id='quarter_value',
#                 options=[{'label': i.strftime('%YQ%q'), 'value': i.strftime('%YQ%q')} for i in q],
#                 value='Quarter'
#             )
#     ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    
    # top right drop menu for teams
    html.Div([
            dcc.Dropdown(
                id='season_value',
                options=[{'label': s, 'value': s} for s in seasons],
                value='Season'
            )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

#     dcc.Graph(id='cumdist-graphic',
#     dcc.Slider(
#         id='year--slider',
#         min=df['Year'].min(),
#         max=df['Year'].max(),
#         value=df['Year'].min(),
#         marks={str(year): str(year) for year in df['Year'].unique()},
#         step=None
#     )
])

# @app.callback(
#     Output('cumdist-graphic', 'figure'),
#     Input('team_value', 'value'),
#     Input('season_value', 'value'))

# def update_graph(team_value, season_value):
    
#         d=data[data['opponent_name']==team].sort_values(by='datetime').reset_index()
# #         if quarter_value !='Quarter':
# #             d=d[d['quarter']==quarter_value]
#         if season_value !='Season':
#             d=d[d['season']==season_value]
#         dt=d['distance_traveled']
#         cd=np.cumsum(dt)
    
#     fig = go.Figure()

#     for i,team in enumerate(teams):

#         d=data[data['opponent_name']==team].sort_values(by='datetime')
#         if quarter_value !='Quarter':
#             d=d[d['quarter']==quarter_value]
#         dt=d['distance_traveled']
#         cd=np.cumsum(dt)

# #         fig.add_trace(go.Scatter(x = d['datetime'], 
# #                          y = cd,
# #                          mode = 'lines',
# #                          name=team,
# #                              line = dict(color = colors[i])
# #                          ))

#         if team_value =='Teams' or team==team_value:
#             fig.add_trace(
#                 go.Scatter(x = d['datetime'], 
#                         y = cd,
#                         mode = 'lines',
#                         line={'color': 'green'},
#                         name=team,
#                         )
#             )
#             fig.add_trace(
#                 go.Scatter(x = d['datetime'], 
#                         y = cd.where(d['result'] == 'Loss'),
#                         mode = 'lines',
#                         line={'color': 'red'},
#                         name='',
#                         )
#             )
#         else:
#             fig.add_trace(
#                 go.Scatter(x = d['datetime'], 
#                         y = cd,
#                         mode = 'lines',
#                         line={'color': 'gray'},
#                         name=team,
#                         )
#             )

#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# #############################################################################

