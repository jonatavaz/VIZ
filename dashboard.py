# -*- coding: utf-8 -*-


#Passo 1 -> Lendo os dados e realizando o tratamento

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

# Load the CSV file
df=pd.read_csv('Summer_olympic_Medals.csv')
# Replace 'United States' with 'United States of America' in the 'Country_Name' column
df['Country_Name'] = df['Country_Name'].replace('United States', 'United States of America')

df

#Passo 2: Plotando gráfico de Mapa

# Filtre os dados entre 1992 e 2020
df = df [( df['Year'] >= 1992) & ( df ['Year'] <= 2020)]

# Calcula o total de medalhas para cada país
df [ 'Total_Medals' ] = df [ 'Gold' ] + df [ 'Silver' ] + df [ 'Bronze' ]
df_country_medals = df.groupby('Country_Name')['Total_Medals'].sum().reset_index()

# Gera um mapa gráfico
map_fig = px.choropleth(df_country_medals,
                    locations= 'Country_Name' ,      # Coluna DataFrame com nomes de países
                    locationmode= 'country names' ,
                    color= 'Total_Medals' ,          # Coluna DataFrame com valores de cor
                    hover_name= 'Country_Name' ,     # Coluna DataFrame hover info
                    color_continuous_scale=px.colors.sequential.YlOrRd,   # Defina a escala de cores
                    title= 'Total de medalhas de 1992 a 2020' )   # Título do enredo
map_fig.show()

df

#Passo 3 -> Plotando gráfico de área dos 10 paises com maior número de medalhas

# Crie um gráfico de área empilhado para os 10 principais países por contagem total de medalhas
top_countries = df_country_medals.groupby('Country_Name')['Total_Medals'].sum().nlargest(10).index
top_countries

df_countries = df.groupby(['Country_Name', 'Year'])['Total_Medals'].sum().reset_index()
df_countries

df_top_10_countries = df_countries[df_countries['Country_Name'].isin(top_countries)]
df_top_10_countries

area_fig = px.area(df_top_10_countries,
                   x= "Year" ,
                   y= "Total_Medals",
                   color= "Country_Name",
                   title= 'Top 10 Países por contagem total de medalhas de 1992 a 2020' )

area_fig.show()

# Crie um aplicativo Dash
app = dash.Dash(__name__)


# Defina o layout
app.layout = html.Div(children=[
    dcc.Graph(figure=map_fig),
    dcc. Graph(figure=area_fig)
])

# Execute o aplicativo
if __name__ == '__main__' :
    app.run( debug = False )  #com debug=True -> fica ativado o modo debug e exibindo as mensagens de erro

#Passo 4 -> Plotando gráfico de Barra com os 10 paises com maior número de medalhas de ouro

# Crie um gráfico de área empilhado para os 10 principais países por contagem total de medalhas
df_top_countries_gold = df.groupby('Country_Name')['Gold'].sum().nlargest(10).reset_index()
df_top_countries_gold

# Create a bar chart for the top 10 countries with most gold medals

bar_fig = px.bar(df_top_countries_gold, x='Country_Name', y='Gold', title='Top 10 Countries with Most Gold Medals from 1992 to 2020')
bar_fig.show()

#Passo 5 -> Estilazando a tela com color_discrete_sequence = gold

bar_fig = px.bar(df_top_countries_gold, x='Country_Name', y='Gold', color_discrete_sequence=['gold'], title='Top 10 Countries with Most Gold Medals from 1992 to 2020')
bar_fig.show()

# Create a Dash Application
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Graph(figure=map_fig, id='map'),
    html.Div([
        dcc.Graph(figure=area_fig, id='area-chart'),
        dcc.Graph(figure=bar_fig, id='bar-chart')
    ], style={'display': 'flex'})
])


# Execute o aplicativo
if __name__ == '__main__' :
    app.run( debug = False )  #com debug=True -> fica ativado o modo debug e exibindo as mensagens de erro

#Passo 5 -> Estizando a tela com ajuste do mapa dentro do container div

# Create a Dash Application
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=map_fig, id='map', style={'height': '50vh', 'width': '100%'}),
    html.Div([
        dcc.Graph(figure=area_fig, id='area-chart'),
        dcc.Graph(figure=bar_fig, id='bar-chart')
    ], style={'display': 'flex'})
])

