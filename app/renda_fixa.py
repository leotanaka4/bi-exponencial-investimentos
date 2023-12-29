from dash import Dash, dcc, html, Input, Output, callback, ctx, dash_table
import dash_bootstrap_components as dbc

import plotly.express as px

import pandas as pd

def formatar_numero(numero):
    if abs(numero) < 1000:
        return f'{numero:.3g}'
    elif abs(numero) < 1_000_000:
        return f'{numero / 1000:.3g} mil'
    elif abs(numero) < 1_000_000_000:
        return f'{numero / 1_000_000:.3g} milhões'
    else:
        return f'{numero / 1_000_000_000:.3g} bilhões'

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Exponencial Investimentos LTDA'

# Carregando os DataFrames
df_coe = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='Relatório de COE')
df_diversificador = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='Diversificador')
df_clientes = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='DadosClientes')
df_assessores = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='DadosAssessor')
df_produtos = pd.read_excel('../data/Bases de Dados.xlsx', sheet_name='Produtos')

# Fazendo as alterações do DataFrame de COE
df_coe = pd.merge(df_coe, df_clientes, how='left', left_on='Cliente', right_on='Código Cliente')
df_coe = df_coe.sort_values(by='Data')
df_coe.dropna(inplace=True)

# Fazendo as métricas de COE
total_de_ativos_coe = int(df_coe['Cliente'].count())
renda_por_ativo_coe = df_coe['Valor Aplicado'].sum()/len(df_coe)
receita_total_coe = df_coe['Valor Aplicado'].sum()
comissao_coe = df_coe['Valor Aplicado'].sum()*0.025

tabela_coe = df_coe[['Data', 'Nome do Produto (30)', 'Tipo', 'Status', 'Valor Aplicado']].copy()
tabela_coe['Data'] = df_coe['Data'].dt.strftime('%d/%m/%Y')
tabela_coe['Valor Aplicado'] = df_coe['Valor Aplicado'].round(2).map('R$ {:.2f}'.format).str.replace('.', ',', regex=False)

# Filtrando o DataFrame df_diversificador para 'Renda Fixa'
df_renda_fixa = df_diversificador[df_diversificador['Produto'] == 'Renda Fixa']

df_renda_fixa = pd.merge(df_renda_fixa, df_clientes, how='left', left_on='Cliente', right_on='Código Cliente')
df_renda_fixa = pd.merge(df_renda_fixa, df_assessores, how='left', left_on='Assessor', right_on='Código assessor')
df_renda_fixa = pd.merge(df_renda_fixa, df_produtos, how='left', on='Produto')

df_renda_fixa = df_renda_fixa.sort_values(by='Data de Vencimento')

df_renda_fixa.dropna(inplace=True)

# Fazendo as métricas de renda fixa
total_de_ativos_renda_fixa = int(df_renda_fixa['Quantidade'].sum())
renda_por_ativo_renda_fixa = df_renda_fixa['NET'].sum()/len(df_renda_fixa) # Rever essa conta, porque não tenho certeza dessa conta
receita_total_renda_fixa = df_renda_fixa['NET'].sum()
numero_de_clientes_renda_fixa = df_renda_fixa['Cliente'].nunique()

# Criar DataFrame com formatação desejada
tabela_renda_fixa = df_renda_fixa[['Data de Vencimento', 'Ativo', 'Emissor', 'Quantidade', 'NET']].copy()
tabela_renda_fixa['Data de Vencimento'] = df_renda_fixa['Data de Vencimento'].dt.strftime('%d/%m/%Y')
tabela_renda_fixa['NET'] = df_renda_fixa['NET'].round(2).map('R$ {:.2f}'.format).str.replace('.', ',', regex=False)

# Calcular o somatório de vencimentos por dia
df_somatorio = df_renda_fixa.groupby('Data de Vencimento')['Quantidade'].sum().reset_index()

# Criar gráfico de vencimentos ao longo do tempo
fig_vencimentos = px.line(df_somatorio, x='Data de Vencimento', y='Quantidade', labels={'Quantidade': 'Quantidade de Vencimentos'}, template='plotly')

