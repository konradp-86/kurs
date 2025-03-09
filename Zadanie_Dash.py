import pandas as pd
import datetime as dt
import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Klasa do zarządzania danymi
class DB:
    def __init__(self):
        self.transactions = self.transaction_init()
        self.cc = pd.read_csv(r'db/country_codes.csv', index_col=0)
        self.customers = pd.read_csv(r'db/customers.csv', index_col=0)
        self.prod_info = pd.read_csv(r'db/prod_cat_info.csv')
        self.merged = self.merge()
        print("[INFO] Połączony DataFrame załadowany:")
        print(self.merged.head())

    @staticmethod
    def transaction_init():
        transactions = pd.DataFrame()
        src = r'db/transactions'
        if not os.path.exists(src):
            raise FileNotFoundError(f"Directory '{src}' does not exist.")
        if not os.listdir(src):
            raise ValueError(f"No transaction files found in directory '{src}'.")

        for filename in os.listdir(src):
            filepath = os.path.join(src, filename)
            if filename.endswith('.csv'):
                transactions = pd.concat([transactions, pd.read_csv(filepath, index_col=0)], ignore_index=True)

        def convert_dates(x):
            try:
                return dt.datetime.strptime(x, '%d-%m-%Y')
            except:
                try:
                    return dt.datetime.strptime(x, '%d/%m/%Y')
                except:
                    return None

        transactions['tran_date'] = transactions['tran_date'].apply(lambda x: convert_dates(x))
        if transactions['tran_date'].isnull().any():
            raise ValueError("Some transaction dates could not be converted.")

        print("[INFO] Transakcje załadowane:")
        print(transactions.head())
        return transactions

    def merge(self):
        df = self.transactions.join(
            self.prod_info.drop_duplicates(subset=['prod_cat_code']).set_index('prod_cat_code')['prod_cat'],
            on='prod_cat_code', how='left'
        )
        df = df.join(
            self.prod_info.drop_duplicates(subset=['prod_sub_cat_code']).set_index('prod_sub_cat_code')['prod_subcat'],
            on='prod_subcat_code', how='left'
        )
        df = df.join(
            self.customers.join(self.cc, on='country_code').set_index('customer_Id'),
            on='cust_id', how='left'
        )

        if df.empty:
            raise ValueError("Merged dataset is empty. Check input files or join conditions.")
        return df


# Inicjalizacja bazy danych
db_instance = DB()
df = db_instance.merged

# Inicjalizacja aplikacji Dash
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Layout aplikacji
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Sprzedaż globalna', value='tab-1'),
        dcc.Tab(label='Produkty', value='tab-2')
    ]),
    html.Div(id='tabs-content')
])

# Funkcja renderująca zakładkę 'Sprzedaż globalna'
def render_tab_sales(df):
    layout = html.Div([
        html.H1('Sprzedaż globalna', style={'text-align': 'center'}),
        html.Div([
            dcc.DatePickerRange(
                id='sales-range',
                start_date=df['tran_date'].min(),
                end_date=df['tran_date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '100%', 'text-align': 'center'}),
        html.Div([
            html.Div([dcc.Graph(id='bar-sales')], style={'width': '50%'}),
            html.Div([dcc.Graph(id='choropleth-sales')], style={'width': '50%'})
        ], style={'display': 'flex'})
    ])
    return layout

# Funkcja renderująca zakładkę 'Produkty'
def render_tab_products(df):
    grouped = df[df['total_amt'] > 0].groupby('prod_cat')['total_amt'].sum()
    fig = go.Figure(
        data=[go.Pie(labels=grouped.index, values=grouped.values)],
        layout=go.Layout(title='Udział grup produktów w sprzedaży')
    )

    layout = html.Div([
        html.H1('Produkty', style={'text-align': 'center'}),
        html.Div([
            html.Div([dcc.Graph(id='pie-prod-cat', figure=fig)], style={'width': '50%'}),
            html.Div([
                dcc.Dropdown(
                    id='prod_dropdown',
                    options=[{'label': prod_cat, 'value': prod_cat} for prod_cat in df['prod_cat'].unique()],
                    value=df['prod_cat'].unique()[0]
                ),
                dcc.Graph(id='barh-prod-subcat')
            ], style={'width': '50%'})
        ], style={'display': 'flex'})
    ])
    return layout

# Callback do renderowania zawartości aktywnej zakładki
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return render_tab_sales(df)
    elif tab == 'tab-2':
        return render_tab_products(df)
    return html.Div("Zakładka w budowie.")

# Callbacky dla wykresów:
@app.callback(Output('bar-sales', 'figure'),
            [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
def tab1_bar_sales(start_date, end_date):
    truncated = df[(df['tran_date'] >= start_date) & (df['tran_date'] <= end_date)]
    print("\nZakres dat:", start_date, end_date)
    print("\nDane po filtracji (Sprzedaż):")
    print(truncated.head())

    grouped = truncated[truncated['total_amt'] > 0].groupby(
        [pd.Grouper(key='tran_date', freq='M'), 'Store_type']
    )['total_amt'].sum().round(2).unstack()

    print("\nDane pogrupowane dla wykresu:")
    print(grouped)

    traces = []
    for col in grouped.columns:
        traces.append(go.Bar(
            x=grouped.index, y=grouped[col], name=col
        ))

    return go.Figure(data=traces)

@app.callback(Output('choropleth-sales', 'figure'),
            [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
def tab1_choropleth_sales(start_date, end_date):
    truncated = df[(df['tran_date'] >= start_date) & (df['tran_date'] <= end_date)]
    grouped = truncated.groupby('country')['total_amt'].sum()

    print("\nDane dla mapy (Sprzedaż globalna):")
    print(grouped.head())

    return go.Figure(data=[go.Choropleth(
        locations=grouped.index, z=grouped.values, locationmode='country names'
    )])

# Uruchomienie serwera
if __name__ == '__main__':
    app.run_server(debug=True)
