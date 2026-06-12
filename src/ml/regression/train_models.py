from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

def train_linear_regression(X_train,y_train):
    
    model = LinearRegression()

    model.fit(X_train, y_train)

    return model

def train_decision_tree(X_train,y_train):
    
    model = DecisionTreeRegressor(random_state=42)

    model.fit(X_train,y_train)

    return model

def train_random_forest(X_train,y_train):
    
    model = RandomForestRegressor(random_state=42,n_estimators=100)
    
    model.fit(X_train,y_train)

    return model

def train_model(X_train,y_train):
    
    linear_regression = train_linear_regression(X_train,y_train)

    decision_tree = train_decision_tree(X_train,y_train)

    random_forest = train_random_forest(X_train,y_train)

    return {
        "Linear Regression" : linear_regression,
        "Decision Tree" : decision_tree,
        "Random Forest" : random_forest
    }