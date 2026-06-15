from .target_detector import detect_problem_type, get_features_target
from .regression.train_regressoin_models import train_regression_models
from .regression.evaluate_regression_models import evaluate_models
from .regression.regression_insights import generate_regression_insights
from .regression.regression_story import generate_regression_story
from .select_best_model import select_best_model
from sklearn.model_selection import train_test_split


def ml_pipeline(df,target_col):

    problem_info = detect_problem_type(df,target_col)

    X, y = get_features_target(df,target_col)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if problem_info['problem_type'] == 'regression':

        trained_models = train_regression_models(X_train,y_train)

        evaluation_results = evaluate_models(trained_models, X_test, y_test)

        best_model_info = select_best_model(evaluation_results)

        insights = generate_regression_insights(evaluation_results,best_model_info)

        story = generate_regression_story(insights)

    else:
        raise NotImplementedError("Classification pipeline not implemented yet")

    return {
        "problem_info": problem_info,
        "evaluation_results": evaluation_results,
        "best_model_info": best_model_info,
        "insights": insights,
        "story": story
    }