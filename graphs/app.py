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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv('schedule.csv', index_col=0)


teams=data['opponent_name'].unique()
team_abbr = data['opponent_abbr'].unique()
seasons=data['season'].unique()

app.layout = html.Div([
    
    # top left drop menu for teams
    html.Div([
            dcc.Dropdown(
                id='team_value',
                options=[{'label': teams[i], 'value': team_abbr[i]} for i in range(len(teams))],
                value='Teams'
            )
    ], style={'width': '30%', 'display': 'inline-block'}), 
   
    
    # top middle drop menu for seasons
    html.Div([
            dcc.Dropdown(
                id='season_value',
                options=[{'label': s, 'value': s} for s in seasons],
                value='Season'
            )
    ], style={'width': '30%', 'float': 'center', 'display': 'inline-block'}),


    # top left date range picker 
    html.Div([
    		dcc.DatePickerRange(
    			id='datepicker',
    			month_format='YYYY MMM'
    		)
    ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='b2b_graph')
])


@app.callback(
	Output('datepicker', 'start_date'),
	Output('datepicker', 'end_date'),
	Input('season_value', 'value')
	)

def update_date_range(season_value): 
	df = pd.read_csv('schedule.csv', index_col=0)
	df = df[df['season']==season_value]
	df = df[df['playoffs']==0]
	min_date = df['datetime'].min()
	max_date = df['datetime'].max()
	return min_date, max_date



@app.callback(
    Output('b2b_graph', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
	Input('datepicker', 'start_date'),
	Input('datepicker', 'end_date'))

def update_graph(team_value, season_value, start_date, end_date): 
	df = pd.read_csv('schedule.csv', index_col=0)
	df = df[df['season']==season_value]
	df = df[df['playoffs']==0] 
	df = df[(df['datetime'] > start_date) & (df['datetime'] < end_date)]

	data = pd.DataFrame(df.groupby('team')['back_to_back'].sum())

	data['count'] = 1 
	data.reset_index(level=0, inplace=True)
	data['color'] = ['blue' if i == team_value else 'grey' for i in data['team']]


	fig = px.bar(data, x='back_to_back', y='count', color = 'color',
                hover_data={'color':False, 'back_to_back': False, 'count':False, 'team':True},
                title =team_value + ' Back-to-Back Games', 
                labels = {'count': 'Number of Teams', 'back_to_back': 'Number of Games'}
                )

	games = data['back_to_back'].unique()
	tick_vals = list(range(min(games), max(games)+1))
	fig.update_xaxes(tickvals = tick_vals)


	fig.update_layout(showlegend=False)

	return fig

if __name__ == '__main__':
    app.run_server(debug=True)

















