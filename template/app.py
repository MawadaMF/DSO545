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


app = dash.Dash(__name__)

# read the data
data = pd.read_csv('schedule.csv')

# list of all unique teams
teams=data['opponent_name'].unique()

#list of all unique quarters
q= pd.PeriodIndex(data.datetime, freq='Q').unique()

app.layout = html.Div([
    
    # top left drop menu for teams
    html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in teams],
#                 value='Fertility rate, total (births per woman)'
            )
    ], style={'width': '48%', 'display': 'inline-block'}), 
    
    # top right drop menu for teams
    html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i.strftime('%YQ%q'), 'value': i.strftime('%YQ%q')} for i in q],
#                 value='Life expectancy at birth, total (years)'
            )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

#     dcc.Graph(id='indicator-graphic'),
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
#     Output('indicator-graphic', 'figure'),
#     Input('xaxis-column', 'value'),
#     Input('yaxis-column', 'value'),
#     Input('xaxis-type', 'value'),
#     Input('yaxis-type', 'value'),
#     Input('year--slider', 'value'))
# def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value):

#     df_year = df[df['Year'] == year_value]

#     fig = px.scatter(x=df_year[df_year['Indicator Name'] == xaxis_column_name]['Value'],
#                      y=df_year[df_year['Indicator Name'] == yaxis_column_name]['Value'],
#                      hover_name=df_year[df_year['Indicator Name'] == yaxis_column_name]['Country Name'])

#     fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

#     fig.update_xaxes(title=xaxis_column_name,
#                      type='linear' if xaxis_type == 'Linear' else 'log')

#     fig.update_yaxes(title=yaxis_column_name,
#                      type='linear' if yaxis_type == 'Linear' else 'log')

#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# #############################################################################

