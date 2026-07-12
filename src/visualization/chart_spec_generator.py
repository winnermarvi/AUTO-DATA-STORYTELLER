def generate_chart_spec(intent, result):

    operation = intent["operation"]
    target_column = intent["target_column"]
    group_by = intent["group_by"]

    chart_spec = {}

    # Grouped Analytics
    if group_by is not None:

        chart_spec = {
            "chart_type": "bar",
            "x": group_by,
            "y": target_column,
            "title": f"{operation.title()} {target_column} by {group_by}"
        }

    # Single Aggregation
    else:

        chart_spec = {
            "chart_type": "histogram",
            "x": target_column,
            "y": None,
            "title": f"Distribution of {target_column}"
        }

    return chart_spec