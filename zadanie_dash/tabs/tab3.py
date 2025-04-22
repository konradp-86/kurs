from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

def render_tab(df):
    # Przygotowanie danych
    df['weekday'] = df['tran_date'].dt.day_name()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['weekday'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True)
    
    # Layout zakładki
    layout = html.Div([
        html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
        
        html.Div([
            html.Div([
                dcc.Graph(id='sales-by-weekday'),
                dcc.RadioItems(
                    id='weekday-metric',
                    options=[
                        {'label': 'Kwota sprzedaży', 'value': 'total_amt'},
                        {'label': 'Liczba transakcji', 'value': 'count'}
                    ],
                    value='total_amt',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                )
            ], style={'width': '50%'}),
            
            html.Div([
                dcc.Graph(id='customer-gender'),
                dcc.Dropdown(
                    id='store-type-dropdown',
                    options=[{'label': stype, 'value': stype} 
                            for stype in df['Store_type'].unique()],
                    value=df['Store_type'].unique()[0]
                )
            ], style={'width': '50%'})
        ], style={'display': 'flex'}),
        
        html.Div([
            dcc.Graph(id='age-distribution')
        ])
    ])
    
    return layout