# Execute o aplicativo
if __name__ == '__main__' :
    app.run( debug = False )  #com debug=True -> fica ativado o modo debug e exibindo as mensagens de erro

"""# Questão 1"""

# Questão 1 - Gere um gráfico de pizza com filtro. Selecione o país, e exiba um gráfico com o total de medalhas de Ouro, prata e bronze.

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load the CSV file
df = pd.read_csv('Summer_olympic_Medals.csv')
df['Country_Name'] = df['Country_Name'].replace('United States', 'United States of America')
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)]

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Distribuição de Medalhas"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Country_Name'].unique()],
        value=df['Country_Name'].unique()[5]  # Default value
    ),
    dcc.Graph(id='pie-chart')
])

# Define the callback to update the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    Input('country-dropdown', 'value')
)

def update_pie_chart(selected_country):
    filtered_df = df[df['Country_Name'] == selected_country]
    if filtered_df.empty:
        return px.pie(title=f"No data available for {selected_country}")

    medal_counts = filtered_df.agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'})

    # Cria um dicionário para mapear as medalhas às cores corretas
    color_map = {'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'brown'}

    fig = px.pie(
        medal_counts,
        values=medal_counts.values,
        names=medal_counts.index,
        title=f"Distribuição de Medalhas do País {selected_country}",
        # Usa o color_discrete_map para atribuir as cores corretamente
        color_discrete_map=color_map
    )
    return fig



# Run the app
if __name__ == '__main__':
    app.run(debug=False)

"""# Questão 2"""

#Questão II - Nos 3 gráficos gerados aplique um filtro para que o usuário escolha o tipo de medalha: Ouro, Prata, Bronze ou Todos.

import plotly.express as px

# Supondo que o DataFrame df já esteja carregado e com as colunas 'Gold', 'Silver', 'Bronze', 'Year', 'Country_Name'

# Filtra os dados entre 1992 e 2020
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)]

# Solicita ao usuário o tipo de medalha
tipo_medalha = input("Escolha o tipo de medalha (Ouro, Prata, Bronze, Todos): ").strip().lower()

# Filtra de acordo com a escolha
if tipo_medalha == 'ouro':
    df['Total_Medals'] = df['Gold']
elif tipo_medalha == 'prata':
    df['Total_Medals'] = df['Silver']
elif tipo_medalha == 'bronze':
    df['Total_Medals'] = df['Bronze']
elif tipo_medalha == 'todos':
    df['Total_Medals'] = df['Gold'] + df['Silver'] + df['Bronze']
else:
    raise ValueError("Escolha inválida. Opções: Ouro, Prata, Bronze ou Todos.")

# Agrupa por país
df_country_medals = df.groupby('Country_Name')['Total_Medals'].sum().reset_index()

# Gera o gráfico do mapa
map_fig = px.choropleth(
    df_country_medals,
    locations='Country_Name',
    locationmode='country names',
    color='Total_Medals',
    hover_name='Country_Name',
    color_continuous_scale=px.colors.sequential.YlOrRd,
    title=f'Total de medalhas ({tipo_medalha.capitalize()}) de 1992 a 2020'
)

map_fig.show()

import plotly.express as px

# Suponha que o DataFrame df já está carregado e contém as colunas 'Year', 'Country_Name', 'Gold', 'Silver', 'Bronze'

# Filtra os dados entre 1992 e 2020
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)]

# Solicita ao usuário o tipo de medalha
tipo_medalha = input("Escolha o tipo de medalha (Ouro, Prata, Bronze, Todas): ").strip().lower()

# Processa a escolha do usuário
if tipo_medalha == 'ouro':
    medal_col = 'Gold'
    cor = 'gold'
    titulo = 'Top 10 Países com Mais Medalhas de Ouro (1992-2020)'
elif tipo_medalha == 'prata':
    medal_col = 'Silver'
    cor = 'silver'
    titulo = 'Top 10 Países com Mais Medalhas de Prata (1992-2020)'
