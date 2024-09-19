import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def plot_kuznets_curve_depletion(df, country):
    df["original_period"] = pd.to_datetime(df["original_period"], errors='coerce')
    df = df.dropna(subset=["original_period"])
    df["date"] = df["original_period"].dt.strftime("%Y")
    df["customdata"] = df.apply(
        lambda row: [row["date"], row["natural depletion"], row["gdp per capita"]], axis=1
    )
    
    df = df.dropna(subset=["gdp per capita", "natural depletion"])

    fig = px.scatter(
        df,
        x="gdp per capita",
        y="natural depletion",
        title=f"Kuznets environmental curve for {country}",
        labels={
            "gdp per capita": "GDP per capita",
            "natural depletion": "Natural resources depletion (% of GNI)",
        },
        custom_data=["date", "natural depletion", "gdp per capita"],
    )

    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Date: %{customdata[0]}",
                "Natural resources depletion (%): %{customdata[1]}",
                "GDP per capita: %{customdata[2]}",
            ]),
        marker=dict(size=8, symbol="circle-open-dot"),
        selector=dict(mode="markers")
        
    )

    # Polynomial Regression
    poly_features = PolynomialFeatures(degree=3)
    X_poly = poly_features.fit_transform(df[["gdp per capita"]])
    poly_model = LinearRegression()
    poly_model.fit(X_poly, df["natural depletion"])

    x_line = np.linspace(df["gdp per capita"].min(), df["gdp per capita"].max(), 100)
    x_line_poly = poly_features.transform(x_line.reshape(-1, 1))
    y_line = poly_model.predict(x_line_poly)

    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            name='Trend Line',
            line=dict(color='limegreen', width=2)
        )
    )

    return fig

def plot_kutznet_curve_greenhouse(df, country):
    df["original_period"] = pd.to_datetime(df["original_period"], errors='coerce')
    df = df.dropna(subset=["original_period"])
    df["date"] = df["original_period"].dt.strftime("%Y")
    df["customdata"] = df.apply(
        lambda row: [row["date"], row["greenhouse emission"], row["gdp per capita"]], axis=1
    )
    
    df = df.dropna(subset=["gdp per capita", "greenhouse emission"])

    fig = px.scatter(
        df,
        x="gdp per capita",
        y="greenhouse emission",
        title=f"Kutznet environmental curve for {country}",
        labels={
            "gdp per capita": "GDP per capita",
            "greenhouse emission": "Greenhouse Gas emission (kt of CO2 equivalent)",
        },
        custom_data=["date", "greenhouse emission", "gdp per capita"],
    )

    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Date: %{customdata[0]}",
                "Greenhouse Gas Emission (%): %{customdata[1]}",
                "GDP per capita: %{customdata[2]}",
            ]
        ),
        marker=dict(size=10, symbol="circle-open-dot"),
        selector=dict(mode="markers")
    )
    fig.update_layout(height = 700)
     # Polynomial Regression
    poly_features = PolynomialFeatures(degree=3)
    X_poly = poly_features.fit_transform(df[["gdp per capita"]])
    poly_model = LinearRegression()
    poly_model.fit(X_poly, df["greenhouse emission"])

    x_line = np.linspace(df["gdp per capita"].min(), df["gdp per capita"].max(), 100)
    x_line_poly = poly_features.transform(x_line.reshape(-1, 1))
    y_line = poly_model.predict(x_line_poly)

    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            name='Trend Line',
            line=dict(color='limegreen', width=2)
        )
    )

    return fig


def plot_greenhouse(merged_newdfs): 
    df_combined = pd.concat(merged_newdfs.values())
    df_combined["original_period"] = pd.to_datetime(df_combined["original_period"], errors='coerce')
    df_combined = df_combined.dropna(subset=["original_period"])
    df_combined["date"] = df_combined["original_period"].dt.strftime("%Y")
    df_combined = df_combined[df_combined["date"] >= '1990']
    fig = px.line(
        df_combined,
        x="original_period",
        y="greenhouse emission",
        color="country_x",
        title="Greenhouse Gas Emissions Over Time for All Countries",
        labels={
            "original_period": "Years",
            "greenhouse emission": "Greenhouse Gas Emission (kt of CO2 equivalent)",
            "country_x" : "Country" 
        },

        custom_data=["date", "greenhouse emission", "country_x"],
    )

    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Country: %{customdata[2]}",
                "Date: %{customdata[0]}",
                "Greenhouse Gas Emission (%): %{customdata[1]}",
            ]
        )
    )
    fig.update_layout(height = 700)
    return fig

