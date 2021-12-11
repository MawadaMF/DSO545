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
from dash.exceptions import PreventUpdate


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv('schedule.csv', index_col=0)


teams=data['opponent_name'].unique()
team_abbr = data['opponent_abbr'].unique()
seasons=data['season'].unique()


################################################################################################################################
##### APP LAYOUT #####

app.layout = html.Div([
    
    # top left drop menu for teams
    html.Div([
            dcc.Dropdown(
                id='team_value',
                options=sorted([{'label': teams[i], 'value': team_abbr[i]} for i in range(len(teams))], key = lambda x: x['label']),
                value='ATL'
            )
    ], style={'width': '30%', 'display': 'inline-block'}), 
   
    
    # top middle drop menu for seasons
    html.Div([
            dcc.Dropdown(
                id='season_value',
                options=[{'label': str(int(s)-1)+'-'+ str(int(s)), 'value': s} for s in seasons],
                value=2021
            )
    ], style={'width': '30%', 'float': 'center', 'display': 'inline-block'}),


    # top right date range picker 
    html.Div([
    		dcc.DatePickerRange(
    			id='datepicker',
    			month_format='YYYY MMM'
    		)
    ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='b2b_graph')
])



################################################################################################################################
################################################################################################################################
# Dynamically update the date range depending on the season 

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

################################################################################################################################
# Graph for Back-to-Back Games 

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
	data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
	data.sort_values(by='color', ascending = False, inplace=True)


	fig = px.bar(data, x='back_to_back', y='count', color = 'color',
                hover_data={'color':False, 'back_to_back': False, 'count':False, 'team':True},
                title =team_value + ' Back-to-Back Games', 
                labels = {'count': 'Count', 'back_to_back': 'Number of B2B Games'},
                color_discrete_map = {
                						'chosen_team': '#5880c4',
                						'others': '#dedede'
                }
                )

	games = data['back_to_back'].unique()
	tick_vals = list(range(min(games), max(games)+1))
	fig.update_xaxes(tickvals = tick_vals)
	fig.update_layout({'plot_bgcolor':'white'})

	fig.update_layout(showlegend=False)

	return fig

if __name__ == '__main__':
    app.run_server(debug=True)

















