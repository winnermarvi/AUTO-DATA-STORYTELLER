

def generate_regression_insights(evaluation_results,best_model_info):
    
    insights = []

    #Best model
    insights.append(f"{best_model_info['best_model']} was selected as the best performing model based on RMSE.")

    #RMSE score of best model
    insights.append(f"{best_model_info['best_model']} achieved the lowest RMSE of {best_model_info['best_rmse']}")

    #R2 insights
    r2 = evaluation_results[best_model_info['best_model']]['r2']
    r2_percentage = round(r2*100,1)
    insights.append(f"The model explains approximately {r2_percentage}% of the variation in the target variable.")

    #R2 interpretation
    if r2 >= 0.80:

        insights.append(f"The model demonstrates strong predictive performance.")

    elif 0.80 > r2 >= 0.50:

        insights.append(f"The model captures a moderate amount of target variability.")

    else:

        insights.append(f"The model captures only a limited amount of target variability.") 


    #comparison
    comparison_models = []

    for key in evaluation_results:
        if key != best_model_info['best_model']:
            comparison_models.append(key)

    comparison_sentence = (
        f"{best_model_info['best_model']} outperformed "
        f"{', '.join(comparison_models)} based on RMSE."
    )

    insights.append(comparison_sentence)
    return insights