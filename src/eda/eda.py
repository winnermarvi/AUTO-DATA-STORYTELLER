"""{
  "shape": ?,                  # rows, columns
  "columns": ?,                # list of column names
  "missing_values": ?,         # per column
  "numerical_summary": ?,      # stats for numeric columns
  "categorical_summary": ?     # stats for categorical columns
}"""

import pandas as pd

def analyze_data(df):
    report = {}

    #shape of df
    report["shape"] = {"rows" : df.shape[0],"columns" : df.shape[1]}

    #columns names
    report["columns"] = df.columns.to_list()

    #missing values
    report["missing_values"] = df.isnull().sum().to_dict()

    #separating numeric and category columns
    numerical_cols = df.select_dtypes(include = ['number']).columns.to_list()
    categorical_cols = df.select_dtypes(exclude = ['number']).columns.to_list()

    #calculating numeric summary
    numerical_summary = {}

    for i in numerical_cols:
        numerical_summary[i] = { "mean" : float(df[i].mean()) , 
                                "max" : float(df[i].max()) ,
                                "min" : float(df[i].min()), 
                                "std" : float(df[i].std()) 
                                }
        
    report["numerical_summary"] = numerical_summary

    #calculating categorical summary
    categorical_summary = {}

    for i in categorical_cols:                #checks if mode is empty and handle error by replacing empty with none
        top_value = df[i].mode()
        if len(top_value) > 0:
            top = top_value[0]
        else:
            top = None

        categorical_summary[i] = {"unique" : df[i].nunique(),
                                  "top" : top
                                  }
        
    report["categorical_summary"] = categorical_summary


    return report
