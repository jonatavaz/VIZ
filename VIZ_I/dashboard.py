import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# ======================
# CARREGAMENTO E TRATAMENTO
# ======================

# Carrega o dataset
df = pd.read_csv('Summer_olympic_Medals.csv')
df['Country_Name'] = df['Country_Name'].replace('United States', 'United States of America')
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)].copy()

# ======================
# DASH APP
# ======================

app = dash.Dash(__name__)
server = app.server  # Para deploy

# ======================
# LAYOUT
# ======================

app.layout = html.Div([
    html.H1("Dashboard de Medalhas Olímpicas", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Selecione o Ano Olímpico:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': 'Total de 1992-2020', 'value': 'total_1992_2020'}
            ] + [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
            value='total_1992_2020'
        ),

        html.Label("Selecione o Tipo de Medalha:"),
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

        html.Label("Selecione o País para o Gráfico de Pizza:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in sorted(df['Country_Name'].unique())],
            value='United States of America'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

    html.Div([
        html.Div([dcc.Graph(id='map-figure')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='bar-chart')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='area-figure')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='pie-chart')], style={'width': '48%', 'display': 'inline-block'})
    ])
])

# ======================
# CALLBACKS
# ======================

# Mapa
@app.callback(
    Output('map-figure', 'figure'),
    Input('year-dropdown', 'value'),
    Input('medal-dropdown', 'value')
)
def update_map(selected_year, tipo_medalha):
    df_filtered = df if selected_year == 'total_1992_2020' else df[df['Year'] == selected_year].copy()

    if tipo_medalha == 'ouro':
        df_filtered['Total_Medals'] = df_filtered['Gold']
    elif tipo_medalha == 'prata':
        df_filtered['Total_Medals'] = df_filtered['Silver']
    elif tipo_medalha == 'bronze':
        df_filtered['Total_Medals'] = df_filtered['Bronze']
    else:
        df_filtered['Total_Medals'] = df_filtered['Gold'] + df_filtered['Silver'] + df_filtered['Bronze']

    df_country = df_filtered.groupby('Country_Name')['Total_Medals'].sum().reset_index()

    fig = px.choropleth(
        df_country,
        locations='Country_Name',
        locationmode='country names',
        color='Total_Medals',
        hover_name='Country_Name',
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title=f"Total de medalhas ({tipo_medalha.capitalize()})"
    )
    return fig

# Barras
@app.callback(
    Output('bar-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('medal-dropdown', 'value')
)
def update_bar(selected_year, tipo_medalha):
    df_filtered = df if selected_year == 'total_1992_2020' else df[df['Year'] == selected_year].copy()

    if tipo_medalha == 'ouro':
        col, cor = 'Gold', 'gold'
    elif tipo_medalha == 'prata':
        col, cor = 'Silver', 'silver'
    elif tipo_medalha == 'bronze':
        col, cor = 'Bronze', '#cd7f32'
    else:
        df_filtered['Total'] = df_filtered['Gold'] + df_filtered['Silver'] + df_filtered['Bronze']
        col, cor = 'Total', 'darkcyan'

    df_bar = df_filtered.groupby('Country_Name')[col].sum().reset_index().sort_values(by=col, ascending=False).head(10)

    fig = px.bar(df_bar, x='Country_Name', y=col, color='Country_Name',
                 color_discrete_sequence=[cor], title=f"Top 10 Países - Medalhas de {tipo_medalha.capitalize()}")
    fig.update_layout(showlegend=False)
    return fig

# Área
@app.callback(
    Output('area-figure', 'figure'),
    Input('medal-dropdown', 'value')
)
def update_area(tipo_medalha):
    if tipo_medalha == 'ouro':
        col = 'Gold'
    elif tipo_medalha == 'prata':
        col = 'Silver'
    elif tipo_medalha == 'bronze':
        col = 'Bronze'
    else:
        df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']
        col = 'Total'

    df_top = df.groupby('Country_Name')[col].sum().nlargest(10).index.tolist()
    df_filtered = df[df['Country_Name'].isin(df_top)].copy()
    country_order = df_filtered.groupby('Country_Name')[col].sum().sort_values().index.tolist()

    fig = px.area(df_filtered, x='Year', y=col, color='Country_Name',
                  title=f"Top 10 Países por Medalhas de {tipo_medalha.capitalize()} (1992-2020)",
                  category_orders={"Country_Name": country_order})
    return fig

# Pizza
@app.callback(
    Output('pie-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_pie(selected_country):
    df_country = df[df['Country_Name'] == selected_country]

    if df_country.empty:
        return px.pie(title=f"Nenhum dado para {selected_country}")

    medals = df_country[['Gold', 'Silver', 'Bronze']].sum()
    fig = px.pie(values=medals.values, names=medals.index,
                 title=f"Distribuição de Medalhas - {selected_country}",
                 color_discrete_map={'Gold': 'gold', 'Silver': 'silver', 'Bronze': '#cd7f32'})
    return fig

# ======================
# EXECUÇÃO
# ======================

if __name__ == '__main__':
    app.run(debug=True)
