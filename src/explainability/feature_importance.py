import numpy as np
from src.utils.identifier_detector import is_identifier_column


def extract_feature_importance(model, feature_names, top_n=5):

    if hasattr(model, 'feature_importances_'):

        importance_scores = model.feature_importances_

        importance_pairs = [
            (feature, float(score))
            for feature, score in zip(feature_names, importance_scores)
        ]

    elif hasattr(model, 'coef_'):

        importance_scores = np.abs(model.coef_).flatten()

        importance_pairs = [
            (feature, float(score))
            for feature, score in zip(feature_names, importance_scores)
        ]

    else:

        raise ValueError(
            "Unsupported attribute"
        )

    importance_pairs = [
        (feature, score)
        for feature, score in importance_pairs
        if not is_identifier_column(feature)
    ]

    importance_pairs = sorted(
        importance_pairs,
        key=lambda x: x[1],
        reverse=True
    )

    return importance_pairs[:top_n]