import plotly.express as px
import plotly.graph_objects as go


def dash_graph_figure(track_df, photo_df):
    fig = px.line_map(
        track_df,
        # color="speed",
        lat="latitude",
        lon="longitude",
        zoom=12,
        map_style="satellite",  # "open-street-map"
        hover_data={"latitude": False, "longitude": False, "elevation": True, "time": True, "speed": True},
    )

    if photo_df is not None and not photo_df.empty:
        fig.add_trace(
            go.Scattermap(
                lat=photo_df["lat"],
                lon=photo_df["lon"],
                mode="markers",
                marker=dict(size=16, color="white", symbol="marker"),
                text=photo_df["filename"],
                hoverinfo="text",
                showlegend=False,
            )
        )

    return fig
