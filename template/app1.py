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

data = pd.read_csv('schedule.csv', index_col=0)


teams=data['opponent_name'].unique()
team_abbr = data['opponent_abbr'].unique()
seasons=data['season'].unique()







app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
)



app.layout = html.Div(
    [
        html.Div(
            [
                html.H2('NBA Schdule Visualization Tool', style={'color': 'lightgrey', 'fontSize': '18px'})
        ]), 

        dbc.Card([


            ## Top left box 

            dbc.CardBody([

                html.Div([html.H4('Select Team', style = {'fontSize':'18px'})]), 

                html.Div([
                    dcc.Dropdown(
                        id='team_value',
                        options=sorted([{'label': teams[i], 'value': team_abbr[i]} for i in range(len(teams))], key = lambda x: x['label']),
                        value='ATL'
                                )
                        ], style={'width': '85%', 'display': 'inline-block'}), 



                html.Div([html.H4('Select Season', style = {'fontSize':'18px'})]), 
                

                html.Div([
                    dcc.Dropdown(
                        id='season_value',
                        options=[{'label': str(int(s)-1)+'-'+ str(int(s)), 'value': s} for s in seasons],
                        value=2022
                                )
                        ], style={'width': '85%', 'float': 'center', 'display': 'inline-block'}),


                html.Div([html.H4('Select Date Range', style = {'fontSize':'18px'})]), 


                html.Div([
                dcc.DatePickerRange(
                    id='datepicker',
                    month_format='YYYY MMM'
                        )
                    ], style={'width': '85%', 'float': 'center', 'display': 'inline-block'}),

                ]),

            ],
            style={"width": "30%", 'padding': '5px 5px 5px 5px'}),

        ### Top right box

        dbc.Card([

            dbc.CardBody([
                html.Div([html.H4('INSERT MAP HERE', style = {'fontSize':'18px'})]), 




                ])
            ],
            style={'width':'68%', 'float': 'right'}), 


        ### Bottom left box
        dbc.Card([
            dbc.CardBody([
                html.Div([html.H4('INSERT GRAPHS HERE', style = {'fontSize':'18px'})]), 


            dbc.Tabs([

            
                # Home Tab
                dbc.Tab([
                    dcc.Graph(id='home_graph'),
                    ], label = 'Home'), 

                # Away Tab
                dbc.Tab([
                    dcc.Graph(id='away_graph'),
                    ], label = 'Away'), 

                # B2B Tab
                dbc.Tab([
                    dcc.Graph(id='b2b_graph'),
                    ], label = 'B2B'), 

                # 3-in-4 Tab
                dbc.Tab([
                    dcc.Graph(id='3in4_graph'),
                    ], label = '3 In 4'), 

                # 4-in-5 Tab
                dbc.Tab([
                    dcc.Graph(id='4in5_graph'),
                    ], label = '4 In 5'), 

            ])

            



                ])
            ],
            style={'width':'49%', 'float': 'left'}), 

        ### Bottom right box
        dbc.Card([
            dbc.CardBody([

                dash_table.DataTable(

                    id='table', 
                    style_as_list_view=True,
                    style_cell = {
                        'font_family': 'helvetica',
                        'font_size': '18px',
                        'text_align': 'center',
                        'color': 'black'
                    },
                    sort_action='native',
                    style_header={
                        'fontWeight': 'bold',
                        'backgroundColor': '#5880c4',
                        'color': 'white'
                    }, 
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Result} eq "Win"',
                                'column_id': 'Result'
                            }, 
                            'color':'green'

                        }, 
                        {
                            'if': {
                                'filter_query': '{Result} eq "Loss"',
                                'column_id': 'Result'
                            }, 
                            'color':'red'

                        }, 

                    ]
                    )
                ])
            ],
            style={'width':'49%', 'float': 'right'}), 




]
)






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
# Table 


