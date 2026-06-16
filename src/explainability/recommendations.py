def generate_recommendations(feature_importance, best_model_info, evaluation_results, problem_info):

    recommendations = []

    recommendations.append(f"{feature_importance[0][0]} appears to be the strongest driver of predictions and should be monitored closely.")

    if problem_info['problem_type'] == 'classification':

        score = best_model_info['best_metric_value']

    elif problem_info['problem_type'] == 'regression':

        score = evaluation_results[best_model_info['best_model']]['r2']

    else :
        raise ValueError(
            f"Unsupported problem type: {problem_info['problem_type']}"
        )

    if score >= 0.80:
        
        confidence = "strong"

    elif score >= 0.50:

        confidence = "moderate"

    else :

        confidence = "limited"

    recommendations.append(f"The model demonstrates {confidence} predictive performance, making the insights reasonably reliable.")

    recommendations.append(f"The most influential features should be tracked regularly, as changes in these variables are likely to have the largest effect on outcomes.")


    return recommendations