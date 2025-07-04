# src/plots/viz.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy.stats import pearsonr
import plotly.graph_objects as go
import plotly.colors

sns.set(style="whitegrid")


def plot_comparative_indicator(df: pd.DataFrame, countries: list[str], indicator: str) -> plt.Figure:
    """
    Plota a evolução temporal de um indicador LPI para múltiplos países.

    Parameters:
        df (pd.DataFrame): DataFrame contendo os dados do LPI.
        countries (list[str]): Lista de países para comparação.
        indicator (str): Nome do indicador LPI a ser plotado.

    Returns:
        matplotlib.figure.Figure: Objeto figura do gráfico gerado.
    """
    plt.figure(figsize=(12, 6))
    for country in countries:
        country_data = df[df["Country"] == country]
        plt.plot(country_data["Year"], country_data[indicator], marker='o', label=country)
    plt.title(f'Evolução do Indicador {indicator}')
    plt.xlabel('Ano')
    plt.ylabel(indicator)
    plt.legend(title='País')
    plt.grid(True)
    fig = plt.gcf()
    plt.close()
    return fig


def plot_europe_map(df: pd.DataFrame, year: int, indicator: str = "LPI Aggregate") -> go.Figure:
    """
    Gera um mapa interativo da Europa mostrando os valores de um indicador LPI em um dado ano.

    Parameters:
        df (pd.DataFrame): DataFrame com dados do LPI.
        year (int): Ano a ser exibido no mapa.
        indicator (str, optional): Indicador a ser exibido. Padrão é "LPI Aggregate".

    Returns:
        plotly.graph_objects.Figure: Figura do mapa interativo.
    """
    df_year = df[df["Year"] == year].copy()

    if indicator not in df_year.columns:
        raise ValueError(f"Indicador '{indicator}' não encontrado nos dados.")

    # Tooltip customizado
    def format_tooltip(row):
        return (
            f"<b>{row['Country']}</b><br>"
            f"LPI Aggregate: {row.get('LPI Aggregate', 'N/A')}<br>"
            f"Customs: {row.get('Customs', 'N/A')}<br>"
            f"Infrastructure: {row.get('Infrastructure', 'N/A')}<br>"
            f"International Shipments: {row.get('International Shipments', 'N/A')}<br>"
            f"Logistics Quality: {row.get('Logistics Quality and Competence', 'N/A')}<br>"
            f"Tracking and Tracing: {row.get('Tracking and Tracing', 'N/A')}<br>"
            f"Timeliness: {row.get('Timeliness', 'N/A')}"
        )

    df_year["tooltip"] = df_year.apply(format_tooltip, axis=1)

    fig = px.choropleth(
        df_year,
        locations="Country",
        locationmode="country names",
        color=indicator,
        hover_name="Country",
        color_continuous_scale="RdYlGn",
        title=f"{indicator} na Europa - {year}"
    )

    # Usar hovertemplate para customizar tooltip, sem incluir dados padrão do hover_data
    fig.update_traces(
        hovertemplate=df_year["tooltip"],
        marker_line_width=0.5
    )

    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="LightGray",
        center={"lat": 54, "lon": 15},
        lataxis_range=[35, 70],
        lonaxis_range=[-25, 40]
    )

    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        height=650,
        width=950,
        coloraxis_colorbar=dict(title=indicator)
    )

    return fig


def plot_histogram(df: pd.DataFrame, indicator: str) -> plt.Figure:
    """
    Cria um histograma com curva KDE para um indicador do LPI.

    Parameters:
        df (pd.DataFrame): DataFrame com dados do LPI.
        indicator (str): Indicador para o histograma.

    Returns:
        matplotlib.figure.Figure: Figura com o histograma.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df[indicator], kde=True, color='skyblue')
    plt.title(f'Histograma do Indicador {indicator}')
    plt.xlabel(indicator)
    plt.ylabel('Frequência')
    fig = plt.gcf()
    plt.close()
    return fig


def plot_boxplot_by_year(df: pd.DataFrame, indicator: str) -> plt.Figure:
    """
    Gera boxplots do indicador por ano para visualizar distribuição e outliers.

    Parameters:
        df (pd.DataFrame): DataFrame com dados do LPI.
        indicator (str): Indicador para o boxplot.

    Returns:
        matplotlib.figure.Figure: Figura contendo o boxplot.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Year", y=indicator, data=df)
    plt.title(f'Boxplot do Indicador {indicator} por Ano')
    plt.xlabel('Ano')
    plt.ylabel(indicator)
    fig = plt.gcf()
    plt.close()
    return fig


def plot_correlation_heatmap_seaborn(df: pd.DataFrame, indicators: list[str]) -> plt.Figure:
    """
    Plota heatmap da matriz de correlação entre indicadores do LPI.

    Parameters:
        df (pd.DataFrame): DataFrame com dados do LPI.
        indicators (list[str]): Lista de indicadores para correlação.

    Returns:
        matplotlib.figure.Figure: Figura do heatmap da correlação.
    """
    corr = df[indicators].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True, linewidths=.5)
    plt.title('Mapa de Correlação entre Indicadores')
    fig = plt.gcf()
    plt.close()
    return fig


