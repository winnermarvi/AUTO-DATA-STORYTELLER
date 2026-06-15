from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def train_logistic_regression(X_train,y_train):

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train,y_train)

    return model

def train_decision_tree(X_train,y_train):

    model = DecisionTreeClassifier(random_state=42)

    model.fit(X_train,y_train)

    return model

def train_random_forest(X_train,y_train):

    model = RandomForestClassifier(random_state=42,n_estimators=100)

    model.fit(X_train,y_train)

    return model

def train_classification_models(X_train,y_train):

    logistic_regression = train_logistic_regression(X_train,y_train)

    decision_tree = train_decision_tree(X_train,y_train)

    random_forest = train_random_forest(X_train,y_train)

    return {
        "Logistic Regression" : logistic_regression,
        "Decision Tree" : decision_tree,
        "Random Forest" : random_forest
    }