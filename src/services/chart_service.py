from src.visualization.feature_importance_chart import plot_feature_importance
from src.visualization.missing_value_chart import plot_missing_values

def generate_chart(feature_importance,missing_values):

    plot_feature_importance(feature_importance)
    plot_missing_values(missing_values)

    return None