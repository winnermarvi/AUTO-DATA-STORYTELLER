

def select_best_model(evaluation_results,metric_name,higher_is_better):

    best_metric_value = None
    best_model = None
    for model_name in evaluation_results:

        if best_metric_value is None:
            best_metric_value = evaluation_results[model_name][metric_name]
            best_model = model_name

        else:
            if higher_is_better:
                if best_metric_value < evaluation_results[model_name][metric_name]:

                    best_metric_value = evaluation_results[model_name][metric_name]
                    best_model = model_name

            else:
                if best_metric_value > evaluation_results[model_name][metric_name]:

                    best_metric_value = evaluation_results[model_name][metric_name]
                    best_model = model_name

    return {
            "best_model" : best_model,
            "selection_metrics" : metric_name,
            "best_metric_value" : best_metric_value
    }