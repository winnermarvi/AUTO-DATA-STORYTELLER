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
    report["shape"] = {"rows" : int(df.shape[0]),"columns" : int(df.shape[1])}

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
        counts = df[i].value_counts()
        
        if len(top_value) > 0:
            top = top_value[0]
            top_counts = counts[top]
        else:
            top = None
            top_counts = 0


        categorical_summary[i] = {"unique" : int(df[i].nunique()),
                                  "top" : top,
                                  "top_count" : int(top_counts)
                                  }
        
    report["categorical_summary"] = categorical_summary


    #Creating correlation matrix of df
    report["correlation"] = df.select_dtypes(include=['number']).corr().to_dict()

    #Calculationg health score

    total_cells = report['shape']['rows'] * report['shape']['columns']

    total_missing = df.isnull().sum().sum()

    missing_pct = (total_missing / total_cells) * 100

    duplicate_rows = df.duplicated().sum()

    duplicate_pct = ( duplicate_rows / report['shape']['rows'] ) * 100

    constant_cols = 0

    for col in df.columns:
        if df[col].nunique() <= 1:
            constant_cols += 1

    constant_pct = (constant_cols / report['shape']['columns']) * 100

    health_score = ( 100 - missing_pct - duplicate_pct - constant_pct)

    report["health_score"] = max(0, round(health_score, 1))

    report["missing_pct"] = round(missing_pct, 1)

    report["total_missing"] = int(total_missing)

    return report

