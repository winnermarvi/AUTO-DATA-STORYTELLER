

def select_best_model(evaluation_results):

    best_rmse = None
    best_model = None
    for model_name in evaluation_result:

        if best_rmse is None:
            best_rmse = evaluation_result[model_name]['rmse']
            best_model = model_name

        else:
            if best_rmse > evaluation_result[model_name]['rmse']:

                best_rmse = evaluation_result[model_name]['rmse']
                best_model = model_name

    return {
            "best_model" : best_model,
            "Selection_metrics" : 'rmse',
            "best_rmse" : best_rmse
    }