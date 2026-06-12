

def generate_regression_insights(evaluation_results,best_model_info):
    
    insights = []

    #Best model
    insights.append(f"{best_model_info['best_model']} was selected as the best performing model based on RMSE.")

    #RMSE score of best model
    insights.append(f"{best_model_info['best_model']} achieved the lowest RMSE of {best_model_info['best_rmse']}")

    #R2 insights
    r2 = round(evaluation_results[best_model_info['best_model']]['r2'],2)
    insights.append(f"The model explains approximately {r2 * 100}% of the variation in the target variable.")

    #R2 interpretation
    if r2 >= 0.80:

        insights.append(f"The model demonstrates strong predictive performance.")

    elif 0.80 > r2 >= 0.50:

        insights.append(f"The model captures a moderate amount of target variability.")

    else:

        insights.append(f"The model captures only a limited amount of target variability.") 


    #comparison
    camparision_sentence = f"{best_model_info['best_model']} outperformed "
    model_names = []

    for key in evaluation_results:

        if key is not best_model_info['best_model']:

            model_names.append(key)

    for i in range(len(model_names)-1):
        if i is not len(model_names)-1:
            camparision_sentence += f"{model_names[i]}"
        else :
            camparision_sentence += f"and {model_names[i]}"

    insights.append(camparision_sentence)

    return insights