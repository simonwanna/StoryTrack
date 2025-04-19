# Reads from delta and visualise in plotly dash app
import os

from dash import dcc, html, Dash
import dash_mantine_components as dmc

from delta_reader import load_data
from dash_components import dash_figure


def run_dash_app(df):
    # Visualise runs
    app = Dash(__name__, assets_folder=os.path.join(os.getcwd(), "assets"))

    fig = dash_figure(df)

    app.layout = dmc.MantineProvider(
        dmc.Grid(
            children=[dmc.GridCol(html.Div(dcc.Graph(figure=fig, className="graph"), className="graph-div"), span=8)],
            justify="center",
            align="stretch",
            gutter="0px",
        )
    )

    app.run(debug=False, host="0.0.0.0", port=8050)


def main():
    # Load data
    df = load_data("run_21_06_24")

    # Run app
    run_dash_app(df)


if __name__ == "__main__":
    main()
