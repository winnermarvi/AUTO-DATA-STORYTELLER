from sklearn.metrics import (accuracy_score,precision_score,f1_score,recall_score)

def evaluate_classification_models(trained_models,X_test,y_test):

    evaluation_results = {}
    
    for model_name,model in trained_models.items():

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test,predictions)

        precision = precision_score(y_test, predictions, average="weighted")

        recall = recall_score(y_test, predictions, average="weighted")

        f1 = f1_score(y_test, predictions, average="weighted")

        evaluation_results[model_name] = {
            'accuracy' : accuracy,
            'precision' : precision,
            'recall' : recall,
            'f1' : f1
        }


    return evaluation_results