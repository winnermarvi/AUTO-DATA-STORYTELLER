from sklearn.metrics import (mean_absolute_error,r2_score,root_mean_squared_error)

def evaluate_models(trained_models,X_test,y_test):

    evaluation_results = {}

    for model_name,model in trained_models.items():

        predictions = model.predict(X_test)

        r2 = r2_score(y_test, predictions)

        mae = mean_absolute_error(y_test, predictions)

        rmse = root_mean_squared_error(y_test,predictions)

        evaluation_results[model_name] = {
            'r2' : r2,
            'mae' : mae,
            'rmse' : rmse
        }

    return evaluation_results