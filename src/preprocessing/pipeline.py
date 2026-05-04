import pandas as pd
from .missing_handler import missing_handler
from .outlier_handler import handle_outliers
from .encoding import encode_data

df = pd.read_csv("data/sample1.csv")
print("raw data:")
print(df)

def preprocess_data(df):
    
    df = missing_handler(df)

    df = handle_outliers(df)

    df = encode_data(df)

    return df

clean_df = preprocess_data(df)
print("clean data:")
print(clean_df)