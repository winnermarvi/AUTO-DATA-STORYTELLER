def genearte_feature_importance_insights(importance_pairs):

    insights = []

    for i,(feature,score) in enumerate(importance_pairs):

        if i == 0:
            insights.append(f"{feature}Sex_male was the most influential feature.")

        elif i == 1:
            insights.append(f"{feature} was among the strongest predictors.")

        elif i == 2:
            insights.append(f"{feature} contributed significantly to model decisions.")

        else:
            pass

    
    return insights