elif tipo_medalha == 'bronze':
    medal_col = 'Bronze'
    cor = '#cd7f32'  # Cor bronze hexadecimal
    titulo = 'Top 10 Países com Mais Medalhas de Bronze (1992-2020)'
elif tipo_medalha == 'todas':
    df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']
    medal_col = 'Total'
    cor = 'darkcyan'
    titulo = 'Top 10 Países com Mais Medalhas (1992-2020)'
else:
    raise ValueError("Escolha inválida. Opções: Ouro, Prata, Bronze ou Todas.")

# Agrupa e seleciona os top 10 países
df_medals = df.groupby('Country_Name')[medal_col].sum().reset_index()
df_top_countries = df_medals.sort_values(by=medal_col, ascending=False).head(10)
df_top_countries['Medalha'] = tipo_medalha.capitalize()

# Gera o gráfico de barras
bar_fig = px.bar(
    df_top_countries,
    x='Country_Name',
    y=medal_col,
    color='Medalha',  # Habilita color_discrete_sequence
    color_discrete_sequence=[cor],
    title=titulo
)

bar_fig.update_layout(showlegend=False)
bar_fig.show()

import plotly.express as px
import pandas as pd

# Filtra os dados entre 1992 e 2020
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)]

# Entrada do usuário
tipo_medalha = input("Escolha o tipo de medalha (Ouro, Prata, Bronze, Todas): ").strip().lower()

# Define coluna e título
if tipo_medalha == 'ouro':
    medal_col = 'Gold'
    titulo = 'Top 10 Países por Medalhas de Ouro (1992-2020)'
elif tipo_medalha == 'prata':
    medal_col = 'Silver'
    titulo = 'Top 10 Países por Medalhas de Prata (1992-2020)'
elif tipo_medalha == 'bronze':
    medal_col = 'Bronze'
    titulo = 'Top 10 Países por Medalhas de Bronze (1992-2020)'
elif tipo_medalha == 'todas':
    df['Total_Medals'] = df['Gold'] + df['Silver'] + df['Bronze']
    medal_col = 'Total_Medals'
    titulo = 'Top 10 Países por Medalhas Totais (1992-2020)'
else:
    raise ValueError("Escolha inválida. Opções: Ouro, Prata, Bronze ou Todas.")

# Encontra os top 10 países
df_total = df.groupby('Country_Name')[medal_col].sum().reset_index()
top_10 = df_total.sort_values(by=medal_col, ascending=False).head(10)['Country_Name']

# Filtra o dataframe
df_top_10 = df[df['Country_Name'].isin(top_10)]

# Recalcula os totais apenas para os top 10 e ordena (menor para maior, para empilhar corretamente)
country_order = df_top_10.groupby('Country_Name')[medal_col].sum().sort_values().index.tolist()

# Gráfico de área com ordem de empilhamento correta
area_fig = px.area(
    df_top_10,
    x="Year",
    y=medal_col,
    color="Country_Name",
    title=titulo,
    category_orders={"Country_Name": country_order}  # Ordem explícita para empilhamento
)

area_fig.show()

