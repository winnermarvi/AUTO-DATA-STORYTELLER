
def generate_classification_insights(evaluation_results,best_model_info):

    insights = []

    # best model
    insights.append(f"{best_model_info['best_model']} was selected as the best performing model based on F1.")

    # Score of best model
    insights.append(f"{best_model_info['best_model']} achieved the highest F1 score of {round(best_model_info['best_metric_value'],2)}.")

    # Accuracy insight
    insights.append(f"The model correctly classified approximately {round(evaluation_results[best_model_info['best_model']]['accuracy'] * 100,1)}% of records.")

    # F1 intrepretation
 
    f1_score_value = evaluation_results[best_model_info['best_model']]['f1']

    if f1_score_value >= 0.80:
        insights.append("The model demonstrates strong classification performance.")

    elif f1_score_value >= 0.50:
        insights.append("The model demonstrates moderate classification performance.")

    else:
        insights.append("The model demonstrates limited classification performance.")


    #comparison
    comparison_models = []

    for key in evaluation_results:
        if key != best_model_info['best_model']:
            comparison_models.append(key)

    comparison_sentence = (
        f"{best_model_info['best_model']} outperformed "
        f"{', '.join(comparison_models)} based on {best_model_info['selection_metric'].upper()}."
    )

    insights.append(comparison_sentence)


    return insights