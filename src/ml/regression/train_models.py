from sklearn.linear_model import LinearRegression

def train_linear_regression(X_train,y_train):
    
    model = LinearRegression()

    model.fit(X_train, y_train)

    return model

def train_decision_tree(X_train,y_train):
    pass

def train_random_forest(X_train,y_train):
    pass

def train_model(X_train,y_train):
    pass