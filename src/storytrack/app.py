# Reads from delta and visualise in plotly dash app

from dash import dcc, html
import dash

from delta_reader import load_data
from dash_components import dash_figure


def run_dash_app(df):
    # Visualise runs
    app = dash.Dash(__name__)

    fig = dash_figure(df)

    app.layout = html.Div(
        children=[
            dcc.Graph(
                figure=fig,
                style={"height": "100vh", "width": "100vw"},  # full viewport
            )
        ],
        style={"margin": 0, "padding": 0, "height": "100vh", "width": "100vw"},
    )

    app.run(debug=False, host="0.0.0.0", port=8050)


def main():
    # Load data
    df = load_data("run_21_06_24")

    # Run app
    run_dash_app(df)


if __name__ == "__main__":
    main()