"""# Questão 3

"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Suponha que df já esteja carregado e contém colunas: Year, Host_country, Host_city, Country_Name, Gold, Silver, Bronze
# Exemplo:
# df = pd.read_csv('medalhas.csv')

# Filtra os dados entre 1992 e 2020
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)]

app = dash.Dash(__name__)

# Layout do app
app.layout = html.Div([
    html.H1("Top 10 Países por Medalhas no Ano Olímpico"),

    # Dropdown de ano (com país sede e cidade)
    dcc.Dropdown(
        id='year-dropdown',
        options=[
            {
                'label': f"{year} - {df[df['Year'] == year]['Host_country'].iloc[0]} ({df[df['Year'] == year]['Host_city'].iloc[0]})",
                'value': year
            }
            for year in sorted(df['Year'].unique())
        ],
        value=sorted(df['Year'].unique())[0]
    ),

    # Dropdown de tipo de medalha
    dcc.Dropdown(
        id='medal-dropdown',
        options=[
            {'label': 'Ouro', 'value': 'ouro'},
            {'label': 'Prata', 'value': 'prata'},
            {'label': 'Bronze', 'value': 'bronze'},
            {'label': 'Todas', 'value': 'todas'}
        ],
        value='todas'
    ),

    # Gráfico de barras
    dcc.Graph(id='bar-chart')
])

# Callback interativo
@app.callback(
    Output('bar-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('medal-dropdown', 'value')
)
def update_bar_chart(selected_year, tipo_medalha):
    # Filtra dados do ano selecionado
    year_df = df[df['Year'] == selected_year]

    # Determina coluna e cor com base na medalha
    if tipo_medalha == 'ouro':
        medal_col = 'Gold'
        cor = 'gold'
        titulo = f"Top 10 Países com Mais Medalhas de Ouro - {selected_year}"
    elif tipo_medalha == 'prata':
        medal_col = 'Silver'
        cor = 'silver'
        titulo = f"Top 10 Países com Mais Medalhas de Prata - {selected_year}"
    elif tipo_medalha == 'bronze':
        medal_col = 'Bronze'
        cor = '#cd7f32'
        titulo = f"Top 10 Países com Mais Medalhas de Bronze - {selected_year}"
    elif tipo_medalha == 'todas':
        year_df['Total'] = year_df['Gold'] + year_df['Silver'] + year_df['Bronze']
        medal_col = 'Total'
        cor = 'darkcyan'
        titulo = f"Top 10 Países com Mais Medalhas - {selected_year}"
    else:
        return px.bar(title="Seleção inválida.")

    # Agrupa e ordena os top 10 países no ano selecionado
    df_medals = year_df.groupby('Country_Name')[medal_col].sum().reset_index()
    df_top = df_medals.sort_values(by=medal_col, ascending=False).head(10)
    df_top['Medalha'] = tipo_medalha.capitalize()

    # Gráfico
    fig = px.bar(
        df_top,
        x='Country_Name',
        y=medal_col,
        color='Medalha',
        color_discrete_sequence=[cor],
        title=titulo
    )
    fig.update_layout(showlegend=False)

    return fig

# Executa o app
if __name__ == '__main__':
    app.run(debug=True)

"""# Questão 4"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Carregando o DataFrame
df = pd.read_csv('Summer_olympic_Medals.csv')

# Pré-processamento dos dados
df['Country_Name'] = df['Country_Name'].replace('United States', 'United States of America')
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)]

# Inicializando o aplicativo Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div([
    html.H1("Dashboard de Medalhas Olímpicas"),

    # Filtros de seleção
    html.Div([
        html.Label("Selecione o Ano Olímpico"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': 'Total de 1992-2020', 'value': 'total_1992_2020'}
            ] + [{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
            value='total_1992_2020'  # Valor padrão
        ),
        html.Label("Selecione o Tipo de Medalha"),
        dcc.Dropdown(
            id='medal-dropdown',
            options=[
                {'label': 'Ouro', 'value': 'ouro'},
                {'label': 'Prata', 'value': 'prata'},
                {'label': 'Bronze', 'value': 'bronze'},
                {'label': 'Todas', 'value': 'todas'}
            ],
            value='todas'  # Valor padrão
        ),
        html.Label("Selecione o País para o Gráfico de Pizza"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Country_Name'].unique()],
            value=df['Country_Name'].unique()[0]  # Valor padrão
        )
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),

    # Div para exibir os gráficos
    html.Div([
        html.Div([dcc.Graph(id='map-figure')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='bar-chart')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='area-figure')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='pie-chart')], style={'width': '48%', 'display': 'inline-block'})
    ])
])


# Callback para atualizar o gráfico de mapa
@app.callback(
    Output('map-figure', 'figure'),
    Input('year-dropdown', 'value'),
    Input('medal-dropdown', 'value')
)
def update_map(selected_year, tipo_medalha):
    # Se for 'total_1992_2020', agregue os dados de 1992-2020
    if selected_year == 'total_1992_2020':
        year_df = df
    else:
        year_df = df[df['Year'] == selected_year]

    if tipo_medalha == 'ouro':
        year_df['Total_Medals'] = year_df['Gold']
    elif tipo_medalha == 'prata':
        year_df['Total_Medals'] = year_df['Silver']
    elif tipo_medalha == 'bronze':
        year_df['Total_Medals'] = year_df['Bronze']
    elif tipo_medalha == 'todas':
        year_df['Total_Medals'] = year_df['Gold'] + year_df['Silver'] + year_df['Bronze']

    # Agrupa por país e gera o gráfico de mapa
    df_country_medals = year_df.groupby('Country_Name')['Total_Medals'].sum().reset_index()

    map_fig = px.choropleth(
        df_country_medals,
        locations='Country_Name',
        locationmode='country names',
        color='Total_Medals',
        hover_name='Country_Name',
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title=f'Total de medalhas ({tipo_medalha.capitalize()})'
    )

    return map_fig