@app.callback(
    [Output('table', 'data'),
    Output('table', 'columns')],
    [Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date')]
    )

def updateTable(team_value, season_value, start_date, end_date): 
    df = pd.read_csv('schedule.csv', index_col=0)
    df = df[df['season']==season_value]
    df = df[df['playoffs']==0]
    df = df[df['team']==team_value]
    df = df[(df['datetime'] > start_date) & (df['datetime'] < end_date)]

    data = df[['datetime', 'team', 'opponent_abbr', 'location', 'result','streak', 'back_to_back', '3_in_4', '4_in_5']]
    data.set_index('datetime', inplace=True)
    data.reset_index(inplace=True)
    data.rename(columns = {'datetime':'Date','team':'Team','opponent_abbr':'Opponent',
                        'location':'Location', 'result':'Result', 'streak':'Streak', 
                        'back_to_back':'B2B', '3_in_4':'3-In-4', '4_in_5':'4-In-5'}, inplace=True)

    columns = []
    for i,j in enumerate(data.columns): 
        item = {'id': j, 'name':j}
        columns.append(item)

    df1 = data.to_dict("rows")

    return [df1, columns]







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

################################################################################################################################
# Graph for Home Games 


@app.callback(
    Output('home_graph', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date'))

def update_graph(team_value, season_value, start_date, end_date): 


    df = pd.read_csv('schedule.csv', index_col=0)
    df = df[df['season']==season_value]
    df = df[df['playoffs']==0] 
    df = df[(df['datetime'] > start_date) & (df['datetime'] < end_date)]


    df['home'] = [1 if i == 'Home' else 0 for i in df['location']] 

    data = pd.DataFrame(df.groupby('team')['home'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='home', y='count', color = 'color',
                hover_data={'color':False, 'home': False, 'count':False, 'team':True},
                title =team_value + ' Home Games', 
                labels = {'count': 'Count', 'home': 'Number of Home Games'},
                color_discrete_map = {
                                        'chosen_team': '#5880c4',
                                        'others': '#dedede'
                }
                )

    games = data['home'].unique()
    tick_vals = list(range(min(games), max(games)+1))
    fig.update_xaxes(tickvals = tick_vals)
    fig.update_layout({'plot_bgcolor':'white'})

    fig.update_layout(showlegend=False)

    return fig


################################################################################################################################
# Graph for Away Games 


@app.callback(
    Output('away_graph', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date'))

def update_graph(team_value, season_value, start_date, end_date): 


    df = pd.read_csv('schedule.csv', index_col=0)
    df = df[df['season']==season_value]
    df = df[df['playoffs']==0] 
    df = df[(df['datetime'] > start_date) & (df['datetime'] < end_date)]


    df['away'] = [1 if i == 'Away' else 0 for i in df['location']] 

    data = pd.DataFrame(df.groupby('team')['away'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='away', y='count', color = 'color',
                hover_data={'color':False, 'away': False, 'count':False, 'team':True},
                title =team_value + ' Away Games', 
                labels = {'count': 'Count', 'away': 'Number of Away Games'},
                color_discrete_map = {
                                        'chosen_team': '#5880c4',
                                        'others': '#dedede'
                }
                )

    games = data['away'].unique()
    tick_vals = list(range(min(games), max(games)+1))
    fig.update_xaxes(tickvals = tick_vals)
    fig.update_layout({'plot_bgcolor':'white'})

    fig.update_layout(showlegend=False)

    return fig

################################################################################################################################
# Graph for 3-in-4 Games 

@app.callback(
    Output('3in4_graph', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date'))

def update_graph(team_value, season_value, start_date, end_date): 


    df = pd.read_csv('schedule.csv', index_col=0)
    df = df[df['season']==season_value]
    df = df[df['playoffs']==0] 
    df = df[(df['datetime'] > start_date) & (df['datetime'] < end_date)]

    data = pd.DataFrame(df.groupby('team')['3_in_4'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='3_in_4', y='count', color = 'color',
                hover_data={'color':False, '3_in_4': False, 'count':False, 'team':True},
                title =team_value + ' 3 in 4 Games', 
                labels = {'count': 'Count', '3_in_4': 'Number of 3-in-4 Games'},
                color_discrete_map = {
                                        'chosen_team': '#5880c4',
                                        'others': '#dedede'
                }
                )

    games = data['3_in_4'].unique()
    tick_vals = list(range(min(games), max(games)+1))
    fig.update_xaxes(tickvals = tick_vals)
    fig.update_layout({'plot_bgcolor':'white'})

    fig.update_layout(showlegend=False)

    return fig

################################################################################################################################
# Graph for 4-in-5 Games 

@app.callback(
    Output('4in5_graph', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date'))

def update_graph(team_value, season_value, start_date, end_date): 


    df = pd.read_csv('schedule.csv', index_col=0)
    df = df[df['season']==season_value]
    df = df[df['playoffs']==0] 
    df = df[(df['datetime'] > start_date) & (df['datetime'] < end_date)]

    data = pd.DataFrame(df.groupby('team')['4_in_5'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='4_in_5', y='count', color = 'color',
                hover_data={'color':False, '4_in_5': False, 'count':False, 'team':True},
                title =team_value + ' 4 in 5 Games', 
                labels = {'count': 'Count', '4_in_5': 'Number of 4-in-5 Games'},
                color_discrete_map = {
                                        'chosen_team': '#5880c4',
                                        'others': '#dedede'
                }
                )

    games = data['4_in_5'].unique()
    tick_vals = list(range(min(games), max(games)+1))
    fig.update_xaxes(tickvals = tick_vals)
    fig.update_layout({'plot_bgcolor':'white'})

    fig.update_layout(showlegend=False)

    return fig









# run the app
if __name__ == '__main__':
    app.run_server(debug=True)

































