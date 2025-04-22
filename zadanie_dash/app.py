import pandas as pd
import datetime as dt
import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from tabs import tab1, tab2, tab3 # type: ignore
import sys
sys.path.append(r'c:\Kodilla\zadanie dash\tabs')
import plotly.express as px
import plotly.graph_objects as go

class db:
    def __init__(self):
        self.transactions = self.transaction_init()
        self.cc = pd.read_csv(r'db\country_codes.csv', index_col=0)
        self.customers = pd.read_csv(r'db\customers.csv', index_col=0)
        self.prod_info = pd.read_csv(r'db\prod_cat_info.csv')
    
    @staticmethod
    def transaction_init():
        transactions = pd.DataFrame()
        src = r'db\transactions'
        for filename in os.listdir(src):
            transactions = transactions._append(pd.read_csv(os.path.join(src, filename), index_col=0))

        def convert_dates(x):
            return pd.to_datetime(x, dayfirst=True, errors='coerce')

        
        transactions['tran_date'] = transactions['tran_date'].apply(lambda x: convert_dates(x))
        return transactions

    def merge(self):
        df = self.transactions.join(
            self.prod_info.drop_duplicates(subset=['prod_cat_code'])
            .set_index('prod_cat_code')['prod_cat'],
            on='prod_cat_code', how='left'
        )

        df = df.join(
            self.prod_info.drop_duplicates(subset=['prod_sub_cat_code'])
            .set_index('prod_sub_cat_code')['prod_subcat'],
            on='prod_subcat_code', how='left'
        )

        df = df.join(
            self.customers.join(self.cc, on='country_code')
            .set_index('customer_Id'),
            on='cust_id', how='left'
        )

        self.merged = df

df = db()
df.merge()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)


app.layout = html.Div([
    html.Div([
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Sprzedaż globalna', value='tab-1'),
            dcc.Tab(label='Produkty', value='tab-2'),
            dcc.Tab(label='Kanały sprzedaży', value='tab-3')  # Nowa zakładka
        ]),
        html.Div(id='tabs-content')
    ], style={'width': '80%', 'margin': 'auto'})
])

def render_tab(df):
    # Grupowanie danych sprzedaży według kategorii produktów
    grouped = df[df['total_amt'] > 0].groupby('prod_cat')['total_amt'].sum()

    # Wykres kołowy: udział grup produktów w sprzedaży
    pie_fig = go.Figure(
        data=[go.Pie(labels=grouped.index, values=grouped.values)],
        layout=go.Layout(title='Udział grup produktów w sprzedaży')
    )

    # Układ zakładki
    layout = html.Div([
        html.H1('Produkty', style={'text-align': 'center'}),
        html.Div([
            dcc.Graph(id='pie-prod-cat', figure=pie_fig),
            dcc.Dropdown(
                id='prod_dropdown',
                options=[{'label': cat, 'value': cat} for cat in df['prod_cat'].unique()],
                value=df['prod_cat'].unique()[0],
                placeholder='Wybierz kategorię produktu'
            ),
            dcc.Graph(id='bar-prod-subcat')  # Dodano komponent z identyfikatorem 'bar-prod-subcat'
        ], style={'width': '80%', 'margin': 'auto'})
    ])

@app.callback(Output('tabs-content','children'),[Input('tabs','value')])
def render_content(tab):

    if tab == 'tab-1':
        return tab1.render_tab(df.merged)
    elif tab == 'tab-2':
        return tab2.render_tab(df.merged)
    elif tab == 'tab-3':
        return tab3.render_tab(df.merged)
## tab1 callbacks
@app.callback(Output('bar-sales','figure'),
    [Input('sales-range','start_date'),Input('sales-range','end_date')])

def tab1_bar_sales(start_date,end_date):

    truncated = df.merged[(df.merged['tran_date']>=start_date)&(df.merged['tran_date']<=end_date)]
    grouped = truncated[truncated['total_amt']>0].groupby([pd.Grouper(key='tran_date',freq='M'),'Store_type'])['total_amt'].sum().round(2).unstack()

    traces = []
    for col in grouped.columns:
        traces.append(go.Bar(x=grouped.index,y=grouped[col],name=col,hoverinfo='text',
        hovertext=[f'{y/1e3:.2f}k' for y in grouped[col].values]))

    data = traces
    fig = go.Figure(data=data,layout=go.Layout(title='Przychody',barmode='stack',legend=dict(x=0,y=-0.5)))

    return fig