# Callback para atualizar o gráfico de barras
@app.callback(
    Output('bar-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('medal-dropdown', 'value')
)
def update_bar_chart(selected_year, tipo_medalha):
    # Se for 'total_1992_2020', agregue os dados de 1992-2020
    if selected_year == 'total_1992_2020':
        year_df = df
    else:
        year_df = df[df['Year'] == selected_year]

    # Determina a coluna de medalha e o título
    if tipo_medalha == 'ouro':
        medal_col = 'Gold'
        cor = 'gold'
    elif tipo_medalha == 'prata':
        medal_col = 'Silver'
        cor = 'silver'
    elif tipo_medalha == 'bronze':
        medal_col = 'Bronze'
        cor = '#cd7f32'
    elif tipo_medalha == 'todas':
        year_df['Total'] = year_df['Gold'] + year_df['Silver'] + year_df['Bronze']
        medal_col = 'Total'
        cor = 'darkcyan'

    # Agrupa os top 10 países e gera o gráfico
    df_medals = year_df.groupby('Country_Name')[medal_col].sum().reset_index()
    df_top = df_medals.sort_values(by=medal_col, ascending=False).head(10)

    fig = px.bar(
        df_top,
        x='Country_Name',
        y=medal_col,
        color='Country_Name',
        color_discrete_sequence=[cor],
        title=f"Top 10 Países com Mais Medalhas ({tipo_medalha.capitalize()})"
    )
    return fig


# Callback para atualizar o gráfico de área
@app.callback(
    Output('area-figure', 'figure'),
    Input('medal-dropdown', 'value')
)
def update_area(tipo_medalha):
    # Se for 'total_1992_2020', agregue os dados de 1992-2020
    if tipo_medalha == 'ouro':
        medal_col = 'Gold'
    elif tipo_medalha == 'prata':
        medal_col = 'Silver'
    elif tipo_medalha == 'bronze':
        medal_col = 'Bronze'
    elif tipo_medalha == 'todas':
        df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']
        medal_col = 'Total'

    # Encontra os top 10 países
    df_total = df.groupby('Country_Name')[medal_col].sum().reset_index()
    top_10 = df_total.sort_values(by=medal_col, ascending=False).head(10)['Country_Name']

    df_top_10 = df[df['Country_Name'].isin(top_10)]

    country_order = df_top_10.groupby('Country_Name')[medal_col].sum().sort_values().index.tolist()

    area_fig = px.area(
        df_top_10,
        x="Year",
        y=medal_col,
        color="Country_Name",
        title=f"Top 10 Países por Medalhas de {tipo_medalha.capitalize()} (1992-2020)",
        category_orders={"Country_Name": country_order}  # Ordena para empilhamento correto
    )
    return area_fig


# Callback para atualizar o gráfico de pizza
@app.callback(
    Output('pie-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_pie_chart(selected_country):
    # Filtra os dados do país selecionado
    filtered_df = df[df['Country_Name'] == selected_country]
    if filtered_df.empty:
        return px.pie(title=f"No data available for {selected_country}")

    medal_counts = filtered_df.agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'})

    # Cria o gráfico de pizza
    fig = px.pie(
        medal_counts,
        values=medal_counts.values,
        names=medal_counts.index,
        title=f"Distribuição de Medalhas do País {selected_country}",
        color_discrete_map={'Gold': 'gold', 'Silver': 'silver', 'Bronze': '#cd7f32'}
    )
    return fig


# Rodando o aplicativo
if __name__ == '__main__':
    app.run(debug=True)

app = Dash(__name__)
server = app.server
