import plotly.express as px


def dash_figure(df):
    # Basic map
    fig = px.line_map(
        df,
        lat="latitude",
        lon="longitude",
        zoom=12,
        map_style="carto-darkmatter",
        hover_data={"latitude": False, "longitude": False, "elevation": True, "time": True, "speed": True},
    )
    return fig
