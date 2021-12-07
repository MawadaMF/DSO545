import pandas as pd
import numpy as np

# plotly 
import plotly.express as px
import plotly.graph_objects as go


# dashboards
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from dash.exceptions import PreventUpdate
import base64
from PIL import Image


data = pd.read_csv('schedule.csv', index_col=0)


teams=data['opponent_name'].unique()
team_abbr = data['opponent_abbr'].unique()
seasons=data['season'].unique()







app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])


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

        dbc.Navbar(

            dbc.Container([

                dbc.Row([

                    dbc.Col(

                        html.Img(src=Image.open('nba_logo.png'), style={
                                        "height": "50px",
                                        "width": "auto",
                                    }), md='auto', width='auto'

                        ), 

                    dbc.Col(

                        html.H1(' NBA Schedule Dashboard', 
                            style={'color': 'white', 
                                    'fontSize': '40px',

                                    }), md=True

                        )


                    ], justify='start') 


                ], fluid=True,id= 'header', 
                    style={"margin-bottom": "0px", 'color':'blue'}), dark=True, color='#081c2c', sticky='top'

    ),


        dbc.Card([


            ## Top left box 

            dbc.CardBody([

                html.Div([html.H4('Select Team', style = {'fontSize':'18px', 'margin-bottom':'15px'})]), 

                html.Div([
                    dcc.Dropdown(
                        id='team_value',
                        options=sorted([{'label': teams[i], 'value': team_abbr[i]} for i in range(len(teams))], key = lambda x: x['label']),
                        value='ATL'
                                )
                        ], style={'width': '85%', 'vertical-align': 'top','display': 'inline-block', 'margin-bottom':'15px'}), 



                html.Div([html.H4('Select Season', style = {'fontSize':'18px', 'margin-bottom':'15px'})]), 
                

                html.Div([
                    dcc.Dropdown(
                        id='season_value',
                        options=[{'label': str(int(s)-1)+'-'+ str(int(s)), 'value': s} for s in seasons],
                        value=2022
                                )
                        ], style={'width': '85%', 'float': 'center', 'display': 'inline-block', 'margin-bottom':'15px'}),


                html.Div([html.H4('Select Date Range', style = {'fontSize':'18px', 'margin-bottom':'15px'})]), 


                html.Div([
                dcc.DatePickerRange(
                    id='datepicker',
                    month_format='YYYY MMM'
                        )
                    ], style={'width': '85%','float': 'center', 'display': 'inline-block', 'margin-bottom':'15px'}),

                ]),

            ],
            style={"width": "30%", 'padding': '5px 5px 5px 5px', 'vertical-align':'left', 'display':'inline-block', 'margin-bottom':'15px'}),

        ### Top right box

        dbc.Card([

            dbc.CardBody([
                html.Div([html.H4('Travel Path', style = {'fontSize':'18px'})]), 

                dcc.Graph(id='map', style={'margin-bottom':'-10px'}), 




                ])
            ],
            style={'width':'68%','height':'50vh', 'vertical-align': 'top', 'float': 'right', 'display':'inline-block', 'padding': '5px 5px 5px 5px', 'margin-bottom':'5px'}), 


        ### Bottom left box
        dbc.Card([
            dbc.CardBody([
                html.Div([html.H4('Charts', style = {'fontSize':'18px'})]), 


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
                
                # dot graph
                dbc.Tab([
                    dcc.Graph(id='Dot_plot') 
                    ], label = 'Average Distance'),

                # line graph
                dbc.Tab([
                    dcc.Graph(id='line_plot') 
                    ], label = 'Cumulative Distance'),
            ])

            



                ])
            ],
            style={'width':'49%', 'float': 'left', 'padding': '5px 5px 5px 5px'}), 

        ### Bottom right box
        dbc.Card([
            dbc.CardBody([

                html.Div([html.H4('Table', style = {'fontSize':'18px'})]),

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

                        } 
                    ],
                    style_table={'height': '560px', 'overflowY': 'auto'}

                    
                    )
                ])
            ],
            style={'width':'49%', 'float': 'right', 'padding': '5px 5px 5px 5px'}), 
    
    



]
)





