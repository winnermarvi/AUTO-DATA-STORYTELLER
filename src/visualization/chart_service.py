from src.visualization.chart_spec_generator import generate_chart_spec
from src.visualization.plotly_generator import generate_plot


def generate_chart(intent, result):

    chart_spec = generate_chart_spec(intent, result)

    figure = generate_plot(chart_spec, result)

    return figure