@app.callback(Output('choropleth-sales','figure'),
            [Input('sales-range','start_date'),Input('sales-range','end_date')])
def tab1_choropleth_sales(start_date,end_date):

    truncated = df.merged[(df.merged['tran_date']>=start_date)&(df.merged['tran_date']<=end_date)]
    grouped = truncated[truncated['total_amt']>0].groupby('country')['total_amt'].sum().round(2)

    trace0 = go.Choropleth(colorscale='Viridis',reversescale=True,
                            locations=grouped.index,locationmode='country names',
                            z = grouped.values, colorbar=dict(title='Sales'))
    data = [trace0]
    fig = go.Figure(data=data,layout=go.Layout(title='Mapa',geo=dict(showframe=False,projection={'type':'natural earth'})))

    return fig

## tab2 callbacks
@app.callback(Output('barh-prod-subcat','figure'),
            [Input('prod_dropdown','value')])
def tab2_barh_prod_subcat(chosen_cat):

    grouped = df.merged[(df.merged['total_amt']>0)&(df.merged['prod_cat']==chosen_cat)].pivot_table(index='prod_subcat',columns='Gender',values='total_amt',aggfunc='sum').assign(_sum=lambda x: x['F']+x['M']).sort_values(by='_sum').round(2)

    traces = []
    for col in ['F','M']:
        traces.append(go.Bar(x=grouped[col],y=grouped.index,orientation='h',name=col))

    data = traces
    fig = go.Figure(data=data,layout=go.Layout(barmode='stack',margin={'t':20,}))
    return fig

# Callback dla wykresu sprzedaży według dni tygodnia
@app.callback(
    Output('sales-by-weekday', 'figure'),
    [Input('weekday-metric', 'value')]
)
def update_weekday_chart(metric):
    if metric == 'total_amt':
        grouped = df.merged[df.merged['total_amt'] > 0].groupby(['weekday', 'Store_type'])['total_amt'].sum().unstack()
        title = 'Sprzedaż według dnia tygodnia'
    else:
        grouped = df.merged[df.merged['total_amt'] > 0].groupby(['weekday', 'Store_type']).size().unstack()
        title = 'Liczba transakcji według dnia tygodnia'
    
    fig = go.Figure()
    for store_type in grouped.columns:
        fig.add_trace(go.Bar(
            x=grouped.index,
            y=grouped[store_type],
            name=store_type
        ))
    
    fig.update_layout(
        title=title,
        barmode='group',
        xaxis_title='Dzień tygodnia',
        yaxis_title='Wartość' if metric == 'total_amt' else 'Liczba transakcji'
    )
    
    return fig

# Callback dla wykresu płci klientów
@app.callback(
    Output('customer-gender', 'figure'),
    [Input('store-type-dropdown', 'value')]
)
def update_gender_chart(store_type):
    filtered = df.merged[df.merged['Store_type'] == store_type]
    gender_counts = filtered['Gender'].value_counts()
    
    fig = go.Figure(go.Pie(
        labels=gender_counts.index,
        values=gender_counts.values,
        hole=.3
    ))
    
    fig.update_layout(
        title=f'Podział płci klientów ({store_type})'
    )
    
    return fig

@app.callback(
    Output('age-distribution', 'figure'),
    [Input('store-type-dropdown', 'value')]
)
def update_age_chart(store_type):
    filtered = df.merged[df.merged['Store_type'] == store_type].copy()
    filtered['DOB'] = pd.to_datetime(filtered['DOB'], dayfirst=True)
    filtered['age'] = (pd.to_datetime('today') - filtered['DOB']).dt.days // 365

    fig = px.box(
        filtered,
        y='age',
        title=f'Rozkład wieku klientów ({store_type})',
        labels={'age': 'Wiek'}
    )

    fig.update_layout(
        yaxis_title='Wiek',
        margin=dict(t=40)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
