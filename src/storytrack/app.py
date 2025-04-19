# Reads from delta and visualise in plotly dash app
import os

from dash import dcc, html, Dash, Input, Output, callback
import dash_mantine_components as dmc

from delta_reader import load_data
from dash_components import dash_graph_figure
from photo_process import scan_photos, match_photos_to_track


def run_dash_app(track_df, photo_matches=None):
    # Visualise runs with geotagged images
    app = Dash(__name__, assets_folder=os.path.join(os.getcwd(), "assets"))

    fig = dash_graph_figure(track_df, photo_matches)

    app.layout = dmc.MantineProvider(
        dmc.Grid(
            children=[
                dmc.GridCol(
                    html.Div(dcc.Graph(id="map", figure=fig, className="graph"), className="graph-div"), span=8
                ),
                dmc.GridCol(
                    html.Div(
                        id="photos", children=[html.H3("Click on a map marker to see the photo")], className="img-div"
                    ),
                    span="auto",
                ),
            ],
            justify="center",
            align="stretch",
            gutter="0px",
        )
    )

    app.run(debug=False, host="0.0.0.0", port=8050)


@callback(
    Output("photos", "children"),
    Input("map", "clickData"),
    prevent_initial_call=True,
)
def display_image(clickData):
    filename = clickData.get("points")[0].get("text")
    if filename is None:
        return html.H3("No image found at this point")
    # Return an <img> tag pointing to the asset
    return html.Img(src=f"assets/photos/{filename}", className="img")


def main():
    track_df = load_data("run_21_06_24")

    photo_df = scan_photos("assets/photos")

    if not photo_df.empty:
        photo_matches = match_photos_to_track(track_df, photo_df)
    else:
        print("No photos found within the timestamp range.")
        photo_matches = None

    run_dash_app(track_df, photo_matches)


if __name__ == "__main__":
    main()
