from pandas.api.types import is_numeric_dtype


def detect_problem_type(df,target_col):
    
    target = df[target_col]

    unique_values = target.nunique()

    if not is_numeric_dtype(target):
        return {
            "problem_type" : "classification",
            "reason" : "target column is categorical"
        }
    
    elif unique_values <= 5:
        return {
            "problem_type" : "classification",
            "reason" : f"Numeric target column only has {unique_values} unique values"
        }
    
    else:
        return {
            "problem_type" : "regression",
            "reason" : f"Numeric target column has {unique_values} unique values"
        }


def get_features_target(df,target_col):

    X = df.drop(columns=[target_col])
    y = df[target_col]

    return X,y