@app.callback(
    Output('datepicker', 'start_date'),
    Output('datepicker', 'end_date'),
    Output('datepicker', 'min_date_allowed'),
    Output('datepicker', 'max_date_allowed'),
    Input('season_value', 'value')
    )

def update_date_range(season_value): 

    df = pd.read_csv('schedule.csv', index_col=0)
    df = df[df['season']==season_value]
    df = df[df['playoffs']==0]
    min_date = df['datetime'].min()
    max_date = df['datetime'].max()
    return min_date, max_date, min_date, max_date


################################################################################################################################
# Map 


@app.callback(
    Output('map', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date'))

def update_graph(team_value, season_value, start_date, end_date): 
    
    df=pd.read_csv('schedule.csv')
    df=df[df['team']==team_value]

    df=df[df['season']==season_value]
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

    df1=df
    # finding the locations of the team
    df1['previous_location']= np.NaN
    df1['previous_location']= df1.team_coords


    df1['current_location']=df1[['location','team_coords','opp_coords']].apply(lambda row: row['team_coords'] if row['location']=='Home' else row['opp_coords'],axis =1)
    #df1['previous_location'][1:]=df1['current_location'][:-1]

    df1.reset_index(drop=True, inplace=True)

    #print(df1['previous_location'][0])

    # get list of coordinates
    list_coord= list(df1['current_location'])

    # get lon and lat
    lat_list=[]
    long_list=[]
    for i in range(len(list_coord)):
        lat_list.append(list_coord[i][1:list_coord[i].index(',')])
        long_list.append(list_coord[i][(list_coord[i].index(',')+2):-1])

    df1['lat']=lat_list[0:]
    df1['lon']=long_list[0:]
    df1['lat']=pd.to_numeric(df1["lat"], downcast="float")
    df1['lon']=pd.to_numeric(df1["lon"], downcast="float")
    df1['location_team']=[df1['opponent_abbr'][i] if x=='Away' else df1['team'][i] for i,x in enumerate(df1['location'])]
    #df1.head()

    #plotting 

    fig = px.line_mapbox(df1, lat="lat", lon="lon", zoom=3, hover_name="location_team",height=250)
    fig.update_layout(
            mapbox_style="open-street-map", 
            mapbox_zoom=3.5, 
            mapbox_center_lat = 38,
            mapbox_center_lon = -94, 
            margin={"r":0,"t":0,"l":0,"b":0}


            )

    fig.add_trace(go.Scattermapbox(
        lat=[df1['team_lat'][0]],
        lon=[df1['team_long'][0]],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        hoverinfo='none'
        ) 
        )
    
    return fig







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
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

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
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

    data = pd.DataFrame(df.groupby('team')['back_to_back'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='back_to_back', y='count', color = 'color',
                hover_data={'color':False, 'back_to_back': False, 'count':False, 'team':True},
                title =team_value + ' Back-to-Back Games', 
                labels = {'count': 'Number of Teams', 'back_to_back': 'Number of B2B Games'},
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
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]


    df['home'] = [1 if i == 'Home' else 0 for i in df['location']] 

    data = pd.DataFrame(df.groupby('team')['home'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='home', y='count', color = 'color',
                hover_data={'color':False, 'home': False, 'count':False, 'team':True},
                title =team_value + ' Home Games', 
                labels = {'count': 'Number of Teams', 'home': 'Number of Home Games'},
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
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]


    df['away'] = [1 if i == 'Away' else 0 for i in df['location']] 

    data = pd.DataFrame(df.groupby('team')['away'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='away', y='count', color = 'color',
                hover_data={'color':False, 'away': False, 'count':False, 'team':True},
                title =team_value + ' Away Games', 
                labels = {'count': 'Number of Teams', 'away': 'Number of Away Games'},
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
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

    data = pd.DataFrame(df.groupby('team')['3_in_4'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='3_in_4', y='count', color = 'color',
                hover_data={'color':False, '3_in_4': False, 'count':False, 'team':True},
                title =team_value + ' 3 in 4 Games', 
                labels = {'count': 'Number of Teams', '3_in_4': 'Number of 3-in-4 Games'},
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
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

    data = pd.DataFrame(df.groupby('team')['4_in_5'].sum())

    data['count'] = 1 
    data.reset_index(level=0, inplace=True)
    data['color'] = ['chosen_team' if i == team_value else 'others' for i in data['team']]
    data.sort_values(by='color', ascending = False, inplace=True)


    fig = px.bar(data, x='4_in_5', y='count', color = 'color',
                hover_data={'color':False, '4_in_5': False, 'count':False, 'team':True},
                title =team_value + ' 4 in 5 Games', 
                labels = {'count': 'Number of Teams', '4_in_5': 'Number of 4-in-5 Games'},
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


################################################################################################################################
# Dot Plot
 
@app.callback(
    Output('Dot_plot', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date'))
def update_graph(team_value, season_value,start_date,end_date):
    #df_newdata = data_loc[['team','distance_traveled','team']]
    #df_year = df[df['Year'] == year_value]
    #filter by the season
    #groupby the team
    df = pd.read_csv('schedule.csv',index_col = False)
    df= df[df['season']==season_value]
    df = df[df['playoffs']==0] 
    df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
    df_dot = df.groupby('team').mean().sort_values('distance_traveled',ascending=False)
    df_dot.reset_index(inplace=True)
    team = team_value
    df_dot['color'] = ['red' if i==team else 'blue' for i in df_dot['team']]
    #mycolors = ['red' if i==team else 'blue' for i in df_dot['team']]
    
    fig = px.scatter(df_dot,x= 'team',y='distance_traveled',color= 'color')
    fig.update_traces(
        marker_size=16,
        selector=dict(mode='markers')
    )
    
    fig.update_layout(title_text =
                   f"Average Distance Traveled Per Trip: {team_value}",
                    title_font_size = 18)
    color = ['red' if t==team else 'blue' for t in df_dot['team']]
    distances = df_dot['distance_traveled']
    #for dist,col in zip(distances,color):
        #for i,v in enumerate(df_dot['distance_traveled']):
    for i,v in enumerate(df_dot['distance_traveled']):
        if v == df_dot.loc[df_dot['team']==team_value,'distance_traveled'].values[0]:
            fig.add_shape(type='line',
                              x0 = i, y0 = 0,
                              y1 = v,
                              x1 = i,
                              line=dict(color= 'red', width = 3))
        else:
            fig.add_shape(type='line',
                              x0 = i, y0 = 0,
                              y1 = v,
                              x1 = i,
                              line=dict(color= 'blue', width = 3))
    fig.update_xaxes(categoryorder='total descending')
    return fig

################################################################################################################################
# line Plot
 
@app.callback(
    Output('line_plot', 'figure'),
    Input('team_value', 'value'),
    Input('season_value', 'value'),
    Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date'))

def update_graph(team_value, season_value, start_date, end_date):
    
    fig = go.Figure()
    
    df = pd.read_csv('schedule_cd.csv',index_col=0)
    df = df[df['season']==season_value]
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df[(df.datetime >= start_date) & (df.datetime <= end_date)]
    
    #for average
    gb = df.groupby('week')
    a=gb.agg({'datetime' : np.min,
            'cd' : np.mean})
    a.sort_values(by='datetime', key=pd.to_datetime, inplace=True)

    #for team
    d=df[df['team']==team_value].sort_values(by='datetime', key=pd.to_datetime)

    fig.add_trace(
        go.Scatter(x = a['datetime'], 
                y = a['cd'],
                mode = 'lines',
                line={'color': 'gray'},
                name='League Average',
                )
    )

    fig.add_trace(
        go.Scatter(x = d['datetime'], 
                y = d['cd'],
                mode = 'lines',
                line={'color': 'green'},
                name=team_value,
                )
    )

    fig.update_layout(title_text =
                   f"Cumulative Distance Traveled: {team_value}",
                    title_font_size = 18)
    
    return fig


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)

































