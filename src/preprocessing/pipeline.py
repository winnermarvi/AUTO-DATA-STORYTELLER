import pandas as pd
from .missing_handler import missing_handler
from .outlier_handler import handle_outliers

df = pd.read_csv("data/sample1.csv")
print("raw data:")
print(df)

def preprocess_data(df):
    
    df = missing_handler(df)

    df = handle_outliers(df)


    return df

clean_df = preprocess_data(df)
print("clean data:")
print(clean_df)