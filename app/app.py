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


colors = {
    'background': '#17408B',
    'text': '#FFFFFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='NBA Schedule Visualization',
        style={
            'textAlign': 'center', 
            'color': colors['text']
        }
    ),

    html.Div()

])



















if __name__ == '__main__':
    app.run_server(debug=True)

























