from dash import Dash, dcc, html, Input, Output, callback, ctx
import pandas as pd

import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carregando os DataFrames
df_diversificador = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='Diversificador')
df_clientes = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='DadosClientes')
df_assessores = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='DadosAssessor')
df_produtos = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='Produtos')

# Filtrando o DataFrame df_diversificador para 'Renda Fixa'
df_renda_fixa = df_diversificador[df_diversificador['Produto'] == 'Renda Fixa']

df_renda_fixa = pd.merge(df_renda_fixa, df_clientes, how='left', left_on='Cliente', right_on='Código Cliente')
df_renda_fixa = pd.merge(df_renda_fixa, df_assessores, how='left', left_on='Assessor', right_on='Código assessor')
df_renda_fixa = pd.merge(df_renda_fixa, df_produtos, how='left', on='Produto')

df_renda_fixa.dropna(inplace=True)

total_de_ativos = int(df_renda_fixa['Quantidade'].sum())
renda_por_ativo = df_renda_fixa['NET'].sum()/len(df_renda_fixa) # Rever essa conta, porque não tenho certeza dessa conta
receita_total = df_renda_fixa['NET'].sum()
numero_de_clientes = df_renda_fixa['Cliente'].nunique()

button_style = {
    'backgroundColor': 'white',      # Fundo branco
    'color': '#001F3F',               # Letra azul escuro
    'border': 'none',                 # Sem borda
    'padding': '10px 20px',           # Preenchimento interno
    'text-align': 'center',           # Alinhamento de texto
    'text-decoration': 'none',        # Sem decoração de texto
    'display': 'inline-block',        # Exibição em linha
    'font-size': '20px',              # Tamanho da fonte
    'margin': '4px 2px',              # Margem
    'cursor': 'pointer',              # Cursor do mouse
    'border-radius': '10px',          # Borda curva
}

kpi_card_style = {
    'padding': '20px',
    'margin': '10px',
    'border-radius': '10px',
    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'background-color': 'white',
    'color': '#2ecc71',  # Cor do texto padrão
}

div_style = {
    'backgroundColor': '#001F3F',   # Cor de fundo azul escuro
    'padding': '20px',               # Preenchimento interno
}

# Layout renda fixa
layout_renda_fixa = [
     html.Div(children=[
        html.Div(children=[
            html.H1(children='Exponencial Investimentos LTDA', style={'textAlign': 'left', 'color': 'white', 'margin-left': '10px'}),
            html.H2(children='Renda Fixa', style={'textAlign': 'left', 'color': 'white', 'margin-left': '10px'}),
        ], className='col-md-6'),

        html.Div(children=[
            html.Button('COE', id='btn_coe', n_clicks=0, style=button_style, className='button'),
            html.Button('Carteira Automatizada', id='btn_carteira_automatizada', n_clicks=0, style=button_style, className='button'),
            html.Button('Renda Fixa', id='btn_renda_fixa', n_clicks=0, style=button_style, className='button'),
            html.Button('Oferta Pública', id='btn_oferta_publica', n_clicks=0, style=button_style, className='button'),
        ], style={'display': 'flex','textAlign': 'center', 'align-items': 'center', 'justify-content': 'space-evenly'}, className='col-md-6'),  
    ], style={'margin-bottom': '40px'}, className='header row'),

    html.Div(id='filtros', children=[
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in ['Todos os assessores'] + df_renda_fixa['Nome assessor'].astype(str).unique().tolist()],
            value='Todos os assessores',
            id='assessores',
            className='dropdown',
            style={'min-width': '220px'}
        ),
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in ['Todos os clientes'] + df_renda_fixa['NomeCliente'].astype(str).unique().tolist()],
            value='Todos os clientes',
            id='clientes',
            className='dropdown',
            style={'min-width': '220px'}
        ),
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in ['Todos os sub produtos'] + df_renda_fixa['Sub Produto'].astype(str).unique().tolist()],
            value='Todos os sub produtos',
            id='sub_produtos',
            className='dropdown',
            style={'min-width': '220px'}
        ),
    ], className='filter-container', style={'display': 'flex','align-items': 'center', 'justify-content': 'space-evenly', 'margin-bottom': '40px'}),

    html.Div(children=[
        html.Div(children=[
            html.H4(children='Total de Ativos', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='total_de_ativos', children=[total_de_ativos], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Receita por Ativo', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='renda_por_ativo', children=[renda_por_ativo], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Receita Total', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='receita_total', children=[receita_total], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Número de Clientes', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='numero_de_clientes', children=[numero_de_clientes], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-evenly', 'margin-bottom': '40px'},
       className='kpi-container'),
]

app.layout= html.Div(id="container_tela", children=layout_renda_fixa, style=div_style)

@callback(
    Output("total_de_ativos", "children"),
    Output("renda_por_ativo", "children"),
    Output("receita_total", "children"),
    Output("numero_de_clientes", "children"),
    Input("assessores", "value"),
    Input("clientes", "value"),
    Input("sub_produtos", "value"),
    )
def callback_kpis(nome_assessor, nome_cliente, nome_sub_produto):
    df_auxiliar = df_renda_fixa.copy()

    if nome_assessor != "Todos os assessores":
        df_auxiliar = df_auxiliar.loc[df_auxiliar['Nome assessor']==nome_assessor,:]
    if nome_cliente != "Todos os clientes":
        df_auxiliar = df_auxiliar.loc[df_auxiliar['NomeCliente']==nome_cliente,:]
    if nome_sub_produto != "Todos os sub produtos":
        df_auxiliar = df_auxiliar.loc[df_auxiliar['Sub Produto']==nome_sub_produto,:]

    total_de_ativos = int(df_auxiliar['Quantidade'].sum())
    renda_por_ativo = df_auxiliar['NET'].sum()/len(df_auxiliar) # Rever essa conta, porque não tenho certeza dessa conta
    receita_total = df_auxiliar['NET'].sum()
    numero_de_clientes = df_auxiliar['Cliente'].nunique()

    return total_de_ativos, renda_por_ativo, receita_total, numero_de_clientes

@callback(
    Output('container_tela', 'children'),
    Input('btn_coe', 'n_clicks'),
    Input('btn_carteira_automatizada', 'n_clicks'),
    Input('btn_renda_fixa', 'n_clicks'),
    Input('btn_oferta_publica', 'n_clicks'),
)
def menu_produtos(btn_coe, btn_carteira_automatizada, btn_renda_fixa, btn_oferta_publica):
    if 'btn_coe' == ctx.triggered_id:
        return layout_renda_fixa
    elif 'btn_carteira_automatizada' == ctx.triggered_id:
        return layout_renda_fixa
    elif 'btn_renda_fixa' == ctx.triggered_id:
        return layout_renda_fixa
    elif 'btn_oferta_publica' == ctx.triggered_id:
        return layout_renda_fixa
    return layout_renda_fixa

# Execute o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)