# Adicionar título ao gráfico
fig_vencimentos.update_layout(
    title='Quantidade de Vencimentos por Dia',
    font=dict(color='#000000'),  # Cor do texto
)

# Personalizar a cor da linha no gráfico de vencimentos
fig_vencimentos.update_traces(line_color='#001F3F')

# Criar gráfico boxplot de Quantidade
fig_quantidades = px.box(df_renda_fixa, x='Quantidade', template='plotly')

# Adicionar título ao gráfico
fig_quantidades.update_layout(
    title='Quantidade de Ativos',
    font=dict(color='#000000'),  # Cor do texto
)

# Personalizar as cores do boxplot
fig_quantidades.update_traces(marker=dict(color='#001F3F'), line=dict(color='#001F3F'))

# Criar gráfico boxplot de NET
fig_net = px.box(df_renda_fixa, x='NET', template='plotly')

# Adicionar título ao gráfico
fig_net.update_layout(
    title='NET de Ativos',
    font=dict(color='#000000'),  # Cor do texto
)

# Personalizar as cores do boxplot
fig_net.update_traces(marker=dict(color='#001F3F'), line=dict(color='#001F3F'))

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

# Estilo base para os botões
button_clicked_style = {
    'backgroundColor': '#001F3F',      # Fundo branco
    'color': 'white',               # Letra azul escuro
    'border': '2px solid white',      # Borda branca
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

# Adicionar margens entre os gráficos
margin_style = {'margin-top': '20px'}

# Layout COE
layout_coe = [
    html.Div(children=[
        html.Div(children=[
            html.H1(children='Exponencial Investimentos LTDA', style={'textAlign': 'left', 'color': 'white', 'margin-left': '10px'}),
        ], className='col-md-6'),

        html.Div(children=[
            html.Button('COE', id='btn_coe', n_clicks=0, style=button_clicked_style, className='button'),
            html.Button('Carteira Automatizada', id='btn_carteira_automatizada', n_clicks=0, style=button_style, className='button'),
            html.Button('Renda Fixa', id='btn_renda_fixa', n_clicks=0, style=button_style, className='button'),
            html.Button('Oferta Pública', id='btn_oferta_publica', n_clicks=0, style=button_style, className='button'),
        ], style={'display': 'flex', 'flex-wrap': 'wrap','textAlign': 'center', 'align-items': 'center', 'justify-content': 'space-evenly'}, className='col-md-6'),  
    ], style={'margin-bottom': '40px'}, className='header row'),

    html.Div(id='filtros', children=[
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in ['Todos os clientes'] + sorted(df_coe['NomeCliente'].astype(str).unique().tolist())],
            value='Todos os clientes',
            id='clientes_coe',
            className='dropdown',
            style={'min-width': '220px', 'margin-bottom': '10px'}
        ),
    ], className='filter-container', style={'display': 'flex', 'flex-wrap': 'wrap','align-items': 'center', 'justify-content': 'space-evenly', 'margin-bottom': '30px'}),

    html.Div(children=[
        html.Div(children=[
            html.H4(children='Total de Ativos', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='total_de_ativos_coe', children=[formatar_numero(total_de_ativos_coe)], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Receita por Ativo', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='renda_por_ativo_coe', children=["R$ "+formatar_numero(renda_por_ativo_coe)], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Receita Total', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='receita_total_coe', children=["R$ "+formatar_numero(receita_total_coe)], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Comissão', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='comissao_coe', children=["R$ "+formatar_numero(comissao_coe)], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'space-evenly', 'margin-bottom': '40px'},
       className='kpi-container'),

    html.Div([
        html.H2(children='Ativos', style={'textAlign': 'left', 'color': 'white', 'margin-left': '10px'}),
        dash_table.DataTable(
            id='tabela-coe',
            columns=[{"name": i, "id": i} for i in tabela_coe.columns],
            data=tabela_coe.to_dict('records'),
            style_table={
                'height': '300px',
                'overflowY': 'auto',
                'border': 'thin lightgrey solid',  # Adiciona borda à tabela
            },
            style_header={'backgroundColor': '#001F3F', 'color': 'white', 'fontWeight': 'bold'},  # Estilo do cabeçalho
            style_cell={
                'backgroundColor': '#f4f4f4',  # Cor de fundo das células
                'color': '#001F3F',  # Cor do texto nas células
                'textAlign': 'left',  # Alinhamento do texto
                'font_size': '14px',  # Tamanho da fonte
                'padding': '10px',  # Preenchimento interno
                'whiteSpace': 'normal',  # Permite que o texto quebre em várias linhas
            },
        ),
    ]),
]

# Layout renda fixa
layout_renda_fixa = [
     html.Div(children=[
        html.Div(children=[
            html.H1(children='Exponencial Investimentos LTDA', style={'textAlign': 'left', 'color': 'white', 'margin-left': '10px'}),
        ], className='col-md-6'),

        html.Div(children=[
            html.Button('COE', id='btn_coe', n_clicks=0, style=button_style, className='button'),
            html.Button('Carteira Automatizada', id='btn_carteira_automatizada', n_clicks=0, style=button_style, className='button'),
            html.Button('Renda Fixa', id='btn_renda_fixa', n_clicks=0, style=button_clicked_style, className='button'),
            html.Button('Oferta Pública', id='btn_oferta_publica', n_clicks=0, style=button_style, className='button'),
        ], style={'display': 'flex', 'flex-wrap': 'wrap','textAlign': 'center', 'align-items': 'center', 'justify-content': 'space-evenly'}, className='col-md-6'),  
    ], style={'margin-bottom': '40px'}, className='header row'),

    html.Div(id='filtros', children=[
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in ['Todos os assessores'] + sorted(df_renda_fixa['Nome assessor'].astype(str).unique().tolist())],
            value='Todos os assessores',
            id='assessores_renda_fixa',
            className='dropdown',
            style={'min-width': '220px', 'margin-bottom': '10px'}
        ),
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in ['Todos os clientes'] + sorted(df_renda_fixa['NomeCliente'].astype(str).unique().tolist())],
            value='Todos os clientes',
            id='clientes_renda_fixa',
            className='dropdown',
            style={'min-width': '220px', 'margin-bottom': '10px'}
        ),
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in ['Todos os sub produtos'] + sorted(df_renda_fixa['Sub Produto'].astype(str).unique().tolist())],
            value='Todos os sub produtos',
            id='sub_produtos_renda_fixa',
            className='dropdown',
            style={'min-width': '220px', 'margin-bottom': '10px'}
        ),
    ], className='filter-container', style={'display': 'flex', 'flex-wrap': 'wrap','align-items': 'center', 'justify-content': 'space-evenly', 'margin-bottom': '30px'}),

    html.Div(children=[
        html.Div(children=[
            html.H4(children='Total de Ativos', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='total_de_ativos_renda_fixa', children=[formatar_numero(total_de_ativos_renda_fixa)], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Receita por Ativo', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='renda_por_ativo_renda_fixa', children=["R$ "+formatar_numero(renda_por_ativo_renda_fixa)], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Receita Total', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='receita_total_renda_fixa', children=["R$ "+formatar_numero(receita_total_renda_fixa)], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),

        html.Div(children=[
            html.H4(children='Número de Clientes', style={'textAlign': 'center', 'color': '#001F3F'}),
            html.Div(id='numero_de_clientes_renda_fixa', children=[numero_de_clientes_renda_fixa], style={'textAlign': 'center', 'color': '#001F3F'}),
        ], className='kpi-card', style=kpi_card_style),
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'space-evenly', 'margin-bottom': '40px'},
       className='kpi-container'),

    html.Div([
        html.H2(children='Ativos', style={'textAlign': 'left', 'color': 'white', 'margin-left': '10px'}),
        dash_table.DataTable(
            id='tabela-renda-fixa',
            columns=[{"name": i, "id": i} for i in tabela_renda_fixa.columns],
            data=tabela_renda_fixa.to_dict('records'),
            style_table={
                'height': '300px',
                'overflowY': 'auto',
                'border': 'thin lightgrey solid',  # Adiciona borda à tabela
            },
            style_header={'backgroundColor': '#001F3F', 'color': 'white', 'fontWeight': 'bold'},  # Estilo do cabeçalho
            style_cell={
                'backgroundColor': '#f4f4f4',  # Cor de fundo das células
                'color': '#001F3F',  # Cor do texto nas células
                'textAlign': 'left',  # Alinhamento do texto
                'font_size': '14px',  # Tamanho da fonte
                'padding': '10px',  # Preenchimento interno
                'whiteSpace': 'normal',  # Permite que o texto quebre em várias linhas
            },
        ),
    ]),
    dcc.Graph(
        id='num-vencimentos',
        figure=fig_vencimentos,
        style=margin_style,
    ),
    dcc.Graph(
        id='box-plot-quantidade',
        figure=fig_quantidades,
        style=margin_style,
    ),
    dcc.Graph(
        id='box-plot-net',
        figure=fig_net,
        style=margin_style,
    ),
]

app.layout= html.Div(id="container_tela", children=layout_coe, style=div_style)

@callback(
    Output('container_tela', 'children'),
    Input('btn_coe', 'n_clicks'),
    Input('btn_carteira_automatizada', 'n_clicks'),
    Input('btn_renda_fixa', 'n_clicks'),
    Input('btn_oferta_publica', 'n_clicks'),
)
def menu_produtos(btn_coe, btn_carteira_automatizada, btn_renda_fixa, btn_oferta_publica):
    if 'btn_coe' == ctx.triggered_id:
        return layout_coe
    elif 'btn_carteira_automatizada' == ctx.triggered_id:
        return layout_renda_fixa
    elif 'btn_renda_fixa' == ctx.triggered_id:
        return layout_renda_fixa
    elif 'btn_oferta_publica' == ctx.triggered_id:
        return layout_renda_fixa
    return layout_coe

@callback(
    Output("total_de_ativos_coe", "children"),
    Output("renda_por_ativo_coe", "children"),
    Output("receita_total_coe", "children"),
    Output("comissao_coe", "children"),
    Output("tabela-coe", "data"),
    Input("clientes_coe", "value"),
    )
def callback_kpis_coe(nome_cliente):
    df_auxiliar = df_coe.copy()

    if nome_cliente != "Todos os clientes":
        df_auxiliar = df_auxiliar.loc[df_auxiliar['NomeCliente']==nome_cliente,:]

    total_de_ativos_coe = int(df_auxiliar['cliente'].count())
    renda_por_ativo_coe = df_auxiliar['Valor Aplicado'].sum()/len(df_auxiliar)
    receita_total_coe = df_auxiliar['Valor Aplicado'].sum()
    comissao_coe = df_auxiliar['Valor Aplicado'].sum()*0.025

    # Criar DataFrame com formatação desejada
    tabela_renda_fixa = df_auxiliar[['Data de Vencimento', 'Ativo', 'Emissor', 'Quantidade', 'NET']].copy()
    tabela_renda_fixa['Data de Vencimento'] = df_auxiliar['Data de Vencimento'].dt.strftime('%d/%m/%Y')
    tabela_renda_fixa['NET'] = df_auxiliar['NET'].round(2).map('R$ {:.2f}'.format).str.replace('.', ',', regex=False)

    return formatar_numero(total_de_ativos_coe),"R$ "+formatar_numero(renda_por_ativo_coe), "R$ "+formatar_numero(receita_total_coe), "R$ "+formatar_numero(comissao_coe), tabela_coe.to_dict('records')

@callback(
    Output("total_de_ativos_renda_fixa", "children"),
    Output("renda_por_ativo_renda_fixa", "children"),
    Output("receita_total_renda_fixa", "children"),
    Output("numero_de_clientes_renda_fixa", "children"),
    Output("tabela-renda-fixa", "data"),
    Output("num-vencimentos", "figure"),
    Output("box-plot-quantidade", "figure"),
    Output("box-plot-net", "figure"),
    Input("assessores_renda_fixa", "value"),
    Input("clientes_renda_fixa", "value"),
    Input("sub_produtos_renda_fixa", "value"),
    )
def callback_kpis_renda_fixa(nome_assessor, nome_cliente, nome_sub_produto):
    df_auxiliar = df_renda_fixa.copy()

    if nome_assessor != "Todos os assessores":
        df_auxiliar = df_auxiliar.loc[df_auxiliar['Nome assessor']==nome_assessor,:]
    if nome_cliente != "Todos os clientes":
        df_auxiliar = df_auxiliar.loc[df_auxiliar['NomeCliente']==nome_cliente,:]
    if nome_sub_produto != "Todos os sub produtos":
        df_auxiliar = df_auxiliar.loc[df_auxiliar['Sub Produto']==nome_sub_produto,:]

    total_de_ativos_renda_fixa = int(df_auxiliar['Quantidade'].sum())
    renda_por_ativo_renda_fixa = df_auxiliar['NET'].sum()/len(df_auxiliar) # Rever essa conta, porque não tenho certeza dessa conta
    receita_total_renda_fixa = df_auxiliar['NET'].sum()
    numero_de_clientes_renda_fixa = df_auxiliar['Cliente'].nunique()

    # Criar DataFrame com formatação desejada
    tabela_renda_fixa = df_auxiliar[['Data de Vencimento', 'Ativo', 'Emissor', 'Quantidade', 'NET']].copy()
    tabela_renda_fixa['Data de Vencimento'] = df_auxiliar['Data de Vencimento'].dt.strftime('%d/%m/%Y')
    tabela_renda_fixa['NET'] = df_auxiliar['NET'].round(2).map('R$ {:.2f}'.format).str.replace('.', ',', regex=False)

    # Calcular o somatório de vencimentos por dia
    df_somatorio = df_auxiliar.groupby('Data de Vencimento')['Quantidade'].sum().reset_index()

    # Criar gráfico de vencimentos ao longo do tempo
    fig_vencimentos = px.line(df_somatorio, x='Data de Vencimento', y='Quantidade', labels={'Quantidade': 'Quantidade de Vencimentos'}, template='plotly')

    # Adicionar título ao gráfico
    fig_vencimentos.update_layout(
        title='Quantidade de Vencimentos por Dia',
        font=dict(color='#000000'),  # Cor do texto
    )

    # Personalizar a cor da linha no gráfico de vencimentos
    fig_vencimentos.update_traces(line_color='#001F3F')

    # Criar gráfico boxplot de Quantidade
    fig_quantidades = px.box(df_renda_fixa, x='Quantidade', template='plotly')

    # Adicionar título ao gráfico
    fig_quantidades.update_layout(
        title='Quantidade de Ativos',
        font=dict(color='#000000'),  # Cor do texto
    )

    # Personalizar as cores do boxplot
    fig_quantidades.update_traces(marker=dict(color='#001F3F'), line=dict(color='#001F3F'))

    # Criar gráfico boxplot de NET
    fig_net = px.box(df_renda_fixa, x='NET', template='plotly')

    # Adicionar título ao gráfico
    fig_net.update_layout(
        title='NET de Ativos',
        font=dict(color='#000000'),  # Cor do texto
    )

    # Personalizar as cores do boxplot
    fig_net.update_traces(marker=dict(color='#001F3F'), line=dict(color='#001F3F'))

    return formatar_numero(total_de_ativos_renda_fixa),"R$ "+formatar_numero(renda_por_ativo_renda_fixa), "R$ "+formatar_numero(receita_total_renda_fixa), numero_de_clientes_renda_fixa, tabela_renda_fixa.to_dict('records'), fig_vencimentos, fig_quantidades, fig_net

# Execute o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)