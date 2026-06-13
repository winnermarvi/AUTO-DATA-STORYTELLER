import pandas as pd
from .missing_handler import missing_handler
from .outlier_handler import handle_outliers
from .encoding import encode_data
from .scaler import scaling



def preprocess_data_pipeline(df):
    
    df = missing_handler(df)

    df = handle_outliers(df)

    df = encode_data(df)

    df = scaling(df)

    return df

