import pandas as pd
from src.preprocessing.missing_handler import missing_handler
from src.preprocessing.outlier_handler import handle_outliers
from src.preprocessing.encoding import encode_data
from src.preprocessing.scaler import scaling



def preprocess_data_pipeline(df):
    
    df = missing_handler(df)

    df = handle_outliers(df)

    df = encode_data(df)

    df = scaling(df)

    return df

