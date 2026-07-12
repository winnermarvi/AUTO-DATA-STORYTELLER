import plotly.express as px
import plotly.io as pio


def generate_plot(chart_spec, result):

    chart_type = chart_spec["chart_type"]
    title = chart_spec["title"]

    if hasattr(result, "reset_index"):
        result = result.reset_index()

    if chart_type == "bar":

        fig = px.bar(
            result,
            x=result.columns[0],
            y=result.columns[1],
            title=title
        )

    elif chart_type == "histogram":

        fig = px.histogram(
            result,
            x=chart_spec["x"],
            title=title
        )

    else:

        raise ValueError(f"Unsupported chart type: {chart_type}")

    return pio.to_json(fig)