def build_knowledge(analysis):

    eda = analysis['eda']
    ml = analysis['ml']
    feature_importance = {
        'feature_importance': ml.get("feature_importance",None),
        'feature_importance_insights' : ml.get("feature_importance_insights",None),
        'feature_importance_story' :ml.get("feature_importance_story",None)
    }
    recommendations = {
        'recommendations': ml.get("recommendations",None),
        'recommendation_story': ml.get("recommendation_story",None)
    }
    llm = analysis['llm']

    _eda = {
        'id' : "eda_story",
        'type' : "eda",
        'content' : "\n".join(eda.get("eda_story",None)),
        'metadata': eda
    }

    _ml = {
        'id' : "ml_story",
        'type' : "ml",
        'content' : "\n".join(ml.get("ml_story",None)),
        'metadata': ml
    }

    _feature_importance = {
        'id' : "feature_importance",
        'type' : "feature_importance",
        'content' : "\n".join(feature_importance.get("feature_importance_story",None)),
        'metadata': feature_importance
    }

    _recommendations = {
        'id' : "recommendations",
        'type' : "recommendation",
        'content' : "\n".join(recommendations.get("recommendation_story",None)),
        'metadata': feature_importance
    }

    _executive_summary = {
        'id' : "executive_summary",
        'type' : "executive_summary",
        'content' : llm.get("narrative",None),
        'metadata': {}
    }

    knowledge = [_eda,_ml,_feature_importance,_recommendations,_executive_summary]

    return knowledge