def plot_scatter_regression(df: pd.DataFrame, x_indicator: str, y_indicator: str) -> plt.Figure:
    """
    Cria um scatterplot com linha de regressão entre dois indicadores.

    Parameters:
        df (pd.DataFrame): DataFrame com dados do LPI.
        x_indicator (str): Indicador para eixo X.
        y_indicator (str): Indicador para eixo Y.

    Returns:
        matplotlib.figure.Figure: Figura do gráfico scatter com regressão.
    """
    plt.figure(figsize=(10, 6))
    sns.regplot(x=x_indicator, y=y_indicator, data=df, scatter_kws={"alpha":0.6})
    plt.title(f'Regressão entre {x_indicator} e {y_indicator}')
    plt.xlabel(x_indicator)
    plt.ylabel(y_indicator)
    fig = plt.gcf()
    plt.close()
    return fig


def pearson_correlation_test(df: pd.DataFrame, x_indicator: str, y_indicator: str) -> dict[str, float]:
    """
    Calcula a correlação de Pearson entre dois indicadores.

    Parameters:
        df (pd.DataFrame): DataFrame com dados do LPI.
        x_indicator (str): Indicador X para correlação.
        y_indicator (str): Indicador Y para correlação.

    Returns:
        dict[str, float]: Dicionário contendo 'correlation' (coeficiente de Pearson) e 'p_value' (significância).
    """
    corr, p_value = pearsonr(df[x_indicator], df[y_indicator])
    return {"correlation": corr, "p_value": p_value}


def plot_radar_subindicators(
    df: pd.DataFrame,
    country: str,
    years: list[int],
    subindicators: list[str]
) -> tuple[go.Figure, pd.DataFrame]:
    """
    Gera gráfico radar para evolução dos subindicadores LPI de um país em anos selecionados.

    Parameters:
        df (pd.DataFrame): DataFrame com dados do LPI.
        country (str): País a ser analisado.
        years (list[int]): Lista de anos para comparação.
        subindicators (list[str]): Lista de subindicadores para o radar.

    Returns:
        tuple: Figura plotly do radar e DataFrame pivotado dos valores.
    """
    df_country = df[(df["Country"] == country) & (df["Year"].isin(years))]

    # Seleciona somente as colunas dos subindicadores e o ano como índice
    df_selected = df_country.set_index("Year")[subindicators]

    fig = go.Figure()
    categories = subindicators

    colors = plotly.colors.qualitative.Plotly
    n_colors = len(colors)

    for i, year in enumerate(years):
        if year in df_selected.index:
            values = df_selected.loc[year].values
            color = colors[i % n_colors]

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=str(year),
                line=dict(color=color),
                marker=dict(color=color)
            ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickvals=[0,1,2,3,4,5])),
        title=f'Evolução dos Subindicadores LPI - {country}',
        showlegend=True,
        template='plotly_white'
    )
    return fig, df_selected


def plot_dea_efficiency(results_df: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de barras facetado mostrando a eficiência DEA por país e ano.

    Parameters:
        results_df (pd.DataFrame): DataFrame com colunas 'Country', 'DEA Efficiency' e 'Year'.

    Returns:
        plotly.graph_objects.Figure: Gráfico interativo da eficiência DEA.
    """
    fig = px.bar(
        results_df,
        x='Country',
        y='DEA Efficiency',
        color='Country',
        facet_col='Year',
        facet_col_wrap=2,
        title='Eficiência DEA por País e Ano',
        labels={'DEA Efficiency': 'Eficiência DEA'}
    )
    fig.update_layout(showlegend=False)
    fig.update_layout(template='plotly_white')
    return fig


def plot_topsis_ranking(df: pd.DataFrame, ano: int) -> go.Figure:
    """
    Cria gráfico de barras ordenado com scores TOPSIS dos países.

    Parameters:
        df (pd.DataFrame): DataFrame com colunas 'Country' e 'TOPSIS Score'.
        ano (int): Ano da análise para título.

    Returns:
        plotly.graph_objects.Figure: Gráfico de barras interativo.
    """
    df_sorted = df.sort_values('TOPSIS Score', ascending=False)
    fig = px.bar(
        df_sorted,
        x='Country',
        y='TOPSIS Score',
        color='TOPSIS Score'
        title=f'Ranking TOPSIS - {ano}',
        labels={'TOPSIS Score': 'Score TOPSIS'},
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(template='plotly_white')
    return fig


def plot_correlation_heatmap_plotly(corr_matrix: pd.DataFrame) -> go.Figure:
    """
    Gera heatmap interativo da matriz de correlação usando Plotly.

    Parameters:
        corr_matrix (pd.DataFrame): Matriz de correlação.

    Returns:
        plotly.graph_objects.Figure: Figura do heatmap interativo.
    """
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        origin='lower',
        aspect='auto',
        title='Matriz de Correlação Interativa'
    )
    fig.update_layout(template='plotly_white')
    return fig


def plot_scatter_ranking(
    comparativo: pd.DataFrame,
    x: str,
    y: str,
    label_x: str,
    label_y: str
) -> go.Figure:
    """
    Gera gráfico de dispersão interativo entre dois rankings.

    Parameters:
        comparativo (pd.DataFrame): DataFrame com colunas x, y e 'Country'.
        x (str): Coluna para eixo X.
        y (str): Coluna para eixo Y.
        label_x (str): Rótulo eixo X.
        label_y (str): Rótulo eixo Y.

    Returns:
        plotly.graph_objects.Figure: Gráfico de dispersão interativo.
    """
    fig = px.scatter(
        comparativo,
        x=x,
        y=y,
        color='Country',
        hover_name='Country',
        labels={x: label_x, y: label_y},
        title=f'Relação entre {label_x} e {label_y}'
    )
    fig.update_layout(template='plotly_white')
    return fig
