def is_analytics_question(question):

    analytics_keywords = [
        "average",
        "mean",
        "sum",
        "total",
        "count",
        "maximum",
        "minimum",
        "max",
        "min",
        "compare",
        "comparison",
        "group by",
        "highest",
        "lowest",
        "calculate",
        "percentage",
        "percent",
        "median"
    ]

    words = question.lower().split()

    for keyword in analytics_keywords:
        if " " in keyword:
            if keyword in question:
                return True
        else:
            if keyword in words:
                return True
            
    return False