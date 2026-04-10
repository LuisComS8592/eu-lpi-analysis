# src/plots/viz.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy.stats import pearsonr
import plotly.graph_objects as go
import plotly.colors

# Set global style for Seaborn
sns.set(style="whitegrid")


def plot_comparative_indicator(df: pd.DataFrame, countries: list[str], indicator: str) -> plt.Figure:
    """
    Plots the time evolution of an LPI indicator for multiple countries.

    Parameters:
        df (pd.DataFrame): DataFrame containing LPI data.
        countries (list[str]): List of countries for comparison.
        indicator (str): Name of the LPI indicator to be plotted.

    Returns:
        matplotlib.figure.Figure: Generated plot figure object.
    """
    plt.figure(figsize=(12, 6))
    for country in countries:
        country_data = df[df["Country"] == country]
        plt.plot(country_data["Year"], country_data[indicator], marker='o', label=country)
    
    plt.title(f'Evolution of Indicator: {indicator}')
    plt.xlabel('Year')
    plt.ylabel(indicator)
    plt.legend(title='Country')
    plt.grid(True)
    fig = plt.gcf()
    plt.close()
    return fig


def plot_europe_map(df: pd.DataFrame, year: int, indicator: str = "LPI Aggregate") -> go.Figure:
    """
    Generates an interactive map of Europe showing the values of an LPI indicator in a given year.

    Parameters:
        df (pd.DataFrame): DataFrame with LPI data.
        year (int): Year to be displayed on the map.
        indicator (str, optional): Indicator to be displayed. Default is "LPI Aggregate".

    Returns:
        plotly.graph_objects.Figure: Interactive map figure.
    """
    df_year = df[df["Year"] == year].copy()

    if indicator not in df_year.columns:
        raise ValueError(f"Indicator '{indicator}' not found in data.")

    # Customized Tooltip
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
        title=f"{indicator} in Europe - {year}"
    )

    # Use hovertemplate for custom tooltip
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
        coloraxis_colorbar=dict(title=indicator),
        template='plotly_white'
    )

    return fig


def plot_histogram(df: pd.DataFrame, indicator: str) -> plt.Figure:
    """
    Creates a histogram with a KDE curve for an LPI indicator.

    Parameters:
        df (pd.DataFrame): DataFrame with LPI data.
        indicator (str): Indicator for the histogram.

    Returns:
        matplotlib.figure.Figure: Figure containing the histogram.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df[indicator], kde=True, color='skyblue')
    plt.title(f'Histogram of Indicator: {indicator}')
    plt.xlabel(indicator)
    plt.ylabel('Frequency')
    fig = plt.gcf()
    plt.close()
    return fig


def plot_boxplot_by_year(df: pd.DataFrame, indicator: str) -> plt.Figure:
    """
    Generates boxplots of the indicator by year to visualize distribution and outliers.

    Parameters:
        df (pd.DataFrame): DataFrame with LPI data.
        indicator (str): Indicator for the boxplot.

    Returns:
        matplotlib.figure.Figure: Figure containing the boxplot.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Year", y=indicator, data=df)
    plt.title(f'Boxplot of {indicator} by Year')
    plt.xlabel('Year')
    plt.ylabel(indicator)
    fig = plt.gcf()
    plt.close()
    return fig


def plot_correlation_heatmap_seaborn(df: pd.DataFrame, indicators: list[str]) -> plt.Figure:
    """
    Plots a heatmap of the correlation matrix between LPI indicators.

    Parameters:
        df (pd.DataFrame): DataFrame with LPI data.
        indicators (list[str]): List of indicators for correlation.

    Returns:
        matplotlib.figure.Figure: Correlation heatmap figure.
    """
    corr = df[indicators].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True, linewidths=.5)
    plt.title('Correlation Heatmap between Indicators')
    fig = plt.gcf()
    plt.close()
    return fig


def plot_scatter_regression(df: pd.DataFrame, x_indicator: str, y_indicator: str) -> plt.Figure:
    """
    Creates a scatterplot with a regression line between two indicators.

    Parameters:
        df (pd.DataFrame): DataFrame with LPI data.
        x_indicator (str): Indicator for X-axis.
        y_indicator (str): Indicator for Y-axis.

    Returns:
        matplotlib.figure.Figure: Scatterplot figure with regression.
    """
    plt.figure(figsize=(10, 6))
    sns.regplot(x=x_indicator, y=y_indicator, data=df, scatter_kws={"alpha":0.6})
    plt.title(f'Regression between {x_indicator} and {y_indicator}')
    plt.xlabel(x_indicator)
    plt.ylabel(y_indicator)
    fig = plt.gcf()
    plt.close()
    return fig


def pearson_correlation_test(df: pd.DataFrame, x_indicator: str, y_indicator: str) -> dict[str, float]:
    """
    Calculates the Pearson correlation between two indicators.

    Returns:
        dict[str, float]: Dictionary containing 'correlation' and 'p_value'.
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
    Generates a radar chart for the evolution of LPI sub-indicators of a country.
    """
    df_country = df[(df["Country"] == country) & (df["Year"].isin(years))]
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
        title=f'Evolution of LPI Sub-indicators - {country}',
        showlegend=True,
        template='plotly_white'
    )
    return fig, df_selected


def plot_dea_efficiency(results_df: pd.DataFrame) -> go.Figure:
    """
    Creates a faceted bar chart showing DEA efficiency by country and year.
    """
    fig = px.bar(
        results_df.sort_values("DEA Efficiency", ascending=False),
        x='Country',
        y='DEA Efficiency',
        color='DEA Efficiency',
        color_continuous_scale="RdYlGn",
        facet_col='Year',
        facet_col_wrap=2,
        title='DEA Efficiency by Country and Year',
        labels={'DEA Efficiency': 'DEA Efficiency', 'Country': 'Country'}
    )
    fig.update_layout(showlegend=False, template='plotly_white')
    return fig


def plot_topsis_ranking(df: pd.DataFrame, ano: int) -> go.Figure:
    """
    Creates an ordered bar chart with TOPSIS scores of countries.
    """
    df_sorted = df.sort_values('TOPSIS Score', ascending=False)
    fig = px.bar(
        df_sorted,
        x='Country',
        y='TOPSIS Score',
        color='TOPSIS Score',
        title=f'TOPSIS Ranking - {ano}',
        labels={'TOPSIS Score': 'TOPSIS Score', 'Country': 'Country'},
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(template='plotly_white')
    return fig


def plot_correlation_heatmap_plotly(corr_matrix: pd.DataFrame) -> go.Figure:
    """
    Generates an interactive heatmap of the correlation matrix using Plotly.
    """
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        origin='lower',
        aspect='auto',
        title='Interactive Correlation Matrix'
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
    Generates an interactive scatter plot between two rankings.
    """
    fig = px.scatter(
        comparativo,
        x=x,
        y=y,
        color='Country',
        hover_name='Country',
        labels={x: label_x, y: label_y},
        title=f'Relationship between {label_x} and {label_y}'
    )
    fig.update_layout(template='plotly_white')
    return fig
