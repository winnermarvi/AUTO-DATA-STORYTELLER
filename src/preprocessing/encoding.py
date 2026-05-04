import pandas as pd

#Encode string to numbers for ml model to understand
def encode_data(df):

    categorical_cols = df.select_dtypes(exclude = ['number']).columns.to_list()

    cols_to_drop = []
    #if no. of unique values are greter tha 90% we drop as they maybe identifiers(eg. name,email)
    for i in categorical_cols:
        if (df[i].nunique() / df.shape[0]) > 0.9:
            cols_to_drop.append(i)

    df = df.drop(columns = cols_to_drop)
    
    #Recomputing categorical columns as we have dropped some columns
    categorical_cols = df.select_dtypes(exclude = ['number']).columns.to_list()

    #encoding function
    df = pd.get_dummies(df, columns = categorical_cols)

    return df